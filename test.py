import torch
from torch.utils.data import Dataset, random_split
from transformers import AutoTokenizer, AutoModelWithLMHead
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_text", default = "Convolutional Neral Networks", help='init text')
    parser.add_argument("--model_path", default = 'checkpoint/', help='path to checkpoint')
    parser.add_argument("--num_samples", default = 1, type=int, help='number of output samples')
    args = parser.parse_args()

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    tokenizer = AutoTokenizer.from_pretrained("gpt2", bos_token='<|startoftext|>', eos_token='<|endoftext|>', pad_token='<|pad|>')
    model = AutoModelWithLMHead.from_pretrained(args.model_path).to(device)
    model.resize_token_embeddings(len(tokenizer))

    generated = tokenizer("<|startoftext|> " + args.input_text, return_tensors="pt").input_ids.to(device)
    sample_outputs = model.generate(generated, do_sample=True, top_k=50, max_length=300, num_return_sequences=args.num_samples)

    for i, sample_output in enumerate(sample_outputs):
        print("{}: {}".format(i, tokenizer.decode(sample_output, skip_special_tokens=True)))
    
    tokenizer_summary = AutoTokenizer.from_pretrained("t5-small")
    model_summary = AutoModelWithLMHead.from_pretrained("t5-small")

    inputs = tokenizer_summary.encode("summarize: " + tokenizer.decode(sample_output, skip_special_tokens=True), return_tensors="pt")
    outputs = model_summary.generate(inputs, max_length=100, do_sample = False)

    output_text = tokenizer_summary.decode(outputs[0], skip_special_tokens=True)
    print(output_text)
