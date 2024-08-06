<<<<<<< HEAD
#!/bin/bash

set -e

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-bima360_user}"
DB_PASS="${DB_PASS:-bima360_password}"
DB_NAME="${DB_NAME:-bima360}"

DB_EXISTS=$(psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")

if [ -z "$DB_EXISTS" ]; then
    createdb -U postgres $DB_NAME

    USER_EXISTS=$(psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'")

    if [ -z "$USER_EXISTS" ]; then
        psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
        psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
        psql -U postgres -c "ALTER USER $DB_USER CREATEDB;"
    fi

    psql -U $DB_USER -d $DB_NAME < /docker-entrypoint-initdb/20231016_bima360_db_backup.sql
fi

exec "$@"
=======
#!/bin/bash

set -e

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-bima360_user}"
DB_PASS="${DB_PASS:-bima360_password}"
DB_NAME="${DB_NAME:-bima360}"

DB_EXISTS=$(psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")

if [ -z "$DB_EXISTS" ]; then
    createdb -U postgres $DB_NAME

    USER_EXISTS=$(psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'")

    if [ -z "$USER_EXISTS" ]; then
        psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
        psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
        psql -U postgres -c "ALTER USER $DB_USER CREATEDB;"
    fi

    psql -U $DB_USER -d $DB_NAME < /docker-entrypoint-initdb/20231016_bima360_db_backup.sql
fi

exec "$@"
>>>>>>> origin/ma-branch
