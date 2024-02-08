FROM python:3.10-slim
MAINTAINER Gilwell Muhati <gilwellm@gmail.com>

ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT

# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system # wrong→ same. -- system

COPY . .
CMD python manage.py runserver 0.0.0.0:8000