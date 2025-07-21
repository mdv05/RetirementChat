# RetireChat - Google Cloud Run Deployment Guide

This guide will help you deploy your RetireChat Streamlit application to Google Cloud Platform using Docker and Cloud Run.

## Prerequisites

1. **Google Cloud Platform Account**: Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud CLI**: Install from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
3. **Docker**: Install from [docker.com/get-started](https://www.docker.com/get-started)
4. **Google API Key**: Get a Gemini API key from [AI Studio](https://aistudio.google.com/app/apikey)

## Quick Deployment (Using the Script)

### Step 1: Set up your environment

```bash
# Authenticate with Google Cloud
gcloud auth login

# Set your project ID (replace with your actual project ID)
export PROJECT_ID="your-gcp-project-id"
gcloud config set project $PROJECT_ID

# Set your Google API key
export GOOGLE_API_KEY="your-google-api-key-here"
```

### Step 2: Update the deployment script

Edit `deploy.sh` and update the `PROJECT_ID` variable:

```bash
PROJECT_ID="your-actual-gcp-project-id"
```

### Step 3: Make the script executable and run it

```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
- ✅ Build your Docker image
- ✅ Push it to Google Container Registry
- ✅ Deploy to Cloud Run
- ✅ Provide you with the live URL

## Manual Deployment Steps

If you prefer to deploy manually, follow these steps:

### Step 1: Enable required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Build and push the Docker image

```bash
# Build the image
docker build -t gcr.io/$PROJECT_ID/retirechat .

# Push to Container Registry
docker push gcr.io/$PROJECT_ID/retirechat
```

### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy retirechat \
    --image gcr.io/$PROJECT_ID/retirechat \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY
```

## Using Cloud Build for CI/CD

For automated deployments, you can use the included `cloudbuild.yaml` file:

### Step 1: Update Cloud Build configuration

Edit `cloudbuild.yaml` and replace `your-google-api-key-here` with your actual API key.

### Step 2: Create a Cloud Build trigger

```bash
# Create a trigger for automatic deployments
gcloud builds triggers create github \
    --repo-name=your-repo-name \
    --repo-owner=your-github-username \
    --branch-pattern="^main$" \
    --build-config=cloudbuild.yaml
```

## Environment Variables

Your app requires the following environment variable:

- `GOOGLE_API_KEY`: Your Google Gemini API key

## Configuration Details

### Docker Configuration
- **Base Image**: `python:3.9-slim`
- **Port**: 8080 (Cloud Run standard)
- **User**: Non-root user for security
- **Health Check**: Included for monitoring

### Cloud Run Configuration
- **Memory**: 1GB
- **CPU**: 1 vCPU
- **Max Instances**: 10
- **Region**: us-central1
- **Authentication**: Public (unauthenticated access)

## Monitoring and Logs

### View logs
```bash
gcloud logs read --service-name=retirechat
```

### View metrics
Visit the [Cloud Run Console](https://console.cloud.google.com/run) to see:
- Request metrics
- Error rates
- Latency
- Instance usage

## Troubleshooting

### Common Issues

1. **Authentication Error**
   ```bash
   gcloud auth login
   ```

2. **API Not Enabled**
   ```bash
   gcloud services enable run.googleapis.com
   ```

3. **Insufficient Permissions**
   - Ensure your user has Cloud Run Admin and Storage Admin roles

4. **Docker Build Fails**
   - Check that all dependencies in `requirements.txt` are valid
   - Ensure Docker is running

### Local Testing

Test your Docker image locally before deploying:

```bash
# Build the image
docker build -t retirechat-local .

# Run locally
docker run -p 8080:8080 -e GOOGLE_API_KEY=$GOOGLE_API_KEY retirechat-local
```

Visit http://localhost:8080 to test your app.

## Cost Optimization

Cloud Run pricing is based on:
- **Requests**: $0.40 per million requests
- **CPU/Memory**: $0.00002400 per vCPU-second
- **Free Tier**: 2 million requests per month

To optimize costs:
- Set appropriate memory limits
- Use minimum CPU allocation
- Set max instances based on expected traffic

## Security Best Practices

1. **Environment Variables**: Never commit API keys to version control
2. **IAM**: Use least privilege principle for service accounts
3. **VPC**: Consider VPC connectors for private resources
4. **HTTPS**: Cloud Run provides automatic SSL certificates

## Next Steps

After deployment:
1. Set up custom domain (optional)
2. Configure monitoring and alerting
3. Set up backup strategies
4. Consider implementing authentication if needed

## Support

For issues:
- Check [Cloud Run documentation](https://cloud.google.com/run/docs)
- Review [Streamlit deployment guide](https://docs.streamlit.io/deploy/tutorials/docker)
- Use `gcloud logs read` for debugging

Your RetireChat app is now ready for production! 🚀 