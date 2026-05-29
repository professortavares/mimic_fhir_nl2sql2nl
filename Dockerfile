FROM jupyter/base-notebook:python-3.11

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /home/jovyan/work

# Copia o código fonte e o adiciona ao PYTHONPATH
COPY src /home/jovyan/work/src
ENV PYTHONPATH=/home/jovyan/work/src:$PYTHONPATH

EXPOSE 8888
