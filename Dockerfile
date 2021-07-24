FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y apt-utils wget

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p /app
WORKDIR /app
COPY . .

# https://drive.google.com/file/d/1HIHIXIVdj1SZGgW8PFXxqqL-Pt0FMZa3/view?usp=sharing

RUN curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=1HIHIXIVdj1SZGgW8PFXxqqL-Pt0FMZa3" > /dev/null
RUN curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=1HIHIXIVdj1SZGgW8PFXxqqL-Pt0FMZa3" -o ckpt.tar.gz
RUN tar -xvf ckpt.tar.gz
RUN mv checkpoint-80000 checkpoint
RUN rm ckpt.tar.gz
RUN rm cookie 

EXPOSE 80

CMD ["python3", "app.py"]
