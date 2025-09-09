# 🔥 PyTorch Integration Guide for TrustWrapper

**Version**: 1.0.0  
**Last Updated**: June 22, 2025  
**Compatibility**: PyTorch 2.0+ with TrustWrapper v1.0+

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Model Wrapping](#model-wrapping)
5. [Custom Layer Integration](#custom-layer-integration)
6. [Explainability Methods](#explainability-methods)
7. [Performance Optimization](#performance-optimization)
8. [Advanced Examples](#advanced-examples)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## 🎯 Overview

This guide demonstrates how to integrate PyTorch models with TrustWrapper for zero-knowledge verified AI inference with explainability. TrustWrapper adds trust and transparency to your PyTorch models without modifying their core functionality.

### **Key Benefits**
- **Zero-Knowledge Proofs**: Verify model predictions without exposing weights
- **Explainable AI**: SHAP, LIME, and gradient-based explanations
- **Hallucination Detection**: Automatic detection of uncertain predictions
- **Performance Monitoring**: Track model performance and reliability
- **Blockchain Verification**: On-chain attestations of predictions

## 📋 Prerequisites

### **Required Packages**
```bash
# Install TrustWrapper
pip install trustwrapper

# Install PyTorch (if not already installed)
pip install torch torchvision torchaudio

# Install explainability libraries
pip install shap lime torch-explain captum
```

### **Environment Setup**
```python
import torch
import torch.nn as nn
from trustwrapper import TrustWrapper, Config
from trustwrapper.pytorch import PyTorchAdapter
```

## 🚀 Quick Start

### **Basic PyTorch Model Wrapping**

```python
import torch
import torch.nn as nn
from trustwrapper.pytorch import wrap_pytorch_model

# Define a simple PyTorch model
class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return self.softmax(x)

# Create and train your model
model = SimpleNet(10, 64, 3)
# ... training code ...

# Wrap with TrustWrapper
wrapped_model = wrap_pytorch_model(
    model=model,
    model_name="simple_classifier",
    enable_explanations=True,
    enable_zk_proofs=True
)

# Use the wrapped model
input_tensor = torch.randn(1, 10)
result = wrapped_model.predict(input_tensor)

print(f"Prediction: {result.prediction}")
print(f"Trust Score: {result.trust_score}")
print(f"Explanation: {result.explanation}")
print(f"ZK Proof: {result.zk_proof}")
```

## 🔧 Model Wrapping

### **Comprehensive Model Wrapping**

```python
from trustwrapper.pytorch import PyTorchWrapper, WrapperConfig

# Configure TrustWrapper for PyTorch
config = WrapperConfig(
    # Core settings
    model_name="advanced_classifier",
    model_version="1.0.0",
    
    # Explainability settings
    explanation_methods=["shap", "lime", "gradcam"],
    explanation_samples=100,
    
    # Trust settings
    confidence_threshold=0.85,
    hallucination_detection=True,
    uncertainty_quantification=True,
    
    # ZK proof settings
    enable_zk_proofs=True,
    proof_level="full",  # "basic", "standard", "full"
    
    # Blockchain settings
    blockchain_verification=True,
    target_chain="aleo",  # "aleo", "icp", "ethereum"
    
    # Performance settings
    optimization_level="balanced",  # "speed", "balanced", "accuracy"
    batch_verification=True
)

# Wrap any PyTorch model
class ComplexModel(nn.Module):
    def __init__(self):
        super(ComplexModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        self.fc1 = nn.Linear(128 * 8 * 8, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, 10)
    
    def forward(self, x):
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        x = self.pool(torch.relu(self.bn2(self.conv2(x))))
        x = x.view(-1, 128 * 8 * 8)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)

# Load pre-trained model
model = ComplexModel()
model.load_state_dict(torch.load('model_weights.pth'))
model.eval()

# Create TrustWrapper instance
trust_wrapper = PyTorchWrapper(config)

# Wrap the model
wrapped_model = trust_wrapper.wrap(model)

# Advanced prediction with all features
input_batch = torch.randn(32, 3, 32, 32)
results = wrapped_model.predict_batch(
    input_batch,
    return_explanations=True,
    return_uncertainties=True,
    generate_proofs=True
)

for i, result in enumerate(results):
    print(f"\nSample {i}:")
    print(f"  Prediction: {result.prediction}")
    print(f"  Confidence: {result.confidence:.2%}")
    print(f"  Trust Score: {result.trust_score:.2f}")
    print(f"  Uncertainty: {result.uncertainty:.4f}")
    print(f"  Hallucination Risk: {result.hallucination_risk}")
    print(f"  Top Features: {result.explanation.top_features[:3]}")
```

## 🎨 Custom Layer Integration

### **Wrapping Custom PyTorch Layers**

```python
from trustwrapper.pytorch import TrustLayer, track_gradients

# Create a custom layer with trust tracking
class TrustAwareAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.attention = nn.MultiheadAttention(embed_dim, num_heads)
        self.trust_layer = TrustLayer(
            layer_name="custom_attention",
            track_gradients=True,
            track_activations=True
        )
    
    def forward(self, x, mask=None):
        # Apply attention
        attn_output, attn_weights = self.attention(x, x, x, attn_mask=mask)
        
        # Track with TrustWrapper
        tracked_output = self.trust_layer(attn_output, {
            'attention_weights': attn_weights,
            'input_shape': x.shape,
            'mask_used': mask is not None
        })
        
        return tracked_output

# Use in a model
class TransformerWithTrust(nn.Module):
    def __init__(self, d_model=512, nhead=8, num_layers=6):
        super().__init__()
        self.embedding = nn.Embedding(10000, d_model)
        self.positional_encoding = nn.Parameter(torch.randn(1, 1000, d_model))
        
        # Use trust-aware layers
        self.layers = nn.ModuleList([
            TrustAwareAttention(d_model, nhead) 
            for _ in range(num_layers)
        ])
        
        self.output_proj = nn.Linear(d_model, 10000)
    
    def forward(self, x):
        # Embed and add positional encoding
        x = self.embedding(x)
        seq_len = x.size(1)
        x = x + self.positional_encoding[:, :seq_len, :]
        
        # Pass through trust-aware layers
        for layer in self.layers:
            x = layer(x)
        
        return self.output_proj(x)

# Wrap the custom model
model = TransformerWithTrust()
wrapped_model = wrap_pytorch_model(
    model,
    track_custom_layers=True,
    custom_layer_handlers={
        'TrustAwareAttention': 'attention_explainer'
    }
)
```

### **Gradient Tracking and Analysis**

```python
from trustwrapper.pytorch import GradientTracker

# Enable gradient tracking for explainability
class GradientTrackedModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.base_model = base_model
        self.gradient_tracker = GradientTracker()
    
    def forward(self, x):
        # Enable gradient tracking
        x.requires_grad_(True)
        
        # Forward pass with tracking
        with self.gradient_tracker.track():
            output = self.base_model(x)
        
        return output, self.gradient_tracker.get_gradients()

# Use gradient information for explanations
tracked_model = GradientTrackedModel(model)
wrapped_tracked = wrap_pytorch_model(
    tracked_model,
    explanation_methods=["gradient", "integrated_gradient", "smoothgrad"]
)

# Get detailed gradient explanations
input_data = torch.randn(1, 3, 224, 224)
result = wrapped_tracked.explain(input_data)

print("Gradient-based explanations:")
print(f"  Saliency Map: {result.saliency_map.shape}")
print(f"  Feature Importance: {result.feature_importance[:10]}")
print(f"  Layer Contributions: {result.layer_contributions}")
```

## 🔍 Explainability Methods

### **SHAP Integration**

```python
from trustwrapper.pytorch.explainers import SHAPExplainer

# Configure SHAP for PyTorch
shap_config = {
    'n_samples': 100,
    'feature_names': [f'feature_{i}' for i in range(10)],
    'output_names': ['class_0', 'class_1', 'class_2'],
    'use_gpu': torch.cuda.is_available()
}

# Create SHAP explainer
shap_explainer = SHAPExplainer(model, **shap_config)

# Wrap model with SHAP
wrapped_model = wrap_pytorch_model(
    model,
    explainers={'shap': shap_explainer}
)

# Get SHAP explanations
test_input = torch.randn(5, 10)
results = wrapped_model.predict_with_explanations(test_input)

for i, result in enumerate(results):
    print(f"\nSample {i}:")
    print(f"  Prediction: {result.prediction}")
    print(f"  SHAP values: {result.shap_values}")
    print(f"  Feature contributions:")
    for j, (feature, value) in enumerate(result.feature_contributions[:3]):
        print(f"    {feature}: {value:.4f}")
```

### **LIME Integration**

```python
from trustwrapper.pytorch.explainers import LIMEExplainer

# Configure LIME for different data types
# For tabular data
lime_tabular = LIMEExplainer(
    model,
    data_type='tabular',
    feature_names=['age', 'income', 'education', 'experience'],
    class_names=['rejected', 'approved'],
    num_samples=1000
)

# For image data
lime_image = LIMEExplainer(
    model,
    data_type='image',
    num_samples=1000,
    num_features=10,
    num_segments=50
)

# For text data
lime_text = LIMEExplainer(
    model,
    data_type='text',
    class_names=['negative', 'neutral', 'positive'],
    num_samples=1000
)

# Use LIME explanations
# Tabular example
tabular_input = torch.tensor([[25, 50000, 16, 3]], dtype=torch.float32)
lime_result = lime_tabular.explain(tabular_input)
print(f"LIME explanation: {lime_result.as_list()}")

# Image example
image_input = torch.randn(1, 3, 224, 224)
image_explanation = lime_image.explain(image_input)
print(f"Top image regions: {image_explanation.top_labels}")

# Text example (assuming tokenized input)
text_input = torch.tensor([[101, 2023, 2003, 1037, 2307, 2566, 102]])
text_explanation = lime_text.explain(text_input)
print(f"Important words: {text_explanation.as_list()}")
```

### **Captum Integration**

```python
from captum.attr import IntegratedGradients, DeepLift, GradientShap
from trustwrapper.pytorch.explainers import CaptumExplainer

# Create Captum-based explainers
explainers = {
    'integrated_gradients': IntegratedGradients(model),
    'deeplift': DeepLift(model),
    'gradient_shap': GradientShap(model)
}

# Wrap with Captum support
captum_wrapper = CaptumExplainer(model, explainers)
wrapped_model = wrap_pytorch_model(
    model,
    explainers={'captum': captum_wrapper}
)

# Get multiple explanation types
input_tensor = torch.randn(1, 3, 32, 32)
baseline = torch.zeros_like(input_tensor)

explanations = wrapped_model.explain_with_captum(
    input_tensor,
    baseline=baseline,
    methods=['integrated_gradients', 'deeplift'],
    target_class=None  # Explain predicted class
)

print("Captum explanations:")
for method, attribution in explanations.items():
    print(f"  {method}: {attribution.shape}, sum={attribution.sum().item():.4f}")
```

## ⚡ Performance Optimization

### **Model Optimization Techniques**

```python
from trustwrapper.pytorch.optimization import optimize_for_inference

# Optimize model for TrustWrapper inference
optimized_model = optimize_for_inference(
    model,
    optimization_level='aggressive',  # 'conservative', 'balanced', 'aggressive'
    techniques=[
        'quantization',      # INT8 quantization where possible
        'pruning',          # Remove unnecessary connections
        'fusion',           # Fuse operations
        'caching',          # Cache intermediate results
        'batch_optimization' # Optimize for batch inference
    ]
)

# Benchmark performance
from trustwrapper.pytorch.benchmark import benchmark_model

results = benchmark_model(
    original_model=model,
    optimized_model=optimized_model,
    test_inputs=torch.randn(100, 3, 224, 224),
    metrics=['latency', 'throughput', 'memory', 'accuracy']
)

print("Performance improvements:")
print(f"  Latency: {results.latency_improvement:.1%} faster")
print(f"  Throughput: {results.throughput_improvement:.1%} higher")
print(f"  Memory: {results.memory_reduction:.1%} less")
print(f"  Accuracy: {results.accuracy_delta:.4f} difference")
```

### **Batch Processing Optimization**

```python
from trustwrapper.pytorch import BatchProcessor

# Configure batch processing
batch_processor = BatchProcessor(
    model=wrapped_model,
    batch_size=32,
    num_workers=4,
    device='cuda' if torch.cuda.is_available() else 'cpu',
    mixed_precision=True,
    gradient_checkpointing=True
)

# Process large dataset efficiently
dataset = torch.utils.data.TensorDataset(
    torch.randn(10000, 3, 224, 224),
    torch.randint(0, 10, (10000,))
)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)

# Run batch inference with trust metrics
all_results = []
for batch_inputs, batch_labels in dataloader:
    results = batch_processor.process_batch(
        batch_inputs,
        compute_explanations=True,
        aggregate_trust_scores=True
    )
    all_results.extend(results)

# Aggregate metrics
avg_trust = sum(r.trust_score for r in all_results) / len(all_results)
print(f"Average trust score: {avg_trust:.2f}")
```

### **GPU Acceleration**

```python
from trustwrapper.pytorch.cuda import CUDAAccelerator

# Enable GPU acceleration for TrustWrapper
if torch.cuda.is_available():
    accelerator = CUDAAccelerator(
        device_id=0,
        memory_fraction=0.8,
        enable_cudnn_benchmark=True
    )
    
    # Accelerate wrapped model
    gpu_wrapped_model = accelerator.accelerate(wrapped_model)
    
    # Use mixed precision for faster inference
    with accelerator.mixed_precision():
        input_batch = torch.randn(64, 3, 224, 224).cuda()
        results = gpu_wrapped_model.predict_batch(input_batch)
    
    print(f"GPU inference time: {accelerator.last_inference_time:.2f}ms")
```

## 🎯 Advanced Examples

### **Computer Vision Example**

```python
import torchvision.models as models
from trustwrapper.pytorch.vision import VisionWrapper

# Load pre-trained ResNet
resnet = models.resnet50(pretrained=True)
resnet.eval()

# Create vision-specific wrapper
vision_wrapper = VisionWrapper(
    model=resnet,
    model_name="resnet50_imagenet",
    input_size=(224, 224),
    normalization_mean=[0.485, 0.456, 0.406],
    normalization_std=[0.229, 0.224, 0.225],
    class_names=None,  # Will load ImageNet classes
    explanation_methods=['gradcam', 'gradcam++', 'scorecam']
)

# Process image
from PIL import Image
import torchvision.transforms as transforms

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
])

image = Image.open('sample_image.jpg')
input_tensor = transform(image).unsqueeze(0)

# Get prediction with visual explanations
result = vision_wrapper.predict_with_visualization(
    input_tensor,
    save_visualization=True,
    output_path='explanation.png'
)

print(f"Predicted class: {result.class_name}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Trust score: {result.trust_score:.2f}")
print(f"Visualization saved to: {result.visualization_path}")
```

### **NLP Example**

```python
from transformers import AutoModel, AutoTokenizer
from trustwrapper.pytorch.nlp import NLPWrapper

# Load Hugging Face model
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModel.from_pretrained(model_name)

# Add classification head
class BERTClassifier(nn.Module):
    def __init__(self, bert_model, num_classes=3):
        super().__init__()
        self.bert = bert_model
        self.classifier = nn.Linear(768, num_classes)
    
    def forward(self, input_ids, attention_mask=None):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        pooled = outputs.last_hidden_state[:, 0]  # [CLS] token
        return self.classifier(pooled)

classifier = BERTClassifier(bert_model)

# Create NLP-specific wrapper
nlp_wrapper = NLPWrapper(
    model=classifier,
    tokenizer=tokenizer,
    model_name="bert_sentiment_classifier",
    max_length=128,
    explanation_methods=['attention', 'integrated_gradients']
)

# Process text
text = "This product is absolutely amazing! Best purchase ever."
result = nlp_wrapper.predict_text(
    text,
    return_attention_weights=True,
    return_token_importance=True
)

print(f"Sentiment: {result.prediction}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Trust score: {result.trust_score:.2f}")
print(f"Important tokens: {result.important_tokens[:5]}")
```

### **Reinforcement Learning Example**

```python
from trustwrapper.pytorch.rl import RLWrapper

# Define RL policy network
class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.action_head = nn.Linear(128, action_dim)
        self.value_head = nn.Linear(128, 1)
    
    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        action_probs = torch.softmax(self.action_head(x), dim=-1)
        value = self.value_head(x)
        return action_probs, value

# Create RL-specific wrapper
policy = PolicyNetwork(state_dim=4, action_dim=2)
rl_wrapper = RLWrapper(
    model=policy,
    model_name="cartpole_policy",
    track_episode_trust=True,
    explanation_methods=['action_influence', 'state_importance']
)

# Use in environment
state = torch.tensor([0.1, -0.2, 0.05, 0.3], dtype=torch.float32)
action_result = rl_wrapper.select_action(
    state,
    return_trust_metrics=True
)

print(f"Selected action: {action_result.action}")
print(f"Action confidence: {action_result.confidence:.2%}")
print(f"State trust score: {action_result.trust_score:.2f}")
print(f"Explanation: {action_result.explanation}")
```

## 📋 Best Practices

### **1. Model Preparation**
```python
# Always put model in eval mode before wrapping
model.eval()

# Disable gradient computation for inference
with torch.no_grad():
    wrapped_model = wrap_pytorch_model(model)

# Use appropriate data types
model = model.float()  # or .half() for FP16
```

### **2. Error Handling**
```python
from trustwrapper.pytorch import TrustWrapperError

try:
    result = wrapped_model.predict(input_data)
except TrustWrapperError as e:
    print(f"TrustWrapper error: {e}")
    # Fallback to original model
    with torch.no_grad():
        original_result = model(input_data)
```

### **3. Memory Management**
```python
# Clear cache periodically
wrapped_model.clear_explanation_cache()

# Use context manager for large batches
with wrapped_model.efficient_mode():
    results = wrapped_model.predict_batch(large_dataset)

# Enable gradient checkpointing for large models
wrapped_model.enable_gradient_checkpointing()
```

### **4. Custom Metrics**
```python
from trustwrapper.pytorch import MetricTracker

# Add custom metrics
metric_tracker = MetricTracker()
metric_tracker.add_metric('domain_specific_score', 
                         lambda pred, conf: pred * conf)

wrapped_model.add_metric_tracker(metric_tracker)
```

## 🔧 Troubleshooting

### **Common Issues and Solutions**

#### **1. CUDA Out of Memory**
```python
# Solution: Reduce batch size or use gradient accumulation
wrapped_model.configure(
    max_batch_size=16,
    gradient_accumulation_steps=4,
    mixed_precision=True
)
```

#### **2. Slow Explanation Generation**
```python
# Solution: Use faster explanation methods or sampling
wrapped_model.configure(
    explanation_methods=['gradient'],  # Faster than SHAP/LIME
    explanation_samples=50,  # Reduce sample size
    cache_explanations=True
)
```

#### **3. Model Compatibility Issues**
```python
# Solution: Use compatibility mode
from trustwrapper.pytorch import CompatibilityMode

wrapped_model = wrap_pytorch_model(
    model,
    compatibility_mode=CompatibilityMode.LEGACY,
    strict_mode=False
)
```

#### **4. Inconsistent Results**
```python
# Solution: Set random seeds and use deterministic mode
torch.manual_seed(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

wrapped_model.set_deterministic(True)
```

### **Debug Mode**
```python
# Enable detailed logging
import logging
logging.getLogger('trustwrapper').setLevel(logging.DEBUG)

# Use debug wrapper
from trustwrapper.pytorch import debug_mode

with debug_mode():
    result = wrapped_model.predict(input_data)
    print(f"Debug info: {result.debug_info}")
```

## 📚 Additional Resources

### **PyTorch Integration Examples**
- [Computer Vision Demo](../../demos/pytorch_vision_demo.py)
- [NLP Demo](../../demos/pytorch_nlp_demo.py)  
- [Custom Layer Demo](../../demos/pytorch_custom_layer_demo.py)

### **Documentation**
- [TrustWrapper API Reference](../api/TRUSTWRAPPER_API_REFERENCE.md)
- [PyTorch Best Practices](https://pytorch.org/tutorials/beginner/best_practices.html)
- [Explainable AI Methods](../technical/EXPLAINABLE_AI_METHODS.md)

### **Community**
- [GitHub Issues](https://github.com/lamassu-labs/trustwrapper/issues)
- [Discord Community](https://discord.gg/trustwrapper)
- [Stack Overflow Tag](https://stackoverflow.com/questions/tagged/trustwrapper)

---

**Next Steps**: Explore our [TensorFlow Integration Guide](TENSORFLOW_INTEGRATION.md) or check out the [demo applications](../../demos/) for real-world examples.