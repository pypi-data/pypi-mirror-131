FROM public.ecr.aws/amazonlinux/amazonlinux:latest

RUN yum -y update
RUN yum -y install yum-utils
RUN yum -y groupinstall development

RUN yum list python3*
RUN yum -y install python3 python3-dev python3-pip python3-virtualenv

RUN mkdir /app
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install poetry venv-pack jupyter
RUN yum install -y which

WORKDIR /app
ENV PATH=/root/.local/bin:$PATH

COPY spark_submit.sh /spark_submit.sh
COPY run_pyspark.sh /run_pyspark.sh
COPY run_notebook.sh /run_notebook.sh
COPY run_python.sh /run_python.sh
COPY build.sh /build.sh

RUN amazon-linux-extras install -y java-openjdk11
RUN pip install pyspark findspark

ENV POETRY_VIRTUALENVS_PATH=./.docker_venv