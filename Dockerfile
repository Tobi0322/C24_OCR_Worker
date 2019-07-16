#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------
FROM ubuntu:latest

# Install git, process tools
RUN apt-get update

# Install tesseract
RUN apt-get -y install tesseract-ocr && \
    apt-get -y install tesseract-ocr-deu
    
# Install poppler
RUN apt-get -y install poppler-utils 

RUN apt-get -y install python3-pip 
    
RUN apt-get install -y libsm6 libxext6 libxrender-dev

RUN apt-get -y install libmysqlclient-dev python-dev

RUN mkdir /workspace
WORKDIR /workspace

ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8
RUN apt-get install locales
RUN echo "de_DE.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["main.py"]
