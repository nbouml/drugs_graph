FROM openjdk:8-jre
#FROM apache/airflow:2.2.3

# Set environmental variables
ENV AIRFLOW_HOME=/home/user/airflow

#Copy requirements
COPY packages.txt python_requirements.txt /

#Installing packages
RUN chmod +x /packages.txt && \
    apt-get -y update && \
    xargs -a /packages.txt apt-get -y install && \
    rm /packages.txt

# Install Python requirements
RUN pip3 install -r /python_requirements.txt && \
    rm /python_requirements.txt


# Copy configuration files
COPY config/airflow.cfg $AIRFLOW_HOME/
COPY config/supervisord.conf /home/user/supervisor/conf.d/supervisord.conf
RUN mkdir /home/user/supervisor/logs


COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

WORKDIR $AIRFLOW_HOME

RUN airflow users create --role Admin --username admin/ \
    --password admin --email admin@example.com --firstname foo --lastname bar

EXPOSE 8080 9001
ENTRYPOINT [ "/entrypoint.sh" ]

CMD ["/usr/bin/supervisord","-c","/home/user/supervisor/conf.d/supervisord.conf"]
