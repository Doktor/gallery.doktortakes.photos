FROM alpine/openssl as ssl

RUN mkdir -p /app/ssl/ && \
    openssl req \
        -x509 -newkey rsa:4096 -sha256 -nodes -days 365 -subj '/CN=localhost' \
        -out /app/ssl/certificate.pem -keyout /app/ssl/key.pem


FROM nginx:1.21-alpine

RUN mkdir -p /app/logs/ && \
    # Remove default virtual host
    rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

COPY --from=ssl /app/ssl/ /app/ssl/
