# GPT2-arXiv style text

This project generates arXiv abstract style text and its summary using finetuned GPT-2 model.

Training was done by fine-tuning gpt2 with arXiv dataset. 

For training and preprocessing, check the ./train folder 

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/jays0606/gpt2-arXiv)

![image](./demo.gif)

model: [Google Drive](https://drive.google.com/file/d/1CYVs3ZjePZAfFCsVt-fEIqiCj6UTi7uU/view?usp=sharing)

dataset: [Kaggle arXiv](https://www.kaggle.com/Cornell-University/arxiv)

## Model Info 
    Base model: gpt2-small 

    Finetuned model: 

    Summary base model: T5-small

## Docker
    docker build -t arxiv . (build image)

    docker run -p 80:80 --name arxiv -d arxiv (run container)

    docker logs -f arxiv (Check logs)
    
    docker stop arxiv (Stop Container)

    docker rm -f arxiv (Remove container)
    
    ------------------------------------------------------------
    
    Download might take a while. Once completed, server is 
    available at http://localhost, or http://0.0.0.0

## How to use  [Demo](https://master-gpt2-ar-xiv-jays0606.endpoint.ainize.ai/)

    First, Fill text in "text". This will be the base of your abstract. 

    Choose the length of your text. 

    Submit! 
 
## API page   [Ainize](https://ainize.ai/jays0606/gpt2-arXiv?branch=master)

    Curl Input: 

        curl -X POST "https://master-gpt2-ar-xiv-jays0606.endpoint.ainize.ai/GPT2-arXiv/" -H "accpet: application/json" -H "Content-Type: multipart/form-data" - F "text=CNNs" -F "length=200"
    
    output format: {"abstract": generated_text, "summary: "summary}

    
### References

    https://github.com/fpem123/GPT2-marketing-man
    
    https://www.kaggle.com/officialshivanandroy/transformers-generating-titles-from-abstracts
    
    https://medium.com/geekculture/fine-tune-eleutherai-gpt-neo-to-generate-netflix-movie-descriptions-in-only-47-lines-of-code-40c9b4c32475
    
    

  

  


