import torch
torch.cuda.is_available()
from transformers import AutoTokenizer
from transformers import AutoConfig, AutoModelForCausalLM
import transformers

from torch import cuda, bfloat16
from transformers import BitsAndBytesConfig

bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

access_token = "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"
model = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model, token=access_token)

model = AutoModelForCausalLM.from_pretrained(
    model,
    token=access_token,
    quantization_config=bnb_config
)

model.config.use_cache = False
model.config.pretraining_tp = 1

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
    tokenizer=tokenizer
)
sequences = pipeline(
    'Hi! Tell me about yourself!',
    do_sample=True,
)
print(sequences[0].get("generated_text"))