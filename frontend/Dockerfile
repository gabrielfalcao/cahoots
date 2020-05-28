FROM node:12.16.1-alpine

# Create Directory for the Container
WORKDIR /usr/src/app
# Only copy the package.json file to work directory
COPY package.json .
# Install all Packages
RUN npm install

ADD . /usr/src/app

RUN npm install -g tsc react-scripts create-react-app
RUN npm run build

CMD [ "npm", "start" ]
EXPOSE 3000
