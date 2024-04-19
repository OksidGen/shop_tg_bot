FROM python:3.12-alpine3.18
LABEL authors="cyber_codeer"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /shop_wd_bot
COPY ./req.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./req.txt

COPY ./ ./

RUN chmod +x ./