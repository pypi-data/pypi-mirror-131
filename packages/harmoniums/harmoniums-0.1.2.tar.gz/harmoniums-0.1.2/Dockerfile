FROM ubuntu:21.10
ARG DEBIAN_FRONTEND=noninteractive
ARG PIP_IGNORE_INSTALLED=0

# Install binary packages so that not all pip packages have to be rebuilt.
RUN apt update -qq && \
        apt install -y -qq \
        python3-pip \
        python3-dev \
        python3-setuptools \
        python3-wheel \
        python3-numpy \
        python3-scipy \
        python3-pandas \
        python3-sklearn \
        python3-mypy \
        python3-seaborn \
        python3-cvxopt \
        python3-joblib

# Instal libraries for compiling from source.
RUN apt update -qq && \
        apt install -y -qq \
        libblas3 \
        liblapack3 \
        liblapack-dev \
        libblas-dev \
        gfortran \
        libatlas-base-dev \
        cmake \
        g++
# Install pip packages.
RUN mkdir /model
RUN mkdir /model/output
WORKDIR /model
COPY requirements.txt .
RUN pip3 install --prefer-binary -r requirements.txt
RUN ldconfig
COPY . /model/

ENTRYPOINT [ "/bin/bash", "-c" ]
