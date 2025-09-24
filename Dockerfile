FROM python:3.12-alpine
COPY server.py /tmp
EXPOSE 8080
ENTRYPOINT python3 /tmp/server.py