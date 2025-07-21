#!/bin/bash

# RetireChat Cloud Build Deployment Script
# No local Docker installation required!

set -e

# Configuration
PROJECT_ID="retirementchat"
REGION="us-central1"
SERVICE_NAME="retirechat"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting RetireChat deployment using Cloud Build${NC}"

# Check if required environment variables are set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${RED}❌ Error: GOOGLE_API_KEY environment variable is not set${NC}"
    echo "Please set your Google API key: export GOOGLE_API_KEY=your_api_key_here"
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    exit 1
fi

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Error: gcloud CLI is not installed${NC}"
    echo "Please install gcloud CLI: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}❌ Error: Not authenticated with gcloud${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
echo -e "${YELLOW}📋 Setting GCP project...${NC}"
gcloud config set project $PROJECT_ID

echo -e "${YELLOW}🏗️  Building and deploying using Cloud Build...${NC}"

# Submit to Cloud Build and deploy to Cloud Run in one step
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌐 Your app is available at: ${SERVICE_URL}${NC}"
echo -e "${BLUE}📊 View logs: gcloud logs read --service-name=${SERVICE_NAME}${NC}"
echo -e "${BLUE}🔧 Manage service: https://console.cloud.google.com/run/detail/${REGION}/${SERVICE_NAME}${NC}"
echo -e "${BLUE}💡 Tip: Cloud Build automatically built your container remotely!${NC}" 