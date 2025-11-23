# the repo already contains everything pre-installed. In case you want to modify something, you can still do this below
# The base image is build from https://github.com/OpenWebSearch/wows-code/blob/main/ecir26/template-new-approach/Dockerfile.dev
FROM ghcr.io/openwebsearch/wows-code/ecir-2026-pyterrier:latest

ADD requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt
