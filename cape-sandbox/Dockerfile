FROM python:3.12-alpine

ENV CONNECTOR_TYPE=INTERNAL_ENRICHMENT

# Set workdir
WORKDIR /opt/opencti-connector-cape-sandbox
COPY src/requirements.txt .

# Install build deps
RUN apk --no-cache add git build-base libmagic libffi-dev
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apk del git build-base

# Copy the rest of the source code
COPY src/ .

# Entry point
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
