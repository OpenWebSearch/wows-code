#docker build -t webis/wows-2024-baseline:0.0.5 .
FROM pytorch/pytorch:latest

ENV PYTERRIER_VERSION='5.8'
ENV PYTERRIER_HELPER_VERSION='0.0.8'

RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y git openjdk-11-jre wget \
	&& rm -rf /root/.cache

RUN apt-get install -y gcc \
	&& pip3 install tira ir_datasets python-terrier \
	&& rm -rf /root/.cache

