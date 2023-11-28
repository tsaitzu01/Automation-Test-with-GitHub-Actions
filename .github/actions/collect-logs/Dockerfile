FROM ubuntu:latest

# Install required tools
RUN apt-get update && \
    apt-get install -y python3-allure && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
