

#.env for docker-compose
docker
```
# Put in folder with docker-compose.yml
#
# POSTGRES database
#
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
#DB_ANON_ROLE=anonymous
#DB_SCHEMA=aad_schema
#DB_USER=postgres
#DB_PASS=PASSWORDmustBEATLEAST32CHARSLONG
#
# POSTGREST rest service
#
#PGRST_DB_ANON_ROLE=api_user
#PGRST_DB_URI=postgres://api_user:password@db:5432/aad_db
#PGRST_DB_SCHEMA=public
#PGRST_DB_ANON_ROLE=api_user #In production this role should not be the same as the one used for the connection
# PGRST_SERVER_PROXY_URI="http://127.0.0.1:3000"

```

Roles
* exmpl_guest