FROM python:3.7.3-slim-stretch

# Copy local code to the container image.
WORKDIR /
COPY checkpoint /checkpoint

# Install production dependencies.
RUN pip3 install --upgrade pip && pip3 install tensorflow-cpu==1.15 gpt_2_simple uvicorn fastapi

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
# ENV PORT 8080

COPY main.py /

ENV GRACEFUL_TIMEOUT 250
ENV TIMEOUT 250 
ARG ARGRUN
ENV ENVRUN=$ARGRUN

ENTRYPOINT ["python3", "-X", "utf8", "main.py"]