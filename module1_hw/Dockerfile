FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
RUN pip install pandas pyarrow 

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked
COPY hw_ingest_data.py .

ENTRYPOINT ["python", "hw_ingest_data.py"]