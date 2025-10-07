# AI Foundry Databricks Sample

This sample showcases a notebook-based walkthrough of how to integrate **Databricks Genie** with **Azure AI Foundry Agent**, and how to enhance the agent's functionality by adding external tools such as Logic Apps.

## Files

- `adb-aifoundry.ipynb` - Jupyter notebook demonstrating the integration between Logic Apps and Genie agent as tool extension
- `streamlit_chat_app.py` - Streamlit web app for a simple, interactive chat interface with the agent
- `requirements.txt` - Python dependencies

## Features

- Integration between Azure AI Foundry and Databricks Genie
- Extendable agent with tools like `send_email` and `get_weather` (powered by Logic Apps)
- Easy-to-use Streamlit frontend

## Based On

This example is extended from the official Azure sample:  
👉 [sample_agent_adb_genie_conversation.py](https://github.com/Azure-Samples/AI-Foundry-Connections/blob/main/src/samples/python/sample_agent_adb_genie_conversation.py)

## Prerequisites

Before running the samples, ensure the following are set up:

- An **Azure subscription** with an active **AI Foundry project**
- A **Databricks workspace** with **Genie** enabled
- Python **3.8+**
- Azure authentication configured via:
  - Azure CLI (`az login`)
  - or a service principal

## Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run streamlit_chat_app.py
```

## Configuration

Select Genie as connection type in AI Foundry as shown in the main repository README.