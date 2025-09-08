# Explainable AI Methods Comparison

**Version**: 1.0
**Date**: June 22, 2025
**Status**: Technical Comparison Guide

## 🎯 Overview

This document provides a comprehensive comparison of explainable AI (XAI) methods implemented in TrustWrapper, helping developers choose the right approach for their specific use cases and model types.

## 📊 XAI Methods Overview

### Quick Comparison Matrix

| Method | Model Agnostic | Speed | Explanation Type | Best For |
|--------|----------------|-------|------------------|----------|
| **SHAP** | ✅ Yes | Medium | Feature importance | Any model, global insights |
| **LIME** | ✅ Yes | Fast | Local explanations | Individual predictions |
| **Grad-CAM** | ❌ No | Very Fast | Visual heatmaps | CNNs, computer vision |
| **Attention** | ❌ No | Very Fast | Attention weights | Transformers, NLP |
| **Counterfactual** | ✅ Yes | Slow | What-if scenarios | Decision support |
| **Anchors** | ✅ Yes | Medium | Rule-based | High-precision rules |

## 🔬 Detailed Method Analysis

### 1. SHAP (SHapley Additive exPlanations)

#### Theory
Based on game theory, SHAP assigns each feature an importance value for a particular prediction by computing Shapley values.

#### Implementation
```python
import shap
from trustwrapper.xai import SHAPExplainer

class TrustWrapperSHAP(SHAPExplainer):
    def __init__(self, model, background_data, method='deep'):
        """
        Initialize SHAP explainer

        Args:
            model: The AI model to explain
            background_data: Representative samples for baseline
            method: 'deep' for neural networks, 'tree' for tree-based
        """
        self.model = model

        if method == 'deep':
            self.explainer = shap.DeepExplainer(model, background_data)
        elif method == 'tree':
            self.explainer = shap.TreeExplainer(model)
        else:
            self.explainer = shap.KernelExplainer(model.predict, background_data)

    def explain_instance(self, instance):
        """Generate SHAP values for a single instance"""
        shap_values = self.explainer.shap_values(instance)

        return {
            'shap_values': shap_values,
            'base_value': self.explainer.expected_value,
            'feature_names': self.feature_names,
            'instance_values': instance
        }

    def explain_global(self, test_data, top_k=10):
        """Generate global feature importance"""
        shap_values = self.explainer.shap_values(test_data)

        # Aggregate SHAP values
        global_importance = np.abs(shap_values).mean(axis=0)

        # Get top k features
        top_features = np.argsort(global_importance)[-top_k:][::-1]

        return {
            'top_features': [(self.feature_names[i], global_importance[i])
                           for i in top_features],
            'shap_values': shap_values,
            'summary_plot': self._generate_summary_plot(shap_values)
        }
```

#### Advantages
- **Consistent**: Satisfies important theoretical properties
- **Global & Local**: Provides both types of explanations
- **Proven**: Widely adopted and validated

#### Disadvantages
- **Computational Cost**: O(2^n) for exact computation
- **Background Dependence**: Results vary with background data choice
- **Correlation Handling**: May assign importance to correlated features arbitrarily

#### Performance Optimization
```python
# Optimized SHAP with sampling
class OptimizedSHAP(TrustWrapperSHAP):
    def explain_batch(self, instances, sample_size=100):
        """Batch explanation with sampling for efficiency"""
        if len(instances) > sample_size:
            # Random sampling for large batches
            indices = np.random.choice(len(instances), sample_size, replace=False)
            sampled_instances = instances[indices]
        else:
            sampled_instances = instances

        # Parallel computation
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for instance in sampled_instances:
                future = executor.submit(self.explain_instance, instance)
                futures.append(future)

            results = [future.result() for future in futures]

        return results
```

### 2. LIME (Local Interpretable Model-agnostic Explanations)

#### Theory
LIME explains individual predictions by approximating the model locally with an interpretable model.

#### Implementation
```python
import lime
from lime.lime_tabular import LimeTabularExplainer

class TrustWrapperLIME:
    def __init__(self, training_data, feature_names, class_names=None,
                 mode='classification'):
        """
        Initialize LIME explainer

        Args:
            training_data: Training data for statistics
            feature_names: List of feature names
            class_names: List of class names for classification
            mode: 'classification' or 'regression'
        """
        self.explainer = LimeTabularExplainer(
            training_data,
            feature_names=feature_names,
            class_names=class_names,
            mode=mode,
            discretize_continuous=True
        )

    def explain_instance(self, instance, predict_fn, num_features=10):
        """Explain a single instance"""
        explanation = self.explainer.explain_instance(
            instance,
            predict_fn,
            num_features=num_features,
            num_samples=5000  # Number of perturbed samples
        )

        return {
            'feature_importance': explanation.as_list(),
            'local_pred': explanation.local_pred,
            'score': explanation.score,
            'visualization': self._generate_plot(explanation)
        }

    def _generate_perturbations(self, instance, num_samples):
        """Custom perturbation strategy for better locality"""
        # Generate perturbations closer to the instance
        perturbations = []

        for _ in range(num_samples):
            perturbed = instance.copy()
            # Perturb with decreasing variance
            noise_scale = np.random.exponential(0.1)
            noise = np.random.normal(0, noise_scale, instance.shape)
            perturbed += noise
            perturbations.append(perturbed)

        return np.array(perturbations)
```

#### Advantages
- **Fast**: Quick local explanations
- **Intuitive**: Simple linear models are easy to understand
- **Flexible**: Works with any model type

#### Disadvantages
- **Local Only**: No global model understanding
- **Instability**: Explanations can vary between runs
- **Sampling Bias**: Quality depends on perturbation strategy

### 3. Grad-CAM (Gradient-weighted Class Activation Mapping)

#### Theory
Uses gradients of the target concept flowing into the final convolutional layer to produce a localization map.

#### Implementation
```python
import torch
import torch.nn.functional as F

class TrustWrapperGradCAM:
    def __init__(self, model, target_layer):
        """
        Initialize Grad-CAM

        Args:
            model: PyTorch CNN model
            target_layer: Layer to compute CAM for
        """
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        # Register hooks
        self._register_hooks()

    def _register_hooks(self):
        """Register forward and backward hooks"""
        def forward_hook(module, input, output):
            self.activations = output.detach()

        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_backward_hook(backward_hook)

    def generate_cam(self, input_image, target_class=None):
        """Generate class activation map"""
        # Forward pass
        output = self.model(input_image)

        if target_class is None:
            target_class = output.argmax(1)

        # Backward pass
        self.model.zero_grad()
        one_hot = torch.zeros_like(output)
        one_hot[0][target_class] = 1.0
        output.backward(gradient=one_hot, retain_graph=True)

        # Generate CAM
        gradients = self.gradients[0]
        activations = self.activations[0]

        # Global average pooling of gradients
        weights = gradients.mean(dim=(1, 2), keepdim=True)

        # Weighted combination of activations
        cam = (weights * activations).sum(dim=0)

        # ReLU and normalize
        cam = F.relu(cam)
        cam = cam / cam.max()

        # Resize to input size
        cam = F.interpolate(
            cam.unsqueeze(0).unsqueeze(0),
            size=input_image.shape[-2:],
            mode='bilinear',
            align_corners=False
        )[0, 0]

        return cam.numpy()
```

#### Advantages
- **Visual**: Intuitive heatmap explanations
- **Fast**: Single forward-backward pass
- **No Training**: Works immediately with trained CNNs

#### Disadvantages
- **CNN Only**: Limited to convolutional architectures
- **Coarse**: Limited by feature map resolution
- **Single Layer**: Focuses on one layer only

### 4. Attention Visualization

#### Theory
Leverages attention mechanisms in transformers to show which parts of the input the model focuses on.

#### Implementation
```python
class TrustWrapperAttention:
    def __init__(self, model, layer_names=None):
        """
        Initialize attention visualizer

        Args:
            model: Transformer model with attention
            layer_names: Specific layers to analyze
        """
        self.model = model
        self.layer_names = layer_names or self._get_attention_layers()
        self.attention_weights = {}

    def extract_attention(self, input_ids, attention_mask=None):
        """Extract attention weights from model"""
        # Hook to capture attention
        handles = []

        def hook_fn(name):
            def hook(module, input, output):
                if hasattr(output, 'attentions'):
                    self.attention_weights[name] = output.attentions
            return hook

        # Register hooks
        for name, module in self.model.named_modules():
            if name in self.layer_names:
                handle = module.register_forward_hook(hook_fn(name))
                handles.append(handle)

        # Forward pass
        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                output_attentions=True
            )

        # Remove hooks
        for handle in handles:
            handle.remove()

        return self.attention_weights

    def visualize_attention(self, tokens, layer_idx=11, head_idx=0):
        """Create attention visualization"""
        attention = self.attention_weights[f'layer_{layer_idx}']
        attention_head = attention[0, head_idx].cpu().numpy()

        return {
            'tokens': tokens,
            'attention_matrix': attention_head,
            'attention_plot': self._create_heatmap(tokens, attention_head)
        }
```

#### Advantages
- **Built-in**: Uses model's inherent attention mechanism
- **Multi-head**: Can analyze different attention patterns
- **Interpretable**: Shows direct model focus

#### Disadvantages
- **Architecture Specific**: Only for attention-based models
- **Not Causal**: Attention ≠ importance always
- **Complex Patterns**: Multi-head attention can be hard to interpret

### 5. Counterfactual Explanations

#### Theory
Finds minimal changes to input that would change the model's prediction.

#### Implementation
```python
class TrustWrapperCounterfactual:
    def __init__(self, model, feature_ranges):
        """
        Initialize counterfactual explainer

        Args:
            model: The model to explain
            feature_ranges: Valid ranges for each feature
        """
        self.model = model
        self.feature_ranges = feature_ranges

    def generate_counterfactual(self, instance, target_class,
                              max_iterations=1000, learning_rate=0.01):
        """Generate counterfactual explanation"""
        # Convert to tensor
        x = torch.tensor(instance, requires_grad=True)
        original_class = self.model(x.unsqueeze(0)).argmax()

        # Optimization loop
        for i in range(max_iterations):
            # Forward pass
            output = self.model(x.unsqueeze(0))
            pred_class = output.argmax()

            # Check if we reached target
            if pred_class == target_class:
                return self._format_counterfactual(instance, x.detach().numpy())

            # Loss: maximize target class probability + minimize changes
            loss = -output[0, target_class] + 0.1 * torch.norm(x - torch.tensor(instance))

            # Backward pass
            loss.backward()

            # Update with constraints
            with torch.no_grad():
                x -= learning_rate * x.grad
                x.grad.zero_()

                # Apply feature constraints
                for i, (min_val, max_val) in enumerate(self.feature_ranges):
                    x[i] = torch.clamp(x[i], min_val, max_val)

        return None  # Failed to find counterfactual

    def _format_counterfactual(self, original, counterfactual):
        """Format the counterfactual explanation"""
        changes = []
        for i, (orig, cf) in enumerate(zip(original, counterfactual)):
            if abs(orig - cf) > 0.01:  # Significant change
                changes.append({
                    'feature': i,
                    'original': orig,
                    'counterfactual': cf,
                    'change': cf - orig
                })

        return {
            'original': original,
            'counterfactual': counterfactual,
            'changes': sorted(changes, key=lambda x: abs(x['change']), reverse=True),
            'num_changes': len(changes)
        }
```

#### Advantages
- **Actionable**: Shows exactly what to change
- **Intuitive**: "What-if" scenarios are natural
- **Personalized**: Specific to each instance

#### Disadvantages
- **Computationally Expensive**: Optimization process
- **Multiple Solutions**: Many valid counterfactuals exist
- **Feasibility**: May suggest impossible changes

### 6. Anchors

#### Theory
Finds high-precision rules that "anchor" the prediction locally.

#### Implementation
```python
from anchor import anchor_tabular

class TrustWrapperAnchors:
    def __init__(self, training_data, feature_names, categorical_names=None):
        """
        Initialize Anchors explainer

        Args:
            training_data: Training data for perturbations
            feature_names: List of feature names
            categorical_names: Dict mapping categorical features to values
        """
        self.explainer = anchor_tabular.AnchorTabularExplainer(
            class_names=['0', '1'],
            feature_names=feature_names,
            train_data=training_data,
            categorical_names=categorical_names
        )

    def explain_instance(self, instance, predict_fn, threshold=0.95):
        """Find anchor rules for instance"""
        explanation = self.explainer.explain_instance(
            instance,
            predict_fn,
            threshold=threshold,
            max_anchor_size=None,
            coverage_samples=10000
        )

        return {
            'anchor': explanation.names(),
            'precision': explanation.precision(),
            'coverage': explanation.coverage(),
            'features': explanation.features(),
            'rule': self._format_rule(explanation)
        }

    def _format_rule(self, explanation):
        """Convert anchor to readable rule"""
        conditions = []
        for feature_idx, op, value in explanation.data()['anchor']:
            feature_name = self.feature_names[feature_idx]
            conditions.append(f"{feature_name} {op} {value}")

        return " AND ".join(conditions)
```

#### Advantages
- **High Precision**: Rules have guarantees
- **Clear Boundaries**: Defines decision regions
- **Verifiable**: Easy to validate rules

#### Disadvantages
- **Coverage Trade-off**: High precision often means low coverage
- **Complexity**: Rules can become very specific
- **Computational**: Expensive to find optimal anchors

## 🔄 Hybrid Approaches

### Combining Multiple Methods

```python
class HybridExplainer:
    def __init__(self, model, config):
        """Initialize multiple explainers"""
        self.model = model
        self.shap_explainer = TrustWrapperSHAP(model, config['background_data'])
        self.lime_explainer = TrustWrapperLIME(
            config['training_data'],
            config['feature_names']
        )
        self.counterfactual = TrustWrapperCounterfactual(
            model,
            config['feature_ranges']
        )

    def explain_comprehensive(self, instance):
        """Generate multi-method explanation"""
        explanations = {}

        # Fast local explanation with LIME
        explanations['local'] = self.lime_explainer.explain_instance(
            instance,
            self.model.predict,
            num_features=5
        )

        # Detailed SHAP analysis
        explanations['shap'] = self.shap_explainer.explain_instance(instance)

        # Actionable counterfactual
        target_class = 1 - self.model.predict(instance).argmax()
        explanations['counterfactual'] = self.counterfactual.generate_counterfactual(
            instance,
            target_class
        )

        # Aggregate insights
        explanations['summary'] = self._aggregate_explanations(explanations)

        return explanations

    def _aggregate_explanations(self, explanations):
        """Combine insights from multiple methods"""
        # Extract top features from each method
        lime_features = set(f[0] for f in explanations['local']['feature_importance'][:3])
        shap_features = set(np.argsort(np.abs(explanations['shap']['shap_values']))[-3:])
        cf_features = set(c['feature'] for c in explanations['counterfactual']['changes'][:3])

        # Find consensus features
        consensus_features = lime_features & shap_features

        return {
            'consensus_features': list(consensus_features),
            'all_important_features': list(lime_features | shap_features | cf_features),
            'confidence': len(consensus_features) / 3.0
        }
```

## 📊 Method Selection Guide

### Decision Tree for Method Selection

```python
def select_xai_method(model_type, use_case, constraints):
    """Recommend XAI method based on requirements"""

    if model_type == 'cnn' and use_case == 'visual':
        return 'grad_cam'

    if model_type == 'transformer' and use_case == 'nlp':
        return 'attention'

    if constraints.get('real_time', False):
        if constraints.get('global_insights', False):
            return 'shap_sampling'  # SHAP with aggressive sampling
        return 'lime'

    if use_case == 'regulatory_compliance':
        return 'shap'  # Most rigorous

    if use_case == 'user_recourse':
        return 'counterfactual'

    if use_case == 'high_stakes_decision':
        return 'hybrid'  # Multiple methods for confidence

    return 'shap'  # Good default
```

### Performance Benchmarks

| Method | Setup Time | Explanation Time (per instance) | Memory Usage |
|--------|------------|--------------------------------|--------------|
| SHAP (Deep) | 5-30s | 100-500ms | 2-8 GB |
| SHAP (Kernel) | <1s | 1-10s | 1-4 GB |
| LIME | <1s | 50-200ms | <1 GB |
| Grad-CAM | <1s | 10-50ms | <500 MB |
| Attention | 0s | 1-10ms | Model size |
| Counterfactual | <1s | 0.5-5s | <1 GB |
| Anchors | 1-5s | 1-10s | 1-2 GB |

## 🎯 Best Practices

### 1. Method Validation

```python
def validate_explanation_quality(explainer, test_set, model):
    """Validate explanation quality metrics"""
    metrics = {
        'fidelity': [],
        'stability': [],
        'consistency': []
    }

    for instance in test_set:
        # Fidelity: How well explanation approximates model
        explanation = explainer.explain_instance(instance)
        fidelity = measure_fidelity(explanation, model, instance)
        metrics['fidelity'].append(fidelity)

        # Stability: Consistency across similar inputs
        perturbed = instance + np.random.normal(0, 0.01, instance.shape)
        explanation_perturbed = explainer.explain_instance(perturbed)
        stability = measure_stability(explanation, explanation_perturbed)
        metrics['stability'].append(stability)

        # Consistency: Agreement with other methods
        other_explanation = alternative_explainer.explain_instance(instance)
        consistency = measure_consistency(explanation, other_explanation)
        metrics['consistency'].append(consistency)

    return {k: np.mean(v) for k, v in metrics.items()}
```

### 2. Explanation Caching

```python
class CachedExplainer:
    def __init__(self, base_explainer, cache_size=1000):
        self.explainer = base_explainer
        self.cache = LRUCache(maxsize=cache_size)
        self.similarity_threshold = 0.98

    def explain_instance(self, instance):
        # Check cache for similar instances
        instance_hash = self._hash_instance(instance)

        for cached_hash, (cached_instance, explanation) in self.cache.items():
            similarity = cosine_similarity(instance, cached_instance)
            if similarity > self.similarity_threshold:
                return self._adapt_explanation(explanation, instance, cached_instance)

        # Generate new explanation
        explanation = self.explainer.explain_instance(instance)
        self.cache[instance_hash] = (instance, explanation)

        return explanation
```

### 3. Explanation Presentation

```python
class ExplanationPresenter:
    """Format explanations for different audiences"""

    def format_for_developer(self, explanation):
        """Technical details with feature indices"""
        return {
            'feature_importance': explanation['shap_values'],
            'base_value': explanation['base_value'],
            'prediction_path': self._trace_decision_path(explanation)
        }

    def format_for_end_user(self, explanation, feature_descriptions):
        """Natural language with meaningful names"""
        important_features = self._get_top_features(explanation, n=3)

        narrative = "This prediction was made because:\n"
        for feature, importance in important_features:
            description = feature_descriptions[feature]
            direction = "increases" if importance > 0 else "decreases"
            narrative += f"- {description} {direction} the likelihood\n"

        return narrative

    def format_for_regulator(self, explanation):
        """Comprehensive audit trail"""
        return {
            'timestamp': datetime.now().isoformat(),
            'model_version': self.model_version,
            'explanation_method': explanation['method'],
            'feature_contributions': explanation['feature_importance'],
            'confidence_intervals': self._compute_confidence_intervals(explanation),
            'validation_metrics': self._get_validation_metrics()
        }
```

## 🔗 Integration with TrustWrapper

### Unified API

```python
from trustwrapper import TrustWrapper

# Initialize with XAI configuration
wrapper = TrustWrapper(
    model=your_model,
    xai_config={
        'primary_method': 'shap',
        'secondary_method': 'counterfactual',
        'background_samples': 1000,
        'explanation_features': 10,
        'cache_explanations': True
    }
)

# Get explanation with verification
result = wrapper.explain_and_verify(input_data)

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']}")
print(f"Top factors: {result['explanation']['top_factors']}")
print(f"Verification proof: {result['zk_proof'][:50]}...")
```

---

*For method-specific implementation details and optimization techniques, refer to the individual method guides in the [TrustWrapper Documentation](https://docs.trustwrapper.io/xai)*
