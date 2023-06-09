FROM linuxserver/code-server:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-virtualenv python-is-python3  curl wget git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
    
RUN pip install --upgrade pip && pip install poetry aiofauna pipenv

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

COPY ./setup.sh /config/workspace/setup.sh

# docker run -d -p 8080:8080 -v data:/app python-dev
# docker run -d -p 8000:8443 -v data:/config/workspace code-server
