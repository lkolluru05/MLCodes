# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

access_token = "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"
quantization_config = BitsAndBytesConfig(load_in_8bit=True)

tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b", token=access_token)
model = AutoModelForCausalLM.from_pretrained("google/gemma-7b",quantization_config=quantization_config, token=access_token)

input_text = "Tell me something about universe"
input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")

outputs = model.generate(**input_ids, max_length= 5000)
for i in range(len(outputs)):
    print(tokenizer.decode(outputs[i]))