# Usamos una versión ligera y segura basada en Alpine
FROM httpd:2.4.33-alpine

# Actualizamos paquetes para corregir vulnerabilidades conocidas (CVEs)
RUN apk update && apk upgrade

# Copiamos la configuración personalizada del WAF/Proxy
COPY demo.apache.conf /usr/local/apache2/conf/demo.apache.conf

# Copiamos todo el contenido del frontend (HTML, JS, CSS) a la ruta por defecto
# Asegúrate de que tus .html estén en la carpeta ./apache/static/
COPY ./static/ /usr/local/apache2/htdocs/

# Habilitamos nuestra configuración en el servidor principal
RUN echo "Include /usr/local/apache2/conf/demo.apache.conf" \
    >> /usr/local/apache2/conf/httpd.conf

# Exponemos el puerto 80 (el que mapeamos como 6004 en el docker-compose)
EXPOSE 80
