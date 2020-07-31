FROM python
WORKDIR /code

ENV FLASK_APP local
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

# RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt
EXPOSE 5000

CMD ["flask", "run"]