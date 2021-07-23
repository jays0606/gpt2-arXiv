from transformers import AutoTokenizer, AutoModelWithLMHead
import torch 

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
model = AutoModelWithLMHead.from_pretrained("gpt2-medium")

model = model.to(device)

input_text = "We propose an alternative generator architecture for generative adversarial networks,"
input_ids = tokenizer.encode(input_text, return_tensors = 'pt').to(device)

sample_outputs = model.generate(input_ids, max_length=len(input_text)+200, do_sample=True, top_k=50)[0].tolist()
output_text = tokenizer.decode(sample_outputs, skip_special_tokens=True)
print(output_text)

