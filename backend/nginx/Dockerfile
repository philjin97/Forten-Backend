FROM nginx:latest

# RUN rm /etc/nginx/nginx.conf
COPY /nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

WORKDIR /usr/src/app

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]