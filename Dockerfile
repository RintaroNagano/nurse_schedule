# docker run --rm -v /Users/rintaro/workspace/nurse_schedule/:/home/jovyan/work/nurse_schedule -p 8888:8888 --name isp -it isp:1.0 bash
# jupyter notebook
FROM --platform=linux/amd64 jupyter/scipy-notebook:latest

EXPOSE 8888
RUN pip install pulp

