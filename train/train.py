import torch
from torch.utils.data import Dataset, random_split
from transformers import AutoTokenizer, TrainingArguments, Trainer, AutoModelWithLMHead
import pandas as pd

class arXivDataset(Dataset):
    def __init__(self, txt_list, tokenizer, max_length):
        self.input_ids = []
        self.attn_masks = []
        self.labels = []
        for txt in txt_list:
            encodings_dict = tokenizer('<|startoftext|>' + txt + '<|endoftext|>', truncation=True,
                                       max_length=300, padding="max_length")
            self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.attn_masks[idx]


torch.manual_seed(42)
tokenizer = AutoTokenizer.from_pretrained("gpt2", bos_token='<|startoftext|>',
                                          eos_token='<|endoftext|>', pad_token='<|pad|>')
model = AutoModelWithLMHead.from_pretrained("gpt2").cuda()
model.resize_token_embeddings(len(tokenizer))

with open('arXiv.txt', 'r') as f:
    abstract_lst = f.read().splitlines()

abstracts = pd.Series(abstract_lst)

dataset = arXivDataset(abstracts, tokenizer, max_length=300)
train_size = int(0.9 * len(dataset))
train_dataset, val_dataset = random_split(dataset, [train_size, len(dataset) - train_size])

training_args = TrainingArguments(output_dir='./results', num_train_epochs=10, logging_steps=10000, save_steps=10000,
                                  per_device_train_batch_size=8, per_device_eval_batch_size=8,
                                  warmup_steps=100, weight_decay=0.01, logging_dir='./logs')

trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset,
        eval_dataset=val_dataset, data_collator=lambda data: {'input_ids': torch.stack([f[0] for f in data]),
                                                              'attention_mask': torch.stack([f[1] for f in data]),
                                                              'labels': torch.stack([f[0] for f in data])})

print("Train initiated")
trainer.train()



