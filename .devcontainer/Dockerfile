# Use Python 3.12-slim (Debian-based image for better package compatibility)
FROM python:3.12.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies, including Node.js, npm, and build tools
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    build-essential \
    gfortran \
    cmake \
    libopenblas-dev \
    libc6-dev \
    libssl-dev \
    git \
    libffi-dev \
    make \
    nodejs \
    npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Install pip wheel to ensure packages are built faster with wheels
RUN pip install --upgrade pip wheel

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock (if available) for dependency installation
COPY pyproject.toml poetry.lock* /app/

# Copy the rest of your project files
COPY . /app

RUN poetry config virtualenvs.create false

# Install project dependencies using Poetry
RUN poetry install

# Verify installations (optional)
RUN curl --version && gcc --version && git --version && node --version && npm --version && poetry --version && python -c 'import blockhead'
