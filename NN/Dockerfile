FROM python:3.8-slim

WORKDIR /workdir
COPY . ./

ENV FLASK_APP=webapp
ENV FLASK_ENV=development

RUN pip install -r requirements.txt && \
    apt update && \
    apt install ffmpeg libsm6 libxext6  -y && \
    apt clean && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
