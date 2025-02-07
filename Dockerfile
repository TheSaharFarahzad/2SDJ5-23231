FROM python:3.12-slim

WORKDIR /code

COPY requirements /code/requirements

RUN pip install --no-cache-dir -r /code/requirements/local.txt

COPY . /code

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
