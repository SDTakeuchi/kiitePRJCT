FROM python:3.10-buster

# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

COPY . /kiite/

WORKDIR /kiite/

RUN apt-get update \
&&  apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 \
&&  pip install --upgrade pip \
&&  pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]