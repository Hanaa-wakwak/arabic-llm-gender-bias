# Extra Model Compatibility Notes

During the enrichment phase, `aubmindlab/aragpt2-large` was tested as an additional Arabic-specific model.

However, the model requires custom Hugging Face code through `trust_remote_code=True`.

When loading the model, the custom configuration file attempted to import:

```python
from transformers.onnx import OnnxConfigWithPast, PatchingSpec