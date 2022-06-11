FROM python:3.8.11-buster


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/venv/bin:$PATH"

COPY requirements/requirements.txt requirements/


RUN python -m pip install pip wheel --upgrade \
 && python -m pip install -r requirements/requirements.txt --no-cache-dir

WORKDIR /app

COPY . .

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
