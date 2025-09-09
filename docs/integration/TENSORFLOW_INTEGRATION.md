# 🧠 TensorFlow Integration Guide for TrustWrapper

**Version**: 1.0.0  
**Last Updated**: June 22, 2025  
**Compatibility**: TensorFlow 2.10+ with TrustWrapper v1.0+

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Model Integration](#model-integration)
5. [TF Serving Integration](#tf-serving-integration)
6. [Explainability with TensorFlow](#explainability-with-tensorflow)
7. [Distributed Training](#distributed-training)
8. [Performance Optimization](#performance-optimization)
9. [Advanced Examples](#advanced-examples)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

## 🎯 Overview

This guide demonstrates how to integrate TensorFlow models with TrustWrapper for zero-knowledge verified AI inference. TrustWrapper seamlessly wraps TensorFlow models, adding trust, explainability, and verification capabilities without modifying model architecture.

### **Key Features**
- **SavedModel Support**: Direct integration with TF SavedModel format
- **TF Serving Compatible**: Deploy with TensorFlow Serving
- **Keras Integration**: Full support for Keras models
- **TPU Support**: Optimized for TPU inference
- **TensorFlow Lite**: Mobile deployment with trust features

## 📋 Prerequisites

### **Required Packages**
```bash
# Install TrustWrapper
pip install trustwrapper[tensorflow]

# Install TensorFlow (if not already installed)
pip install tensorflow>=2.10.0

# For GPU support
pip install tensorflow-gpu>=2.10.0

# Additional dependencies
pip install tensorflow-serving-api tensorflow-hub tf-explain
```

### **Environment Setup**
```python
import tensorflow as tf
from trustwrapper.tensorflow import TensorFlowWrapper, TFConfig
from trustwrapper import Config
```

## 🚀 Quick Start

### **Basic Keras Model Wrapping**

```python
import tensorflow as tf
from tensorflow import keras
from trustwrapper.tensorflow import wrap_tf_model

# Create a simple Keras model
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(10,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(3, activation='softmax')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train your model (example)
# model.fit(x_train, y_train, ...)

# Wrap with TrustWrapper
wrapped_model = wrap_tf_model(
    model=model,
    model_name="keras_classifier",
    enable_explanations=True,
    enable_zk_proofs=True
)

# Use the wrapped model
import numpy as np
test_input = np.random.randn(1, 10)
result = wrapped_model.predict(test_input)

print(f"Prediction: {result.prediction}")
print(f"Trust Score: {result.trust_score}")
print(f"Explanation: {result.explanation}")
print(f"ZK Proof: {result.zk_proof}")
```

## 🔧 Model Integration

### **SavedModel Integration**

```python
from trustwrapper.tensorflow import SavedModelWrapper

# Load a SavedModel
saved_model_path = '/path/to/saved_model'
loaded_model = tf.saved_model.load(saved_model_path)

# Configure TrustWrapper for SavedModel
config = TFConfig(
    model_name="production_model",
    model_version="2.0.0",
    
    # Signature configuration
    signature_name="serving_default",
    input_names=["input_tensor"],
    output_names=["predictions", "probabilities"],
    
    # Trust configuration
    enable_trust_scoring=True,
    confidence_threshold=0.9,
    hallucination_detection=True,
    
    # Explainability
    explanation_methods=["integrated_gradients", "smoothgrad"],
    
    # ZK proof configuration
    enable_zk_proofs=True,
    proof_backend="aleo",
    
    # Performance
    enable_xla=True,
    enable_mixed_precision=True
)

# Create wrapper
wrapper = SavedModelWrapper(config)
wrapped_saved_model = wrapper.wrap(loaded_model)

# Use with signature
inputs = {"input_tensor": tf.constant([[1.0, 2.0, 3.0, 4.0]])}
results = wrapped_saved_model.serve(inputs)

print(f"Predictions: {results['predictions']}")
print(f"Trust Metrics: {results['trust_metrics']}")
print(f"Explanations: {results['explanations']}")
```

### **Functional API Integration**

```python
# Complex model using Functional API
inputs = keras.Input(shape=(224, 224, 3))
x = keras.layers.Conv2D(64, 3, activation='relu')(inputs)
x = keras.layers.MaxPooling2D()(x)
x = keras.layers.Conv2D(128, 3, activation='relu')(x)
x = keras.layers.MaxPooling2D()(x)
x = keras.layers.GlobalAveragePooling2D()(x)
x = keras.layers.Dense(256, activation='relu')(x)
outputs = keras.layers.Dense(10, activation='softmax')(x)

functional_model = keras.Model(inputs=inputs, outputs=outputs)

# Wrap functional model
wrapped_functional = wrap_tf_model(
    functional_model,
    model_type="functional",
    track_intermediate_outputs=True,
    explanation_layers=['conv2d', 'conv2d_1', 'dense']
)

# Get layer-wise explanations
test_image = np.random.randn(1, 224, 224, 3)
detailed_result = wrapped_functional.predict_with_intermediates(test_image)

print("Layer activations:")
for layer_name, activation in detailed_result.intermediate_outputs.items():
    print(f"  {layer_name}: {activation.shape}")
```

### **Custom Model Integration**

```python
class CustomTFModel(tf.keras.Model):
    def __init__(self, num_classes=10):
        super(CustomTFModel, self).__init__()
        self.conv1 = keras.layers.Conv2D(32, 3, activation='relu')
        self.pool1 = keras.layers.MaxPooling2D()
        self.conv2 = keras.layers.Conv2D(64, 3, activation='relu')
        self.pool2 = keras.layers.MaxPooling2D()
        self.flatten = keras.layers.Flatten()
        self.dense1 = keras.layers.Dense(128, activation='relu')
        self.dropout = keras.layers.Dropout(0.5)
        self.dense2 = keras.layers.Dense(num_classes)
        
        # Add TrustWrapper tracking
        self.trust_tracker = TrustTracker()
    
    def call(self, inputs, training=False):
        x = self.conv1(inputs)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dropout(x, training=training)
        outputs = self.dense2(x)
        
        # Track confidence
        self.trust_tracker.update(outputs)
        
        return outputs
    
    @tf.function
    def serve(self, inputs):
        """Optimized serving function"""
        return self.call(inputs, training=False)

# Instantiate and wrap custom model
custom_model = CustomTFModel(num_classes=10)
custom_model.build((None, 28, 28, 1))

wrapped_custom = wrap_tf_model(
    custom_model,
    model_type="custom",
    serving_function="serve",
    enable_tf_function_optimization=True
)
```

## 🚀 TF Serving Integration

### **Preparing Model for TF Serving**

```python
from trustwrapper.tensorflow.serving import prepare_for_serving

# Prepare model with TrustWrapper signatures
serving_model = prepare_for_serving(
    model=wrapped_model,
    export_dir='./serving_model',
    version=1,
    signatures={
        'predict': {
            'inputs': {'image': tf.TensorSpec([None, 224, 224, 3], tf.float32)},
            'outputs': {
                'predictions': tf.TensorSpec([None, 10], tf.float32),
                'trust_score': tf.TensorSpec([None], tf.float32),
                'explanation': tf.TensorSpec([None, 224, 224, 3], tf.float32)
            }
        },
        'explain': {
            'inputs': {'image': tf.TensorSpec([None, 224, 224, 3], tf.float32)},
            'outputs': {
                'shap_values': tf.TensorSpec([None, 224, 224, 3], tf.float32),
                'feature_importance': tf.TensorSpec([None, 10], tf.float32)
            }
        }
    }
)

# Export for serving
tf.saved_model.save(serving_model, './serving_model/1')
```

### **TF Serving Client**

```python
from trustwrapper.tensorflow.serving import TrustServingClient

# Create client for TF Serving
client = TrustServingClient(
    host='localhost',
    port=8501,
    model_name='trustwrapper_model',
    model_version=1
)

# Make prediction request
image_data = np.random.randn(1, 224, 224, 3).astype(np.float32)
response = client.predict(
    inputs={'image': image_data},
    include_trust_metrics=True,
    include_explanations=True
)

print(f"Predictions: {response.predictions}")
print(f"Trust Score: {response.trust_score}")
print(f"Latency: {response.latency_ms}ms")

# Batch prediction
batch_images = np.random.randn(32, 224, 224, 3).astype(np.float32)
batch_response = client.predict_batch(
    inputs={'images': batch_images},
    max_batch_size=16,  # Split into smaller batches if needed
    aggregate_trust_scores=True
)
```

### **Model Versioning and A/B Testing**

```python
from trustwrapper.tensorflow.serving import ModelVersionManager

# Manage multiple model versions
version_manager = ModelVersionManager(
    base_path='./models',
    models={
        'model_v1': {'version': 1, 'weight': 0.8},
        'model_v2': {'version': 2, 'weight': 0.2}
    }
)

# A/B test with trust metrics
def ab_test_request(input_data):
    model_version = version_manager.select_model()
    
    result = client.predict(
        inputs={'data': input_data},
        model_version=model_version,
        track_performance=True
    )
    
    # Update weights based on trust scores
    version_manager.update_weight(
        model_version, 
        performance_score=result.trust_score
    )
    
    return result

# Run A/B test
for _ in range(100):
    test_input = np.random.randn(1, 10)
    result = ab_test_request(test_input)
    print(f"Used model v{result.model_version}, trust: {result.trust_score:.2f}")
```

## 🔍 Explainability with TensorFlow

### **Integrated Gradients**

```python
from trustwrapper.tensorflow.explainers import IntegratedGradientsExplainer

# Create explainer
ig_explainer = IntegratedGradientsExplainer(
    model=model,
    n_steps=50,
    baseline_type='zero'  # 'zero', 'random', 'blur'
)

# Wrap model with explainer
wrapped_model = wrap_tf_model(
    model,
    explainers={'integrated_gradients': ig_explainer}
)

# Get explanations
test_input = tf.constant(np.random.randn(1, 224, 224, 3), dtype=tf.float32)
result = wrapped_model.explain(
    test_input,
    method='integrated_gradients',
    target_class=None  # Explain predicted class
)

# Visualize attributions
import matplotlib.pyplot as plt
attributions = result.attributions.numpy()[0]
plt.imshow(attributions.sum(axis=-1), cmap='RdBu_r')
plt.colorbar()
plt.title('Feature Attributions')
plt.show()
```

### **GradCAM for CNNs**

```python
from trustwrapper.tensorflow.explainers import GradCAMExplainer

# Setup GradCAM for specific layers
gradcam = GradCAMExplainer(
    model=model,
    layer_names=['conv2d_1', 'conv2d_2'],  # Target conv layers
    use_guided_gradcam=True
)

# Get visual explanations
wrapped_cnn = wrap_tf_model(model, explainers={'gradcam': gradcam})

# Generate heatmaps
image = tf.constant(np.random.randn(1, 224, 224, 3), dtype=tf.float32)
explanation = wrapped_cnn.explain_visual(
    image,
    method='gradcam',
    overlay_on_image=True,
    alpha=0.5
)

# Save visualization
tf.keras.preprocessing.image.save_img(
    'gradcam_explanation.png',
    explanation.overlay_image[0]
)
```

### **SHAP with TensorFlow**

```python
from trustwrapper.tensorflow.explainers import TFShapExplainer

# Create SHAP explainer for TensorFlow
shap_explainer = TFShapExplainer(
    model=model,
    background_samples=100,
    link='identity'  # 'identity' or 'logit'
)

# Explain predictions
wrapped_model = wrap_tf_model(model, explainers={'shap': shap_explainer})

# Get SHAP values
test_batch = np.random.randn(5, 10)
shap_results = wrapped_model.explain_batch(
    test_batch,
    method='shap',
    return_phi0=True  # Return base values
)

# Analyze feature importance
for i, result in enumerate(shap_results):
    print(f"\nSample {i}:")
    print(f"  Prediction: {result.prediction}")
    print(f"  Base value: {result.phi0}")
    print(f"  Top 3 features: {result.top_features[:3]}")
```

## 🔄 Distributed Training

### **Multi-GPU Training with Trust Metrics**

```python
from trustwrapper.tensorflow.distributed import DistributedWrapper

# Setup distribution strategy
strategy = tf.distribute.MirroredStrategy()
print(f'Number of devices: {strategy.num_replicas_in_sync}')

with strategy.scope():
    # Create model within strategy scope
    model = create_model()
    
    # Wrap with distributed support
    distributed_wrapper = DistributedWrapper(
        model=model,
        strategy=strategy,
        track_device_trust=True,
        sync_trust_metrics=True
    )
    
    # Compile with trust-aware loss
    distributed_wrapper.compile(
        optimizer=keras.optimizers.Adam(0.001),
        loss=TrustAwareLoss(base_loss='categorical_crossentropy'),
        metrics=['accuracy', TrustMetric()]
    )

# Train with trust tracking
history = distributed_wrapper.fit(
    train_dataset,
    epochs=10,
    validation_data=val_dataset,
    callbacks=[
        TrustCheckpoint(filepath='best_trust_model.h5'),
        TrustEarlyStopping(monitor='val_trust_score', patience=3)
    ]
)
```

### **TPU Integration**

```python
from trustwrapper.tensorflow.tpu import TPUWrapper

# Initialize TPU
resolver = tf.distribute.cluster_resolver.TPUClusterResolver()
tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)
strategy = tf.distribute.TPUStrategy(resolver)

# Create TPU-optimized wrapper
with strategy.scope():
    model = create_model()
    
    tpu_wrapper = TPUWrapper(
        model=model,
        enable_mixed_precision=True,
        enable_xla_optimization=True,
        batch_size_per_replica=128
    )
    
    # Compile for TPU
    tpu_wrapper.compile(
        optimizer=keras.optimizers.Adam(0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

# Train on TPU with trust metrics
tpu_wrapper.fit(
    train_dataset,
    epochs=10,
    steps_per_epoch=1000,
    validation_data=val_dataset,
    track_tpu_utilization=True
)

# Get TPU performance metrics
tpu_metrics = tpu_wrapper.get_tpu_metrics()
print(f"TPU Utilization: {tpu_metrics.utilization:.1%}")
print(f"Average step time: {tpu_metrics.avg_step_time:.2f}ms")
```

## ⚡ Performance Optimization

### **TensorFlow Optimization Techniques**

```python
from trustwrapper.tensorflow.optimization import optimize_model

# Apply multiple optimization techniques
optimized_model = optimize_model(
    model,
    techniques=[
        'quantization',     # INT8 quantization
        'pruning',         # Structured pruning
        'graph_optimization',  # Graph level optimizations
        'op_fusion',       # Fuse compatible operations
        'layout_optimization'  # Optimize memory layout
    ],
    target_device='gpu',  # 'cpu', 'gpu', 'tpu', 'edge'
    optimization_level=2  # 0=none, 1=basic, 2=aggressive
)

# Compare performance
from trustwrapper.tensorflow.benchmark import compare_models

comparison = compare_models(
    original=model,
    optimized=optimized_model,
    test_data=test_dataset,
    metrics=['latency', 'throughput', 'accuracy', 'model_size']
)

print("Optimization Results:")
print(f"  Latency reduction: {comparison.latency_reduction:.1%}")
print(f"  Throughput increase: {comparison.throughput_increase:.1%}")
print(f"  Model size reduction: {comparison.size_reduction:.1%}")
print(f"  Accuracy change: {comparison.accuracy_delta:.4f}")
```

### **TensorFlow Lite Conversion**

```python
from trustwrapper.tensorflow.lite import TFLiteWrapper

# Convert to TFLite with trust features
tflite_converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_converter.target_spec.supported_types = [tf.float16]

# Wrap TFLite model
tflite_wrapper = TFLiteWrapper(
    converter=tflite_converter,
    maintain_trust_features=True,
    quantization_aware=True
)

# Convert and save
tflite_model = tflite_wrapper.convert()
with open('model_with_trust.tflite', 'wb') as f:
    f.write(tflite_model)

# Use TFLite model with trust
interpreter = tflite_wrapper.create_interpreter('model_with_trust.tflite')
interpreter.allocate_tensors()

# Run inference
input_data = np.random.randn(1, 224, 224, 3).astype(np.float32)
result = tflite_wrapper.run_inference(
    interpreter,
    input_data,
    compute_trust_score=True
)

print(f"TFLite prediction: {result.prediction}")
print(f"Trust score: {result.trust_score}")
print(f"Inference time: {result.inference_time_ms}ms")
```

### **XLA Compilation**

```python
from trustwrapper.tensorflow.xla import XLAOptimizer

# Enable XLA optimization
@tf.function(jit_compile=True)
def xla_inference(model, inputs):
    return model(inputs, training=False)

# Create XLA-optimized wrapper
xla_wrapper = XLAOptimizer(
    model=model,
    enable_auto_clustering=True,
    memory_optimization=True
)

# Benchmark XLA performance
import time

# Warm up
for _ in range(10):
    _ = xla_wrapper.predict(test_input)

# Benchmark
times = []
for _ in range(100):
    start = time.time()
    _ = xla_wrapper.predict(test_input)
    times.append(time.time() - start)

print(f"XLA average inference time: {np.mean(times)*1000:.2f}ms")
print(f"XLA speedup: {baseline_time/np.mean(times):.2f}x")
```

## 🎯 Advanced Examples

### **Object Detection with Trust**

```python
from trustwrapper.tensorflow.vision import ObjectDetectionWrapper

# Load a pre-trained object detection model
base_model = tf.saved_model.load('path/to/detection_model')

# Create object detection wrapper
detection_wrapper = ObjectDetectionWrapper(
    model=base_model,
    model_name="yolo_v4",
    confidence_threshold=0.5,
    nms_threshold=0.4,
    track_object_trust=True
)

# Process image with trust scores per detection
image = tf.io.read_file('sample_image.jpg')
image = tf.image.decode_image(image)
image = tf.image.resize(image, [640, 640])

detections = detection_wrapper.detect(
    image,
    return_trust_per_object=True,
    return_explanations=True
)

for detection in detections:
    print(f"Object: {detection.class_name}")
    print(f"  Confidence: {detection.confidence:.2%}")
    print(f"  Trust score: {detection.trust_score:.2f}")
    print(f"  Bbox: {detection.bbox}")
    print(f"  Explanation: {detection.explanation}")
```

### **Time Series with LSTM**

```python
from trustwrapper.tensorflow.timeseries import TimeSeriesWrapper

# Create LSTM model for time series
model = keras.Sequential([
    keras.layers.LSTM(64, return_sequences=True, input_shape=(None, 10)),
    keras.layers.LSTM(32),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1)
])

# Wrap for time series analysis
ts_wrapper = TimeSeriesWrapper(
    model=model,
    lookback_window=30,
    forecast_horizon=7,
    track_temporal_trust=True,
    uncertainty_estimation='monte_carlo'
)

# Make predictions with uncertainty
time_series_data = np.random.randn(1, 30, 10)
forecast = ts_wrapper.forecast(
    time_series_data,
    n_samples=100,  # Monte Carlo samples
    return_confidence_intervals=True
)

print(f"Forecast: {forecast.predictions}")
print(f"95% CI: [{forecast.lower_bound}, {forecast.upper_bound}]")
print(f"Temporal trust scores: {forecast.trust_scores}")
print(f"Uncertainty: {forecast.uncertainty}")
```

### **Transformer Models**

```python
from trustwrapper.tensorflow.transformers import TransformerWrapper

# Create a simple transformer model
class TransformerBlock(keras.layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim):
        super().__init__()
        self.att = keras.layers.MultiHeadAttention(
            num_heads=num_heads, 
            key_dim=embed_dim
        )
        self.ffn = keras.Sequential([
            keras.layers.Dense(ff_dim, activation="relu"),
            keras.layers.Dense(embed_dim),
        ])
        self.layernorm1 = keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = keras.layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = keras.layers.Dropout(0.1)
        self.dropout2 = keras.layers.Dropout(0.1)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

# Build transformer model
inputs = keras.Input(shape=(None,), dtype=tf.int32)
embedding_layer = keras.layers.Embedding(10000, 128)
x = embedding_layer(inputs)

transformer_block = TransformerBlock(128, 8, 512)
x = transformer_block(x)

x = keras.layers.GlobalAveragePooling1D()(x)
outputs = keras.layers.Dense(3, activation='softmax')(x)

transformer_model = keras.Model(inputs=inputs, outputs=outputs)

# Wrap with attention tracking
transformer_wrapper = TransformerWrapper(
    model=transformer_model,
    track_attention_weights=True,
    explain_attention_patterns=True,
    aggregation_method='max'  # How to aggregate multi-head attention
)

# Get predictions with attention explanations
text_input = np.random.randint(0, 10000, size=(1, 50))
result = transformer_wrapper.predict_with_attention(
    text_input,
    return_attention_matrices=True,
    return_token_importance=True
)

print(f"Prediction: {result.prediction}")
print(f"Trust score: {result.trust_score}")
print(f"Important tokens: {result.important_token_indices[:5]}")
print(f"Attention pattern shape: {result.attention_weights.shape}")
```

## 📋 Best Practices

### **1. Model Preparation**
```python
# Standardize inputs
@tf.function
def preprocess(x):
    x = tf.cast(x, tf.float32)
    x = tf.nn.l2_normalize(x, axis=-1)
    return x

# Apply preprocessing in model
inputs = keras.Input(shape=(10,))
preprocessed = keras.layers.Lambda(preprocess)(inputs)
# ... rest of model

# Save with signatures
signatures = {
    'serving_default': tf.function(
        lambda x: model(preprocess(x))
    ).get_concrete_function(
        tf.TensorSpec(shape=[None, 10], dtype=tf.float32)
    )
}
```

### **2. Memory Management**
```python
# Use tf.data for efficient data loading
dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
dataset = dataset.batch(32).prefetch(tf.data.AUTOTUNE)

# Clear session periodically
tf.keras.backend.clear_session()

# Limit GPU memory growth
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
```

### **3. Deployment Considerations**
```python
# Version your models
model_version = "2.1.0"
export_path = f"./models/{model_name}/{model_version}"

# Include metadata
metadata = {
    'model_name': model_name,
    'version': model_version,
    'input_shape': model.input_shape,
    'output_shape': model.output_shape,
    'trust_config': wrapper.get_config()
}

# Save with TrustWrapper metadata
wrapper.save(export_path, include_metadata=True)
```

## 🔧 Troubleshooting

### **Common Issues and Solutions**

#### **1. TF Function Tracing Issues**
```python
# Solution: Use explicit tf.function decoration
@tf.function(
    input_signature=[
        tf.TensorSpec(shape=[None, 224, 224, 3], dtype=tf.float32)
    ]
)
def inference_fn(inputs):
    return wrapped_model(inputs)
```

#### **2. Memory Leaks**
```python
# Solution: Proper resource cleanup
def process_batch_safely(batch_data):
    try:
        result = wrapped_model.predict(batch_data)
        return result
    finally:
        # Clean up
        tf.keras.backend.clear_session()
        if hasattr(wrapped_model, 'cleanup'):
            wrapped_model.cleanup()
```

#### **3. Slow Serving Performance**
```python
# Solution: Optimize serving pipeline
from trustwrapper.tensorflow.serving import OptimizedServer

server = OptimizedServer(
    model=wrapped_model,
    enable_batching=True,
    max_batch_size=32,
    batch_timeout_micros=1000,
    num_batch_threads=4,
    enable_model_warmup=True
)

# Warm up model
server.warmup(num_samples=100)
```

#### **4. Incompatible TF Versions**
```python
# Check compatibility
from trustwrapper.tensorflow import check_compatibility

compatibility = check_compatibility()
print(f"TF Version: {compatibility.tf_version}")
print(f"Compatible: {compatibility.is_compatible}")
print(f"Warnings: {compatibility.warnings}")

# Use compatibility mode if needed
wrapped_model = wrap_tf_model(
    model,
    compatibility_mode='tf_2_10'  # Force specific version behavior
)
```

### **Debug Mode**
```python
# Enable debug logging
tf.debugging.set_log_device_placement(True)
tf.config.run_functions_eagerly(True)

# Use TrustWrapper debug mode
from trustwrapper.tensorflow import enable_debug_mode

enable_debug_mode()
result = wrapped_model.predict(test_input)
print(f"Debug info: {result.debug_info}")
```

## 📚 Additional Resources

### **TensorFlow Integration Examples**
- [Image Classification Demo](../../demos/tf_image_classification_demo.py)
- [NLP with BERT Demo](../../demos/tf_bert_demo.py)
- [Time Series Forecasting Demo](../../demos/tf_timeseries_demo.py)

### **Documentation**
- [TrustWrapper API Reference](../api/TRUSTWRAPPER_API_REFERENCE.md)
- [TensorFlow Best Practices](https://www.tensorflow.org/guide/keras/custom_layers_and_models)
- [TF Serving Guide](https://www.tensorflow.org/tfx/guide/serving)

### **Community**
- [GitHub Issues](https://github.com/lamassu-labs/trustwrapper/issues)
- [TensorFlow Forum](https://discuss.tensorflow.org/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/trustwrapper+tensorflow)

---

**Next Steps**: Check out our [Hugging Face Integration Guide](HUGGINGFACE_INTEGRATION.md) or explore the [PyTorch Integration Guide](PYTORCH_INTEGRATION.md) for cross-framework compatibility.