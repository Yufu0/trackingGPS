FROM node:latest

WORKDIR /usr/local/app

COPY ./ /usr/local/app/

RUN npm install

RUN npm install -g @angular/cli

RUN ng serve
