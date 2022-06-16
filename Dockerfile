FROM python:3.8-alpine
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /src
COPY app.py /src/app.py
CMD ["python", "app.py"]
