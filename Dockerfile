FROM $cloud/$image

COPY ../drugs_graph/requirements.txt .
COPY . /drugs_graph
# RUN apt install vim -y
RUN pip install pip -U
RUN pip install /drugs_graph/.
RUN chmod -R 777 /drugs_graph/

RUN useradd -ms /bin/bash nboumlaik
USER nboumlaik

WORKDIR /home/nboumlaik
