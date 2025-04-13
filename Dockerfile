FROM python:3.11.12-slim-bookworm
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry==1.3.2
RUN poetry install && poetry cache clear --all -n pypi
COPY . /app
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]
