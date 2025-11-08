FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.3 /uv /uvx /bin/
ENV PATH="/uv:/uvx:/root/.local/bin:$PATH"
ADD . /authenticator
WORKDIR /authenticator
RUN uv sync --locked
ENV PATH="/authenticator/.venv/bin:$PATH"
# CMD ["tail", "-f", "/dev/null"]
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]