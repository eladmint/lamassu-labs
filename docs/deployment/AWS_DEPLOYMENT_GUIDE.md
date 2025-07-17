# 🚀 AWS Deployment Guide for TrustWrapper

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

This guide provides comprehensive instructions for deploying TrustWrapper on AWS infrastructure. TrustWrapper can be deployed using several AWS services depending on your scalability, cost, and operational requirements.

### **Key Benefits of AWS Deployment**
- **Scalability**: Auto-scaling based on demand
- **Global Reach**: Deploy across multiple regions
- **Integration**: Native integration with AWS AI/ML services
- **Security**: Enterprise-grade security with AWS compliance
- **Cost-Effective**: Pay-as-you-go with multiple pricing options

## 📋 Prerequisites

### **AWS Account Requirements**
- [ ] AWS account with appropriate permissions
- [ ] AWS CLI installed and configured
- [ ] IAM roles for service deployment
- [ ] VPC with public/private subnets
- [ ] S3 bucket for artifact storage

### **Local Development Requirements**
```bash
# Install required tools
pip install awscli boto3
npm install -g aws-cdk

# Configure AWS CLI
aws configure
# Enter: AWS Access Key ID, Secret Access Key, Region, Output format
```

### **TrustWrapper Requirements**
- Docker image of TrustWrapper API
- Leo contract addresses (if using blockchain features)
- API keys for AI services (stored in AWS Secrets Manager)

## 🏗️ Architecture Options

### **Option 1: Serverless (Recommended for Variable Load)**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   API Gateway   │────▶│  Lambda Function │────▶│   DynamoDB      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  SageMaker      │
                        │  (AI Models)    │
                        └─────────────────┘
```

### **Option 2: Container-Based (Recommended for Consistent Load)**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   ALB/NLB       │────▶│    ECS/EKS      │────▶│   RDS/Aurora    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  ElastiCache    │
                        │  (Redis)        │
                        └─────────────────┘
```

### **Option 3: Hybrid (Best of Both)**
```
┌─────────────────┐
│   CloudFront    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  API Gateway    │────▶│  Lambda@Edge    │ (Light operations)
└────────┬────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│    ALB          │────▶│   ECS Fargate   │ (Heavy operations)
└─────────────────┘     └─────────────────┘
```

## 🚀 Deployment Methods

### **Method 1: AWS CDK (Infrastructure as Code)**

#### **1. Initialize CDK Project**
```bash
mkdir trustwrapper-aws-deployment
cd trustwrapper-aws-deployment
cdk init app --language python
```

#### **2. Define Infrastructure**
```python
# app.py
from aws_cdk import (
    App,
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticache as elasticache,
    aws_rds as rds,
    aws_secretsmanager as secrets,
    aws_cloudwatch as cloudwatch,
    Duration
)

class TrustWrapperStack(Stack):
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # VPC (uses default VPC or create new one)
        vpc = ec2.Vpc(self, "TrustWrapperVPC",
            max_azs=2,
            nat_gateways=1
        )
        
        # ECS Cluster
        cluster = ecs.Cluster(self, "TrustWrapperCluster",
            vpc=vpc,
            container_insights=True
        )
        
        # Redis Cache
        redis_subnet_group = elasticache.CfnSubnetGroup(
            self, "RedisSubnetGroup",
            subnet_ids=[subnet.subnet_id for subnet in vpc.private_subnets],
            description="Subnet group for TrustWrapper Redis"
        )
        
        redis_cluster = elasticache.CfnCacheCluster(
            self, "TrustWrapperRedis",
            cache_node_type="cache.t3.micro",
            engine="redis",
            num_cache_nodes=1,
            cache_subnet_group_name=redis_subnet_group.ref
        )
        
        # RDS Database
        database = rds.DatabaseInstance(
            self, "TrustWrapperDB",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_14_7
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3,
                ec2.InstanceSize.SMALL
            ),
            vpc=vpc,
            multi_az=True,
            allocated_storage=100,
            storage_encrypted=True,
            database_name="trustwrapper"
        )
        
        # Fargate Service
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "TrustWrapperService",
            cluster=cluster,
            cpu=512,
            memory_limit_mib=1024,
            desired_count=2,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("your-registry/trustwrapper:latest"),
                container_port=8000,
                environment={
                    "REDIS_URL": f"redis://{redis_cluster.attr_redis_endpoint_address}",
                    "DATABASE_URL": database.instance_endpoint.socket_address,
                    "AWS_REGION": self.region
                }
            ),
            public_load_balancer=True,
            domain_name="trustwrapper.yourdomain.com",
            domain_zone=route53.HostedZone.from_lookup(
                self, "Zone",
                domain_name="yourdomain.com"
            )
        )
        
        # Auto Scaling
        scaling = fargate_service.service.auto_scale_task_count(
            max_capacity=10,
            min_capacity=2
        )
        
        scaling.scale_on_cpu_utilization("CpuScaling",
            target_utilization_percent=70,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60)
        )
        
        scaling.scale_on_request_count("RequestScaling",
            requests_per_target=1000,
            target_group=fargate_service.target_group
        )

app = App()
TrustWrapperStack(app, "TrustWrapperStack")
app.synth()
```

#### **3. Deploy Infrastructure**
```bash
# Install dependencies
pip install -r requirements.txt

# Deploy
cdk bootstrap
cdk deploy --require-approval never
```

### **Method 2: ECS with Fargate (Direct Deployment)**

#### **1. Create Task Definition**
```json
{
  "family": "trustwrapper",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "trustwrapper-api",
      "image": "your-registry/trustwrapper:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "environment": [
        {
          "name": "AWS_REGION",
          "value": "us-east-1"
        }
      ],
      "secrets": [
        {
          "name": "ANTHROPIC_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:trustwrapper/api-keys"
        },
        {
          "name": "GOOGLE_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:trustwrapper/api-keys"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/trustwrapper",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 10,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ],
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/trustwrapperTaskRole"
}
```

#### **2. Create Service**
```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster trustwrapper-cluster \
  --service-name trustwrapper-api \
  --task-definition trustwrapper:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:region:account:targetgroup/trustwrapper/xxx,containerName=trustwrapper-api,containerPort=8000"
```

### **Method 3: Lambda Deployment (Serverless)**

#### **1. Prepare Lambda Package**
```python
# lambda_handler.py
import json
from mangum import Mangum
from src.api.trustwrapper_api import app  # FastAPI app

# Create Lambda handler
handler = Mangum(app)

def lambda_handler(event, context):
    # Pre-processing if needed
    if event.get('warmup'):
        return {'statusCode': 200, 'body': 'Lambda warmed up'}
    
    # Handle API Gateway events
    return handler(event, context)
```

#### **2. SAM Template**
```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    MemorySize: 1024
    Runtime: python3.11

Resources:
  TrustWrapperAPI:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      Handler: lambda_handler.lambda_handler
      Environment:
        Variables:
          STAGE: prod
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
      Policies:
        - AWSSecretsManagerGetSecretValuePolicy:
            SecretArn: !Ref ApiSecrets
        - DynamoDBCrudPolicy:
            TableName: !Ref VerificationTable
  
  VerificationTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
        - AttributeName: user_id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: user_id_index
          KeySchema:
            - AttributeName: user_id
              KeyType: HASH
          Projection:
            ProjectionType: ALL
  
  ApiSecrets:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: trustwrapper/api-keys
      SecretString: !Sub |
        {
          "ANTHROPIC_API_KEY": "your-key",
          "GOOGLE_API_KEY": "your-key",
          "ALEO_PRIVATE_KEY": "your-key"
        }

Outputs:
  ApiUrl:
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/"
```

#### **3. Deploy with SAM**
```bash
# Build and deploy
sam build
sam deploy --guided
```

## ⚙️ Configuration

### **Environment Variables**
```bash
# Core Configuration
ENVIRONMENT=production
API_PORT=8000
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/trustwrapper
REDIS_URL=redis://elasticache-endpoint:6379

# AI Service Keys (from Secrets Manager)
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
GOOGLE_API_KEY=${GOOGLE_API_KEY}

# Blockchain Configuration
ALEO_NETWORK=testnet3
ALEO_PRIVATE_KEY=${ALEO_PRIVATE_KEY}
CONTRACT_ADDRESS_AGENT_REGISTRY=agent_registry_simple.aleo
CONTRACT_ADDRESS_TRUST_VERIFIER=trust_verifier_test.aleo

# AWS Service Configuration
AWS_REGION=us-east-1
S3_BUCKET=trustwrapper-artifacts
CLOUDWATCH_LOG_GROUP=/aws/ecs/trustwrapper
```

### **Secrets Management**
```bash
# Store secrets in AWS Secrets Manager
aws secretsmanager create-secret \
  --name trustwrapper/api-keys \
  --secret-string '{
    "ANTHROPIC_API_KEY": "sk-ant-...",
    "GOOGLE_API_KEY": "AIza...",
    "ALEO_PRIVATE_KEY": "APrivateKey..."
  }'

# Reference in ECS task definition
"secrets": [
  {
    "name": "ANTHROPIC_API_KEY",
    "valueFrom": "arn:aws:secretsmanager:region:account:secret:trustwrapper/api-keys:ANTHROPIC_API_KEY::"
  }
]
```

## 📊 Monitoring & Scaling

### **CloudWatch Metrics**
```python
# Custom metrics for monitoring
import boto3
from datetime import datetime

cloudwatch = boto3.client('cloudwatch')

def put_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='TrustWrapper',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.utcnow()
            }
        ]
    )

# Usage in application
put_metric('VerificationRequests', 1)
put_metric('VerificationLatency', response_time, 'Milliseconds')
put_metric('AITokenUsage', token_count)
```

### **Auto Scaling Configuration**
```json
{
  "targetTrackingScalingPolicies": [
    {
      "targetValue": 70.0,
      "predefinedMetricType": "ECSServiceAverageCPUUtilization"
    },
    {
      "targetValue": 80.0,
      "predefinedMetricType": "ECSServiceAverageMemoryUtilization"
    },
    {
      "targetValue": 1000.0,
      "customizedMetricSpecification": {
        "metricName": "RequestCountPerTarget",
        "namespace": "AWS/ApplicationELB",
        "statistic": "Average"
      }
    }
  ]
}
```

### **CloudWatch Dashboards**
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["TrustWrapper", "VerificationRequests", {"stat": "Sum"}],
          [".", "VerificationLatency", {"stat": "Average"}],
          ["AWS/ECS", "CPUUtilization", {"ServiceName": "trustwrapper-api"}],
          [".", "MemoryUtilization", {"ServiceName": "trustwrapper-api"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "TrustWrapper Performance"
      }
    }
  ]
}
```

## 🔒 Security Best Practices

### **Network Security**
```yaml
# Security Group Configuration
SecurityGroup:
  Ingress:
    - Protocol: tcp
      Port: 443
      Source: 0.0.0.0/0  # HTTPS from anywhere
    - Protocol: tcp
      Port: 80
      Source: 0.0.0.0/0  # HTTP (redirect to HTTPS)
  Egress:
    - Protocol: tcp
      Port: 443
      Destination: 0.0.0.0/0  # HTTPS to external APIs
    - Protocol: tcp
      Port: 5432
      Destination: 10.0.0.0/16  # PostgreSQL within VPC
    - Protocol: tcp
      Port: 6379
      Destination: 10.0.0.0/16  # Redis within VPC
```

### **IAM Roles and Policies**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:*:*:secret:trustwrapper/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::trustwrapper-artifacts/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

### **Encryption**
- **In Transit**: Use ALB with SSL/TLS termination
- **At Rest**: Enable encryption for RDS, ElastiCache, and S3
- **Secrets**: Use AWS Secrets Manager with automatic rotation

## 💰 Cost Optimization

### **Cost Breakdown (Estimated Monthly)**
| Service | Configuration | Estimated Cost |
|:--------|:-------------|:---------------|
| **ECS Fargate** | 2 tasks × 0.5 vCPU × 1GB | ~$30 |
| **ALB** | 1 load balancer | ~$25 |
| **RDS** | db.t3.small, 100GB, Multi-AZ | ~$80 |
| **ElastiCache** | cache.t3.micro | ~$25 |
| **Data Transfer** | 100GB outbound | ~$9 |
| **CloudWatch** | Logs and metrics | ~$20 |
| **Total** | | ~$189/month |

### **Cost Optimization Tips**
1. **Use Spot Instances**: For non-critical workloads
2. **Reserved Instances**: 1-3 year commitments save 30-70%
3. **Auto Scaling**: Scale down during low usage
4. **S3 Lifecycle Policies**: Move old data to cheaper storage
5. **CloudWatch Logs Retention**: Set appropriate retention periods

## 🔧 Troubleshooting

### **Common Issues**

#### **1. Container Fails to Start**
```bash
# Check ECS task logs
aws logs tail /ecs/trustwrapper --follow

# Common causes:
# - Missing environment variables
# - Incorrect IAM permissions
# - Health check failing
```

#### **2. Database Connection Issues**
```bash
# Test RDS connectivity
telnet rds-endpoint 5432

# Check security group rules
aws ec2 describe-security-groups --group-ids sg-xxx
```

#### **3. High Latency**
- Check CloudWatch metrics for CPU/memory
- Verify ElastiCache hit rate
- Review API Gateway throttling limits
- Check cross-region latency

#### **4. Cost Overruns**
- Enable AWS Cost Explorer
- Set up billing alerts
- Review unused resources
- Check data transfer costs

### **Debugging Commands**
```bash
# View ECS service events
aws ecs describe-services --cluster trustwrapper-cluster --services trustwrapper-api

# Check task definition
aws ecs describe-task-definition --task-definition trustwrapper:latest

# View CloudWatch logs
aws logs get-log-events --log-group-name /ecs/trustwrapper --log-stream-name ecs/trustwrapper-api/task-id

# Test API endpoint
curl -X POST https://api.trustwrapper.yourdomain.com/verify \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"query": "test", "response": "test response"}'
```

## 📚 Additional Resources

### **AWS Documentation**
- [ECS Best Practices Guide](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [Lambda Container Images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- [AWS CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)

### **TrustWrapper Resources**
- [API Reference Documentation](/docs/api/TRUSTWRAPPER_API_REFERENCE.md)
- [Architecture Overview](/docs/architecture/TECHNICAL_ARCHITECTURE.md)
- [Security Guidelines](/docs/security/SECURITY_ARCHITECTURE.md)

### **Support**
- **AWS Support**: Via AWS Console
- **TrustWrapper Support**: support@trustwrapper.ai
- **Community**: [Discord](https://discord.gg/trustwrapper)

---

**Next Steps**: After successful deployment, configure monitoring dashboards and set up CI/CD pipelines for automated deployments.