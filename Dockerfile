FROM python:3.6
ADD . /app
RUN apt-get update && apt-get install
RUN cd /app && pip install -r requirements.txt
WORKDIR /app
EXPOSE 8000
CMD exec scripts/run-docker.sh
