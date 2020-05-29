FROM node:12.16.1-alpine

RUN npm install --silent -g typescript react-scripts create-react-app
RUN npm install --silent -g npm eslint yarn

WORKDIR /usr/src/app

COPY package.json .
RUN npm install --silent

ADD . /usr/src/app

RUN npm run build

CMD [ "npm", "start" ]
EXPOSE 3000
