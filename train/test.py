import torch
from torch.utils.data import Dataset, random_split
from transformers import AutoTokenizer, TrainingArguments, Trainer, AutoModelWithLMHead

generated = tokenizer("<|startoftext|> ", return_tensors="pt").input_ids.cuda()
sample_outputs = model.generate(generated, do_sample=True, top_k=50, 
                                max_length=300, top_p=0.95, temperature=1.9, num_return_sequences=10)

for i, sample_output in enumerate(sample_outputs):
    print("{}: {}".format(i, tokenizer.decode(sample_output, skip_special_tokens=True)))