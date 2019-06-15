FROM nginx

COPY webapp/public/ /usr/share/nginx/html/public
COPY nginx.conf /etc/nginx/nginx.conf
