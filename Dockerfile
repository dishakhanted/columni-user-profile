FROM python:3.10

WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV PSQL_DATABASE columni_userdb
ENV PSQL_USER postgres 
ENV PSQL_HOST columni-user-db.cnuwaz8dqxjy.us-east-1.rds.amazonaws.com
ENV PSQL_PASSWORD Disha101
ENV PSQL_PORT 5432

EXPOSE 8011

ENTRYPOINT ["python", "./main.py"]
