FROM python:3.10

WORKDIR /gpa_service

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn pydantic

EXPOSE 8000

CMD ["uvicorn", "main:gpa_service", "--host", "0.0.0.0", "--port", "8000"]