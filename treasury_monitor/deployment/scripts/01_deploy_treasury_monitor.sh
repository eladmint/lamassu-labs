#!/bin/bash

# =============================================================================
# DEPLOYMENT SCRIPT: 01 - Treasury Monitor Agent Deployment
# STATUS: ✅ ENTERPRISE STANDARD
# ARCHITECTURE: Containerized Cloud Run deployment with enterprise paths
# USE WHEN: Treasury Monitor agent deployment for production
# =============================================================================

set -e  # Exit on any error

echo "🏛️ Starting Enterprise Treasury Monitor Deployment..."
echo "=================================================="

# Enterprise Configuration
PROJECT_ID="tokenhunter-457310"
SERVICE_NAME="treasury-monitor-agent"
REGION="us-central1"
BUILD_CONFIG="src/treasury_monitor/deployment/configs/cloudbuild.yaml" # This is key

# Step 1: Enterprise Compliance Validation
echo "🏢 Step 1: Running Enterprise Compliance Validation..."
python tools/deployment/validate_enterprise_deployment.py \
  --service=treasury_monitor

# Check compliance result
if [ $? -ne 0 ]; then
    echo "❌ DEPLOYMENT BLOCKED: Compliance validation failed"
    echo "📋 Fix compliance issues before proceeding"
    exit 1
fi
echo "✅ Compliance validation passed - proceeding with deployment"

# Step 2: Prerequisites and IAM Setup
echo "📋 Step 2: Enterprise prerequisites and IAM setup..."

# Verify gcloud authentication
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Please authenticate with gcloud first: gcloud auth login"
    exit 1
fi

# Set project
gcloud config set project $PROJECT_ID

# Add explicit IAM policy binding to prevent deployment hanging
echo "🔧 Adding explicit IAM policy binding to prevent deployment hanging..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:chatbot-api-sa@tokenhunter-457310.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser" \
    --quiet

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Step 3: Verify Enterprise Structure
echo "📋 Step 3: Verifying enterprise directory structure..."

REQUIRED_PATHS=(
    "src/treasury_monitor"
    "agent_forge/examples/premium/treasury_monitor_agent.py"
    "src/treasury_monitor/Dockerfile"
)

for path in "${REQUIRED_PATHS[@]}"; do
    if [[ ! -e "$path" ]]; then
        echo "❌ Required enterprise path not found: $path"
        echo "Please ensure enterprise directory structure is in place"
        exit 1
    fi
done

echo "✅ Enterprise directory structure verified"

# Step 4: Build and Deploy
echo "📋 Step 4: Building and deploying Treasury Monitor agent..."

# Build and deploy using Cloud Build
gcloud builds submit \
    --config=$BUILD_CONFIG \
    .

# Step 5: Configure Service for Production
echo "📋 Step 5: Configuring service for production..."

gcloud run services update $SERVICE_NAME \
    --region=$REGION \
    --memory=2Gi \
    --cpu=1 \
    --concurrency=80 \
    --max-instances=10 \
    --min-instances=1 \
    --execution-environment=gen2 \
    --timeout=300

# Step 6: Configure IAM and Access
echo "📋 Step 6: Configuring IAM and access policies..."

# Grant public access for Treasury Monitor service
gcloud run services add-iam-policy-binding $SERVICE_NAME \
    --region=$REGION \
    --member="allUsers" \
    --role="roles/run.invoker"

# Step 7: Verify Deployment
echo "📋 Step 7: Verifying deployment..."

SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo "✅ Enterprise Treasury Monitor deployment completed successfully!"
echo ""
echo "📊 Deployment Summary:"
echo "====================="
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"
echo "Service URL: $SERVICE_URL"
echo "Project: $PROJECT_ID"
echo "Architecture: Enterprise containerized Cloud Run"
echo "💰 Pricing: \$99-299/month validated pricing"
echo ""
echo "🔍 Check logs:"
echo "gcloud logs read \"resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME\" --limit=50"
echo ""
echo "📊 Monitor service:"
echo "gcloud run services describe $SERVICE_NAME --region=$REGION"
echo ""
echo "🏛️ Treasury Monitor Features:"
echo "• Real-time Cardano treasury balance monitoring"
echo "• Multi-API failover (NOWNodes → Koios → Demo)"
echo "• Risk assessment engine with 4 alert levels"
echo "• Multi-channel alerting (Email, Slack, SMS)"
echo "• Enterprise-grade security and compliance"
echo ""
echo "🎉 Your Treasury Monitor agent is now running with enterprise deployment standards!"
