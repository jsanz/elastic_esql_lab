FROM quay.io/jupyter/base-notebook

RUN pip install -qU elasticsearch overturemaps pandas geopandas matplotlib

WORKDIR /lab

CMD start-notebook.py --NotebookApp.token='elastic'
