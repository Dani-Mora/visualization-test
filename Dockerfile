FROM continuumio/anaconda3

WORKDIR /usr/src/app

RUN apt update && apt install gcc build-essential -y

# Create and set environment
COPY environment.yaml .
RUN conda env create -f environment.yaml

# Copy app
COPY . .

# Download latest data
RUN curl 'https://analisi.transparenciacatalunya.cat/api/views/xuwf-dxjd/rows.csv' -o rows.csv

EXPOSE 8000

CMD [ "conda", "run", "-n", "dash", "gunicorn", "app:server", "--preload" ]
