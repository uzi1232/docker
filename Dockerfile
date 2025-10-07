FROM python:3.12-alpine
COPY *.py /tmp
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=8081
ENV CONFIG_PATH=/etc/config

EXPOSE 8081
ENTRYPOINT python3 /tmp/server.py -H 0.0.0.0 -p 8081 