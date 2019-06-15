FROM python:3.7

RUN groupadd wsgi
RUN useradd -ms /bin/bash -g wsgi wsgi

WORKDIR /backend
COPY --chown=wsgi:wsgi . /backend

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV PYTHON_ENV production

CMD ["uwsgi", "--ini", "/backend/uwsgi.ini"]
