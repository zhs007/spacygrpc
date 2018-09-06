FROM continuumio/anaconda3

MAINTAINER zerro "zerrozhao@gmail.com"

RUN pip install --upgrade pip \
    && conda install -c conda-forge spacy -y \
    && python -m spacy download en \
    && pip install grpcio-tools \
    && pip install googleapis-common-protos \
    && pip install grpcio \
    && pip install protobuf 

COPY ./src /home/spacygrpc

WORKDIR /home/spacygrpc

CMD ["python", "server.py"]