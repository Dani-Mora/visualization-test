FROM python:3

WORKDIR /usr/src/app

# Install python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

RUN curl 'https://analisi.transparenciacatalunya.cat/api/views/xuwf-dxjd/rows.csv' -o rows.csv

EXPOSE 8000

CMD [ "gunicorn", "app:server", "--preload" ]
