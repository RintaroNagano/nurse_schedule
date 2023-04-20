FROM --platform=linux/amd64 jupyter/scipy-notebook:latest

EXPOSE 8888
RUN pip install pulp

