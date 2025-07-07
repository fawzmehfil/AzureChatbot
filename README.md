# Azure ChatGPT-Style Chatbot (React + Flask + Azure OpenAI)

This project is a fullstack chatbot application powered by React (frontend) and Flask (backend), integrated with Azure OpenAI's GPT model. It is deployed using Azure App Service and supports persistent message context in the client session.

## Features

- Chat interface built with React
- Backend API built with Flask
- Azure OpenAI GPT-35-Turbo for natural language responses
- Client-side conversation memory
- Deployed on Azure App Service
- Environment-secured credentials

## Tech Stack

| Layer      | Technology                  |
|------------|-----------------------------|
| Frontend   | React                       |
| Backend    | Flask (Python)              |
| AI Model   | Azure OpenAI (GPT-35-Turbo) |
| Hosting    | Azure App Service           |
| Deployment | az webapp deploy (zip)      |

## Environment Variables (Required)

These must be set in your Azure App Service Configuration Settings:

| Variable Name           | Description                                             |
|-------------------------|---------------------------------------------------------|
| `OPENAI_API_KEY`        | Your Azure OpenAI resource key                          |
| `AZURE_ENDPOINT`        | Your Azure OpenAI endpoint (e.g. https://...)           |
| `AZURE_DEPLOYMENT_NAME` | Name of your GPT deployment model                       |
| `SQL_SERVER`            | Azure SQL Server FQDN (e.g. `chat-server.database...`)  |
| `SQL_DATABASE`          | SQL database name (e.g. `chatdb`)                       |
| `SQL_USERNAME`          | SQL username (e.g. `sqladmin@servername`)              |
| `SQL_PASSWORD`          | SQL user password                                       |


## Setup Instructions

### 1. Prepare Azure OpenAI

- Create a deployment for gpt-35-turbo
- Copy your key, endpoint, and deployment name

### 2. Navigate to frontend and build
cd frontend
npm install
npm run build

### 3.. Package App
cd ..
zip -r app.zip backend

### 4. Deploy to Azure
az webapp deploy \
  --resource-group <your-resource-group> \
  --name <your-app-name> \
  --src-path app.zip \
  --type zip

### 5. Visit the deployed web app
https://<your-app-name>.azurewebsites.net


With this setup, you've successfully deployed a full-stack React + Flask AI chatbot to Azure App Service, integrating Azure OpenAI for real-time conversational responses. This project demonstrates how to connect modern front-end frameworks with cloud-based AI services, making it a strong foundation for more advanced features such as user authentication, database integration, or multi-user conversation history.

