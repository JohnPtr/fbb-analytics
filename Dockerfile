FROM python:3.8-buster

RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    && wget https://sfc-repo.snowflakecomputing.com/odbc/linux/latest/snowflake-odbc-2.25.7.x86_64.deb \
    && apt install ./snowflake-odbc-2.25.7.x86_64.deb -y

RUN mkdir app
WORKDIR /app

COPY ./return_rates_data return_rates_data/.
COPY ./requirements.txt .
COPY ./setup.py .

RUN pip install -e .
