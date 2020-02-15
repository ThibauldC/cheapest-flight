FROM python:3.8-slim

RUN pip install pipenv

COPY . .

EXPOSE 8501

RUN pipenv install --system --deploy --ignore-pipfile

RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD ["run-app"]