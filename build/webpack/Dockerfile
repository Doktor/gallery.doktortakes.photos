FROM node:15.12.0 AS node

WORKDIR /app/

COPY \
  package.json \
  package-lock.json \
  webpack.*.js \
  /app/

RUN npm install
