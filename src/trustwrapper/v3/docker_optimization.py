#!/usr/bin/env python3
"""
TrustWrapper v3.0 Docker Optimization System
Production-ready container orchestration with multi-stage builds
Task 4.1: Week 4 Phase 1 Implementation
"""

import json
import logging
import os
import subprocess
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContainerType(Enum):
    """Container deployment types"""

    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"


class OptimizationLevel(Enum):
    """Docker optimization levels"""

    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    ENTERPRISE = "enterprise"


class SecurityHardening(Enum):
    """Security hardening levels"""

    MINIMAL = "minimal"
    STANDARD = "standard"
    ENTERPRISE = "enterprise"
    PARANOID = "paranoid"


@dataclass
class DockerConfig:
    """Docker container configuration"""

    base_image: str = "python:3.11-slim"
    working_dir: str = "/app"
    expose_ports: List[int] = None
    environment_vars: Dict[str, str] = None
    volumes: List[str] = None

    # Multi-stage build settings
    use_multi_stage: bool = True
    build_stage: str = "builder"
    runtime_stage: str = "runtime"

    # Optimization settings
    optimization_level: OptimizationLevel = OptimizationLevel.ENTERPRISE
    security_hardening: SecurityHardening = SecurityHardening.ENTERPRISE

    # Resource limits
    memory_limit: str = "2G"
    cpu_limit: str = "1000m"
    memory_request: str = "1G"
    cpu_request: str = "500m"

    def __post_init__(self):
        if self.expose_ports is None:
            self.expose_ports = [8000]
        if self.environment_vars is None:
            self.environment_vars = {}
        if self.volumes is None:
            self.volumes = []


@dataclass
class KubernetesConfig:
    """Kubernetes deployment configuration"""

    app_name: str
    namespace: str = "trustwrapper"
    replicas: int = 3

    # HPA settings
    enable_hpa: bool = True
    min_replicas: int = 3
    max_replicas: int = 100
    target_cpu_percent: int = 70
    target_memory_percent: int = 80

    # Service mesh
    enable_istio: bool = True
    istio_injection: bool = True
    traffic_policy: str = "round_robin"

    # Storage
    storage_class: str = "fast-ssd"
    storage_size: str = "50Gi"

    # Networking
    service_type: str = "ClusterIP"
    ingress_enabled: bool = True
    tls_enabled: bool = True


class DockerOptimizationManager:
    """Enterprise Docker optimization and container management"""

    def __init__(self, base_path: str = "/app"):
        self.base_path = Path(base_path)
        self.configs = {}
        self.templates = {}

    async def generate_production_dockerfile(
        self, config: DockerConfig, container_type: ContainerType
    ) -> str:
        """Generate optimized Dockerfile for production deployment"""

        logger.info(
            f"Generating {config.optimization_level.value} Dockerfile for {container_type.value}"
        )

        dockerfile_content = []

        # Multi-stage build setup
        if config.use_multi_stage:
            dockerfile_content.extend(self._generate_builder_stage(config))
            dockerfile_content.extend(
                self._generate_runtime_stage(config, container_type)
            )
        else:
            dockerfile_content.extend(
                self._generate_single_stage(config, container_type)
            )

        dockerfile = "\n".join(dockerfile_content)

        logger.info(f"Generated Dockerfile: {len(dockerfile_content)} lines")
        return dockerfile

    def _generate_builder_stage(self, config: DockerConfig) -> List[str]:
        """Generate builder stage for multi-stage builds"""
        stage = [
            "# Build stage - Optimized for compilation and dependency building",
            f"FROM {config.base_image} AS {config.build_stage}",
            "",
            "# Build arguments",
            "ARG BUILDPLATFORM",
            "ARG TARGETPLATFORM",
            "ARG BUILDARCH",
            "ARG TARGETARCH",
            "",
            "# Install build dependencies",
            "RUN apt-get update && apt-get install -y \\",
            "    build-essential \\",
            "    curl \\",
            "    git \\",
            "    gcc \\",
            "    g++ \\",
            "    make \\",
            "    cmake \\",
            "    pkg-config \\",
            "    libffi-dev \\",
            "    libssl-dev \\",
            "    && rm -rf /var/lib/apt/lists/*",
            "",
            "# Set up Python environment",
            "RUN python -m pip install --upgrade pip setuptools wheel",
            "",
            "# Copy requirements and install dependencies",
            "COPY requirements.txt /tmp/requirements.txt",
            "RUN pip install --no-cache-dir --user -r /tmp/requirements.txt",
            "",
            "# Copy source code",
            f"WORKDIR {config.working_dir}",
            "COPY . .",
            "",
            "# Compile Python files for faster startup",
            "RUN python -m compileall -b .",
            "",
            "# Remove source files, keep only bytecode for size optimization",
            "RUN find . -name '*.py' -delete",
            "",
        ]

        return stage

    def _generate_runtime_stage(
        self, config: DockerConfig, container_type: ContainerType
    ) -> List[str]:
        """Generate runtime stage for multi-stage builds"""
        stage = [
            "# Runtime stage - Optimized for execution",
            f"FROM {config.base_image} AS {config.runtime_stage}",
            "",
            "# Runtime arguments",
            "ARG VERSION=latest",
            "ARG BUILD_DATE",
            "ARG VCS_REF",
            "",
            "# Metadata labels",
            'LABEL maintainer="Lamassu Labs <info@lamassu-labs.com>"',
            'LABEL version="$VERSION"',
            'LABEL build-date="$BUILD_DATE"',
            'LABEL vcs-ref="$VCS_REF"',
            'LABEL description="TrustWrapper v3.0 Universal Multi-Chain AI Verification Platform"',
            "",
        ]

        # Security hardening
        if config.security_hardening in [
            SecurityHardening.ENTERPRISE,
            SecurityHardening.PARANOID,
        ]:
            stage.extend(
                [
                    "# Security hardening",
                    "RUN groupadd -r trustwrapper && useradd -r -g trustwrapper trustwrapper",
                    "RUN apt-get update && apt-get install -y \\",
                    "    ca-certificates \\",
                    "    && rm -rf /var/lib/apt/lists/*",
                    "",
                ]
            )

        # Runtime dependencies only
        stage.extend(
            [
                "# Install minimal runtime dependencies",
                "RUN apt-get update && apt-get install -y \\",
                "    curl \\",
                "    ca-certificates \\",
                "    && rm -rf /var/lib/apt/lists/* \\",
                "    && apt-get clean \\",
                "    && rm -rf /tmp/* /var/tmp/*",
                "",
            ]
        )

        # Python setup
        stage.extend(
            [
                "# Set up Python environment",
                "RUN python -m pip install --upgrade pip --no-cache-dir",
                "",
                "# Copy installed packages from builder",
                "COPY --from=builder /root/.local /root/.local",
                "",
                "# Copy compiled application",
                f"WORKDIR {config.working_dir}",
                "COPY --from=builder /app .",
                "",
            ]
        )

        # Environment setup
        stage.extend(
            [
                "# Environment configuration",
                "ENV PYTHONPATH=/app",
                "ENV PYTHONUNBUFFERED=1",
                "ENV PYTHONDONTWRITEBYTECODE=1",
                "ENV PIP_NO_CACHE_DIR=1",
                "ENV PIP_DISABLE_PIP_VERSION_CHECK=1",
                "",
            ]
        )

        # Add custom environment variables
        for key, value in config.environment_vars.items():
            stage.append(f"ENV {key}={value}")

        if config.environment_vars:
            stage.append("")

        # Port exposure
        for port in config.expose_ports:
            stage.append(f"EXPOSE {port}")
        stage.append("")

        # Security settings
        if config.security_hardening != SecurityHardening.MINIMAL:
            stage.extend(["# Security configuration", "USER trustwrapper", ""])

        # Health check
        if container_type == ContainerType.PRODUCTION:
            stage.extend(
                [
                    "# Health check",
                    "HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\",
                    f"    CMD curl -f http://localhost:{config.expose_ports[0]}/health || exit 1",
                    "",
                ]
            )

        # Startup command
        stage.extend(
            [
                "# Default command",
                'CMD ["python", "-m", "uvicorn", "src.trustwrapper.v3.api_gateway:create_app", \\',
                f'     "--host", "0.0.0.0", "--port", "{config.expose_ports[0]}", \\',
                '     "--workers", "4", "--access-log"]',
            ]
        )

        return stage

    def _generate_single_stage(
        self, config: DockerConfig, container_type: ContainerType
    ) -> List[str]:
        """Generate single-stage Dockerfile for development"""
        stage = [
            f"# Single-stage Dockerfile for {container_type.value}",
            f"FROM {config.base_image}",
            "",
            "# Install dependencies",
            "RUN apt-get update && apt-get install -y \\",
            "    curl \\",
            "    build-essential \\",
            "    && rm -rf /var/lib/apt/lists/*",
            "",
            f"WORKDIR {config.working_dir}",
            "",
            "# Copy and install requirements",
            "COPY requirements.txt .",
            "RUN pip install -r requirements.txt",
            "",
            "# Copy application code",
            "COPY . .",
            "",
            "# Environment setup",
            "ENV PYTHONPATH=/app",
            "ENV PYTHONUNBUFFERED=1",
            "",
        ]

        # Port exposure
        for port in config.expose_ports:
            stage.append(f"EXPOSE {port}")
        stage.append("")

        # Default command
        stage.extend(
            [
                'CMD ["python", "-m", "uvicorn", "src.trustwrapper.v3.api_gateway:create_app", \\',
                f'     "--host", "0.0.0.0", "--port", "{config.expose_ports[0]}", \\',
                '     "--reload"]',
            ]
        )

        return stage

    async def generate_kubernetes_manifests(
        self, config: KubernetesConfig, docker_config: DockerConfig
    ) -> Dict[str, str]:
        """Generate complete Kubernetes deployment manifests"""

        logger.info(f"Generating Kubernetes manifests for {config.app_name}")

        manifests = {}

        # Namespace
        manifests["namespace.yaml"] = self._generate_namespace(config)

        # ConfigMap
        manifests["configmap.yaml"] = self._generate_configmap(config, docker_config)

        # Secret (template - needs actual values)
        manifests["secret.yaml"] = self._generate_secret_template(config)

        # Deployment
        manifests["deployment.yaml"] = self._generate_deployment(config, docker_config)

        # Service
        manifests["service.yaml"] = self._generate_service(config, docker_config)

        # HPA (if enabled)
        if config.enable_hpa:
            manifests["hpa.yaml"] = self._generate_hpa(config)

        # Ingress (if enabled)
        if config.ingress_enabled:
            manifests["ingress.yaml"] = self._generate_ingress(config)

        # Istio resources (if enabled)
        if config.enable_istio:
            manifests["virtualservice.yaml"] = self._generate_virtual_service(config)
            manifests["destinationrule.yaml"] = self._generate_destination_rule(config)

        # ServiceMonitor for Prometheus
        manifests["servicemonitor.yaml"] = self._generate_service_monitor(config)

        # PersistentVolumeClaim
        manifests["pvc.yaml"] = self._generate_pvc(config)

        logger.info(f"Generated {len(manifests)} Kubernetes manifests")
        return manifests

    def _generate_namespace(self, config: KubernetesConfig) -> str:
        """Generate namespace manifest"""
        return f"""apiVersion: v1
kind: Namespace
metadata:
  name: {config.namespace}
  labels:
    app: {config.app_name}
    environment: production
    managed-by: trustwrapper
"""

    def _generate_configmap(
        self, config: KubernetesConfig, docker_config: DockerConfig
    ) -> str:
        """Generate ConfigMap manifest"""
        env_vars = "\n".join(
            [f'  {k}: "{v}"' for k, v in docker_config.environment_vars.items()]
        )

        return f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {config.app_name}-config
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
data:
  # Application configuration
{env_vars}

  # TrustWrapper specific configuration
  TRUSTWRAPPER_MODE: "production"
  TRUSTWRAPPER_LOG_LEVEL: "INFO"
  TRUSTWRAPPER_METRICS_ENABLED: "true"
  TRUSTWRAPPER_HEALTH_CHECK_ENABLED: "true"

  # Multi-chain configuration
  ENABLE_ETHEREUM: "true"
  ENABLE_POLYGON: "true"
  ENABLE_CARDANO: "true"
  ENABLE_SOLANA: "true"
  ENABLE_BITCOIN: "true"

  # Performance tuning
  WORKER_PROCESSES: "4"
  MAX_CONNECTIONS: "1000"
  TIMEOUT_SECONDS: "30"

  # Security settings
  ENABLE_RATE_LIMITING: "true"
  ENABLE_API_KEY_AUTH: "true"
  ENABLE_JWT_AUTH: "true"
"""

    def _generate_secret_template(self, config: KubernetesConfig) -> str:
        """Generate Secret template (values need to be filled)"""
        return f"""apiVersion: v1
kind: Secret
metadata:
  name: {config.app_name}-secrets
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
type: Opaque
data:
  # Base64 encoded secrets - REPLACE WITH ACTUAL VALUES
  DATABASE_URL: # echo -n "postgresql://..." | base64
  REDIS_URL: # echo -n "redis://..." | base64
  JWT_SECRET_KEY: # echo -n "your-jwt-secret" | base64
  API_ENCRYPTION_KEY: # echo -n "your-encryption-key" | base64

  # Blockchain API keys
  ETHEREUM_API_KEY: # echo -n "your-eth-key" | base64
  POLYGON_API_KEY: # echo -n "your-polygon-key" | base64
  SOLANA_API_KEY: # echo -n "your-solana-key" | base64

  # OAuth secrets
  OAUTH_CLIENT_SECRET: # echo -n "your-oauth-secret" | base64

  # Enterprise integration
  ENTERPRISE_API_KEY: # echo -n "your-enterprise-key" | base64
"""

    def _generate_deployment(
        self, config: KubernetesConfig, docker_config: DockerConfig
    ) -> str:
        """Generate Deployment manifest"""

        # Resource limits and requests
        resources = f"""        resources:
          limits:
            memory: "{docker_config.memory_limit}"
            cpu: "{docker_config.cpu_limit}"
          requests:
            memory: "{docker_config.memory_request}"
            cpu: "{docker_config.cpu_request}\""""

        # Security context
        security_context = ""
        if docker_config.security_hardening != SecurityHardening.MINIMAL:
            security_context = """        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          runAsGroup: 1001
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
          capabilities:
            drop:
              - ALL"""

        # Istio sidecar injection
        istio_annotation = ""
        if config.enable_istio and config.istio_injection:
            istio_annotation = '    sidecar.istio.io/inject: "true"'

        return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {config.app_name}
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
    version: v3.0
spec:
  replicas: {config.replicas}
  selector:
    matchLabels:
      app: {config.app_name}
  template:
    metadata:
      labels:
        app: {config.app_name}
        version: v3.0
      annotations:
{istio_annotation}
        prometheus.io/scrape: "true"
        prometheus.io/port: "{docker_config.expose_ports[0]}"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: {config.app_name}
        image: trustwrapper/{config.app_name}:latest
        imagePullPolicy: Always
        ports:
        - containerPort: {docker_config.expose_ports[0]}
          name: http
          protocol: TCP
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        envFrom:
        - configMapRef:
            name: {config.app_name}-config
        - secretRef:
            name: {config.app_name}-secrets
{resources}
{security_context}
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
        - name: data
          mountPath: /app/data
      volumes:
      - name: tmp
        emptyDir: {{}}
      - name: cache
        emptyDir: {{}}
      - name: data
        persistentVolumeClaim:
          claimName: {config.app_name}-data
      terminationGracePeriodSeconds: 30
      restartPolicy: Always
"""

    def _generate_service(
        self, config: KubernetesConfig, docker_config: DockerConfig
    ) -> str:
        """Generate Service manifest"""
        return f"""apiVersion: v1
kind: Service
metadata:
  name: {config.app_name}
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "{docker_config.expose_ports[0]}"
spec:
  type: {config.service_type}
  ports:
  - port: 80
    targetPort: {docker_config.expose_ports[0]}
    protocol: TCP
    name: http
  selector:
    app: {config.app_name}
"""

    def _generate_hpa(self, config: KubernetesConfig) -> str:
        """Generate HorizontalPodAutoscaler manifest"""
        return f"""apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {config.app_name}-hpa
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {config.app_name}
  minReplicas: {config.min_replicas}
  maxReplicas: {config.max_replicas}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {config.target_cpu_percent}
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: {config.target_memory_percent}
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 120
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Max
"""

    def _generate_ingress(self, config: KubernetesConfig) -> str:
        """Generate Ingress manifest"""
        tls_section = ""
        if config.tls_enabled:
            tls_section = f"""  tls:
  - hosts:
    - {config.app_name}.trustwrapper.io
    secretName: {config.app_name}-tls"""

        return f"""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {config.app_name}-ingress
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "HTTP"
    nginx.ingress.kubernetes.io/rate-limit: "1000"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
{tls_section}
  rules:
  - host: {config.app_name}.trustwrapper.io
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {config.app_name}
            port:
              number: 80
"""

    def _generate_virtual_service(self, config: KubernetesConfig) -> str:
        """Generate Istio VirtualService manifest"""
        return f"""apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: {config.app_name}-vs
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
spec:
  hosts:
  - {config.app_name}.trustwrapper.io
  - {config.app_name}.{config.namespace}.svc.cluster.local
  gateways:
  - {config.app_name}-gateway
  - mesh
  http:
  - match:
    - uri:
        prefix: /health
    route:
    - destination:
        host: {config.app_name}.{config.namespace}.svc.cluster.local
        port:
          number: 80
    timeout: 10s
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: {config.app_name}.{config.namespace}.svc.cluster.local
        port:
          number: 80
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
"""

    def _generate_destination_rule(self, config: KubernetesConfig) -> str:
        """Generate Istio DestinationRule manifest"""
        return f"""apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: {config.app_name}-dr
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
spec:
  host: {config.app_name}.{config.namespace}.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      simple: {config.traffic_policy.upper()}
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 10
        maxRetries: 3
        consecutiveGatewayErrors: 5
    circuitBreaker:
      consecutiveGatewayErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 30
"""

    def _generate_service_monitor(self, config: KubernetesConfig) -> str:
        """Generate Prometheus ServiceMonitor manifest"""
        return f"""apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {config.app_name}-metrics
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
    prometheus: monitoring
spec:
  selector:
    matchLabels:
      app: {config.app_name}
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
    scrapeTimeout: 10s
  namespaceSelector:
    matchNames:
    - {config.namespace}
"""

    def _generate_pvc(self, config: KubernetesConfig) -> str:
        """Generate PersistentVolumeClaim manifest"""
        return f"""apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {config.app_name}-data
  namespace: {config.namespace}
  labels:
    app: {config.app_name}
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: {config.storage_class}
  resources:
    requests:
      storage: {config.storage_size}
"""

    async def generate_docker_compose(self, config: DockerConfig) -> str:
        """Generate Docker Compose file for local development"""

        services = {
            "trustwrapper-api": {
                "build": ".",
                "ports": [f"{config.expose_ports[0]}:8000"],
                "environment": dict(config.environment_vars),
                "volumes": ["./:/app", "/app/.venv"],
                "depends_on": ["redis", "postgres"],
            },
            "redis": {
                "image": "redis:7-alpine",
                "ports": ["6379:6379"],
                "volumes": ["redis_data:/data"],
            },
            "postgres": {
                "image": "postgres:15-alpine",
                "environment": {
                    "POSTGRES_DB": "trustwrapper",
                    "POSTGRES_USER": "trustwrapper",
                    "POSTGRES_PASSWORD": "development",
                },
                "ports": ["5432:5432"],
                "volumes": ["postgres_data:/var/lib/postgresql/data"],
            },
            "prometheus": {
                "image": "prom/prometheus:latest",
                "ports": ["9090:9090"],
                "volumes": [
                    "./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml"
                ],
            },
            "grafana": {
                "image": "grafana/grafana:latest",
                "ports": ["3000:3000"],
                "environment": {"GF_SECURITY_ADMIN_PASSWORD": "admin"},
                "volumes": ["grafana_data:/var/lib/grafana"],
            },
        }

        compose = {
            "version": "3.8",
            "services": services,
            "volumes": {"redis_data": {}, "postgres_data": {}, "grafana_data": {}},
            "networks": {"trustwrapper": {}},
        }

        return f"# TrustWrapper v3.0 Development Environment\n# Generated by Docker Optimization Manager\n\n{json.dumps(compose, indent=2)}"

    async def build_optimized_image(
        self, config: DockerConfig, container_type: ContainerType, tag: str = "latest"
    ) -> Tuple[bool, str]:
        """Build optimized Docker image with advanced caching"""

        logger.info(f"Building optimized {container_type.value} image: {tag}")

        try:
            # Generate Dockerfile
            dockerfile_content = await self.generate_production_dockerfile(
                config, container_type
            )

            # Write Dockerfile to temporary location
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".Dockerfile", delete=False
            ) as f:
                f.write(dockerfile_content)
                dockerfile_path = f.name

            # Build command with optimization flags
            build_args = [
                "docker",
                "build",
                "--platform",
                "linux/amd64,linux/arm64",  # Multi-platform
                "--progress",
                "plain",
                (
                    "--no-cache"
                    if container_type == ContainerType.PRODUCTION
                    else "--cache-from"
                ),
                f"trustwrapper/{tag}:cache",
                "--build-arg",
                f"VERSION={tag}",
                "--build-arg",
                f"BUILD_DATE={os.popen('date -u +%Y-%m-%dT%H:%M:%SZ').read().strip()}",
                "--build-arg",
                f"VCS_REF={os.popen('git rev-parse HEAD').read().strip()[:8]}",
                "-f",
                dockerfile_path,
                "-t",
                f"trustwrapper/{tag}:latest",
                ".",
            ]

            # Execute build
            result = subprocess.run(
                build_args, capture_output=True, text=True, cwd=self.base_path
            )

            # Cleanup
            os.unlink(dockerfile_path)

            if result.returncode == 0:
                logger.info(f"Successfully built image: trustwrapper/{tag}:latest")
                return True, f"Image built successfully: trustwrapper/{tag}:latest"
            else:
                logger.error(f"Build failed: {result.stderr}")
                return False, result.stderr

        except Exception as e:
            logger.error(f"Build error: {e}")
            return False, str(e)

    async def validate_deployment(self, config: KubernetesConfig) -> Dict[str, Any]:
        """Validate Kubernetes deployment readiness"""

        validation_results = {
            "namespace_ready": False,
            "deployment_ready": False,
            "service_ready": False,
            "hpa_ready": False,
            "ingress_ready": False,
            "pods_ready": 0,
            "total_pods": config.replicas,
            "errors": [],
        }

        try:
            # Check namespace
            ns_result = subprocess.run(
                ["kubectl", "get", "namespace", config.namespace],
                capture_output=True,
                text=True,
            )
            validation_results["namespace_ready"] = ns_result.returncode == 0

            # Check deployment
            deploy_result = subprocess.run(
                [
                    "kubectl",
                    "get",
                    "deployment",
                    config.app_name,
                    "-n",
                    config.namespace,
                ],
                capture_output=True,
                text=True,
            )
            validation_results["deployment_ready"] = deploy_result.returncode == 0

            # Check service
            svc_result = subprocess.run(
                ["kubectl", "get", "service", config.app_name, "-n", config.namespace],
                capture_output=True,
                text=True,
            )
            validation_results["service_ready"] = svc_result.returncode == 0

            # Check HPA if enabled
            if config.enable_hpa:
                hpa_result = subprocess.run(
                    [
                        "kubectl",
                        "get",
                        "hpa",
                        f"{config.app_name}-hpa",
                        "-n",
                        config.namespace,
                    ],
                    capture_output=True,
                    text=True,
                )
                validation_results["hpa_ready"] = hpa_result.returncode == 0
            else:
                validation_results["hpa_ready"] = True  # Not required

            # Check pod readiness
            pods_result = subprocess.run(
                [
                    "kubectl",
                    "get",
                    "pods",
                    "-l",
                    f"app={config.app_name}",
                    "-n",
                    config.namespace,
                    "--field-selector=status.phase=Running",
                    "--no-headers",
                ],
                capture_output=True,
                text=True,
            )

            if pods_result.returncode == 0:
                running_pods = len(
                    [
                        line
                        for line in pods_result.stdout.strip().split("\n")
                        if line.strip()
                    ]
                )
                validation_results["pods_ready"] = running_pods

            logger.info(f"Deployment validation: {validation_results}")

        except Exception as e:
            validation_results["errors"].append(str(e))
            logger.error(f"Validation error: {e}")

        return validation_results


# Factory functions for common configurations
async def get_production_docker_config() -> DockerConfig:
    """Get production Docker configuration"""
    return DockerConfig(
        base_image="python:3.11-slim",
        expose_ports=[8000],
        optimization_level=OptimizationLevel.ENTERPRISE,
        security_hardening=SecurityHardening.ENTERPRISE,
        memory_limit="4G",
        cpu_limit="2000m",
        memory_request="2G",
        cpu_request="1000m",
        environment_vars={
            "TRUSTWRAPPER_ENV": "production",
            "PYTHONUNBUFFERED": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )


async def get_production_k8s_config(
    app_name: str = "trustwrapper-api",
) -> KubernetesConfig:
    """Get production Kubernetes configuration"""
    return KubernetesConfig(
        app_name=app_name,
        namespace="trustwrapper",
        replicas=5,
        min_replicas=3,
        max_replicas=100,
        target_cpu_percent=70,
        target_memory_percent=80,
        enable_hpa=True,
        enable_istio=True,
        storage_class="fast-ssd",
        storage_size="100Gi",
        ingress_enabled=True,
        tls_enabled=True,
    )


async def get_docker_optimization_manager() -> DockerOptimizationManager:
    """Get Docker optimization manager instance"""
    return DockerOptimizationManager(
        "/Users/eladm/Projects/token/tokenhunter/lamassu-labs"
    )
