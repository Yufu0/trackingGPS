FROM postgres:16

# Copy the init.sql script to the initialization directory
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
#RUN echo "listen_addresses = '*'" >> /var/lib/postgresql/data/postgresql.conf
RUN echo "host all all all md5" >> /etc/postgresql/16/main/pg_hba.conf

RUN /etc/init.d/postgresql restart