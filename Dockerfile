FROM python:3 as base

ARG ENVIRONMENT=prod

ENV UNAME=andrii
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
ENV PATH="/home/$UNAME/.local/bin:${PATH}"

RUN apt-get update

ENV WORKDIR=/usr/src/app
ENV APP_HOME=/app
USER $UNAME
CMD /bin/bash

ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip

## gateway image for production / dev
FROM base as gateway

WORKDIR $WORKDIR
COPY apps/fithm-gateway/requirements.txt .
COPY apps/fithm-gateway/requirements_dev.txt .

USER root
COPY apps/fithm-gateway/start.sh /usr/bin/
RUN chmod +x /usr/bin/start.sh

USER $UNAME
RUN pip install -r requirements.txt
RUN if [ "x$ENVIRONMENT" = "xprod" ] ; \
    then echo "Production build, no dev dependencies" && pip install -r requirements.txt ; \
    else echo "Dev build" && pip install -r requirements_dev.txt ; \
    fi

WORKDIR $APP_HOME

## tradeshop image for production / dev
FROM base as tradeshop

WORKDIR $WORKDIR
COPY apps/fithm-service/requirements.txt .
COPY apps/fithm-service/requirements_dev.txt .

RUN pip install -r requirements.txt
RUN if [ "x$ENVIRONMENT" = "xprod" ] ; \
    then echo "Production build, no dev dependencies" && pip install -r requirements.txt ; \
    else echo "Dev build" && pip install -r requirements_dev.txt ; \
    fi

WORKDIR $APP_HOME
