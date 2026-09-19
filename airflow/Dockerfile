FROM apache/airflow:3.3.2

USER airflow

COPY airflow/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt

ENV PYTHONPATH=/opt/airflow/project
