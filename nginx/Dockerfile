FROM nginx:latest

RUN mkdir -p /app/staticfiles

RUN rm /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
