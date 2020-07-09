

# .env for docker-compose
Put in folder with docker-compose.yml
```
POSTGRES_DB=exmpl_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_JWT_SECRET=PASSWORDmustBEATLEAST32CHARSLONG


    volumes:
      # anything in initdb directory is created in the database
      # see "How to extend this image" section at https://hub.docker.com/r/_/postgres/
      #      - "./exmpl-db/pg-database/db-scripts/compiled-scripts:/docker-entrypoint-initdb.d"

      - "./db/sql:/docker-entrypoint-initdb.d"

      # Uncomment this if you want to persist the data.

      #- "~/.data/exmpl_db/pgdata:/var/lib/postgresql/data"

    networks:
      - postgrest-backend

    restart: always

```

Roles
* exmpl_guest
