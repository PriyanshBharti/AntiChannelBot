FROM python:3.9

RUN apt update && apt upgrade -y
RUN apt install python3-pip -y

RUN mkdir /megumin/
COPY . /megumin
WORKDIR /megumin

RUN pip3 install --upgrade pip
RUN pip3 install poetry

CMD python3 -m main.py


