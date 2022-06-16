FROM python:3.8-alpine
#FROM alpine:3.16

ENV DOCKER_VERSION 20.10.9
ENV DOCKER_URL https://download.docker.com/linux/static/stable/x86_64/docker-$DOCKER_VERSION.tgz
ENV DOCKER_COMPOSE_URL https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-linux-x86_64

RUN apk add --no-cache \
		ca-certificates \
		libc6-compat \
		openssh-client

RUN set -eux; \
	   wget -O docker.tgz "$DOCKER_URL" \
    && tar --extract \
		--file docker.tgz \
		--strip-components 1 \
		--directory /usr/local/bin/ \
    && wget -O /usr/bin/docker-compose "$DOCKER_COMPOSE_URL" \
    && chmod +x /usr/bin/docker-compose \
	&& rm docker.tgz \
	&& dockerd --version \
	&& docker --version \
    && docker-compose --version

COPY modprobe.sh /usr/local/bin/modprobe
COPY docker-entrypoint.sh /usr/local/bin/

ENV DOCKER_TLS_CERTDIR=/certs
RUN mkdir -p /certs /certs/client /src/stacks \
    && chmod 1777 /certs /certs/client \
    && chmod +x /usr/local/bin/docker-entrypoint.sh /usr/local/bin/modprobe

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY app.py /src/app.py

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "/src/app.py"]


