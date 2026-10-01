FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update \
    && apt-get install --yes --no-install-recommends default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /lab
COPY requirements.txt lab.py ./
COPY data ./data

CMD ["uv", "run", "--with-requirements", "requirements.txt", "python", "lab.py"]
