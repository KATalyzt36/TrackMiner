# Lightweight base OS
FROM python:3.11-alpine

# Optional (Obviously)
LABEL authors="KATalyzt"

# Environment Var to avoid an error
ENV TERM=xterm

# Install FFMPEG in Alpine
RUN apk update && \
    apk add --no-cache ffmpeg

WORKDIR /app

# Copy project to Docker
COPY . /app

# Install dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
