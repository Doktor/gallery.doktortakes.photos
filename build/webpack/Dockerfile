FROM node:15.12.0 AS node

WORKDIR /app/ui/

COPY \
  ui/package.json \
  ui/package-lock.json \
  ui/webpack.*.js \
  /app/ui/

RUN npm install
