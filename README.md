# AI Agent Samples

This repository contains a collection of AI Agent samples demonstrating how to integrate and extend Azure AI Foundry Agent capabilities with various tools and services.

## 📘 Sample: Databricks Genie Chat Assistant

This sample showcases a notebook-based walkthrough of how to integrate **Databricks Genie** with **Azure AI Foundry Agent**, and how to enhance the agent's functionality by adding external tools such as Logic Apps.

It includes:
- A notebook to demonstrate the integration logic and tool extension.
- A **Streamlit** web app for a simple, interactive chat interface with the agent—ideal for demo scenarios.

### 🔧 Features

- Integration between Azure AI Foundry and Databricks Genie
- Extendable agent with tools like `send_email` and `get_weather` (powered by Logic Apps)
- Easy-to-use Streamlit frontend

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

## Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt

streamlit run app.py

```
#Coming soon: Evaluation framework to benchmark tool effectiveness and agent responses.

<img width="1999" height="1148" alt="image" src="https://github.com/user-attachments/assets/e19a83f1-db05-43c7-b805-925727ce462e" />
