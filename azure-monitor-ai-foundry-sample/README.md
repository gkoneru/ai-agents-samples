# Azure Monitor Insights for AI Foundry Agent Service

This sample demonstrates how to monitor, analyze, and create alerts for Azure AI Foundry Agent Service using Azure Monitor, Log Analytics, and Azure Workbooks.

## Files

- `12_azure_monitor_alerts.ipynb` - Jupyter notebook demonstrating how to query diagnostic logs, monitor failures, and create alerts
- `ai_agent_monitoring_workbook.json` - Azure Workbook template for comprehensive AI Agent Service insights and monitoring
- `requirements.txt` - Python dependencies

## Features

- **Log Analytics Queries**: Query diagnostic logs using KQL (Kusto Query Language)
- **Failure Monitoring**: Monitor failures and errors in Azure AI Agent Service
- **Alert Management**: Create and manage alerts for critical issues
- **Performance Dashboards**: Build operational insights dashboards
- **Workbook Template**: Pre-built Azure Workbook for comprehensive monitoring

## Prerequisites

Before running the samples, ensure the following are set up:

- An **Azure subscription** with an active **AI Foundry project**
- **Diagnostic settings** enabled on your AI Foundry resource
- **Log Analytics workspace** configured to receive diagnostic logs
- Python **3.8+**
- Azure authentication configured via:
  - Azure CLI (`az login`)
  - or a service principal

## Configuration

### 1. Enable Diagnostic Settings

Ensure your AI Foundry resource has diagnostic settings configured to send logs to a Log Analytics workspace.

### 2. Update Configuration Variables

Before running the notebook, update the following variables with your actual values:

```python
WORKSPACE_ID = "YOUR_WORKSPACE_ID"  # Your Log Analytics workspace ID
WORKSPACE_NAME = "YOUR_WORKSPACE_NAME"  # Your Log Analytics workspace name
SUBSCRIPTION_ID = "YOUR_SUBSCRIPTION_ID"  # Your Azure subscription ID
```

### 3. Deploy the Workbook

To deploy the Azure Workbook template:

1. Open the Azure portal
2. Navigate to Azure Monitor > Workbooks
3. Click "New" and select "Advanced Editor"
4. Replace the content with the JSON from `ai_agent_monitoring_workbook.json`
5. Update the placeholder values:
   - Replace `{subscription-id}` with your subscription ID
   - Replace `{resource-group}` with your resource group name
   - Replace `{workspace-name}` with your Log Analytics workspace name

## Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Notebook

1. Start Jupyter:
   ```bash
   jupyter notebook
   ```

2. Open `12_azure_monitor_alerts.ipynb`

3. Update the configuration variables with your actual values

4. Run the cells to:
   - Query diagnostic logs
   - Analyze failures and performance
   - Create monitoring alerts
   - Build custom dashboards

### Using the Workbook

1. Deploy the workbook template as described above
2. Open the workbook in Azure Monitor
3. Select your subscription and AI Foundry resources
4. Explore the various monitoring views and insights

## Monitoring Capabilities

The sample provides monitoring for:

- **Agent Operations**: Track agent creation, updates, and execution
- **Thread Activities**: Monitor conversation threads and user interactions
- **Tool Calls**: Analyze tool usage and performance
- **Error Rates**: Track failure rates and error patterns
- **Performance Metrics**: Monitor response times and throughput
- **Resource Utilization**: Track token usage and costs

## Sample Queries

The notebook includes sample KQL queries for:

- Recent AI Agent Service activities
- Error analysis and troubleshooting
- Performance trend analysis
- Usage pattern identification
- Cost and token consumption tracking

## Security Considerations

- All sensitive information (subscription IDs, resource names) has been replaced with placeholders
- Ensure proper access controls are in place for Log Analytics workspaces
- Use managed identities or service principals for authentication in production environments