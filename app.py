# External module.
from transformers import AutoModelWithLMHead, AutoTokenizer, top_k_top_p_filtering, pipeline
from flask import Flask, request, Response, jsonify, render_template
import torch
from torch.nn import functional as F

# Internal module.
from queue import Queue, Empty
import threading
import time

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
model = AutoModelWithLMHead.from_pretrained("gpt2-medium")
summarizer = pipeline("summarization")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   # gpu check.
model.to(device)

requests_queue = Queue()    # request queue.
BATCH_SIZE = 1              # max request size.
CHECK_INTERVAL = 0.1

##
# Request handler.
# GPU app can process only one request in one time.
def handle_requests_by_batch():
    while True:
        request_batch = []

        while not (len(request_batch) >= BATCH_SIZE):
            try:
                request_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in request_batch:
                requests["output"] = run_long(requests['input'][0], requests['input'][1]) # text, length 

handler = threading.Thread(target=handle_requests_by_batch).start()

##
# generate gpt2-arXiv text of length 'length'
def run_long(text, length):
    try:

        if length > 200:
            length = 200 # Occasional error
        input_ids = tokenizer.encode(text, return_tensors = 'pt').to(device)

        output_ids = model.generate(input_ids, max_length=len(text)+length, do_sample=True, top_k=50)
        output_ids = output_ids[0].tolist()
        
        output_text = tokenizer.decode(output_ids, skip_special_tokens=True)
        output_summary = summarizer(output_text, max_length=50, do_sample=False)
        
        return [output_text, output_summary[0]['summary_text']]

    except Exception as e:
        print('Error occur in long generating!', e)
        return jsonify({'error': e}), 500


##
# Get post request page.
@app.route('/GPT2-arXiv/', methods=['POST'])
def generate():

    # GPU app can process only one request in one time.
    if requests_queue.qsize() > BATCH_SIZE:
        return jsonify({'Error': 'Too Many Requests'}), 429

    try:
        args = []

        text = request.form['text']
        length = int(request.form['length'])

        args.append(text)
        args.append(length)

    except Exception as e:
        return jsonify({'message': 'Invalid request'}), 500

    # input a request on queue
    req = {'input': args}
    requests_queue.put(req)

    # wait
    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    return jsonify(req['output'])


##
# Queue deadlock error debug page.
@app.route('/queue_clear')
def queue_clear():
    with requests_queue.mutex:
        requests_queue.queue.clear()

    return "Clear", 200


##
# Sever health checking page.
@app.route('/healthz', methods=["GET"])
def health_check():
    return "Health", 200


##
# Main page.
@app.route('/')
def main():
    return render_template('main.html'), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
