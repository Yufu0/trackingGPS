FROM postgres:16

# Copy the init.sql script to the initialization directory
COPY init.sql /docker-entrypoint-initdb.d/
ENV POSTGRES_HOST_AUTH_METHOD=trust


