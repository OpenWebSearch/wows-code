FROM ubuntu:noble

RUN apt-get update \
	&& apt-get install -y curl python3 python3-pip git

RUN pip3 install git+https://github.com/tira-io/tira.git@pyterrier-artifacts#egg=tira&subdirectory=python-client