# the repo already contains everything pre-installed. In case you want to modify something, you can still do this below
# The base image is build from https://github.com/OpenWebSearch/wows-code/blob/main/ecir26/template-new-approach/Dockerfile.dev
FROM ghcr.io/openwebsearch/wows-code/ecir-2026-pyterrier:latest

RUN apt-get update \
	&& apt-get install -y git openjdk-11-jdk python3 python3-pip

ADD requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

RUN python3 -c 'from tira.third_party_integrations import ensure_pyterrier_is_loaded; ensure_pyterrier_is_loaded(patch_ir_datasets=True, is_offline=False)'

ADD index.py /index.py

