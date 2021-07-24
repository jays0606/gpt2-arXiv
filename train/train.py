import torch
from torch.utils.data import Dataset, random_split
from transformers import AutoTokenizer, TrainingArguments, Trainer, AutoModelWithLMHead
import pandas as pd
from argparse import ArgumentParser

class arXivDataset(Dataset):
    def __init__(self, txt_list, tokenizer, max_length):
        self.input_ids = []
        self.attn_masks = []
        self.labels = []
        for txt in txt_list:
            encodings_dict = tokenizer('<|startoftext|>' + txt + '<|endoftext|>', truncation=True,
                                       max_length=max_length, padding="max_length")
            self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.attn_masks[idx]


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--model_path", default = 'results/checkpoint-80000/', help='path of checkpoint')
    parser.add_argument("--data_path", default = 'arXiv.txt', help='path of data')
    parser.add_argument("--ckpt_dir", default = './results', help='path to save ckpt')
    parser.add_argument("--log_dir", default = './logs', help='path to save log')

    parser.add_argument("--train_epochs", default = 10, type=int)
    parser.add_argument("--logging_steps", default = 10000, type=int)
    parser.add_argument("--save_steps", default = 10000, type=int)
    parser.add_argument("--batch_size", default = 12, type=int)
    parser.add_argument("--decay", default = 0.01, type=float)
    parser.add_argument("--max_length", default = 300, type=int)
    
    args = parser.parse_args()

    torch.manual_seed(42)
    tokenizer = AutoTokenizer.from_pretrained("gpt2", bos_token='<|startoftext|>', eos_token='<|endoftext|>', pad_token='<|pad|>')

    if args.model_path:
        model = AutoModelWithLMHead.from_pretrained(args.model_path).cuda()
    else:
        model = AutoModelWithLMHead.from_pretrained("gpt2").cuda()

    model.resize_token_embeddings(len(tokenizer))

    with open(args.data_path, 'r') as f:
        abstract_lst = f.read().splitlines()

    abstracts = pd.Series(abstract_lst)
    dataset = arXivDataset(abstracts, tokenizer, max_length=args.max_length)
    train_size = int(0.9 * len(dataset))
    train_dataset, val_dataset = random_split(dataset, [train_size, len(dataset) - train_size])

    training_args = TrainingArguments(output_dir=args.ckpt_dir, num_train_epochs=args.train_epochs, logging_steps=args.logging_steps, 
                                    save_steps=args.save_steps, per_device_train_batch_size=args.batch_size, 
                                    per_device_eval_batch_size=args.batch_size, weight_decay=args.decay, logging_dir=args.log_dir)

    trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset,
            eval_dataset=val_dataset, data_collator=lambda data: {'input_ids': torch.stack([f[0] for f in data]),
                                                                'attention_mask': torch.stack([f[1] for f in data]),
                                                                'labels': torch.stack([f[0] for f in data])})

    trainer.train()



