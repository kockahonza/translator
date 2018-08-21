FROM bitspeech/tensor2tensor:1.6.6

RUN apt-get update -y && \
    apt-get install -y python-pip gunicorn
RUN pip install flask flask-cors

COPY app /app
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["gunicorn", "-b 0.0.0.0:8000", "webserver:app"]
