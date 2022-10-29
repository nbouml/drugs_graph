#FROM $cloud/$image
FROM python:3.9-buster
#FROM puckel/docker-airflow

COPY requirements.txt .
COPY main_drugs_graph.py .
COPY ./drugs_graph /drugs_graph
COPY ./data /data

RUN pip install pip -U && pip install -r requirements.txt
RUN chmod -R u+rwx /drugs_graph/
RUN chmod u+rwx main_drugs_graph.py
RUN python main_drugs_graph.py

CMD ["cat", "/data/results/graph.json"]
