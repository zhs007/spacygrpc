FROM continuumio/anaconda3

MAINTAINER zerro "zerrozhao@gmail.com"

RUN conda install -c conda-forge spacy -y \
    && python -m spacy download en

COPY ./src /home/spacygrpc

WORKDIR /home/spacygrpc

CMD ["python", "main.py"]