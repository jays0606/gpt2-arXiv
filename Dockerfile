FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y apt-utils wget && \
    apt-get -qq -y install curl && \
    apt-get install -y tar

RUN mkdir -p /app
WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# https://drive.google.com/file/d/1CYVs3ZjePZAfFCsVt-fEIqiCj6UTi7uU/view?usp=sharing
RUN curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=1CYVs3ZjePZAfFCsVt-fEIqiCj6UTi7uU" > /dev/null
RUN curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=1CYVs3ZjePZAfFCsVt-fEIqiCj6UTi7uU" -o ckpt.tar.gz
RUN tar -xvf ckpt.tar.gz
RUN rm ckpt.tar.gz
RUN rm cookie 

EXPOSE 80

CMD ["python3", "app.py"]

