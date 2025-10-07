import streamlit as st
import json
from databricks.sdk import WorkspaceClient
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from databricks.sdk.service.dashboards import GenieAPI
from azure.ai.agents.models import (FunctionTool, ToolSet)
from typing import Any, Callable, Set
import os

# Configure page
st.set_page_config(
    page_title="Databricks Genie Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

# Environment setup
os.environ["DATABRICKS_SDK_UPSTREAM"] = "AzureAIFoundry"
os.environ["DATABRICKS_SDK_UPSTREAM_VERSION"] = "1.0.0"

# Configuration
DATABRICKS_ENTRA_ID_AUDIENCE_SCOPE = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"
FOUNDRY_PROJECT_ENDPOINT = ""
FOUNDRY_DATABRICKS_CONNECTION_NAME = ""

@st.cache_resource
def initialize_clients():
    """Initialize the Azure AI Project client and Databricks client with caching."""
    # Always show initialization status
    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    try:
        # Step 1: Initialize credentials
        status_placeholder.info("🔐 Setting up Azure credentials...")
        progress_bar.progress(15)
        
        credential = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_interactive_browser_credential=False
        )
        
        # Step 2: Initialize Azure AI Project client
        status_placeholder.info("🚀 Connecting to Azure AI Project...")
        progress_bar.progress(30)
        
        project_client = AIProjectClient(FOUNDRY_PROJECT_ENDPOINT, credential)
        
        # Step 3: Get connection details
        status_placeholder.info("🔗 Retrieving Databricks connection...")
        progress_bar.progress(45)
        
        connection = project_client.connections.get(FOUNDRY_DATABRICKS_CONNECTION_NAME)
        
        if connection.metadata['azure_databricks_connection_type'] != 'genie':
            raise ValueError("Connection is not of type 'genie'")
        
        genie_space_id = connection.metadata['genie_space_id']
        
        # Step 4: Initialize Databricks client
        status_placeholder.info("🏗️ Setting up Databricks workspace client...")
        progress_bar.progress(65)
        
        workspace_client = WorkspaceClient(
            host=connection.target,
            token=credential.get_token(DATABRICKS_ENTRA_ID_AUDIENCE_SCOPE).token,
        )
        
        # Step 5: Initialize Genie API
        status_placeholder.info("🧞 Setting up Genie API...")
        progress_bar.progress(85)
        
        genie_api = GenieAPI(workspace_client.api_client)
        
        # Step 6: Complete
        status_placeholder.success("✅ All clients initialized successfully!")
        progress_bar.progress(100)
        
        # Clear the progress indicators after a moment
        import time
        time.sleep(1)
        status_placeholder.empty()
        progress_bar.empty()
        
        return project_client, genie_api, genie_space_id, workspace_client
        
    except Exception as e:
        error_msg = f"Failed to initialize clients: {str(e)}"
        status_placeholder.error(f"❌ {error_msg}")
        progress_bar.empty()
        if st.session_state.get('debug_mode', False):
            st.error(f"Error type: {type(e).__name__}")
            st.error(f"Full error: {str(e)}")
        return None, None, None, None

def ask_genie(question: str, conversation_id: str | None = None) -> str:
    """
    Ask Genie a question and return the response as JSON.
    """
    try:
        # Debug logging
        if st.session_state.get('debug_mode', False):
            st.write(f"🧞 ask_genie called with question: '{question}'")
            st.write(f"🔗 conversation_id: {conversation_id}")
        
        _, genie_api, genie_space_id, databricks_workspace_client = st.session_state.clients
        
        if conversation_id is None:
            if st.session_state.get('debug_mode', False):
                st.write("🆕 Starting new conversation...")
            message = genie_api.start_conversation_and_wait(genie_space_id, question)
            conversation_id = message.conversation_id
        else:
            if st.session_state.get('debug_mode', False):
                st.write("➡️ Continuing existing conversation...")
            message = genie_api.create_message_and_wait(genie_space_id, conversation_id, question)

        query_result = None
        if message.query_result:
            query_result = genie_api.get_message_query_result(
                genie_space_id, message.conversation_id, message.id
            )

        message_content = genie_api.get_message(genie_space_id, message.conversation_id, message.id)

        # Try to parse structured data if available
        if query_result and query_result.statement_response:
            statement_id = query_result.statement_response.statement_id
            results = databricks_workspace_client.statement_execution.get_statement(statement_id)
            columns = results.manifest.schema.columns
            data = results.result.data_array
            headers = [col.name for col in columns]
            rows = []
            for row in data:
                formatted_row = []
                for value, col in zip(row, columns):
                    if value is None:
                        formatted_value = "NULL"
                    elif col.type_name in ["DECIMAL", "DOUBLE", "FLOAT"]:
                        formatted_value = f"{float(value):,.2f}"
                    elif col.type_name in ["INT", "BIGINT", "LONG"]:
                        formatted_value = f"{int(value):,}"
                    else:
                        formatted_value = str(value)
                    formatted_row.append(formatted_value)
                rows.append(formatted_row)
            return json.dumps({
                "conversation_id": conversation_id,
                "table": {
                    "columns": headers,
                    "rows": rows
                }
            })

        # Fallback to plain message text
        if message_content.attachments:
            for attachment in message_content.attachments:
                if attachment.text and attachment.text.content:
                    return json.dumps({
                        "conversation_id": conversation_id,
                        "message": attachment.text.content
                    })

        return json.dumps({
            "conversation_id": conversation_id,
            "message": message_content.content or "No content returned."
        })

    except Exception as e:
        return json.dumps({
            "error": "An error occurred while talking to Genie.",
            "details": str(e)
        })

@st.cache_resource
def create_agent():
    """Create and cache the Azure AI agent"""
    try:
        debug_mode = st.session_state.get("debug_mode", False)
        project_client, _, _, _ = st.session_state.clients
        
        if debug_mode:
            st.write("🛠️ Setting up agent toolset...")
        toolset = ToolSet()
        user_functions: Set[Callable[..., Any]] = {ask_genie}
        functions = FunctionTool(functions=user_functions)
        toolset.add(functions)
        
        if debug_mode:
            st.write("🔧 Enabling function calls...")
        project_client.agents.enable_auto_function_calls(toolset)
        
        if debug_mode:
            st.write("🤖 Creating AI agent...")
        agent = project_client.agents.create_agent(
            model='gpt-4.1',
            name="Databricks Chat Agent",
            instructions="You are a helpful assistant that has access to Databricks Genie through the ask_genie function. " \
            "When users ask questions about data, transactions, analytics, or database queries, you MUST use the ask_genie function to get the actual data. " \
            "For the first call to ask_genie, don't pass a conversation_id. For follow-up questions, use the conversation_id returned from the previous call. " \
            "Always call ask_genie for data-related questions - never just echo the question back. " \
            "Format tabular data nicely for the user and be conversational in your responses.",
            toolset=toolset,
        )
        
        if debug_mode:
            st.write("💬 Creating conversation thread...")
        thread = project_client.agents.threads.create()
        
        if debug_mode:
            st.write(f"✅ Agent '{agent.name}' created successfully!")
            st.write(f"🆔 Thread ID: {thread.id}")
        
        return agent, thread
    except Exception as e:
        st.error(f"❌ Failed to create agent: {str(e)}")
        st.error(f"Details: {type(e).__name__}")
        return None, None

def display_message_content(content):
    """Display message content, handling both text and JSON responses"""
    try:
        # Handle different content types
        if isinstance(content, list):
            # If content is a list (from Azure AI agents), extract text from it
            text_content = ""
            for item in content:
                if hasattr(item, 'text') and hasattr(item.text, 'value'):
                    text_content += item.text.value
                elif isinstance(item, dict) and 'text' in item:
                    if isinstance(item['text'], dict) and 'value' in item['text']:
                        text_content += item['text']['value']
                    else:
                        text_content += str(item['text'])
                elif isinstance(item, str):
                    text_content += item
                else:
                    text_content += str(item)
            content = text_content
        
        # Convert to string if it's not already
        content_str = str(content) if not isinstance(content, str) else content
        
        # Try to parse as JSON first
        data = json.loads(content_str)
        
        if "table" in data:
            st.subheader("Query Results:")
            import pandas as pd
            df = pd.DataFrame(data["table"]["rows"], columns=data["table"]["columns"])
            st.dataframe(df, use_container_width=True)
        elif "message" in data:
            st.write(data["message"])
        elif "error" in data:
            st.error(f"Error: {data['error']}")
            if "details" in data:
                st.error(f"Details: {data['details']}")
    except (json.JSONDecodeError, TypeError):
        # If not JSON, display as plain text
        if isinstance(content, list):
            # Handle list content for plain text display
            text_content = ""
            for item in content:
                if hasattr(item, 'text') and hasattr(item.text, 'value'):
                    text_content += item.text.value
                elif isinstance(item, dict) and 'text' in item:
                    if isinstance(item['text'], dict) and 'value' in item['text']:
                        text_content += item['text']['value']
                    else:
                        text_content += str(item['text'])
                elif isinstance(item, str):
                    text_content += item
                else:
                    text_content += str(item)
            st.write(text_content)
        else:
            st.write(str(content))

def main():
    st.title("🤖 Azure AI Foundry Databricks Genie Chat Assistant")
    st.markdown("Ask questions about your data and get insights!")
    
    # Add debug mode toggle
    with st.sidebar:
        st.header("🛠️ Settings")
        debug_mode = st.checkbox("Debug Mode", help="Show detailed initialization steps")
    
    # Set debug mode in session state
    if "debug_mode" not in st.session_state:
        st.session_state.debug_mode = debug_mode
    else:
        st.session_state.debug_mode = debug_mode
    
    # Initialize session state
    if "clients" not in st.session_state:
        initialization_container = st.container()
        with initialization_container:
            st.info("🔄 Initializing Azure AI and Databricks connections...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("Connecting to Azure AI Foundry...")
                progress_bar.progress(25)
                st.session_state.clients = initialize_clients()
                
                if st.session_state.clients[0] is None:
                    st.error("❌ Failed to initialize Azure AI clients. Please check your Azure authentication.")
                    st.stop()
                    
                progress_bar.progress(75)
                status_text.text("Clients initialized successfully!")
                progress_bar.progress(100)
                
            except Exception as e:
                st.error(f"❌ Initialization error: {str(e)}")
                st.stop()
    
    if "agent_info" not in st.session_state:
        agent_container = st.container()
        with agent_container:
            st.info("🤖 Creating AI agent...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("Creating Databricks agent...")
                progress_bar.progress(50)
                st.session_state.agent_info = create_agent()
                
                if st.session_state.agent_info[0] is None:
                    st.error("❌ Failed to create AI agent. Please check your configuration.")
                    st.stop()
                    
                progress_bar.progress(100)
                status_text.text("Agent created successfully!")
                st.success("✅ Ready to chat!")
                
            except Exception as e:
                st.error(f"❌ Agent creation error: {str(e)}")
                st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Check if initialization was successful
    if st.session_state.clients[0] is None or st.session_state.agent_info[0] is None:
        st.error("Failed to initialize the application. Please check your configuration.")
        st.stop()
    
    project_client, _, _, _ = st.session_state.clients
    agent, thread = st.session_state.agent_info
    
    # Sidebar with agent info
    with st.sidebar:
        st.header("Agent Information")
        st.write(f"**Agent Name:** {agent.name}")
        st.write(f"**Model:** {agent.model}")
        st.write(f"**Thread ID:** {thread.id}")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.header("Sample Questions")
        sample_questions = [
            "What is the average transaction value?",
            "How many transactions were processed last month?",
            "Show me the top 10 customers by revenue",
            "What are the trending products this quarter?"
        ]
        
        for question in sample_questions:
            if st.button(question, key=f"sample_{hash(question)}"):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                display_message_content(message["content"])
            else:
                st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your data..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    debug_mode = st.session_state.get("debug_mode", False)
                    
                    # Create message in thread
                    if debug_mode:
                        st.write("📝 Creating message...")
                    project_client.agents.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=prompt,
                    )
                    
                    # Create and process run
                    if debug_mode:
                        st.write("🚀 Processing request...")
                    run = project_client.agents.runs.create_and_process(
                        thread_id=thread.id,
                        agent_id=agent.id
                    )
                    
                    if debug_mode:
                        st.write(f"⏳ Run status: {run.status}")
                        st.write(f"🆔 Run ID: {run.id}")
                        # Additional debugging info
                        if hasattr(run, 'usage') and run.usage:
                            st.write(f"💰 Token usage: {run.usage}")
                        if hasattr(run, 'last_error') and run.last_error:
                            st.write(f"❌ Last error: {run.last_error}")
                    
                    if run.status == "completed":
                        if debug_mode:
                            st.write("✅ Getting response...")
                        # Get the latest assistant message
                        messages = project_client.agents.messages.list(thread_id=thread.id)
                        latest_message = next(msg for msg in messages if msg.role == "assistant")
                        
                        response_content = latest_message.content
                        display_message_content(response_content)
                        
                        # Add assistant message to chat history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response_content
                        })
                    else:
                        st.error(f"❌ Run failed with status: {run.status}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.error(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    main()
