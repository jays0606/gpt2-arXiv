# GPT2-arXiv style text

This project generates arXiv abstract style text and its summary using finetuned GPT-2 model.

For training and preprocessing, check the ./train folder 

![image](./demo.gif)

model: [Google Drive](https://drive.google.com/file/d/1HIHIXIVdj1SZGgW8PFXxqqL-Pt0FMZa3/view?usp=sharing)
dataset: [Kaggle arXiv](https://www.kaggle.com/Cornell-University/arxiv)

## Docker
    docker build -t arxiv . (build image)

    docker run -p 80:80 --name arxiv -d arxiv (build container)

    docker logs -f arxiv (To check progress)

    docker rm -f arxiv (To end)
    
    ------------------------------------------------------------
    
    Download might take a while. Once completed, server is 
    available at http://localhost, or http://0.0.0.0
    
    If container dies instantly, you might want to devote 
    more RAM to docker in docker -> preferences -> advanced

## how to use
    First, Fill text in "text". This will be the base of your abstract. 

    Choose the length of your text. 
    
    Complete!

#### /GPT2-arXiv/

    text: The base text to generate arXiv abstract style text. 
    
    length: Size of text.
    
    output format: [generated_text, summary]

    
### References

    https://github.com/fpem123/GPT2-marketing-man
    
    https://www.kaggle.com/officialshivanandroy/transformers-generating-titles-from-abstracts
    
    https://medium.com/geekculture/fine-tune-eleutherai-gpt-neo-to-generate-netflix-movie-descriptions-in-only-47-lines-of-code-40c9b4c32475
    
    

  

  


