# AI Agent Samples

This repository contains a collection of AI Agent samples demonstrating how to integrate and extend Azure AI Foundry Agent capabilities with various tools and services.

## Samples

### AI Foundry Databricks Sample

Located in the `ai-foundry-databricks-sample/` folder, this sample showcases a notebook-based walkthrough of how to integrate **Databricks Genie** with **Azure AI Foundry Agent**, and how to enhance the agent's functionality by adding external tools such as Logic Apps.

It includes:
- A notebook to demonstrate the integration logicapps and Genie agent as tool extension.
- A **Streamlit** web app for a simple, interactive chat interface with the agent—ideal for demo scenarios.

### Azure Monitor AI Foundry Sample

Located in the `azure-monitor-ai-foundry-sample/` folder, this sample demonstrates comprehensive monitoring and alerting for **Azure AI Foundry Agent Service** using **Azure Monitor** and **Log Analytics**.

It includes:
- A **Jupyter notebook** with KQL queries for monitoring failures, performance, and usage patterns
- An **Azure Workbook template** for comprehensive operational insights and dashboards
- Sample queries for analyzing agent operations, thread activities, and tool calls

### Features

- Integration between Azure AI Foundry and Databricks Genie
- Extendable agent with tools like `send_email` and `get_weather` (powered by Logic Apps)
- Easy-to-use Streamlit frontend

### Based On

This example is extended from the official Azure sample:  
👉 [sample_agent_adb_genie_conversation.py](https://github.com/Azure-Samples/AI-Foundry-Connections/blob/main/src/samples/python/sample_agent_adb_genie_conversation.py)

---

## Prerequisites

Before running the samples, ensure the following are set up:

- An **Azure subscription** with an active **AI Foundry project**
- A **Databricks workspace** with **Genie** enabled
- Python **3.8+**
- Azure authentication configured via:
  - Azure CLI (`az login`)
  - or a service principal

---

## Getting Started

Navigate to the sample folder and install the required Python dependencies:

```bash
cd ai-foundry-databricks-sample/
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_chat_app.py
```

## Select Genie as connection type in AI Foundry

<img width="1999" height="1148" alt="image" src="https://github.com/user-attachments/assets/e19a83f1-db05-43c7-b805-925727ce462e" />
