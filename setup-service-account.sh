#!/bin/bash

# GitHub Actions Service Account Setup Script
# Run this script to create the service account and permissions for GitHub Actions

set -e

# Configuration
PROJECT_ID="retirementchat"
SA_NAME="github-actions"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
KEY_FILE="github-actions-key.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔐 Setting up GitHub Actions Service Account${NC}"

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}❌ Error: Not authenticated with gcloud${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
echo -e "${YELLOW}📋 Setting GCP project to ${PROJECT_ID}...${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable iam.googleapis.com

# Check if service account already exists
if gcloud iam service-accounts describe $SA_EMAIL >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Service account ${SA_EMAIL} already exists${NC}"
else
    # Create service account
    echo -e "${YELLOW}👤 Creating service account: ${SA_EMAIL}...${NC}"
    gcloud iam service-accounts create $SA_NAME \
        --description="Service account for GitHub Actions CI/CD" \
        --display-name="GitHub Actions"
fi

# Grant necessary permissions
echo -e "${YELLOW}🔑 Granting IAM permissions...${NC}"

# Cloud Run permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/run.admin"

# Storage permissions (for Cloud Build)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/storage.admin"

# Cloud Build permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/cloudbuild.builds.builder"

# Service Account User (to deploy as service account)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/iam.serviceAccountUser"

# Container Registry permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/storage.objectAdmin"

# Create service account key
echo -e "${YELLOW}🗝️  Creating service account key...${NC}"
gcloud iam service-accounts keys create $KEY_FILE \
    --iam-account=$SA_EMAIL

echo -e "${GREEN}✅ Service account setup completed!${NC}"
echo -e "${BLUE}📋 Next steps:${NC}"
echo -e "1. Go to your GitHub repository: ${YELLOW}https://github.com/mdv05/RetirementChat${NC}"
echo -e "2. Navigate to: ${YELLOW}Settings → Secrets and variables → Actions${NC}"
echo -e "3. Add these secrets:"
echo -e "   ${YELLOW}GCP_SA_KEY${NC}: Contents of ${KEY_FILE}"
echo -e "   ${YELLOW}GOOGLE_API_KEY${NC}: Your Google Gemini API key"
echo ""
echo -e "${BLUE}🔐 Service Account Key (copy this to GitHub secret 'GCP_SA_KEY'):${NC}"
echo -e "${YELLOW}==================== START JSON ====================${NC}"
cat $KEY_FILE
echo -e "${YELLOW}===================== END JSON =====================${NC}"
echo ""
echo -e "${RED}🚨 IMPORTANT: Delete this key file after copying to GitHub:${NC}"
echo -e "   ${YELLOW}rm $KEY_FILE${NC}"
echo ""
echo -e "${GREEN}🚀 Ready to deploy! Push your code to trigger the workflow.${NC}" 