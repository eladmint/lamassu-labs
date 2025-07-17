# ☁️ Google Cloud Platform Deployment Guide for TrustWrapper

**Version**: 1.0.0  
**Last Updated**: June 22, 2025  
**Compatibility**: TrustWrapper v1.0+

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Architecture Options](#architecture-options)
4. [Deployment Methods](#deployment-methods)
5. [Step-by-Step Deployment](#step-by-step-deployment)
6. [Configuration](#configuration)
7. [Monitoring & Scaling](#monitoring--scaling)
8. [Security Best Practices](#security-best-practices)
9. [Cost Optimization](#cost-optimization)
10. [Troubleshooting](#troubleshooting)

## 🎯 Overview

This guide provides comprehensive instructions for deploying TrustWrapper on Google Cloud Platform (GCP). TrustWrapper leverages GCP's cutting-edge AI/ML services, global infrastructure, and developer-friendly tools for optimal performance.

### **Key Benefits of GCP Deployment**
- **AI/ML Native**: Direct integration with Vertex AI and Google AI services
- **Developer Friendly**: Excellent tooling and documentation
- **Global Network**: Premium tier network with low latency
- **Kubernetes Native**: GKE is the gold standard for K8s
- **Cost Effective**: Sustained use discounts and committed use savings

## 📋 Prerequisites

### **GCP Account Requirements**
- [ ] GCP project with billing enabled
- [ ] gcloud CLI installed and configured
- [ ] Required APIs enabled (Compute, Container, Cloud Run, etc.)
- [ ] Service account with appropriate permissions
- [ ] VPC network configured

### **Local Development Requirements**
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize gcloud
gcloud init
gcloud auth application-default login

# Set default project
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable sqladmin.googleapis.com

# Install additional tools
pip install google-cloud-secret-manager google-cloud-logging
```

### **TrustWrapper Requirements**
- Docker image in Google Container Registry or Artifact Registry
- Leo contract addresses for blockchain features
- API keys stored in Secret Manager

## 🏗️ Architecture Options

### **Option 1: Serverless (Cloud Run + Cloud Functions)**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Cloud Load    │────▶│   Cloud Run     │────▶│   Firestore     │
│   Balancing     │     │   (Container)   │     │   (NoSQL DB)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   Vertex AI     │
                        │   (ML Platform) │
                        └─────────────────┘
```

### **Option 2: Container-Based (GKE)**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Cloud Load    │────▶│   GKE Cluster   │────▶│  Cloud SQL      │
│   Balancing     │     │   (Autopilot)   │     │  (PostgreSQL)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   Memorystore   │
                        │   (Redis)       │
                        └─────────────────┘
```

### **Option 3: Hybrid Architecture**
```
┌─────────────────┐
│   Cloud CDN     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   API Gateway   │────▶│ Cloud Functions │ (Light operations)
└────────┬────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   Cloud Load    │────▶│   Cloud Run     │ (Heavy operations)
│   Balancing     │     │   (Autoscale)   │
└─────────────────┘     └─────────────────┘
```

## 🚀 Deployment Methods

### **Method 1: Cloud Run (Recommended for Quick Start)**

#### **1. Build and Push Container**
```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Build container
docker build -t gcr.io/YOUR-PROJECT-ID/trustwrapper:latest .

# Push to Container Registry
docker push gcr.io/YOUR-PROJECT-ID/trustwrapper:latest
```

#### **2. Deploy to Cloud Run**
```bash
# Deploy service
gcloud run deploy trustwrapper-api \
  --image gcr.io/YOUR-PROJECT-ID/trustwrapper:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --memory 2Gi \
  --cpu 2 \
  --min-instances 1 \
  --max-instances 100 \
  --set-env-vars "ENVIRONMENT=production" \
  --set-secrets "ANTHROPIC_API_KEY=anthropic-api-key:latest" \
  --set-secrets "GOOGLE_API_KEY=google-api-key:latest" \
  --set-cloudsql-instances YOUR-PROJECT-ID:us-central1:trustwrapper-db \
  --service-account trustwrapper-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com

# Get service URL
gcloud run services describe trustwrapper-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

#### **3. Configure Cloud Run Service**
```yaml
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: trustwrapper-api
  annotations:
    run.googleapis.com/launch-stage: GA
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "100"
        run.googleapis.com/cpu-throttling: "false"
        run.googleapis.com/startup-cpu-boost: "true"
    spec:
      containerConcurrency: 100
      timeoutSeconds: 300
      serviceAccountName: trustwrapper-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com
      containers:
      - image: gcr.io/YOUR-PROJECT-ID/trustwrapper:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            cpu: "2"
            memory: "2Gi"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-url
              key: latest
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-url
              key: latest
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 1
          successThreshold: 1
          failureThreshold: 3
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          periodSeconds: 10
```

### **Method 2: Google Kubernetes Engine (GKE)**

#### **1. Create GKE Cluster**
```bash
# Create Autopilot cluster (recommended)
gcloud container clusters create-auto trustwrapper-cluster \
  --region us-central1 \
  --release-channel regular \
  --network default \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr 172.16.0.0/28

# Get credentials
gcloud container clusters get-credentials trustwrapper-cluster \
  --region us-central1
```

#### **2. Deploy to GKE**
```yaml
# trustwrapper-k8s.yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: trustwrapper
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trustwrapper-api
  namespace: trustwrapper
spec:
  replicas: 3
  selector:
    matchLabels:
      app: trustwrapper
  template:
    metadata:
      labels:
        app: trustwrapper
    spec:
      serviceAccountName: trustwrapper-ksa
      containers:
      - name: api
        image: gcr.io/YOUR-PROJECT-ID/trustwrapper:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: trustwrapper-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: trustwrapper-secrets
              key: redis-url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: trustwrapper-service
  namespace: trustwrapper
  annotations:
    cloud.google.com/neg: '{"ingress": true}'
    cloud.google.com/backend-config: '{"ports": {"80":"trustwrapper-backendconfig"}}'
spec:
  type: LoadBalancer
  selector:
    app: trustwrapper
  ports:
  - port: 80
    targetPort: 8000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: trustwrapper-hpa
  namespace: trustwrapper
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: trustwrapper-api
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
---
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: trustwrapper-backendconfig
  namespace: trustwrapper
spec:
  connectionDraining:
    drainingTimeoutSec: 60
  healthCheck:
    checkIntervalSec: 30
    port: 8000
    type: HTTP
    requestPath: /health
  sessionAffinity:
    affinityType: "CLIENT_IP"
    affinityCookieTtlSec: 86400
  timeoutSec: 300
  cdn:
    enabled: true
    cachePolicy:
      includeHost: true
      includeProtocol: true
      includeQueryString: false
    negativeCaching: true
    negativeCachingPolicy:
    - code: 404
      ttl: 120
    - code: 410
      ttl: 14400
```

```bash
# Create secrets
kubectl create secret generic trustwrapper-secrets \
  --namespace trustwrapper \
  --from-literal=database-url="postgresql://..." \
  --from-literal=redis-url="redis://..."

# Deploy application
kubectl apply -f trustwrapper-k8s.yaml

# Check deployment
kubectl get all -n trustwrapper
```

### **Method 3: Infrastructure as Code with Terraform**

#### **1. Terraform Configuration**
```hcl
# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "compute.googleapis.com",
    "container.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "redis.googleapis.com",
    "sqladmin.googleapis.com"
  ])
  
  service = each.key
  disable_on_destroy = false
}

# VPC Network
resource "google_compute_network" "vpc" {
  name                    = "trustwrapper-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "trustwrapper-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
  
  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.1.0.0/24"
  }
  
  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.2.0.0/20"
  }
}

# Cloud SQL
resource "google_sql_database_instance" "postgres" {
  name             = "trustwrapper-db"
  database_version = "POSTGRES_14"
  region           = var.region
  
  settings {
    tier = "db-g1-small"
    
    backup_configuration {
      enabled = true
      start_time = "03:00"
    }
    
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
    
    database_flags {
      name  = "max_connections"
      value = "100"
    }
  }
  
  deletion_protection = true
}

resource "google_sql_database" "database" {
  name     = "trustwrapper"
  instance = google_sql_database_instance.postgres.name
}

# Redis
resource "google_redis_instance" "cache" {
  name           = "trustwrapper-redis"
  tier           = "STANDARD_HA"
  memory_size_gb = 5
  region         = var.region
  
  authorized_network = google_compute_network.vpc.id
  
  redis_configs = {
    maxmemory-policy = "allkeys-lru"
  }
}

# Cloud Run
resource "google_cloud_run_service" "api" {
  name     = "trustwrapper-api"
  location = var.region
  
  template {
    spec {
      service_account_name = google_service_account.trustwrapper.email
      
      containers {
        image = "gcr.io/${var.project_id}/trustwrapper:latest"
        
        env {
          name  = "DATABASE_URL"
          value = "postgresql://user:pass@${google_sql_database_instance.postgres.private_ip_address}/trustwrapper"
        }
        
        env {
          name  = "REDIS_URL"
          value = "redis://${google_redis_instance.cache.host}:${google_redis_instance.cache.port}"
        }
        
        resources {
          limits = {
            cpu    = "2000m"
            memory = "2Gi"
          }
        }
      }
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"      = "1"
        "autoscaling.knative.dev/maxScale"      = "100"
        "run.googleapis.com/cpu-throttling"     = "false"
        "run.googleapis.com/startup-cpu-boost"  = "true"
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
}

# IAM
resource "google_service_account" "trustwrapper" {
  account_id   = "trustwrapper-sa"
  display_name = "TrustWrapper Service Account"
}

resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.trustwrapper.email}"
}

# Outputs
output "service_url" {
  value = google_cloud_run_service.api.status[0].url
}
```

#### **2. Deploy with Terraform**
```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="project_id=YOUR-PROJECT-ID" -var="region=us-central1"

# Apply configuration
terraform apply -auto-approve
```

## ⚙️ Configuration

### **Environment Variables**
```bash
# Core Configuration
ENVIRONMENT=production
API_PORT=8000
LOG_LEVEL=INFO
GOOGLE_CLOUD_PROJECT=YOUR-PROJECT-ID

# Database Configuration
DATABASE_URL=postgresql://user:pass@/trustwrapper?host=/cloudsql/PROJECT:REGION:INSTANCE
REDIS_URL=redis://10.0.0.3:6379

# AI Service Keys (from Secret Manager)
ANTHROPIC_API_KEY=${sm://anthropic-api-key}
GOOGLE_API_KEY=${sm://google-api-key}
VERTEX_AI_LOCATION=us-central1

# Blockchain Configuration
ALEO_NETWORK=testnet3
ALEO_PRIVATE_KEY=${sm://aleo-private-key}

# GCP Service Configuration
CLOUD_STORAGE_BUCKET=trustwrapper-artifacts
CLOUD_LOGGING_ENABLED=true
CLOUD_TRACE_ENABLED=true
```

### **Secret Manager Integration**
```python
# Python integration
from google.cloud import secretmanager

def get_secret(secret_id: str, version: str = "latest") -> str:
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(name=name)
    
    return response.payload.data.decode("UTF-8")

# Usage
ANTHROPIC_API_KEY = get_secret("anthropic-api-key")
```

```bash
# Create secrets via CLI
echo -n "sk-ant-..." | gcloud secrets create anthropic-api-key \
  --data-file=- \
  --replication-policy="automatic"

# Grant access to service account
gcloud secrets add-iam-policy-binding anthropic-api-key \
  --member="serviceAccount:trustwrapper-sa@PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## 📊 Monitoring & Scaling

### **Cloud Monitoring Setup**
```python
# Application instrumentation
from google.cloud import monitoring_v3
from opencensus.ext.stackdriver import stats_exporter
from opencensus.stats import aggregation, measure, stats, view

# Initialize exporter
exporter = stats_exporter.new_stats_exporter(
    project_id=os.environ.get("GOOGLE_CLOUD_PROJECT")
)
stats.stats.view_manager.register_exporter(exporter)

# Define custom metrics
verification_measure = measure.MeasureInt(
    "trustwrapper/verifications",
    "Number of verifications processed",
    "1"
)

latency_measure = measure.MeasureFloat(
    "trustwrapper/latency",
    "Verification latency",
    "ms"
)

# Create views
verification_view = view.View(
    "trustwrapper/verifications/count",
    "Count of verifications",
    ["status", "model"],
    verification_measure,
    aggregation.CountAggregation()
)

latency_view = view.View(
    "trustwrapper/latency/distribution",
    "Latency distribution",
    ["endpoint"],
    latency_measure,
    aggregation.DistributionAggregation(
        [0, 100, 200, 500, 1000, 2000, 5000]
    )
)

# Register views
stats.stats.view_manager.register_view(verification_view)
stats.stats.view_manager.register_view(latency_view)

# Record metrics in application
def record_verification(status: str, model: str, latency: float):
    mmap = stats.stats.stats_recorder.new_measurement_map()
    mmap.measure_int_put(verification_measure, 1)
    mmap.measure_float_put(latency_measure, latency)
    mmap.record({"status": status, "model": model, "endpoint": "verify"})
```

### **Cloud Logging**
```python
import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler

# Setup structured logging
client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client)

import logging
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

# Structured log entry
logger = logging.getLogger(__name__)
logger.info(
    "Verification completed",
    extra={
        "labels": {
            "service": "trustwrapper",
            "version": "1.0.0"
        },
        "json_fields": {
            "user_id": "user123",
            "verification_id": "ver456",
            "latency_ms": 234,
            "model_used": "claude-3",
            "success": True
        }
    }
)
```

### **Auto-scaling Configuration**

#### **Cloud Run Auto-scaling**
```yaml
# Annotation-based configuration
metadata:
  annotations:
    # Concurrency
    run.googleapis.com/execution-environment: gen2
    autoscaling.knative.dev/target: "80"
    
    # Scale bounds
    autoscaling.knative.dev/minScale: "1"
    autoscaling.knative.dev/maxScale: "100"
    
    # Scale down delay
    autoscaling.knative.dev/scaleDownDelay: "60s"
    
    # Startup optimization
    run.googleapis.com/startup-cpu-boost: "true"
```

#### **GKE Auto-scaling with Custom Metrics**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: trustwrapper-custom-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: trustwrapper-api
  minReplicas: 3
  maxReplicas: 100
  metrics:
  - type: External
    external:
      metric:
        name: custom.googleapis.com|trustwrapper|verifications_per_second
      target:
        type: AverageValue
        averageValue: "100"
  - type: External
    external:
      metric:
        name: pubsub.googleapis.com|subscription|num_undelivered_messages
        selector:
          matchLabels:
            resource.labels.subscription_id: trustwrapper-tasks
      target:
        type: Value
        value: "30"
```

## 🔒 Security Best Practices

### **VPC Security**
```bash
# Create VPC with private Google access
gcloud compute networks create trustwrapper-vpc \
  --subnet-mode=custom \
  --bgp-routing-mode=regional

gcloud compute networks subnets create trustwrapper-subnet \
  --network=trustwrapper-vpc \
  --region=us-central1 \
  --range=10.0.0.0/24 \
  --enable-private-ip-google-access \
  --enable-flow-logs

# Firewall rules
gcloud compute firewall-rules create allow-internal \
  --network=trustwrapper-vpc \
  --allow=tcp:0-65535,udp:0-65535,icmp \
  --source-ranges=10.0.0.0/24

gcloud compute firewall-rules create allow-health-checks \
  --network=trustwrapper-vpc \
  --allow=tcp:8000 \
  --source-ranges=35.191.0.0/16,130.211.0.0/22
```

### **Identity and Access Management (IAM)**
```bash
# Create custom role
gcloud iam roles create trustwrapperServiceRole \
  --project=YOUR-PROJECT-ID \
  --title="TrustWrapper Service Role" \
  --description="Custom role for TrustWrapper services" \
  --permissions=secretmanager.versions.access,cloudtrace.traces.patch,logging.logEntries.create

# Workload Identity for GKE
kubectl create serviceaccount trustwrapper-ksa \
  --namespace trustwrapper

gcloud iam service-accounts add-iam-policy-binding \
  trustwrapper-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:YOUR-PROJECT-ID.svc.id.goog[trustwrapper/trustwrapper-ksa]"

kubectl annotate serviceaccount trustwrapper-ksa \
  --namespace trustwrapper \
  iam.gke.io/gcp-service-account=trustwrapper-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com
```

### **Encryption**
```python
# Cloud KMS integration
from google.cloud import kms

def encrypt_sensitive_data(plaintext: str, key_name: str) -> bytes:
    client = kms.KeyManagementServiceClient()
    
    response = client.encrypt(
        request={
            "name": key_name,
            "plaintext": plaintext.encode("utf-8")
        }
    )
    
    return response.ciphertext

# Usage
key_name = "projects/PROJECT/locations/global/keyRings/trustwrapper/cryptoKeys/data-key"
encrypted = encrypt_sensitive_data("sensitive_data", key_name)
```

## 💰 Cost Optimization

### **Cost Breakdown (Estimated Monthly)**
| Service | Configuration | Estimated Cost |
|:--------|:-------------|:---------------|
| **Cloud Run** | 2 vCPU, 2GB RAM, 1M requests | ~$50 |
| **Cloud SQL** | db-g1-small, 100GB SSD | ~$75 |
| **Memorystore Redis** | 5GB Standard | ~$200 |
| **Load Balancing** | 1M requests | ~$25 |
| **Cloud Storage** | 100GB standard | ~$2 |
| **Monitoring** | 50GB logs | ~$25 |
| **Total** | | ~$377/month |

### **Cost Optimization Strategies**

#### **1. Committed Use Discounts**
```bash
# Create 1-year commitment
gcloud compute commitments create trustwrapper-commitment \
  --region=us-central1 \
  --resources=vcpu=10,memory=40GB \
  --plan=TWELVE_MONTH
```

#### **2. Preemptible/Spot Instances**
```yaml
# For batch processing
spec:
  nodeSelector:
    cloud.google.com/gke-preemptible: "true"
  tolerations:
  - key: cloud.google.com/gke-preemptible
    operator: Equal
    value: "true"
    effect: NoSchedule
```

#### **3. Resource Optimization**
```bash
# Right-size Cloud SQL
gcloud sql instances patch trustwrapper-db \
  --tier=db-f1-micro \
  --activation-policy=ALWAYS

# Schedule non-prod resources
gcloud scheduler jobs create pubsub start-dev \
  --schedule="0 9 * * 1-5" \
  --topic=resource-scheduler \
  --message-body='{"action":"start","resource":"dev-cluster"}'
```

#### **4. Cost Monitoring**
```bash
# Set budget alerts
gcloud billing budgets create \
  --billing-account=BILLING-ACCOUNT-ID \
  --display-name="TrustWrapper Budget" \
  --budget-amount=500 \
  --threshold-rule=percent=0.5,basis=current-spend \
  --threshold-rule=percent=0.9,basis=current-spend \
  --threshold-rule=percent=1.0,basis=current-spend
```

## 🔧 Troubleshooting

### **Common Issues**

#### **1. Cloud Run Deployment Failures**
```bash
# Check build logs
gcloud builds list --limit=5

# Check deployment logs
gcloud run services describe trustwrapper-api \
  --region=us-central1 \
  --format="value(status.conditions)"

# View service logs
gcloud logging read "resource.type=cloud_run_revision \
  AND resource.labels.service_name=trustwrapper-api" \
  --limit=50 \
  --format=json
```

#### **2. Database Connection Issues**
```bash
# Test Cloud SQL proxy
cloud_sql_proxy -instances=PROJECT:REGION:INSTANCE=tcp:5432

# Check private IP connectivity
gcloud sql instances describe trustwrapper-db \
  --format="value(ipAddresses[0].ipAddress)"

# Verify service account permissions
gcloud projects get-iam-policy YOUR-PROJECT-ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:trustwrapper-sa@*"
```

#### **3. Performance Issues**
```sql
-- Cloud Monitoring MQL query
fetch cloud_run_revision
| metric 'run.googleapis.com/request_latencies'
| filter resource.service_name == 'trustwrapper-api'
| group_by 1m, [value_latencies_percentile: percentile(value.latencies, 95)]
| every 1m
```

#### **4. Authentication/Authorization Issues**
```bash
# Check service account
gcloud iam service-accounts describe \
  trustwrapper-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com

# Test impersonation
gcloud auth print-access-token \
  --impersonate-service-account=trustwrapper-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com

# Verify secret access
gcloud secrets versions access latest \
  --secret=anthropic-api-key \
  --impersonate-service-account=trustwrapper-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com
```

### **Debugging Tools**
```bash
# Cloud Shell debugging
gcloud cloud-shell ssh

# Port forwarding for local testing
kubectl port-forward -n trustwrapper \
  deployment/trustwrapper-api 8000:8000

# Cloud Trace
gcloud trace list --limit=10

# Error Reporting
gcloud beta error-reporting events list \
  --service=trustwrapper-api
```

## 📚 Additional Resources

### **GCP Documentation**
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)

### **TrustWrapper Resources**
- [API Reference Documentation](/docs/api/TRUSTWRAPPER_API_REFERENCE.md)
- [Architecture Overview](/docs/architecture/TECHNICAL_ARCHITECTURE.md)
- [Security Guidelines](/docs/security/SECURITY_ARCHITECTURE.md)

### **Support**
- **GCP Support**: Via Cloud Console
- **TrustWrapper Support**: support@trustwrapper.ai
- **Community**: [Discord](https://discord.gg/trustwrapper)

---

**Next Steps**: Set up Cloud Build for CI/CD automation and configure Cloud Armor for DDoS protection and WAF capabilities.