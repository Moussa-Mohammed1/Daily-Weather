FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY dashboard/requirements.txt /tmp/requirements.txt
RUN pip install --requirement /tmp/requirements.txt

COPY dashboard/app.py /app/dashboard/app.py
COPY data /app/data

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
