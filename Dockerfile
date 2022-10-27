#FROM $cloud/$image
FROM python:3.9-buster

COPY requirements.txt .
COPY . /drugs_graph
# RUN apt install vim -y
RUN pip install pip -U
RUN pip install /drugs_graph/.
RUN chmod -R 777 /drugs_graph/

RUN useradd -ms /bin/bash nboumlaik
USER nboumlaik

#WORKDIR /home/nboumlaik
WORKDIR /drugs_graph
RUN python drugs_graph/main_drugs_graph.py
