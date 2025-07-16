# 🤗 Hugging Face Integration Guide for TrustWrapper

**Version**: 1.0.0
**Last Updated**: June 22, 2025
**Compatibility**: Transformers 4.30+ with TrustWrapper v1.0+

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Model Hub Integration](#model-hub-integration)
5. [Pipeline Integration](#pipeline-integration)
6. [Custom Transformers](#custom-transformers)
7. [Explainability for Transformers](#explainability-for-transformers)
8. [Model Cards with Trust](#model-cards-with-trust)
9. [Advanced Examples](#advanced-examples)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

## 🎯 Overview

This guide demonstrates how to integrate Hugging Face Transformers with TrustWrapper for zero-knowledge verified AI inference. Add trust badges, explainability, and verification to any Hugging Face model while maintaining full compatibility with the ecosystem.

### **Key Features**
- **Hub Integration**: Direct integration with Hugging Face Model Hub
- **Pipeline Support**: Works with all Transformers pipelines
- **AutoModel Compatible**: Seamless with AutoModel classes
- **Trust Badges**: Add verification badges to Model Cards
- **Spaces Integration**: Deploy trusted models on HF Spaces

## 📋 Prerequisites

### **Required Packages**
```bash
# Install TrustWrapper with Hugging Face support
pip install trustwrapper[huggingface]

# Install Transformers (if not already installed)
pip install transformers>=4.30.0 datasets accelerate

# Additional dependencies
pip install tokenizers sentencepiece protobuf
```

### **Environment Setup**
```python
from transformers import AutoModel, AutoTokenizer, pipeline
from trustwrapper.huggingface import HuggingFaceWrapper, wrap_hf_model
from trustwrapper import Config
```

## 🚀 Quick Start

### **Basic Model Wrapping**

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from trustwrapper.huggingface import wrap_hf_model

# Load any Hugging Face model
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Wrap with TrustWrapper
wrapped_model = wrap_hf_model(
    model=model,
    tokenizer=tokenizer,
    task="sentiment-analysis",
    enable_explanations=True,
    enable_zk_proofs=True
)

# Use the wrapped model
text = "I love this new AI model! It's amazing and trustworthy."
result = wrapped_model.predict(text)

print(f"Sentiment: {result.label} ({result.score:.2%})")
print(f"Trust Score: {result.trust_score:.2f}")
print(f"Explanation: {result.explanation}")
print(f"ZK Proof: {result.zk_proof[:50]}...")
```

### **Pipeline Integration**

```python
from transformers import pipeline
from trustwrapper.huggingface import TrustPipeline

# Create a standard pipeline
base_pipeline = pipeline("text-generation", model="gpt2")

# Wrap with TrustWrapper
trust_pipeline = TrustPipeline(
    pipeline=base_pipeline,
    enable_hallucination_detection=True,
    confidence_threshold=0.8,
    max_uncertainty=0.3
)

# Generate text with trust metrics
prompt = "The future of AI is"
results = trust_pipeline(
    prompt,
    max_length=50,
    num_return_sequences=3,
    return_trust_metrics=True
)

for i, result in enumerate(results):
    print(f"\nGeneration {i+1}:")
    print(f"Text: {result['generated_text']}")
    print(f"Trust Score: {result['trust_score']:.2f}")
    print(f"Hallucination Risk: {result['hallucination_risk']}")
    print(f"Uncertainty: {result['uncertainty']:.3f}")
```

## 🔧 Model Hub Integration

### **Loading Models with Trust Features**

```python
from trustwrapper.huggingface import AutoModelWithTrust, AutoTokenizerWithTrust

# Load model with integrated trust features
model = AutoModelWithTrust.from_pretrained(
    "bert-base-uncased",
    trust_config={
        "explanation_method": "attention",
        "track_confidence": True,
        "enable_zk_proofs": True,
        "proof_backend": "aleo"
    }
)

tokenizer = AutoTokenizerWithTrust.from_pretrained("bert-base-uncased")

# Use like a normal Hugging Face model
inputs = tokenizer("Hello world!", return_tensors="pt")
outputs = model(**inputs)

# Access trust features
trust_metrics = outputs.trust_metrics
print(f"Model confidence: {trust_metrics.confidence:.2%}")
print(f"Attention entropy: {trust_metrics.attention_entropy:.3f}")
```

### **Saving Models with Trust Metadata**

```python
# Train or fine-tune your model
# ... training code ...

# Save with trust metadata
output_dir = "./my-trusted-model"
wrapped_model.save_pretrained(
    output_dir,
    trust_metadata={
        "trust_version": "1.0.0",
        "verification_method": "zk_snark",
        "explanation_methods": ["attention", "gradients"],
        "trust_threshold": 0.85,
        "last_verification": "2025-06-22T10:00:00Z"
    }
)

# Push to Hub with trust badge
wrapped_model.push_to_hub(
    "my-username/my-trusted-model",
    commit_message="Add TrustWrapper verification",
    add_trust_badge=True
)
```

### **Model Card with Trust Information**

```python
from trustwrapper.huggingface import create_trust_model_card

# Generate model card with trust information
trust_card = create_trust_model_card(
    model=wrapped_model,
    base_model=model_name,
    tasks=["sentiment-analysis", "text-classification"],
    trust_metrics={
        "average_trust_score": 0.92,
        "hallucination_rate": 0.03,
        "explanation_coverage": 0.95
    },
    verification_results={
        "zk_proof_valid": True,
        "blockchain_verified": True,
        "verification_chain": "aleo",
        "verification_tx": "0x123...abc"
    }
)

# Save model card
with open(f"{output_dir}/README.md", "w") as f:
    f.write(trust_card)
```

## 🚀 Pipeline Integration

### **Wrapping Existing Pipelines**

```python
from transformers import pipeline
from trustwrapper.huggingface import wrap_pipeline

# Question answering pipeline
qa_pipeline = pipeline("question-answering")

# Wrap with trust features
trusted_qa = wrap_pipeline(
    qa_pipeline,
    explanation_method="attention_rollout",
    confidence_threshold=0.7,
    track_context_relevance=True
)

# Use with trust metrics
context = """
The TrustWrapper framework adds verification and explainability to AI models.
It uses zero-knowledge proofs to verify predictions without exposing model weights.
The framework is compatible with PyTorch, TensorFlow, and Hugging Face models.
"""

question = "What does TrustWrapper use for verification?"

answer = trusted_qa(
    question=question,
    context=context,
    return_trust_metrics=True
)

print(f"Answer: {answer['answer']}")
print(f"Confidence: {answer['score']:.2%}")
print(f"Trust Score: {answer['trust_score']:.2f}")
print(f"Context Relevance: {answer['context_relevance']:.2f}")
print(f"Answer Span Trust: {answer['span_trust']:.2f}")
```

### **Multi-Task Pipeline**

```python
from trustwrapper.huggingface import MultiTaskTrustPipeline

# Create multi-task pipeline with trust
multi_pipeline = MultiTaskTrustPipeline([
    ("sentiment", pipeline("sentiment-analysis")),
    ("ner", pipeline("ner")),
    ("summarization", pipeline("summarization"))
])

# Process text with all tasks
text = """
Apple Inc. announced record profits today. The CEO Tim Cook expressed
optimism about future growth. Investors responded positively to the news,
with stock prices rising 5% in after-hours trading.
"""

results = multi_pipeline(text, tasks=["sentiment", "ner"])

print("Multi-task results with trust:")
for task, result in results.items():
    print(f"\n{task.upper()}:")
    print(f"  Output: {result['output']}")
    print(f"  Trust Score: {result['trust_score']:.2f}")
    print(f"  Task Confidence: {result['confidence']:.2%}")
```

### **Custom Pipeline Components**

```python
from transformers import Pipeline
from trustwrapper.huggingface import TrustPipelineComponent

class CustomTrustPipeline(Pipeline):
    def __init__(self, model, tokenizer, **kwargs):
        super().__init__(model=model, tokenizer=tokenizer, **kwargs)
        self.trust_component = TrustPipelineComponent(
            track_token_confidence=True,
            explanation_granularity="token"
        )

    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        forward_kwargs = {}
        postprocess_kwargs = {
            "return_trust": kwargs.get("return_trust", True)
        }
        return preprocess_kwargs, forward_kwargs, postprocess_kwargs

    def preprocess(self, text):
        return self.tokenizer(text, return_tensors="pt", truncation=True)

    def _forward(self, model_inputs):
        outputs = self.model(**model_inputs)
        trust_data = self.trust_component.compute_trust(outputs, model_inputs)
        return {"outputs": outputs, "trust_data": trust_data}

    def postprocess(self, model_outputs, return_trust=True):
        outputs = model_outputs["outputs"]
        predictions = outputs.logits.argmax(-1)

        result = {
            "label": self.model.config.id2label[predictions.item()],
            "score": outputs.logits.softmax(-1).max().item()
        }

        if return_trust:
            result.update(model_outputs["trust_data"])

        return result

# Register custom pipeline
from transformers import PIPELINE_REGISTRY
PIPELINE_REGISTRY.register_pipeline(
    "custom-trust-classification",
    pipeline_class=CustomTrustPipeline,
    pt_model=AutoModelForSequenceClassification
)
```

## 🤖 Custom Transformers

### **Creating Trust-Aware Transformers**

```python
import torch
from torch import nn
from transformers import PreTrainedModel, PretrainedConfig
from trustwrapper.huggingface import TrustMixin

class TrustConfig(PretrainedConfig):
    model_type = "trust_transformer"

    def __init__(
        self,
        vocab_size=30522,
        hidden_size=768,
        num_attention_heads=12,
        num_hidden_layers=12,
        trust_head_size=128,
        explanation_method="attention",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_attention_heads = num_attention_heads
        self.num_hidden_layers = num_hidden_layers
        self.trust_head_size = trust_head_size
        self.explanation_method = explanation_method

class TrustTransformer(PreTrainedModel, TrustMixin):
    config_class = TrustConfig

    def __init__(self, config):
        super().__init__(config)

        # Standard transformer components
        self.embeddings = nn.Embedding(config.vocab_size, config.hidden_size)
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=config.hidden_size,
                nhead=config.num_attention_heads,
                batch_first=True
            ),
            num_layers=config.num_hidden_layers
        )

        # Trust-specific components
        self.trust_head = nn.Sequential(
            nn.Linear(config.hidden_size, config.trust_head_size),
            nn.ReLU(),
            nn.Linear(config.trust_head_size, 1),
            nn.Sigmoid()
        )

        self.init_weights()

    def forward(self, input_ids, attention_mask=None, return_trust=True):
        # Embed inputs
        embeddings = self.embeddings(input_ids)

        # Encode with transformer
        encoded = self.encoder(
            embeddings,
            src_key_padding_mask=~attention_mask.bool() if attention_mask is not None else None
        )

        # Pool for classification
        pooled = encoded.mean(dim=1)

        # Compute trust score
        trust_score = self.trust_head(pooled) if return_trust else None

        # Get attention weights for explainability
        attention_weights = self.get_attention_weights()

        return TrustTransformerOutput(
            last_hidden_state=encoded,
            pooler_output=pooled,
            trust_score=trust_score,
            attention_weights=attention_weights
        )

# Use the custom model
config = TrustConfig()
model = TrustTransformer(config)

# Wrap for additional features
wrapped_model = wrap_hf_model(
    model,
    model_type="custom",
    trust_integration="native"
)
```

### **Fine-tuning with Trust Objectives**

```python
from transformers import Trainer, TrainingArguments
from trustwrapper.huggingface import TrustTrainer, TrustLoss

# Custom loss that includes trust objectives
class TrustAwareTrainingLoss(nn.Module):
    def __init__(self, alpha=0.1):
        super().__init__()
        self.ce_loss = nn.CrossEntropyLoss()
        self.trust_loss = TrustLoss()
        self.alpha = alpha

    def forward(self, outputs, labels, trust_targets=None):
        # Standard classification loss
        ce_loss = self.ce_loss(outputs.logits, labels)

        # Trust regularization
        if trust_targets is not None:
            trust_reg = self.trust_loss(outputs.trust_scores, trust_targets)
        else:
            # Encourage high trust scores
            trust_reg = -outputs.trust_scores.mean()

        return ce_loss + self.alpha * trust_reg

# Create trust-aware trainer
training_args = TrainingArguments(
    output_dir="./trust-finetuned-model",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

trainer = TrustTrainer(
    model=wrapped_model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
    trust_loss_weight=0.1,
    track_trust_improvement=True
)

# Fine-tune with trust objectives
trainer.train()

# Evaluate trust metrics
trust_eval = trainer.evaluate_trust()
print(f"Average trust score: {trust_eval['avg_trust_score']:.2f}")
print(f"Trust improvement: {trust_eval['trust_improvement']:.1%}")
```

## 🔍 Explainability for Transformers

### **Attention-based Explanations**

```python
from trustwrapper.huggingface.explainers import AttentionExplainer

# Create attention explainer
attention_explainer = AttentionExplainer(
    model=model,
    aggregation_method="rollout",  # "mean", "max", "rollout", "flow"
    layers_to_analyze="all",  # "all", "last", [0, 1, 2]
    head_reduction="mean"  # "mean", "max", "specific"
)

# Wrap model with attention explainer
wrapped_model = wrap_hf_model(
    model,
    explainers={"attention": attention_explainer}
)

# Get attention explanations
text = "The movie was fantastic and I loved every moment of it!"
inputs = tokenizer(text, return_tensors="pt")

result = wrapped_model.explain(
    inputs,
    method="attention",
    return_token_importance=True,
    return_attention_matrix=True
)

# Visualize attention
from trustwrapper.huggingface.viz import plot_attention

plot_attention(
    tokens=tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]),
    attention_weights=result.attention_matrix,
    save_path="attention_viz.png"
)

# Get token importance
for token, importance in zip(result.tokens, result.token_importance):
    print(f"{token}: {importance:.3f}")
```

### **Gradient-based Explanations**

```python
from trustwrapper.huggingface.explainers import GradientExplainer

# Setup gradient explainer for transformers
gradient_explainer = GradientExplainer(
    model=model,
    method="integrated_gradients",  # "vanilla", "integrated_gradients", "smoothgrad"
    n_steps=50,
    internal_batch_size=8
)

# Get gradient explanations
wrapped_model = wrap_hf_model(model, explainers={"gradient": gradient_explainer})

explanation = wrapped_model.explain(
    inputs,
    method="gradient",
    target_class=1,  # Explain specific class
    return_visualization=True
)

# Token-level importance from gradients
print("Gradient-based token importance:")
for token, score in explanation.token_scores.items():
    if score > 0.1:  # Show only important tokens
        print(f"  {token}: {score:.3f}")
```

### **SHAP for Transformers**

```python
from trustwrapper.huggingface.explainers import TransformerShapExplainer

# Create SHAP explainer for transformers
shap_explainer = TransformerShapExplainer(
    model=model,
    tokenizer=tokenizer,
    max_sequence_length=128,
    n_samples=100
)

# Explain batch of texts
texts = [
    "This product exceeded my expectations!",
    "Terrible service, would not recommend.",
    "Average quality, nothing special."
]

shap_values = shap_explainer.explain_batch(texts)

# Visualize SHAP values
from trustwrapper.huggingface.viz import plot_shap_values

plot_shap_values(
    shap_values=shap_values,
    feature_names=shap_explainer.feature_names,
    class_names=["Negative", "Positive"],
    save_path="shap_explanation.png"
)
```

## 📝 Model Cards with Trust

### **Enhanced Model Cards**

```python
from trustwrapper.huggingface import TrustModelCard

# Create comprehensive model card
model_card = TrustModelCard(
    model_name="my-org/trust-bert-sentiment",
    base_model="bert-base-uncased",

    # Model details
    model_description="BERT fine-tuned for sentiment analysis with trust verification",
    training_data="IMDB movie reviews + custom trust annotations",

    # Trust information
    trust_features={
        "verification_method": "Zero-knowledge proofs (Aleo)",
        "explanation_methods": ["Attention rollout", "Integrated gradients"],
        "average_trust_score": 0.89,
        "hallucination_detection": True,
        "uncertainty_quantification": "Monte Carlo dropout"
    },

    # Performance metrics
    performance={
        "accuracy": 0.94,
        "f1_score": 0.93,
        "trust_calibration": 0.91,
        "explanation_fidelity": 0.88
    },

    # Verification badges
    badges=[
        "trust-verified",
        "explainable-ai",
        "zk-proof-enabled",
        "hallucination-tested"
    ]
)

# Add evaluation results
model_card.add_evaluation(
    dataset="test_set",
    metrics={
        "accuracy": 0.94,
        "trust_score": 0.89,
        "explanation_coverage": 0.92
    }
)

# Add usage examples
model_card.add_example(
    title="Basic Usage",
    code="""
from transformers import AutoModel, AutoTokenizer
from trustwrapper.huggingface import wrap_hf_model

model = AutoModel.from_pretrained("my-org/trust-bert-sentiment")
tokenizer = AutoTokenizer.from_pretrained("my-org/trust-bert-sentiment")

wrapped_model = wrap_hf_model(model, tokenizer)
result = wrapped_model.predict("I love this movie!")
print(f"Sentiment: {result.label}, Trust: {result.trust_score:.2f}")
"""
)

# Generate and save
model_card_content = model_card.generate()
model_card.save("./model-card.md")
model_card.push_to_hub("my-org/trust-bert-sentiment")
```

### **Trust Badges for Hub**

```python
from trustwrapper.huggingface import add_trust_badge

# Add trust verification badge to existing model
add_trust_badge(
    model_id="my-org/my-model",
    badge_type="trust-verified",  # "trust-verified", "zk-enabled", "explainable"
    verification_data={
        "verifier": "TrustWrapper v1.0.0",
        "date": "2025-06-22",
        "trust_score": 0.92,
        "blockchain_tx": "0xabc...123",
        "proof_system": "Aleo"
    }
)

# Create custom badge
from trustwrapper.huggingface import create_custom_badge

badge_url = create_custom_badge(
    text="ZK Verified",
    color="green",
    logo="shield",
    link="https://trustwrapper.ai/verify/model-hash"
)
```

## 🎯 Advanced Examples

### **Large Language Model Integration**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trustwrapper.huggingface import LLMWrapper

# Load LLM
model_name = "meta-llama/Llama-2-7b-chat-hf"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Wrap with LLM-specific features
llm_wrapper = LLMWrapper(
    model=model,
    tokenizer=tokenizer,

    # Hallucination detection
    enable_hallucination_detection=True,
    hallucination_threshold=0.3,

    # Factuality checking
    enable_fact_checking=True,
    fact_checker="internal",  # or external API

    # Response quality
    track_coherence=True,
    track_relevance=True,

    # Safety
    enable_safety_filter=True,
    toxicity_threshold=0.1
)

# Generate with trust metrics
prompt = "Explain quantum computing in simple terms:"

response = llm_wrapper.generate(
    prompt,
    max_length=200,
    temperature=0.7,
    return_trust_analysis=True
)

print(f"Response: {response.text}")
print(f"\nTrust Analysis:")
print(f"  Overall Trust: {response.trust_score:.2f}")
print(f"  Hallucination Risk: {response.hallucination_risk:.2%}")
print(f"  Factuality Score: {response.factuality:.2f}")
print(f"  Coherence: {response.coherence:.2f}")
print(f"  Safety: {'PASS' if response.safety_check else 'FAIL'}")

# Show explanations for low trust
if response.trust_score < 0.7:
    print(f"\nLow trust reasons:")
    for reason in response.trust_issues:
        print(f"  - {reason}")
```

### **Vision-Language Models**

```python
from transformers import VisionEncoderDecoderModel, ViTImageProcessor
from trustwrapper.huggingface import VLMWrapper

# Load vision-language model
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Wrap with VLM features
vlm_wrapper = VLMWrapper(
    model=model,
    image_processor=image_processor,
    tokenizer=tokenizer,

    # Trust features
    track_visual_attention=True,
    track_text_image_alignment=True,
    detect_visual_hallucinations=True
)

# Process image with trust
from PIL import Image
image = Image.open("sample_image.jpg")

result = vlm_wrapper.generate_caption(
    image,
    max_length=50,
    return_visual_explanations=True
)

print(f"Caption: {result.caption}")
print(f"Trust Score: {result.trust_score:.2f}")
print(f"Visual-Text Alignment: {result.alignment_score:.2f}")
print(f"Detected Objects: {result.detected_objects}")
print(f"Attention Regions: {result.attention_regions}")

# Visualize attention
vlm_wrapper.visualize_attention(
    image,
    result.visual_attention,
    save_path="vlm_attention.png"
)
```

### **Conversational AI**

```python
from transformers import ConversationalPipeline, Conversation
from trustwrapper.huggingface import ConversationalWrapper

# Create conversational pipeline
base_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")

# Wrap with conversation tracking
conv_wrapper = ConversationalWrapper(
    pipeline=base_pipeline,

    # Trust tracking
    track_conversation_coherence=True,
    track_context_relevance=True,
    detect_contradictions=True,

    # Memory
    enable_trust_memory=True,
    remember_user_preferences=True
)

# Start conversation
conversation = Conversation()

# Multi-turn conversation with trust
messages = [
    "Hi! I'm looking for a good Italian restaurant.",
    "What kind of atmosphere do you prefer?",
    "Can you recommend something specific?"
]

for message in messages:
    conversation.add_user_input(message)

    response = conv_wrapper(
        conversation,
        return_trust_analysis=True
    )

    print(f"\nUser: {message}")
    print(f"Bot: {response.generated_responses[-1]}")
    print(f"Trust: {response.trust_score:.2f}")
    print(f"Coherence: {response.coherence_score:.2f}")
    print(f"Context Relevance: {response.context_relevance:.2f}")

    if response.contradictions:
        print(f"⚠️ Contradictions detected: {response.contradictions}")
```

## 📋 Best Practices

### **1. Model Selection**
```python
# Choose appropriate model size for trust computation
from trustwrapper.huggingface import estimate_trust_overhead

overhead = estimate_trust_overhead(
    model_size="bert-base",  # Model size
    batch_size=32,
    sequence_length=128,
    trust_features=["explanations", "zk_proofs"]
)

print(f"Memory overhead: {overhead.memory_mb}MB")
print(f"Latency overhead: {overhead.latency_ms}ms")
print(f"Recommended GPU: {overhead.recommended_gpu}")
```

### **2. Efficient Batching**
```python
from trustwrapper.huggingface import TrustBatcher

# Efficient batching for trust computation
batcher = TrustBatcher(
    model=wrapped_model,
    optimal_batch_size=16,
    max_sequence_length=128,
    pad_to_multiple_of=8
)

# Process large dataset
texts = ["text1", "text2", ...]  # Large list
results = batcher.process_dataset(
    texts,
    show_progress=True,
    aggregate_trust_scores=True
)

print(f"Average trust: {results.aggregate_trust:.2f}")
print(f"Processing time: {results.total_time:.2f}s")
```

### **3. Caching Strategy**
```python
from trustwrapper.huggingface import TrustCache

# Enable trust computation caching
cache = TrustCache(
    cache_size=1000,
    ttl_seconds=3600,
    cache_explanations=True
)

wrapped_model.enable_cache(cache)

# Cached predictions
result1 = wrapped_model.predict("Test text")  # Computed
result2 = wrapped_model.predict("Test text")  # From cache

print(f"Cache hit rate: {cache.hit_rate:.1%}")
```

## 🔧 Troubleshooting

### **Common Issues and Solutions**

#### **1. GPU Memory Issues**
```python
# Solution: Use gradient checkpointing
from trustwrapper.huggingface import enable_memory_efficient_mode

enable_memory_efficient_mode(wrapped_model)

# Or use CPU offloading
wrapped_model.to_bettertransformer()  # If supported
wrapped_model.enable_cpu_offload()
```

#### **2. Slow Explanation Generation**
```python
# Solution: Use faster explanation methods
wrapped_model.configure(
    explanation_method="attention",  # Faster than gradients
    explanation_layers=[-1],  # Only last layer
    sample_explanations=True,  # Sample subset
    explanation_batch_size=4
)
```

#### **3. Tokenization Mismatches**
```python
# Solution: Ensure tokenizer compatibility
from trustwrapper.huggingface import check_tokenizer_compatibility

is_compatible = check_tokenizer_compatibility(model, tokenizer)
if not is_compatible:
    tokenizer = AutoTokenizer.from_pretrained(
        model.config._name_or_path,
        use_fast=True
    )
```

#### **4. Hub Integration Issues**
```python
# Debug hub uploads
from huggingface_hub import HfApi
api = HfApi()

# Check model before pushing
try:
    wrapped_model.validate_for_hub()
    wrapped_model.push_to_hub("username/model", private=True)
except Exception as e:
    print(f"Hub error: {e}")
    # Use alternative upload
    api.upload_folder(
        folder_path="./model",
        repo_id="username/model",
        repo_type="model"
    )
```

### **Debug Mode**
```python
import logging
from trustwrapper.huggingface import enable_debug_logging

# Enable detailed logging
enable_debug_logging()
logging.getLogger("trustwrapper.huggingface").setLevel(logging.DEBUG)

# Debug specific components
result = wrapped_model.predict(
    "Test input",
    debug=True,
    return_intermediates=True
)

print("Debug information:")
print(f"  Token scores: {result.debug.token_scores}")
print(f"  Layer outputs: {result.debug.layer_outputs}")
print(f"  Trust computation time: {result.debug.trust_time}ms")
```

## 📚 Additional Resources

### **Hugging Face Integration Examples**
- [BERT Classification Demo](../../demos/hf_bert_classification_demo.py)
- [GPT Text Generation Demo](../../demos/hf_gpt_generation_demo.py)
- [T5 Summarization Demo](../../demos/hf_t5_summarization_demo.py)
- [CLIP Vision-Language Demo](../../demos/hf_clip_demo.py)

### **Documentation**
- [TrustWrapper API Reference](../api/TRUSTWRAPPER_API_REFERENCE.md)
- [Hugging Face Documentation](https://huggingface.co/docs)
- [Model Hub](https://huggingface.co/models)

### **Community**
- [Hugging Face Forums](https://discuss.huggingface.co/)
- [TrustWrapper Discord](https://discord.gg/trustwrapper)
- [GitHub Issues](https://github.com/lamassu-labs/trustwrapper/issues)

---

**Next Steps**: Deploy your trusted models on [Hugging Face Spaces](https://huggingface.co/spaces) or explore our [cloud deployment guides](../deployment/) for production deployment.
