FROM python:3.7

RUN groupadd wsgi
RUN useradd -ms /bin/bash -g wsgi wsgi
RUN pip install uwsgi
ENV PYTHON_ENV production

WORKDIR /webapp/
COPY --chown=wsgi:wsgi requirements.txt /webapp/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# COPY --chown=wsgi:wsgi webapp/ /webapp/

ENV PYTHONPATH=".."

CMD ["uwsgi", "--ini", "/webapp/uwsgi.ini"]
