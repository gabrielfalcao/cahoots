FROM node:12.16.1-alpine


# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent
RUN npm install --silent -g react-scripts@3.4.1

# add app
COPY . ./

# start app
CMD ["npm", "start"]
