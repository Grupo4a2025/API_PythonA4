FROM httpd:2.4.33-alpine

RUN apk update; apk upgrade;

# Copiar configuración de Apache
COPY demo.apache.conf /usr/local/apache2/conf/demo.apache.conf

# Copiar archivos estáticos a htdocs (NO a /var/www/html)
COPY ./static/ /usr/local/apache2/htdocs/

# Incluir la configuración
RUN echo "Include /usr/local/apache2/conf/demo.apache.conf" \
    >> /usr/local/apache2/conf/httpd.conf