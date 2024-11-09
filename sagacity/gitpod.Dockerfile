FROM gitpod/workspace-full

# Install PostgreSQL
RUN sudo install-packages postgresql postgresql-contrib

# Setup PostgreSQL server for user gitpod
ENV PATH="/usr/lib/postgresql/12/bin:$PATH"
RUN sudo mkdir -p /var/run/postgresql && \
    sudo chown -R gitpod:gitpod /var/run/postgresql && \
    sudo chmod 777 /var/run/postgresql

# Create the PostgreSQL database cluster
ENV PGDATA="/workspace/.pgsql/data"
RUN mkdir -p ~/.pg_ctl/bin ~/.pg_ctl/sockets && \
    printf '#!/bin/bash\npg_ctl -D $PGDATA -l ~/.pg_ctl/log -o "-k ~/.pg_ctl/sockets" start\n' > ~/.pg_ctl/bin/pg_start && \
    printf '#!/bin/bash\npg_ctl -D $PGDATA -l ~/.pg_ctl/log -o "-k ~/.pg_ctl/sockets" stop\n' > ~/.pg_ctl/bin/pg_stop && \
    chmod +x ~/.pg_ctl/bin/*
ENV PATH="$HOME/.pg_ctl/bin:$PATH"
ENV DATABASE_URL="postgresql://gitpod@localhost"
ENV PGHOSTADDR="127.0.0.1"
ENV PGDATABASE="postgres"

# This is where PostgreSQL stores its data
RUN mkdir -p "$PGDATA" && \
    chown -R gitpod:gitpod "$PGDATA" && \
    chmod 777 "$PGDATA"

# Initialize PostgreSQL
RUN initdb -D "$PGDATA"

# Customize PostgreSQL configuration to allow remote connections
RUN echo "host all all all md5" >> "$PGDATA/pg_hba.conf" && \
    echo "listen_addresses='*'" >> "$PGDATA/postgresql.conf"