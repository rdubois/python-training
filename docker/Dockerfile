FROM python:3.10-slim-bullseye AS builder

WORKDIR /repo

# Don't write cython files
ENV PYTHONDONTWRITEBYTECODE=1
# Take Python and Pip from the venv
ENV PATH="/venv/bin:$PATH"

# Install build-essential before dependencies, see https://stackoverflow.com/a/60340115/2121777
RUN apt-get -y update && \
    apt-get -y --no-install-recommends \
    install build-essential libffi-dev

RUN pip install --upgrade pip

RUN python3 -m venv /venv

# Install dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

# Now we use the image created above and copy our virtual environment into it
# See multistage docker builds for more info https://docs.docker.com/develop/develop-images/multistage-build/
FROM python:3.10-slim-bullseye AS app

ARG API_VERSION
ARG DEPLOYMENT_ENV

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/venv/bin:$PATH"

RUN apt-get -y update && \
    apt-get -y --no-install-recommends \
    install build-essential libffi-dev

# Copy our python environment, the app and new relic config file.
COPY --from=builder /venv /venv
COPY ./src/ /repo/src/

# Set permissions for a non-root user
RUN groupadd -r john && useradd -d /repo -r -g john john \
    && chown john:john -R /repo

USER john

WORKDIR /repo

EXPOSE 8000
CMD ["uvicorn", "--port", "8000", "--host", "0.0.0.0", "--proxy-headers", "src.package.app:app" ]