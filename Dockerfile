FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.3 /uv /uvx /bin/
ENV PATH="/uv:/uvx:/root/.local/bin:$PATH"
ADD . /authenticator
WORKDIR /authenticator
CMD ["tail", "-f", "/dev/null"]