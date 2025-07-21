# GitHub Workflow Setup for Automatic GCP Deployment

This guide will help you set up automated deployment to Google Cloud Platform using GitHub Actions.

## 🏗️ Workflow Files Created

### 1. `.github/workflows/deploy-to-gcp.yml`
- **Triggers**: Automatically on push to `main` branch
- **Features**: 
  - Builds and deploys to Cloud Run
  - Runs tests on pull requests
  - Provides deployment URL and logs

### 2. `.github/workflows/manual-deploy.yml`
- **Triggers**: Manual trigger with custom options
- **Features**:
  - Choose environment (production/staging)
  - Customize memory, CPU, and instance limits
  - Deploy on-demand

## 🔐 Required Setup: GitHub Secrets

You need to configure these secrets in your GitHub repository:

### Step 1: Create Google Cloud Service Account

```bash
# Set your project ID
export PROJECT_ID="segalretirechat"

# Create service account
gcloud iam service-accounts create github-actions \
    --description="Service account for GitHub Actions" \
    --display-name="GitHub Actions"

# Get the service account email
export SA_EMAIL="github-actions@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/cloudbuild.builds.builder"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/iam.serviceAccountUser"

# Create and download service account key
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=$SA_EMAIL
```

### Step 2: Add GitHub Secrets

Go to your GitHub repository: `https://github.com/mdv05/RetirementChat`

1. **Navigate to Settings** → **Secrets and variables** → **Actions**

2. **Add these Repository Secrets**:

   **`GCP_SA_KEY`**
   - Click "New repository secret"
   - Name: `GCP_SA_KEY`
   - Value: Contents of `github-actions-key.json` file
   - Copy the entire JSON content (including curly braces)

   **`GOOGLE_API_KEY`**
   - Click "New repository secret"  
   - Name: `GOOGLE_API_KEY`
   - Value: Your Google Gemini API key from [AI Studio](https://aistudio.google.com/app/apikey)

## 🚀 How to Use the Workflows

### Automatic Deployment
1. **Push to main branch**:
   ```bash
   git add .
   git commit -m "Add deployment workflows"
   git push origin main
   ```
   
2. **GitHub Actions will automatically**:
   - Run tests
   - Build your container
   - Deploy to Cloud Run
   - Provide the live URL

### Manual Deployment
1. **Go to GitHub** → **Actions** tab
2. **Select** "Manual Deploy to GCP"
3. **Click** "Run workflow"
4. **Choose** your deployment options:
   - Environment (production/staging)
   - Memory allocation
   - CPU allocation
   - Max instances
5. **Click** "Run workflow"

## 📊 Monitoring Deployments

### View Deployment Status
- **GitHub**: Check the Actions tab for real-time progress
- **Google Cloud**: Visit [Cloud Run Console](https://console.cloud.google.com/run)

### Check Deployment Logs
```bash
# View deployment logs
gcloud logs read --service-name=retirechat --limit=50

# Follow live logs
gcloud logs tail --service-name=retirechat
```

## 🔧 Workflow Features

### Automatic Deployment (`deploy-to-gcp.yml`)
- ✅ **Tests**: Validates imports and configuration
- ✅ **Security**: Uses service account authentication
- ✅ **Build**: Uses Cloud Build for container creation
- ✅ **Deploy**: Deploys to Cloud Run with optimized settings
- ✅ **Notification**: Provides deployment URL in Actions output

### Manual Deployment (`manual-deploy.yml`)
- 🎛️ **Flexible**: Choose environment and resource allocation
- 🔄 **On-demand**: Deploy whenever needed
- 📋 **Staging**: Test changes before production
- ⚡ **Quick**: Deploy with custom settings instantly

## 🛡️ Security Features

- **Service Account**: Limited permissions for security
- **Secrets**: API keys stored securely in GitHub
- **Authentication**: Google Cloud IAM integration
- **Isolation**: Separate environments (staging/production)

## 🚨 Troubleshooting

### Common Issues

1. **Permission Denied**
   - Verify service account has correct roles
   - Check `GCP_SA_KEY` secret is valid JSON

2. **API Key Issues**
   - Verify `GOOGLE_API_KEY` secret is set
   - Test API key at [AI Studio](https://aistudio.google.com/app/apikey)

3. **Build Failures**
   - Check Dockerfile syntax
   - Verify requirements.txt is valid

### Debug Commands
```bash
# Test service account locally
gcloud auth activate-service-account --key-file=github-actions-key.json

# Validate workflow files
gh workflow list  # Requires GitHub CLI

# View workflow runs
gh run list
```

## 🎯 Next Steps

1. **Set up the service account** (run commands above)
2. **Add GitHub secrets** (GCP_SA_KEY and GOOGLE_API_KEY)
3. **Push your code** to trigger first deployment
4. **Test manual deployment** workflow
5. **Monitor your app** at the provided URL

Your RetireChat app will now deploy automatically on every push to main! 🚀 