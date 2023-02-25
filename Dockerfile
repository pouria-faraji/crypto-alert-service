ARG PYTHON_VERSION=3.8.5-slim

#ARG PYTHON_VERSION=3.10.0rc1-slim
FROM python:${PYTHON_VERSION} as runner-image


ARG POETRY_VERSION=1.1.6
# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # poetry https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_HOME="/.poetry" \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_CACHE_DIR="~/.poetry_cache" \
    POETRY_VIRTUALENVS_IN_PROJECT=true

# make poetry available
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for installing poetry
    curl \
    git \
    nano \
    ssh \
    wget \
    # dependencies for building python dependencies
    build-essential \
    && rm -rf /var/lib/apt/lists/*
    

# RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

RUN curl -sSL https://install.python-poetry.org | python3 -

# container env
#FROM runner-image as container-env
    
RUN /usr/local/bin/python -m pip install --upgrade pip


FROM runner-image as test-image
WORKDIR /usr/src/app

COPY pyproject.toml .
COPY poetry.lock .
COPY . .
RUN poetry install

FROM test-image as main-image
CMD ["poetry", "run", "python", "alert/main.py"]