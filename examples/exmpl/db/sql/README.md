# Development Environment Variables
```
# This optional environment variable can be used to define a different name for the default database that is created when the image is first started. If it is not specified, then the value of POSTGRES_USER will be used.
LB_EXAMPLE='{"name":"example"}'

LB_ENV_working_folder=..LyttleBit
LB_ENV_data_folder=.data

#LB_PROJECT_branch=#21.refactor.reorganize.folders

LB_PROJECT_name=exmpl
LB_PROJECT_prefix=exmpl
LB_PROJECT_owner=Wilfongjt

LB_POSTGRES_MODEL_username=postgres
LB_POSTGRES_MODEL_password=mysecretpassword

LB_DB_MODEL_username=postgres
LB_DB_MODEL_role=anonymous
LB_DB_MODEL_password=PASSWORDmustBEATLEAST32CHARSLONG
# MY_REPOURL=https://github.com/${LB_PROJECT_owner}/${LB_PROJECT_name}.git

LB_API_GUEST='{"role":"api_guest"}'
```

# Environment Variables
.env file goes next to the docker-compose.yml
```
  # everything starts here
  POSTGRES_DB=exmpl_db
  POSTGRES_SCHEMA=exmpl_schema
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=mysecretpostgrespassword
  POSTGRES_JWT_SECRET=PASSWORDmustBEATLEAST32CHARSLONG
  LB_GUEST_PASSWORD=secretguestpassword
```

# Docker Compose
You shouldn't have to tweak the docker-compose.yml
```
  docker-compose build

  docker-compose up

```
