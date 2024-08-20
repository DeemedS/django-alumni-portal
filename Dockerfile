FROM python:3.11-slim

WORKDIR /app

COPY . /app/


RUN python3 -m venv /opt/venv

COPY requirements.txt .

RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    chmod +x entrypoint.sh 


CMD [ "/app/entrypoint.sh" ]