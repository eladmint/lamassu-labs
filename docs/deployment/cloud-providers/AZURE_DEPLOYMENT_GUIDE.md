# ☁️ Azure Deployment Guide for TrustWrapper

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

This guide provides comprehensive instructions for deploying TrustWrapper on Microsoft Azure. TrustWrapper leverages Azure's enterprise-grade infrastructure and native AI/ML services for optimal performance and scalability.

### **Key Benefits of Azure Deployment**
- **Enterprise Integration**: Seamless integration with Microsoft ecosystem
- **AI Services**: Native Azure OpenAI and Cognitive Services support
- **Hybrid Cloud**: Strong on-premises integration capabilities
- **Compliance**: Extensive compliance certifications
- **Global Reach**: 60+ regions worldwide

## 📋 Prerequisites

### **Azure Account Requirements**
- [ ] Azure subscription with appropriate permissions
- [ ] Azure CLI installed and configured
- [ ] Service Principal for deployment automation
- [ ] Resource Group created
- [ ] Virtual Network configured

### **Local Development Requirements**
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Set default subscription
az account set --subscription "Your Subscription Name"

# Install additional tools
pip install azure-cli-core azure-mgmt-containerinstance
npm install -g @azure/arm-templates
```

### **TrustWrapper Requirements**
- Docker image in Azure Container Registry
- Leo contract addresses for blockchain features
- API keys stored in Azure Key Vault

## 🏗️ Architecture Options

### **Option 1: Serverless (Azure Functions + Logic Apps)**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   API Management│────▶│ Azure Functions │────▶│  Cosmos DB      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │ Azure OpenAI    │
                        │ Service         │
                        └─────────────────┘
```

### **Option 2: Container-Based (Recommended)**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Application     │────▶│ Container       │────▶│ Azure Database  │
│ Gateway         │     │ Instances/AKS   │     │ for PostgreSQL  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │ Azure Cache     │
                        │ for Redis       │
                        └─────────────────┘
```

### **Option 3: Enterprise Hybrid**
```
┌─────────────────┐
│   Front Door    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ API Management  │────▶│ Azure Functions │ (Light operations)
└────────┬────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ App Gateway     │────▶│ AKS Cluster     │ (Heavy operations)
└─────────────────┘     └─────────────────┘
```

## 🚀 Deployment Methods

### **Method 1: Azure Resource Manager (ARM) Templates**

#### **1. Create ARM Template**
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "containerGroupName": {
      "type": "string",
      "defaultValue": "trustwrapper-api",
      "metadata": {
        "description": "Name for the container group"
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]",
      "metadata": {
        "description": "Location for all resources"
      }
    }
  },
  "variables": {
    "containerRegistryName": "[concat('trustwrapperacr', uniqueString(resourceGroup().id))]",
    "keyVaultName": "[concat('trustwrapperkv', uniqueString(resourceGroup().id))]",
    "redisName": "[concat('trustwrapperredis', uniqueString(resourceGroup().id))]",
    "postgresName": "[concat('trustwrapperdb', uniqueString(resourceGroup().id))]"
  },
  "resources": [
    {
      "type": "Microsoft.ContainerRegistry/registries",
      "apiVersion": "2022-02-01-preview",
      "name": "[variables('containerRegistryName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Standard"
      },
      "properties": {
        "adminUserEnabled": true
      }
    },
    {
      "type": "Microsoft.KeyVault/vaults",
      "apiVersion": "2022-07-01",
      "name": "[variables('keyVaultName')]",
      "location": "[parameters('location')]",
      "properties": {
        "sku": {
          "family": "A",
          "name": "standard"
        },
        "tenantId": "[subscription().tenantId]",
        "accessPolicies": []
      }
    },
    {
      "type": "Microsoft.Cache/redis",
      "apiVersion": "2022-06-01",
      "name": "[variables('redisName')]",
      "location": "[parameters('location')]",
      "properties": {
        "sku": {
          "name": "Standard",
          "family": "C",
          "capacity": 1
        }
      }
    },
    {
      "type": "Microsoft.DBforPostgreSQL/flexibleServers",
      "apiVersion": "2022-12-01",
      "name": "[variables('postgresName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Standard_B2s",
        "tier": "Burstable"
      },
      "properties": {
        "version": "14",
        "administratorLogin": "trustwrapperadmin",
        "administratorLoginPassword": "[concat('P@ssw0rd', uniqueString(resourceGroup().id))]",
        "storage": {
          "storageSizeGB": 32
        }
      }
    },
    {
      "type": "Microsoft.ContainerInstance/containerGroups",
      "apiVersion": "2021-09-01",
      "name": "[parameters('containerGroupName')]",
      "location": "[parameters('location')]",
      "dependsOn": [
        "[resourceId('Microsoft.ContainerRegistry/registries', variables('containerRegistryName'))]",
        "[resourceId('Microsoft.Cache/redis', variables('redisName'))]",
        "[resourceId('Microsoft.DBforPostgreSQL/flexibleServers', variables('postgresName'))]"
      ],
      "properties": {
        "containers": [
          {
            "name": "trustwrapper-api",
            "properties": {
              "image": "[concat(variables('containerRegistryName'), '.azurecr.io/trustwrapper:latest')]",
              "ports": [
                {
                  "port": 8000,
                  "protocol": "TCP"
                }
              ],
              "resources": {
                "requests": {
                  "cpu": 1,
                  "memoryInGB": 2
                }
              },
              "environmentVariables": [
                {
                  "name": "DATABASE_URL",
                  "value": "[concat('postgresql://trustwrapperadmin@', variables('postgresName'), ':', reference(resourceId('Microsoft.DBforPostgreSQL/flexibleServers', variables('postgresName'))).fullyQualifiedDomainName, '/trustwrapper')]"
                },
                {
                  "name": "REDIS_URL",
                  "value": "[concat('redis://', reference(resourceId('Microsoft.Cache/redis', variables('redisName'))).hostName, ':6380')]"
                }
              ]
            }
          }
        ],
        "osType": "Linux",
        "ipAddress": {
          "type": "Public",
          "ports": [
            {
              "port": 8000,
              "protocol": "TCP"
            }
          ],
          "dnsNameLabel": "trustwrapper-api"
        }
      }
    }
  ],
  "outputs": {
    "containerIPAddress": {
      "type": "string",
      "value": "[reference(resourceId('Microsoft.ContainerInstance/containerGroups', parameters('containerGroupName'))).ipAddress.ip]"
    },
    "containerFQDN": {
      "type": "string",
      "value": "[reference(resourceId('Microsoft.ContainerInstance/containerGroups', parameters('containerGroupName'))).ipAddress.fqdn]"
    }
  }
}
```

#### **2. Deploy ARM Template**
```bash
# Create resource group
az group create --name trustwrapper-rg --location eastus

# Deploy template
az deployment group create \
  --resource-group trustwrapper-rg \
  --template-file azuredeploy.json \
  --parameters containerGroupName=trustwrapper-api
```

### **Method 2: Azure Kubernetes Service (AKS)**

#### **1. Create AKS Cluster**
```bash
# Create AKS cluster
az aks create \
  --resource-group trustwrapper-rg \
  --name trustwrapper-aks \
  --node-count 3 \
  --node-vm-size Standard_B2s \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials \
  --resource-group trustwrapper-rg \
  --name trustwrapper-aks
```

#### **2. Deploy to AKS**
```yaml
# trustwrapper-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trustwrapper-api
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
      containers:
      - name: api
        image: trustwrapperacr.azurecr.io/trustwrapper:latest
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
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: trustwrapper-secrets
              key: anthropic-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
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
spec:
  selector:
    app: trustwrapper
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: trustwrapper-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: trustwrapper-api
  minReplicas: 3
  maxReplicas: 10
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
```

```bash
# Create secrets
kubectl create secret generic trustwrapper-secrets \
  --from-literal=database-url=postgresql://... \
  --from-literal=redis-url=redis://... \
  --from-literal=anthropic-api-key=sk-ant-...

# Deploy application
kubectl apply -f trustwrapper-deployment.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services
```

### **Method 3: Azure Container Apps (Serverless Containers)**

#### **1. Create Container App Environment**
```bash
# Create Container Apps environment
az containerapp env create \
  --name trustwrapper-env \
  --resource-group trustwrapper-rg \
  --location eastus

# Create Container App
az containerapp create \
  --name trustwrapper-api \
  --resource-group trustwrapper-rg \
  --environment trustwrapper-env \
  --image trustwrapperacr.azurecr.io/trustwrapper:latest \
  --target-port 8000 \
  --ingress 'external' \
  --min-replicas 1 \
  --max-replicas 10 \
  --cpu 0.5 \
  --memory 1 \
  --secrets database-url=postgresql://... redis-url=redis://... \
  --env-vars DATABASE_URL=secretref:database-url REDIS_URL=secretref:redis-url
```

## ⚙️ Configuration

### **Environment Variables**
```bash
# Core Configuration
ENVIRONMENT=production
API_PORT=8000
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://user:pass@trustwrapperdb.postgres.database.azure.com/trustwrapper
REDIS_URL=rediss://trustwrapperredis.redis.cache.windows.net:6380

# AI Service Keys (from Key Vault)
ANTHROPIC_API_KEY=@Microsoft.KeyVault(SecretUri=https://trustwrapperkv.vault.azure.net/secrets/anthropic-api-key/)
GOOGLE_API_KEY=@Microsoft.KeyVault(SecretUri=https://trustwrapperkv.vault.azure.net/secrets/google-api-key/)
AZURE_OPENAI_KEY=@Microsoft.KeyVault(SecretUri=https://trustwrapperkv.vault.azure.net/secrets/azure-openai-key/)

# Blockchain Configuration
ALEO_NETWORK=testnet3
ALEO_PRIVATE_KEY=@Microsoft.KeyVault(SecretUri=https://trustwrapperkv.vault.azure.net/secrets/aleo-private-key/)

# Azure Service Configuration
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=trustwrapperstorage;...
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...
```

### **Key Vault Integration**
```bash
# Create Key Vault
az keyvault create \
  --name trustwrapperkv \
  --resource-group trustwrapper-rg \
  --location eastus

# Add secrets
az keyvault secret set \
  --vault-name trustwrapperkv \
  --name anthropic-api-key \
  --value "sk-ant-..."

# Grant access to managed identity
az keyvault set-policy \
  --name trustwrapperkv \
  --object-id <managed-identity-object-id> \
  --secret-permissions get list
```

### **Managed Identity Configuration**
```csharp
// In application code
var credential = new DefaultAzureCredential();
var client = new SecretClient(
    new Uri("https://trustwrapperkv.vault.azure.net/"),
    credential
);

KeyVaultSecret secret = await client.GetSecretAsync("anthropic-api-key");
string apiKey = secret.Value;
```

## 📊 Monitoring & Scaling

### **Application Insights**
```python
# Python SDK integration
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

# Initialize Application Insights
exporter = metrics_exporter.new_metrics_exporter(
    connection_string='InstrumentationKey=...;IngestionEndpoint=...'
)

# Create custom metrics
verification_measure = measure_module.MeasureInt(
    "verification_count",
    "Number of verifications",
    "verifications"
)

verification_view = view_module.View(
    "verification_view",
    "Count of verifications",
    ["status"],
    verification_measure,
    aggregation_module.CountAggregation()
)

# Register view and exporter
stats_module.stats.view_manager.register_view(verification_view)
stats_module.stats.view_manager.register_exporter(exporter)

# Record metrics in application
def record_verification(status):
    mmap = tag_map_module.TagMap()
    mmap.insert("status", status)
    stats_module.stats.record_with_tags(
        mmap,
        [verification_measure.create_measurement(1)]
    )
```

### **Azure Monitor Dashboards**
```json
{
  "version": "Notebook/1.0",
  "items": [
    {
      "type": 3,
      "content": {
        "version": "KqlItem/1.0",
        "query": "requests\n| where timestamp > ago(1h)\n| summarize \n    RequestCount = count(), \n    AvgDuration = avg(duration), \n    P95Duration = percentile(duration, 95)\n    by bin(timestamp, 5m)\n| render timechart",
        "size": 0,
        "title": "TrustWrapper API Performance",
        "timeContext": {
          "durationMs": 3600000
        },
        "queryType": 0,
        "resourceType": "microsoft.insights/components"
      },
      "name": "API Performance"
    }
  ]
}
```

### **Auto-scaling Configuration**

#### **Container Apps Auto-scaling**
```json
{
  "scale": {
    "minReplicas": 1,
    "maxReplicas": 10,
    "rules": [
      {
        "name": "http-rule",
        "http": {
          "metadata": {
            "concurrentRequests": "100"
          }
        }
      },
      {
        "name": "cpu-rule",
        "custom": {
          "type": "cpu",
          "metadata": {
            "type": "Utilization",
            "value": "70"
          }
        }
      }
    ]
  }
}
```

#### **AKS Auto-scaling with KEDA**
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: trustwrapper-scaler
spec:
  scaleTargetRef:
    name: trustwrapper-api
  minReplicaCount: 3
  maxReplicaCount: 20
  triggers:
  - type: azure-monitor
    metadata:
      resourceURI: /subscriptions/.../resourceGroups/.../providers/microsoft.insights/components/...
      metricName: requests/rate
      targetValue: "100"
      aggregationType: Average
  - type: redis
    metadata:
      address: trustwrapperredis.redis.cache.windows.net:6380
      listName: verification_queue
      listLength: "10"
```

## 🔒 Security Best Practices

### **Network Security**
```bash
# Create Network Security Group
az network nsg create \
  --resource-group trustwrapper-rg \
  --name trustwrapper-nsg

# Add security rules
az network nsg rule create \
  --resource-group trustwrapper-rg \
  --nsg-name trustwrapper-nsg \
  --name allow-https \
  --protocol tcp \
  --priority 100 \
  --destination-port-range 443 \
  --access Allow

az network nsg rule create \
  --resource-group trustwrapper-rg \
  --nsg-name trustwrapper-nsg \
  --name allow-api \
  --protocol tcp \
  --priority 110 \
  --destination-port-range 8000 \
  --source-address-prefixes VirtualNetwork \
  --access Allow
```

### **Azure AD Integration**
```python
# FastAPI with Azure AD authentication
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from azure.identity import DefaultAzureCredential
import jwt

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # Verify Azure AD token
        decoded = jwt.decode(
            token,
            options={"verify_signature": False}  # Azure AD handles verification
        )

        # Validate claims
        if decoded.get("aud") != "your-app-client-id":
            raise HTTPException(status_code=401, detail="Invalid audience")

        return decoded

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# Protected endpoint
@app.get("/protected")
async def protected_route(token_data: dict = Depends(verify_token)):
    return {"user": token_data.get("preferred_username")}
```

### **Encryption & Compliance**
- **Data at Rest**: Azure Storage Service Encryption (256-bit AES)
- **Data in Transit**: TLS 1.2+ enforced
- **Key Management**: Azure Key Vault with HSM backing
- **Compliance**: SOC 2, ISO 27001, HIPAA ready

## 💰 Cost Optimization

### **Cost Breakdown (Estimated Monthly)**
| Service | Configuration | Estimated Cost |
|:--------|:-------------|:---------------|
| **Container Apps** | 1 vCPU, 2GB RAM, auto-scale | ~$50 |
| **PostgreSQL Flexible** | B2s, 32GB storage | ~$35 |
| **Redis Cache** | C1 Standard | ~$55 |
| **Application Gateway** | WAF_v2 | ~$250 |
| **Key Vault** | Standard, 10k operations | ~$5 |
| **Application Insights** | 5GB data | ~$25 |
| **Total** | | ~$420/month |

### **Cost Optimization Strategies**
1. **Reserved Instances**: Save 30-60% with 1-3 year commitments
2. **Spot Instances**: Use for non-critical batch processing
3. **Auto-shutdown**: Schedule non-production resources
4. **Right-sizing**: Monitor and adjust resource allocation
5. **Azure Hybrid Benefit**: Use existing licenses

### **Cost Management**
```bash
# Set up budget alerts
az consumption budget create \
  --amount 500 \
  --budget-name TrustWrapperBudget \
  --category Cost \
  --time-grain Monthly \
  --start-date 2025-06-01 \
  --end-date 2025-12-31 \
  --resource-group trustwrapper-rg

# View current costs
az consumption usage list \
  --start-date 2025-06-01 \
  --end-date 2025-06-30 \
  --query "[?contains(instanceId, 'trustwrapper')]"
```

## 🔧 Troubleshooting

### **Common Issues**

#### **1. Container Fails to Start**
```bash
# Check container logs
az container logs \
  --resource-group trustwrapper-rg \
  --name trustwrapper-api

# Check container state
az container show \
  --resource-group trustwrapper-rg \
  --name trustwrapper-api \
  --query "containers[0].instanceView.currentState"
```

#### **2. Database Connection Issues**
```bash
# Test PostgreSQL connectivity
psql "host=trustwrapperdb.postgres.database.azure.com \
      port=5432 \
      dbname=trustwrapper \
      user=trustwrapperadmin@trustwrapperdb \
      sslmode=require"

# Check firewall rules
az postgres flexible-server firewall-rule list \
  --resource-group trustwrapper-rg \
  --server-name trustwrapperdb
```

#### **3. Performance Issues**
```kusto
// Application Insights query for slow requests
requests
| where timestamp > ago(1h)
| where duration > 1000
| project timestamp, name, duration, resultCode
| order by duration desc
| take 100
```

#### **4. Authentication Failures**
```bash
# Check managed identity
az identity show \
  --resource-group trustwrapper-rg \
  --name trustwrapper-identity

# Verify Key Vault access
az keyvault secret list \
  --vault-name trustwrapperkv \
  --query "[].{name:name, enabled:attributes.enabled}"
```

### **Diagnostic Commands**
```bash
# Enable diagnostic logging
az monitor diagnostic-settings create \
  --resource /subscriptions/.../resourceGroups/.../providers/Microsoft.ContainerInstance/containerGroups/trustwrapper-api \
  --name trustwrapper-diagnostics \
  --logs '[{"category": "ContainerInstanceLog", "enabled": true}]' \
  --workspace /subscriptions/.../resourceGroups/.../providers/Microsoft.OperationalInsights/workspaces/...

# Stream logs
az container attach \
  --resource-group trustwrapper-rg \
  --name trustwrapper-api

# Get container events
az container show \
  --resource-group trustwrapper-rg \
  --name trustwrapper-api \
  --query "containers[0].instanceView.events[]"
```

## 📚 Additional Resources

### **Azure Documentation**
- [Container Apps Documentation](https://docs.microsoft.com/azure/container-apps/)
- [AKS Best Practices](https://docs.microsoft.com/azure/aks/best-practices)
- [Azure Architecture Center](https://docs.microsoft.com/azure/architecture/)

### **TrustWrapper Resources**
- [API Reference Documentation](/docs/api/TRUSTWRAPPER_API_REFERENCE.md)
- [Architecture Overview](/docs/architecture/TECHNICAL_ARCHITECTURE.md)
- [Security Guidelines](/docs/security/SECURITY_ARCHITECTURE.md)

### **Support**
- **Azure Support**: Via Azure Portal
- **TrustWrapper Support**: support@trustwrapper.ai
- **Community**: [Discord](https://discord.gg/trustwrapper)

---

**Next Steps**: Configure Azure DevOps or GitHub Actions for CI/CD pipeline automation and set up Azure Front Door for global load balancing.
