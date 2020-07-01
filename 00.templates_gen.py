import sys
print(sys.path)
import os
from pathlib import Path
import settings
print('os.getenv', os.getenv('LB_WORKING_FOLDER_NAME'))
print('change projects in .env')
from templates import Template
from app_settings import AppSettings, AppSettingsTest
 
class Template_DockerfileWebDockerfileWebDkJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'dockerfile-web.dockerfile-web.dk.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/web'
    def getOutputName(self): return 'dockerfile-web'
    def getTemplateList(self):
        return '''
FROM node:10.15.3
RUN echo "IN DF"
# set target folder for app
WORKDIR /usr/src
# need only packages to get started
COPY package*.json /usr/src/
RUN ls
# update all the packages in node_modules
RUN npm install && npm run build
# move code from repo to container
COPY . /usr/src
EXPOSE 3000
ENV HOST 0.0.0.0
# CMD ["npm", "run", "dev"]
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "dockerfile",
			    "app-owner": "wilfongjt",
			    "app-name": "web"
			}
        
##########
##########
##########
 
class Template_DockerComposeDockerComposeDcJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'docker-compose.docker-compose.dc.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain'
    def getOutputName(self): return 'docker-compose.yml'
    def getTemplateList(self):
        return '''
version: '3'
# docker-compose up
# ref: http://postgrest.org/en/v6.0/install.html#docker
# ref: https://github.com/mattddowney/compose-postgrest/blob/master/docker-compose.yml
# Issue:  'password authentication failed for user "postgres"'
# Resolution:  then delete the database instance and rerun docker-compose up
# Trouble: Environment variables
# Solution: add .env in same folder as this yml.  include same name variables as those in environment section

services:
  #admin:
  #  container_name: [[admin-name]]
  #  image: [[app-owner]]/[[admin-name]]
  #  build:
  #    context: ./[[admin-name]]
  #    dockerfile: dockerfile-[[admin-name]]
  #  command: >
  #    bash -c "npm install && npm run dev"
  #  volumes:
  #    - ./[[admin-name]]:/usr/src
  #  ports:
  #    - "3200:3000"
  #web:
  #  container_name: [[web-name]]
  #  image: [[app-owner]]/[[web-name]]
  #  build:
  #    context: ./[[web-name]]
  #    dockerfile: dockerfile-[[web-name]]
  #  command: >
  #    bash -c "npm install && npm run dev"
  #  volumes:
  #    - ./[[web-name]]:/usr/src
  #  ports:
  #    - "3000:3000"

  #############
  # POSTGRES
  #########

  db:
    # env_file:
    #     - pg.env
    # create a .env to hold env vars ... see below
    build:
        context: ./db
        dockerfile: dockerfile-db
    ports:
      - "5433:5432"
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=postgres
      - DB_ANON_ROLE=${DB_ANON_ROLE}
      - DB_SCHEMA=${DB_SCHEMA}
      - DB_NAME=postgres
      - DB_USER=${DB_USER}
      - DB_PASS=${DB_PASS}
      #- POSTGRES_USER=${LB_POSTGRES_MODEL_username}
      #- POSTGRES_PASSWORD=${LB_POSTGRES_MODEL_password}
      #- POSTGRES_DB=postgres
      #- DB_ANON_ROLE=${LB_DB_MODEL_role}
      #- DB_SCHEMA=[[LB_PROJECT_prefix]]_schema
      #- DB_NAME=postgres
      #- DB_USER=${LB_DB_MODEL_username}
      #- DB_PASS=${LB_DB_MODEL_password}

    volumes:
      # anything in initdb directory is created in the database
      # see "How to extend this image" section at https://hub.docker.com/r/_/postgres/
      #      - "./[[LB_PROJECT_prefix]]-db/pg-database/db-scripts/compiled-scripts:/docker-entrypoint-initdb.d"

      - "./db/sql:/docker-entrypoint-initdb.d"

      # Uncomment this if you want to persist the data.

      #- "~/.data/[[LB_PROJECT_prefix]]_db/pgdata:/var/lib/postgresql/data"

    networks:
      - postgrest-backend

    restart: always

  ##########
  # POSTGRREST
  #####

  api:
    #container_name: postgrest
    image: postgrest/postgrest:latest

    ports:
      - "3100:3000"

    environment:
      # The standard connection URI format, documented at
      # https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING
      - PGRST_DB_URI=postgres://postgres:${DB_PASS}@db:5432/[[LB_PROJECT_prefix]]_db
      - PGRST_DB_SCHEMA=${DB_SCHEMA}
      - PGRST_DB_ANON_ROLE=${DB_ANON_ROLE}
      #PGRST_DB_URI: postgres://postgres:${DB_PASS}@db:5432/[[LB_PROJECT_prefix]]_db
      #PGRST_DB_SCHEMA: ${DB_SCHEMA}
      #PGRST_DB_ANON_ROLE: ${DB_ANON_ROLE}
      #PGRST_DB_URI: postgres://postgres:${LB_POSTGRES_MODEL_password}@db:5432/[[LB_PROJECT_prefix]]_db
      #PGRST_DB_SCHEMA: [[LB_PROJECT_prefix]]_schema
      #PGRST_DB_ANON_ROLE: ${LB_DB_MODEL_role}
    depends_on:
      - db

    links:

      - db:db

    networks:
      - postgrest-backend

    restart: always

networks:
  postgrest-backend:
    driver: bridge
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "docker-compose",
			    "app-owner": "wilfongjt",
			    "web-name": "web",
			    "admin-name": "admin"
			}
        
##########
##########
##########
 
class Template_DockerfileDbDockerfileDbDkJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'dockerfile-db.dockerfile-db.dk.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db'
    def getOutputName(self): return 'dockerfile-db'
    def getTemplateList(self):
        return '''
FROM postgres:11

# build postres container with jwt included
RUN apt-get update && apt-get install -y make git postgresql-server-dev-11 postgresql-11-pgtap

# set up jwt tokens
RUN mkdir "/postgres-jwt"
WORKDIR "/postgres-jwt"
COPY . .
RUN make && make install

# fire up postres with new config file
CMD ["postgres"]
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "dockerfile",
			    "app-owner": "wilfongjt",
			    "app-name": "db"
			}
        
##########
##########
##########
 
class Template_PgEnvironmentEnvJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'pg.environment.env.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/web'
    def getOutputName(self): return '.env'
    def getTemplateList(self):
        return '''
LB_POSTGRES_MODEL_password=[[LB_POSTGRES_MODEL_password]]
LB_DB_MODEL_password=[[LB_DB_MODEL_password]]
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "environment"
			}
        
##########
##########
##########
 
class Template_DockerfileAdminDockerfileAdminDkJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'dockerfile-admin.dockerfile-admin.dk.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/admin'
    def getOutputName(self): return 'dockerfile-admin'
    def getTemplateList(self):
        return '''
FROM node:10.15.3
RUN echo "IN DF"
# set target folder for app
WORKDIR /usr/src
# need only packages to get started
COPY package*.json /usr/src/
RUN ls
# update all the packages in node_modules
RUN npm install && npm run build
# move code from repo to container
COPY . /usr/src
EXPOSE 3000
ENV HOST 0.0.0.0
# CMD ["npm", "run", "dev"]
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "dockerfile",
			    "app-owner": "wilfongjt",
			    "app-name": "admin"
			}
        
##########
##########
##########
 
class Template_TestJwtTokenTestPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'test-jwt-token.test.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '99.test-jwt-token.test.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db
select '##### TESTS';
BEGIN;
SELECT plan(14);
SELECT
  is(sign('{"sub":"1234567890","name":"John Doe","admin":true}', 'secret'),
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ');
SELECT
  is(sign('{"sub":"1234567890","name":"John Doe","admin":true}', 'secret', 'HS256'),
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ');
SELECT
  throws_ok($$
    SELECT sign('{"sub":"1234567890","name":"John Doe","admin":true}', 'secret', 'bogus')
    $$,
    '22023',
    'Cannot use "": No such hash algorithm',
    'sign() should raise on bogus algorithm'
    );
SELECT
  throws_ok(
    $$SELECT header::text, payload::text, valid FROM verify(
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ',
    'secret', 'bogus')$$,
    '22023',
    'Cannot use "": No such hash algorithm',
    'verify() should raise on bogus algorithm'
);
SELECT throws_ok( -- bogus header
    $$SELECT header::text, payload::text, valid FROM verify(
    'eyJhbGciOiJIUzI1NiIBOGUScCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ',
    'secret', 'HS256')$$
    );
SELECT
  throws_ok( -- bogus payload
    $$SELECT header::text, payload::text, valid FROM verify(
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaBOGUS9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ',
    'secret', 'HS256')$$
);
SELECT
  results_eq(
    $$SELECT header::text, payload::text, valid FROM verify(
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ',
    'secret')$$,
    $$VALUES ('{"alg":"HS256","typ":"JWT"}', '{"sub":"1234567890","name":"John Doe","admin":true}', true)$$,
    'verify() should return return data marked valid'
);
SELECT results_eq(
    $$SELECT header::text, payload::text, valid FROM verify(
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ',
    'badsecret')$$,
    $$VALUES ('{"alg":"HS256","typ":"JWT"}', '{"sub":"1234567890","name":"John Doe","admin":true}', false)$$,
    'verify() should return return data marked invalid'
);
SELECT
  is(sign('{"sub":"1234567890","name":"John Doe","admin":true}', 'secret', 'HS384'),
  E'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.DtVnCyiYCsCbg8gUP-579IC2GJ7P3CtFw6nfTTPw-0lZUzqgWAo9QIQElyxOpoRm');
SELECT
  results_eq(
    $$SELECT header::text, payload::text, valid FROM verify(
    E'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.DtVnCyiYCsCbg8gUP-579IC2GJ7P3CtFw6nfTTPw-0lZUzqgWAo9QIQElyxOpoRm',
    'secret', 'HS384')$$,
    $$VALUES ('{"alg":"HS384","typ":"JWT"}', '{"sub":"1234567890","name":"John Doe","admin":true}', true)$$,
    'verify() should return return data marked valid'
);
SELECT
  results_eq(
    $$SELECT header::text, payload::text, valid FROM verify(
    E'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.DtVnCyiYCsCbg8gUP-579IC2GJ7P3CtFw6nfTTPw-0lZUzqgWAo9QIQElyxOpoRm',
    'badsecret', 'HS384')$$,
    $$VALUES ('{"alg":"HS384","typ":"JWT"}', '{"sub":"1234567890","name":"John Doe","admin":true}', false)$$,
    'verify() should return return data marked invalid'
);
SELECT
  is(sign('{"sub":"1234567890","name":"John Doe","admin":true}', 'secret', 'HS512'),
  E'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.YI0rUGDq5XdRw8vW2sDLRNFMN8Waol03iSFH8I4iLzuYK7FKHaQYWzPt0BJFGrAmKJ6SjY0mJIMZqNQJFVpkuw');
SELECT
  results_eq(
    $$SELECT header::text, payload::text, valid FROM verify(
    E'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.YI0rUGDq5XdRw8vW2sDLRNFMN8Waol03iSFH8I4iLzuYK7FKHaQYWzPt0BJFGrAmKJ6SjY0mJIMZqNQJFVpkuw',
    'secret', 'HS512')$$,
    $$VALUES ('{"alg":"HS512","typ":"JWT"}', '{"sub":"1234567890","name":"John Doe","admin":true}', true)$$,
    'verify() should return return data marked valid'
);
SELECT
  results_eq(
    $$SELECT header::text, payload::text, valid FROM verify(
    E'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.YI0rUGDq5XdRw8vW2sDLRNFMN8Waol03iSFH8I4iLzuYK7FKHaQYWzPt0BJFGrAmKJ6SjY0mJIMZqNQJFVpkuw',
    'badsecret', 'HS512')$$,
    $$VALUES ('{"alg":"HS512","typ":"JWT"}', '{"sub":"1234567890","name":"John Doe","admin":true}', false)$$,
    'verify() should return return data marked invalid'
);
SELECT * FROM finish();
ROLLBACK;
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "test.pg"
			}
        
##########
##########
##########
 
class Template_RegisterTablePgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'register.table.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '05.register.table.pg.sql'
    def getTemplateList(self):
        return '''
---- SET DB
\c [[LB_PROJECT_prefix]]_db
-- TABLE
create table if not exists
[[LB_PROJECT_prefix]]_schema.[[tbl-name]] (
  <<table-fields>>
);

-- INDEXxxx
CREATE UNIQUE INDEX IF NOT EXISTS [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[LB_PROJECT_prefix]]_schema.[[tbl-name]]([[tbl-prefix]]_id);

--CREATE UNIQUE INDEX IF NOT EXISTS [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[LB_PROJECT_prefix]]_schema.[[tbl-name]]([[tbl-prefix]]_id text_pattern_ops);
--CREATE UNIQUE INDEX [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[LB_PROJECT_prefix]]_schema.[[tbl-name]]([[tbl-prefix]]_id);
-- TRIGGER FUNCTION
CREATE OR REPLACE FUNCTION [[tbl-prefix]]_ins_upd_trigger_func() RETURNS trigger
AS $$
Declare _token TEXT;
Declare _custom JSON;
Declare _form JSONB;
Declare _password TEXT;
BEGIN
   -- create application token
    IF (TG_OP = 'INSERT') THEN
        NEW.[[tbl-prefix]]_id := format('%s@%s',NEW.[[tbl-prefix]]_form ->> 'app-name',NEW.[[tbl-prefix]]_form ->> 'version');
        _custom := format('{"app-name":"%s", "version":"%s", "role":"registrar"}',
                    NEW.[[tbl-prefix]]_form ->> 'app-name',
                    NEW.[[tbl-prefix]]_form ->> 'version')::JSON;
        _token := sign( _custom::JSON, current_setting('app.jwt_secret'),  'HS256'::text);
        _form := format('{"token": "%s"}',_token)::JSONB;

        NEW.[[tbl-prefix]]_form := NEW.[[tbl-prefix]]_form || _form;

        NEW.[[tbl-prefix]]_password := crypt(NEW.[[tbl-prefix]]_password, gen_salt('bf'));

    ELSEIF (TG_OP = 'UPDATE') THEN

       NEW.[[tbl-prefix]]_updated := CURRENT_TIMESTAMP;

    END IF;

    RETURN NEW;
END; $$ LANGUAGE plpgsql;



-- TRIGGER
CREATE TRIGGER [[tbl-prefix]]_ins_upd_trigger
 BEFORE INSERT ON [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
 FOR EACH ROW
 EXECUTE PROCEDURE [[tbl-prefix]]_ins_upd_trigger_func();

'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "description":["Single table multiple interfaces"],
			    "type": "table",
			    "db-prefix": "reg",
			    "tbl-name": "register",
			    "tbl-prefix": "reg",
			    "tbl-tests": ["api"],
			    "tbl-roles": ["registrant"],
			
			    "dep-api-overwrite": "0",
			    "dep-api-name": "register",
			    "dep-api-table": "register",
			    "dep-api-methods": ["upsert", "select"],
			    "tbl-fields": [
			        {
			            "name": "id",
			            "context": "pk",
			            "type": "TEXT",
			            "crud": "RI",
			            "search-context": "text"
			        },{
			            "name": "type",
			            "context":"type",
			            "type": "TEXT",
			            "crud": "CRI",
			            "search-context": "type"
			        },{
			            "name": "form",
			            "context": "form",
			            "description": "JSON record",
			            "type": "JSONB",
			            "crud": "FR"
			        },{
			            "name": "password",
			            "context": "password",
			            "description": "Passwords are stored in table row, but not in json row",
			            "type": "TEXT",
			            "crud": "Cu",
			            "calculate": "encrypt(_password)"
			        },{
			            "name": "active",
			            "context": "active",
			            "type": "BOOLEAN",
			            "default": "true",
			            "crud": "ru"
			        },{
			            "name": "created",
			            "context": "created",
			            "type": "TIMESTAMP",
			            "crud": "r"
			        },{
			            "name": "updated",
			            "context": "updated",
			            "type": "TIMESTAMP",
			            "crud": "r"
			        }
			    ],
			    "interfaces": {
			        "app": {
			            "overwrite": "0",
			            "name": "app",
			            "table": "register",
			            "methods": [
			                "upsert",
			                "select",
			                "test"
			            ],
			            "role": "anonymous",
			            "version": "1.0.0",
			            "privileges": [
			                {
			                    "privilege": "EXECUTE",
			                    "type": "FUNCTION",
			                    "parameters": "JSONB",
			                    "role": "anonymous"
			                },
			                {
			                    "privilege": "EXECUTE",
			                    "type": "FUNCTION",
			                    "parameters": "JSONB",
			                    "role": "api_user"
			                }
			            ],
			            "form": [
			                {
			                    "name": "id",
			                    "context": "pk",
			                    "type": "TEXT",
			                    "json": "RI",
			                    "search": "uuid",
			                    "calculated": "uuid_generate_v4()"
			                },
			                {
			                    "name": "type",
			                    "context": "type",
			                    "type": "TEXT",
			                    "json": "CRI",
			                    "const": "app"
			                },
			                {
			                    "name": "app-name",
			                    "context": "name",
			                    "type": "TEXT",
			                    "json": "CRI",
			                    "default": "my-app"
			                },
			                {
			                    "name": "version",
			                    "context": "version",
			                    "type": "TEXT",
			                    "default": "1.0.0",
			                    "json": "CR"
			                },
			                {
			                    "name": "username",
			                    "context": "email",
			                    "type": "TEXT",
			                    "json": "Cru"
			                },
			                {
			                    "name": "password",
			                    "context": "password",
			                    "description": [
			                        "Passwords are stored in table row, but not in json row",
			                        "Remove the password from form before inserting",
			                        "Remove the password from form before updating"
			                    ],
			                    "type": "TEXT",
			                    "json": "CuD"
			                },
			                {
			                    "name": "token",
			                    "context": "token",
			                    "type": "TEXT",
			                    "json": "r",
			                    "function": "sign(_payload, _secret)"
			                }
			            ],
			            "test-forms": [
			                {
			                    "type": "insert",
			                    "description": ["Test the app form insert."],
			                    "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.app( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]",
			                    "token": "sign('{{pattern}}'::json, {{password}})",
			                    "pattern": {
			                        "username": "testuser@register.com",
			                        "role": "anonymous"
			                    },
			                    "password": "current_setting('app.jwt_secret')",
			                    "form": {
			                        "type": "app",
			                        "app-name": "my-test-app",
			                        "version": "1.0.0",
			                        "username": "testuser@register.com",
			                        "email": "test@register.com",
			                        "password": "g1G!gggg",
			                        "test": "insert"
			                    },
			                    "expected": "'{\"msg\": \"OK\", \"status\": \"200\"}'::JSONB",
			                    "description": "'app - insert test'::TEXT"
			                },
			                {
			                    "type": "select",
			                    "description": ["Test the app form select."],
			                    "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.app( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]",
			                    "token": "sign('{{pattern}}'::json, {{password}} )",
			                    "pattern": {
			                        "username": "testuser@register.com",
			                        "role": "anonymous"
			                    },
			                    "password": "current_setting('app.jwt_secret')",
			                    "form": {
			                        "id": "my-test-app@1.0.0"
			                    },
			                    "expected": "'[a-zA-Z\\.0-9_]+'",
			                    "description": "'app - select from {{tbl-name}} by id and check token'::TEXT"
			                }
			            ]
			        },
			        "user": {
			          "overwrite": "0",
			          "name": "user",
			          "table": "register",
			          "methods": [
			            "upsert",
			            "select",
			            "test"
			          ],
			          "role": "anonymous",
			          "version": "1.0.0",
			          "privileges": [
			            {
			              "privilege": "EXECUTE",
			              "type": "FUNCTION",
			              "parameters": "TEXT, JSONB",
			              "role": "anonymous"
			            },
			            {
			              "privilege": "EXECUTE",
			              "type": "FUNCTION",
			              "parameters": "TEXT, TEXT",
			              "role": "anonymous"
			            },
			            {
			              "privilege": "EXECUTE",
			              "type": "FUNCTION",
			              "parameters": "TEXT, JSONB",
			              "role": "api_user"
			            },
			            {
			              "privilege": "EXECUTE",
			              "type": "FUNCTION",
			              "parameters": "TEXT, TEXT",
			              "role": "api_user"
			            }
			          ],
			          "form": [
			            {
			              "name": "id",
			              "context": "pk",
			              "type": "TEXT",
			              "json": "RI",
			              "search": "uuid",
			              "calculated": "uuid_generate_v4()"
			            },
			            {
			              "name": "type",
			              "context": "type",
			              "type": "TEXT",
			              "json": "CRI",
			              "const": "user"
			            },
			            {
			              "name": "app_id",
			              "context": "name",
			              "type": "TEXT",
			              "json": "CRI",
			              "default": "my-test-app@1.0.0"
			            },
			            {
			              "name": "username",
			              "context": "email",
			              "type": "TEXT",
			              "json": "Cru"
			            },
			            {
			              "name": "password",
			              "context": "password",
			              "description": [
			                "Passwords are stored in table row, but not in json row",
			                "Remove the password from form before inserting",
			                "Remove the password from form before updating"
			              ],
			              "type": "TEXT",
			              "json": "CuD"
			            }
			          ],
			          "test-forms": [
			            {
			              "type": "insert",
			              "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.user( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]",
			              "token": "sign('{{pattern}}'::json, {{password}})",
			              "pattern": {
			                "username": "testuser@register.com",
			                "role": "anonymous"
			              },
			              "password": "current_setting('app.jwt_secret')",
			              "form": {
			                "type": "user",
			                "app_id": "my-test-app@1.0.0",
			                "username": "testuser@register.com",
			                "email": "test@register.com",
			                "password": "g1G!gggg",
			                "test": "insert"
			              },
			              "expected": "'{\"status\": \"200\", \"msg\": \"ok\"}'::JSONB",
			              "description": "'user - insert test'::TEXT"
			            },
			            {
			              "type": "select",
			              "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.user( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]",
			              "token": "sign('{{pattern}}'::json, {{password}} )",
			              "pattern": {
			                "username": "testuser@register.com",
			                "role": "anonymous"
			              },
			              "password": "current_setting('app.jwt_secret')",
			              "form": {
			                "id": "my-test-app@1.0.0"
			              },
			              "expected": "'[a-zA-Z\\.0-9_]+'",
			              "description": "'user - select from {{tbl-name}} by id and check token'::TEXT"
			            }
			          ]
			        }
			    }
			}
        
##########
##########
##########
 
class Template_NuxtjsWebScriptShShJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'nuxtjs-web.script-sh.sh.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders'
    def getOutputName(self): return 'nuxtjs-web.sh'
    def getTemplateList(self):
        return '''
#!/bin/bash

source ./_conf.sh

# check for database folder and make if not there
echo "LB_GIT_PROJECT is ${LB_PROJECT_name} "
echo "LB_PROJECT_name is ${LB_PROJECT_name}"
cd ${LB_PROJECT_name}
ls
if [ ! -d "web/node_modules" ] ; then
    echo 'new nuxtjs'
  npx create-nuxt-app web
fi

#npm WARN deprecated core-js@2.6.11: core-js@<3 is no longer maintained and not r
#ecommended for usage due to the number of issues. Please, upgrade your dependenc
#ies to the actual version of core-js@3.
if [ -d "web" ] ; then
    cd "web"
    #npm install --save core-js@3.x
    #npm install --save-dev jest@latest
    cd ..
fi
#npm WARN deprecated request@2.88.2: request has been deprecated, see
#https://github.com/request/request/issues/3142

#npm notice created a lockfile as package-lock.json. You should commit this file.
#npm WARN ts-jest@23.10.5 requires a peer of jest@>=22 <24 but none is installed.
# You must install peer dependencies yourself.

#npm install --save-dev jest@>=22 <24
#npm install --save-dev jest@latest

#npm install --dev jest@>=22 <24
#npm install --save-dev ts-jest@23.10.5
#npm install --save-dev ts-jest@latest
#cd "web"
#npm audit
#npm audit fix --dry-run
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "script-sh",
			    "nuxtjs-name": "web"
			}
        
##########
##########
##########
 
class Template_DownScriptShShJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'down.script-sh.sh.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders'
    def getOutputName(self): return 'down.sh'
    def getTemplateList(self):
        return '''
source ./_conf.sh


# keep stuff from build docker system prune

echo "${LB_ENV_data_folder}/${LB_PROJECT_prefix}_db"
cd ${LB_PROJECT_name}/

docker-compose down

'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "script-sh"
			}
        
##########
##########
##########
 
class Template_NuxtjsAdminScriptShShJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'nuxtjs-admin.script-sh.sh.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders'
    def getOutputName(self): return 'nuxtjs-admin.sh'
    def getTemplateList(self):
        return '''
#!/bin/bash

source ./_conf.sh

# check for database folder and make if not there
echo "LB_GIT_PROJECT is ${LB_PROJECT_name} "
echo "LB_PROJECT_name is ${LB_PROJECT_name}"
cd ${LB_PROJECT_name}
ls
if [ ! -d "[[nuxtjs-name]]/node_modules" ] ; then
  echo 'new nuxtjs'
  npx create-nuxt-app [[nuxtjs-name]]
fi

#npm WARN deprecated core-js@2.6.11: core-js@<3 is no longer maintained and not r
#ecommended for usage due to the number of issues. Please, upgrade your dependenc
#ies to the actual version of core-js@3.
if [ -d "[[nuxtjs-name]]" ] ; then
    cd "[[nuxtjs-name]]"
    #npm install --save core-js@3.x
    #npm install --save-dev jest@latest
    cd ..
fi
#npm WARN deprecated request@2.88.2: request has been deprecated, see
#https://github.com/request/request/issues/3142

#npm notice created a lockfile as package-lock.json. You should commit this file.
#npm WARN ts-jest@23.10.5 requires a peer of jest@>=22 <24 but none is installed.
# You must install peer dependencies yourself.

#npm install --save-dev jest@>=22 <24
#npm install --save-dev jest@latest

#npm install --dev jest@>=22 <24
#npm install --save-dev ts-jest@23.10.5
#npm install --save-dev ts-jest@latest
#cd "[[nuxtjs-name]]"
#npm audit
#npm audit fix --dry-run
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "script-sh",
			    "nuxtjs-name": "admin"
			}
        
##########
##########
##########
 
class Template_UpScriptShShJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'up.script-sh.sh.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders'
    def getOutputName(self): return 'up.sh'
    def getTemplateList(self):
        return '''
source ./_conf.sh


# keep stuff from build docker system prune

echo "${LB_ENV_data_folder}/${LB_PROJECT_prefix}_db"
cd ${LB_PROJECT_name}/
docker-compose down
docker system prune


docker images
ls
if [ ! -f 'web/.env' ] ; then
  echo "  "
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo "   You must setup an .env file in ${LB_PROJECT_name}/"
  echo "       Terminating script."
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo "  "
  exit 1
fi

#docker-compose down

echo "${LB_ENV_data_folder}/db"
if [ -d "${LB_ENV_data_folder}/db" ]; then
  echo "Deleting... ${LB_ENV_data_folder}/db"
  rm -rv "${LB_ENV_data_folder}/db"
  echo "... Deleted ${LB_ENV_data_folder}/db"
else
  echo "Not found ${LB_ENV_data_folder}/db"
fi

# build everything from scratch...slow but works
echo "Ready to start app"

docker-compose build

docker-compose up


# show the environment variables
# docker-compose exec web env
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "script-sh"
			}
        
##########
##########
##########
 
class Template__confScriptShShJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return '_conf.script-sh.sh.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders'
    def getOutputName(self): return '_conf.sh'
    def getTemplateList(self):
        return '''
# generated from _conf.script-sh.sh.tmpl
# change these to match your project

# export LB_ENV=[[LB_ENV]]

export LB_ENV_working_folder=[[LB_ENV_working_folder]]
export LB_ENV_data_folder=[[LB_ENV_data_folder]]

export LB_PROJECT_branch=[[LB_PROJECT_branch]]
export LB_PROJECT_name=[[LB_PROJECT_name]]
export LB_PROJECT_prefix=[[LB_PROJECT_prefix]]
export LB_PROJECT_owner=[[LB_PROJECT_owner]]

export LB_POSTGRES_MODEL_username=[[LB_POSTGRES_MODEL_username]]
export LB_POSTGRES_MODEL_password=[[LB_POSTGRES_MODEL_password]]

export LB_DB_MODEL_username=[[LB_DB_MODEL_username]]
export LB_DB_MODEL_role=[[LB_DB_MODEL_role]]
export LB_DB_MODEL_password=[[LB_DB_MODEL_password]]

export MY_REPOURL=https://github.com/${LB_PROJECT_owner}/${LB_PROJECT_name}.git



# Folders
# /<working_folder>
#     - /<code-folder>
#     --- /<umbrella-folder>
#     ----- /<branch-folder>
#     --------- / <app-folder>
#     ----------- /db
#     ------------- /sql
#     ----------- /web
#     - /<projects-folder>
#     --- / <project-folder>-dev
#     - /<testing-folder>
#     -- /<code-folder>
#     --- /<umbrella-folder>
#     ----- /<branch-folder>
#     --------- /<app-folder>
#     ----------- /db
#     ------------- /sql
#     ----------- /web
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "script-sh"
			}
        
##########
##########
##########
 
class Template_DbScriptShShJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'db.script-sh.sh.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders'
    def getOutputName(self): return 'db.sh'
    def getTemplateList(self):
        return '''
#!/bin/bash
# source ./__scripts/00.settings.sh
source ./_conf.sh

# check for database folder and make if not there
echo "MY GIT PROJECT is ${LB_PROJECT_name}"

cd ${LB_PROJECT_name}

if [ ! -d ${LB_PROJECT_name} ] ; then
   if [ ! -d db/ ] ; then
     # create folder
     mkdir db
   fi
fi

if [ -d db/ ] ; then
     # copy files for postgres
     cd db/
     #cp -r ../../../../../00-Setup/__datastore/* .
     cp -r ~/${LB_ENV_working_folder}/code/00-Setup/__datastore/* .
     # make sql script folder
     mkdir 'sql'
     cd ..
   fi
cd ..
ls
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "script-sh"
			}
        
##########
##########
##########
 
class Template_AuthenticatorRolePgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'authenticator.role.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '03.authenticator.role.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

CREATE ROLE [[role-name]] NOINHERIT LOGIN PASSWORD '[[LB_DB_MODEL_password]]';



'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "role.pg",
			    "role-name": "authenticator"
			}
        
##########
##########
##########
 
class Template_AnonymousRolePgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'role.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '03.anonymous.role.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

CREATE ROLE [[role-name]] ;



'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "role.pg",
			    "role-name": "anonymous",
			    "templates": {
			        "role": "CREATE ROLE ;",
			        "usage": "GRANT USAGE ON SCHEMA {}_schema TO {};",
			        "": ""
			    }
			}
        
##########
##########
##########
 
class Template_EditorRolePgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'role.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '03.editor.role.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

CREATE ROLE [[role-name]] ;



'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "role.pg",
			    "role-name": "editor"
			}
        
##########
##########
##########
 
class Template_Api_userRolePgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'role.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '03.api_user.role.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

CREATE ROLE [[role-name]] ;



'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "role.pg",
			    "role-name": "api_user"
			}
        
##########
##########
##########
 
class Template_Get_idFunctionPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'get_id.function.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '07.get_id.function.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

-------------------------------------------
CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.get_id(_token text) RETURNS TEXT
AS $$
  DECLARE data TEXT;
  DECLARE secret TEXT;

BEGIN

  select payload ->> 'id' as id into data  from verify(_token, current_setting('app.jwt_secret'));

  RETURN data;

END;  $$ LANGUAGE plpgsql;



'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "function.pg"
			}
        
##########
##########
##########
 
class Template_Is_valid_tokenFunctionPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'is_valid_token.function.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '07.is_valid_token.function.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

---------------------------------------------


CREATE OR REPLACE FUNCTION

[[LB_PROJECT_prefix]]_schema.is_valid_token(_token TEXT, role TEXT) RETURNS Boolean

AS $$

  DECLARE good Boolean;
  DECLARE actual_role TEXT;

BEGIN
  -- does role in token match expected role
  -- use db parameter app.jwt_secret
  -- process the token
  -- return true/false
  good:=false;

  select payload ->> 'role' as role into actual_role  from verify(_token, current_setting('app.jwt_secret'));

  if role = actual_role then
    good := true;
  end if;

  RETURN good;
END;  $$ LANGUAGE plpgsql;



--------------------------------------------
/*

CREATE OR REPLACE FUNCTION

[[LB_PROJECT_prefix]]_schema.is_valid_token(_token text) RETURNS Boolean

AS $$

  DECLARE good Boolean;
  DECLARE secret TEXT;

BEGIN

  -- cloak the secret
  -- process the token
  -- return true/false

  good:=false;

  select valid into good from verify(token, current_setting('app.jwt_secret'));

  RETURN good;

END;  $$ LANGUAGE plpgsql;
*/

'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "function.pg"
			}
        
##########
##########
##########
 
class Template_Get_app_idFunctionPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'get_app_id.function.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '07.get_app_id.function.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

----------------------------------------------

CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.get_app_id(app_name TEXT, version TEXT) RETURNS TEXT
AS $$
  DECLARE id TEXT;

BEGIN
    -- get id from register for a specifie version

    select reg_id into id
    from reg_schema.register
    where reg_form->>'version'='1.0.0'
        and reg_form->>'app_name'=app_name;

  RETURN id;

END;  $$ LANGUAGE plpgsql;



'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "function"
			}
        
##########
##########
##########
 
class Template_Validate_passwordValidateFunctionPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'validate_password.validate-function.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '04.validate_password.validate-function.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

----------------------------------------------
/*
CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.validate_password(password text) RETURNS BOOLEAN
AS $$
  DECLARE rc BOOLEAN;
BEGIN

  if length(password) < 8 then
    return false;
  end if;
  if length(password) >512 then
    return false;
  end if;

  RETURN true;

END;  $$ LANGUAGE plpgsql;
*/


'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "function"
			}
        
##########
##########
##########
 
class Template_Get_roleFunctionPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'get_role.function.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '07.get_role.function.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

----------------------------------------------

CREATE OR REPLACE FUNCTION

[[LB_PROJECT_prefix]]_schema.get_role(_token text) RETURNS TEXT

AS $$

  DECLARE data TEXT;

  DECLARE secret TEXT;

BEGIN

  select payload ->> 'role' as role into data  from verify(_token, current_setting('app.jwt_secret'));

  RETURN data;

END;  $$ LANGUAGE plpgsql;



'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "function"
			}
        
##########
##########
##########
 
class Template_Get_usernameFunctionPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'get_username.function.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '07.get_username.function.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

----------------------------------------------

CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.get_username(_token text) RETURNS TEXT
AS $$

  DECLARE data TEXT;

BEGIN

  select payload ->> 'username' as username into data  from verify(_token, current_setting('app.jwt_secret'));

  RETURN data;

END;  $$ LANGUAGE plpgsql;



'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "type": "function"
			}
        
##########
##########
##########
 
class Template_RegisterUserInitializePgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'initialize.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '11.register-user.initialize.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db
-- insert a test user
-- [[api-test-forms..type:insert..select {{LB_PROJECT_prefix}}_schema.{{api-name}}(sign(current_setting('app.lb_register_anonymous')::json, current_setting('app.jwt_secret'))::TEXT,\'{{form}}\'::JSONB);]]
    --
    --  sign(current_setting('app.lb_register_anonymous')::json, current_setting('app.jwt_secret'))

    -- current_setting('app.lb_register_anonymous')


'''.split('\n')
 
    def getDictionary(self):
        return \
			{"description": ["Single table multiple interfaces"], "type": "interface", "db-prefix": "reg", "tbl-name": "register", "tbl-prefix": "reg", "tbl-tests": ["api"], "tbl-roles": ["registrant"], "dep-api-overwrite": "0", "dep-api-name": "register", "dep-api-table": "register", "dep-api-methods": ["upsert", "select"], "tbl-fields": [{"name": "id", "context": "pk", "type": "TEXT", "crud": "RI", "search-context": "text"}, {"name": "type", "context": "type", "type": "TEXT", "crud": "CRI", "search-context": "type"}, {"name": "form", "context": "form", "description": "JSON record", "type": "JSONB", "crud": "FR"}, {"name": "password", "context": "password", "description": "Passwords are stored in table row, but not in json row", "type": "TEXT", "crud": "Cu", "calculate": "encrypt(_password)"}, {"name": "active", "context": "active", "type": "BOOLEAN", "default": "true", "crud": "ru"}, {"name": "created", "context": "created", "type": "TIMESTAMP", "crud": "r"}, {"name": "updated", "context": "updated", "type": "TIMESTAMP", "crud": "r"}], "api-overwrite": "0", "api-name": "user", "api-table": "register", "api-methods": ["upsert", "select", "test"], "api-role": "anonymous", "api-version": "1.0.0", "api-privileges": [{"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, JSONB", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, TEXT", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, JSONB", "role": "api_user"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, TEXT", "role": "api_user"}], "api-form": [{"name": "id", "context": "pk", "type": "TEXT", "json": "RI", "search": "uuid", "calculated": "uuid_generate_v4()"}, {"name": "type", "context": "type", "type": "TEXT", "json": "CRI", "const": "user"}, {"name": "app_id", "context": "name", "type": "TEXT", "json": "CRI", "default": "my-test-app@1.0.0"}, {"name": "username", "context": "email", "type": "TEXT", "json": "Cru"}, {"name": "password", "context": "password", "description": ["Passwords are stored in table row, but not in json row", "Remove the password from form before inserting", "Remove the password from form before updating"], "type": "TEXT", "json": "CuD"}], "api-test-forms": [{"type": "insert", "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.user( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}})", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"type": "user", "app_id": "my-test-app@1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}, "expected": "'{\"status\": \"200\", \"msg\": \"ok\"}'::JSONB", "description": "'user - insert test'::TEXT"}, {"type": "select", "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.user( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}} )", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"id": "my-test-app@1.0.0"}, "expected": "'[a-zA-Z\\.0-9_]+'", "description": "'user - select from {{tbl-name}} by id and check token'::TEXT"}]}
        
##########
##########
##########
 
class Template_RegisterAppInitializePgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'register-app.initialize.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '11.register-app.initialize.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db
-- insert a test user

-- [[api-test-forms..type:insert..select {{LB_PROJECT_prefix}}_schema.{{api-name}}(\'{{form}}\'::JSONB);]]



'''.split('\n')
 
    def getDictionary(self):
        return \
			{"description": ["Single table multiple interfaces"], "type": "interface", "db-prefix": "reg", "tbl-name": "register", "tbl-prefix": "reg", "tbl-tests": ["api"], "tbl-roles": ["registrant"], "dep-api-overwrite": "0", "dep-api-name": "register", "dep-api-table": "register", "dep-api-methods": ["upsert", "select"], "tbl-fields": [{"name": "id", "context": "pk", "type": "TEXT", "crud": "RI", "search-context": "text"}, {"name": "type", "context": "type", "type": "TEXT", "crud": "CRI", "search-context": "type"}, {"name": "form", "context": "form", "description": "JSON record", "type": "JSONB", "crud": "FR"}, {"name": "password", "context": "password", "description": "Passwords are stored in table row, but not in json row", "type": "TEXT", "crud": "Cu", "calculate": "encrypt(_password)"}, {"name": "active", "context": "active", "type": "BOOLEAN", "default": "true", "crud": "ru"}, {"name": "created", "context": "created", "type": "TIMESTAMP", "crud": "r"}, {"name": "updated", "context": "updated", "type": "TIMESTAMP", "crud": "r"}], "api-overwrite": "0", "api-name": "app", "api-table": "register", "api-methods": ["upsert", "select", "test"], "api-role": "anonymous", "api-version": "1.0.0", "api-privileges": [{"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "JSONB", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "JSONB", "role": "api_user"}], "api-form": [{"name": "id", "context": "pk", "type": "TEXT", "json": "RI", "search": "uuid", "calculated": "uuid_generate_v4()"}, {"name": "type", "context": "type", "type": "TEXT", "json": "CRI", "const": "app"}, {"name": "app-name", "context": "name", "type": "TEXT", "json": "CRI", "default": "my-app"}, {"name": "version", "context": "version", "type": "TEXT", "default": "1.0.0", "json": "CR"}, {"name": "username", "context": "email", "type": "TEXT", "json": "Cru"}, {"name": "password", "context": "password", "description": ["Passwords are stored in table row, but not in json row", "Remove the password from form before inserting", "Remove the password from form before updating"], "type": "TEXT", "json": "CuD"}, {"name": "token", "context": "token", "type": "TEXT", "json": "r", "function": "sign(_payload, _secret)"}], "api-test-forms": [{"type": "insert", "description": "'app - insert test'::TEXT", "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.app( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}})", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}, "expected": "'{\"msg\": \"OK\", \"status\": \"200\"}'::JSONB"}, {"type": "select", "description": "'app - select from {{tbl-name}} by id and check token'::TEXT", "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.app( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}} )", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"id": "my-test-app@1.0.0"}, "expected": "'[a-zA-Z\\.0-9_]+'"}]}
        
##########
##########
##########
 
class Template_RegisterUserInterfaceSelectPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'interface-select.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '09.register-user.interface-select.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

-------------------------------
-- Select
---------

CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.[[api-name]](_token TEXT, _form_text TEXT) RETURNS JSONB
AS $$
  DECLARE rc TEXT;
  DECLARE secret TEXT;
  DECLARE rc_form JSONB;
  DECLARE _model_user JSONB;

  [[tbl-fields.*:*.Declare _{{name}} {{type}};]]

BEGIN

    _model_user := current_setting('app.lb_register_anonymous')::jsonb;

    -- figure out which token: app-token or user-token
    if not([[db-prefix]]_schema.is_valid_token(_token, _model_user ->> 'role')) then
        return '{"status": "401"}'::JSONB;
    end if;

    -- convert Text to JSONB to ref
    _form := _form_text::JSONB;

    -- confirm proper attributes in _form
    if not(_form ? 'id') then
        return '{"status":"400", "msg":"Bad Request id"}'::JSONB;
    end if;

    -- set where clause
    _id = _form ->> 'id';

    -- go get the data

    select [[tbl-prefix]]_[[tbl-fields.context:form.{{name}}]]
    into rc_form
    from [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
    where [[tbl-prefix]]_[[api-form.context:uuid-TEXT.{{name}}]]= _id;

    if rc_form is NULL then
      rc_form := '{"status":"204", "msg":"No Content","result": {}}'::JSONB;
    else
      rc_form :=  format('{"status":"200", "result":%s}',rc_form::TEXT)::JSONB;
    end if;

    RETURN rc_form;
END;  $$ LANGUAGE plpgsql;

GRANT EXECUTE ON FUNCTION
  [[LB_PROJECT_prefix]]_schema.[[api-name]](
  TEXT, TEXT
  ) TO anonymous;

[[api-privileges..type:FUNCTION..GRANT {{privilege}} ON {{type}} {{LB_PROJECT_prefix}}_schema.{{api-name}} ({{parameters}}) TO {{role}};]]

'''.split('\n')
 
    def getDictionary(self):
        return \
			{"description": ["Single table multiple interfaces"], "type": "interface", "db-prefix": "reg", "tbl-name": "register", "tbl-prefix": "reg", "tbl-tests": ["api"], "tbl-roles": ["registrant"], "dep-api-overwrite": "0", "dep-api-name": "register", "dep-api-table": "register", "dep-api-methods": ["upsert", "select"], "tbl-fields": [{"name": "id", "context": "pk", "type": "TEXT", "crud": "RI", "search-context": "text"}, {"name": "type", "context": "type", "type": "TEXT", "crud": "CRI", "search-context": "type"}, {"name": "form", "context": "form", "description": "JSON record", "type": "JSONB", "crud": "FR"}, {"name": "password", "context": "password", "description": "Passwords are stored in table row, but not in json row", "type": "TEXT", "crud": "Cu", "calculate": "encrypt(_password)"}, {"name": "active", "context": "active", "type": "BOOLEAN", "default": "true", "crud": "ru"}, {"name": "created", "context": "created", "type": "TIMESTAMP", "crud": "r"}, {"name": "updated", "context": "updated", "type": "TIMESTAMP", "crud": "r"}], "api-overwrite": "0", "api-name": "user", "api-table": "register", "api-methods": ["upsert", "select", "test"], "api-role": "anonymous", "api-version": "1.0.0", "api-privileges": [{"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, JSONB", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, TEXT", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, JSONB", "role": "api_user"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, TEXT", "role": "api_user"}], "api-form": [{"name": "id", "context": "pk", "type": "TEXT", "json": "RI", "search": "uuid", "calculated": "uuid_generate_v4()"}, {"name": "type", "context": "type", "type": "TEXT", "json": "CRI", "const": "user"}, {"name": "app_id", "context": "name", "type": "TEXT", "json": "CRI", "default": "my-test-app@1.0.0"}, {"name": "username", "context": "email", "type": "TEXT", "json": "Cru"}, {"name": "password", "context": "password", "description": ["Passwords are stored in table row, but not in json row", "Remove the password from form before inserting", "Remove the password from form before updating"], "type": "TEXT", "json": "CuD"}], "api-test-forms": [{"type": "insert", "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.user( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}})", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"type": "user", "app_id": "my-test-app@1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}, "expected": "'{\"status\": \"200\", \"msg\": \"ok\"}'::JSONB", "description": "'user - insert test'::TEXT"}, {"type": "select", "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.user( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}} )", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"id": "my-test-app@1.0.0"}, "expected": "'[a-zA-Z\\.0-9_]+'", "description": "'user - select from {{tbl-name}} by id and check token'::TEXT"}]}
        
##########
##########
##########
 
class Template_RegisterUserInterfaceUpsertPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'interface-upsert.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '09.register-user.interface-upsert.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db
-- general solution

CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.[[api-name]](_token TEXT, _json JSONB) RETURNS JSONB
AS $$
  Declare rc jsonb;
  Declare _cur_row JSONB;
  Declare _model_user JSONB;

  [[tbl-fields.*:*.Declare _{{name}} {{type}};]]

  BEGIN

    _model_user := current_setting('app.lb_register_[[api-role]]')::jsonb;

    -- figure out which token: app-token or user-token
    if not([[LB_PROJECT_prefix]]_schema.is_valid_token(_token, _model_user ->> 'role')) then
        return '{"status": "401", "msg": "Bad Request, token."}'::JSONB;
    end if;

    _form = _json;
    -- never store the password in form
    if _json ? 'password' then
        _form = _json - 'password';
    end if;

    -- UPDATE or INSERT
    -- is primary key in form
    if _json ? '[[api-form.context:pk.{{name}}]]' then
    	-- rc := '{"status":"400","msg": "Bad Request, missing id."}'::JSONB;
        BEGIN
            -- get current json object
            select [[tbl-prefix]]_[[tbl-fields.context:form.{{name}}]] as _usr
              into _cur_row
              from [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
              where [[tbl-prefix]]_[[api-form.context:pk.{{name}}]]= cast(_json::jsonb ->> '[[api-form.context:pk.{{name}}]]' as TEXT) and [[tbl-prefix]]_[[api-form.context:type.{{name}}]]= cast(_json::jsonb ->> '[[api-form.context:type.{{name}}]]' as TEXT);

        EXCEPTION
		    WHEN others then
		        rc := '{"status":"200","msg":"Unknown select error"}'::JSONB;
        END;

		-- update existing json object with input values
        BEGIN
            -- sync-json-values to table values

            -- all possible combinations of updates
            <<update-combination-code>>
            -- update_combos_format end

        EXCEPTION
		    WHEN check_violation then
		        rc := '{"status":"400","msg":"Bad Request, validation error"}'::JSONB;
		    WHEN others then
		        rc := '{"status":"500","msg":"Unknown update error"}'::JSONB;
        END;
		if not FOUND then
		  return format('{"status":"404", "msg": "Not Found, on update."}')::JSONB;
		end if;
	    rc := '{"status":"200", "msg": "ok"}'::JSONB;
    else
        -- start insert
    	BEGIN

            -- confirm all required attributes are in form
            if not([[api-form.json:(C)._json ? '{{name}}'. and ]]) then
               return '{"status":"400","msg":"Bad Request, missing form attribute"}'::JSONB;
            end if;

            -- make sure type is correct value
            if not(_json ->> '[[api-form.context:type.{{name}}]]' = '[[api-form.context:type.{{const}}]]') then
                 return '{"status":"400", "msg":"Bad Request, type."}'::JSONB;
            end if;

            -- extract values needed for wrapper record

            _[[api-form.context:type.{{name}}]] := _json ->> '[[api-form.context:type.{{name}}]]';

            _[[api-form.context:password.{{name}}]] := _json ->> '[[api-form.context:password.{{name}}]]';

            -- never store password in form

            _[[tbl-fields.context:form.{{name}}]] := _json - '[[api-form.context:password.{{name}}]]';

            -- validate
            if length(_[[api-form.context:password.{{name}}]]) < 8 then
                return '{"status":"400", "msg": "Bad Request, not acceptable."}'::JSONB;
            end if;

			INSERT INTO [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
                ([[tbl-fields.crud:(CF).{{tbl-prefix}}_{{name}}., ]])
              VALUES
                ([[tbl-fields.crud:(CF)._{{name}}., ]] );

            rc := '{"status":"200", "msg": "ok"}'::JSONB;

		EXCEPTION
		    WHEN unique_violation THEN
		        rc := '{"status":"400","msg":"Bad Request, duplicate." }'::JSONB;
		    WHEN check_violation then
		        rc := '{"status":"400","msg":"Bad Request, validation error."}'::JSONB;
		    WHEN others then
		        rc := '{"status":"400","msg":"Bad Request, unknown insert error."}'::JSONB;
		END;
    end if;
    RETURN rc;
  END;
$$ LANGUAGE plpgsql;

[[api-privileges..type:FUNCTION..GRANT {{privilege}} ON {{type}} {{LB_PROJECT_prefix}}_schema.{{api-name}} ({{parameters}}) TO {{role}};]]
'''.split('\n')
 
    def getDictionary(self):
        return \
			{"description": ["Single table multiple interfaces"], "type": "interface", "db-prefix": "reg", "tbl-name": "register", "tbl-prefix": "reg", "tbl-tests": ["api"], "tbl-roles": ["registrant"], "dep-api-overwrite": "0", "dep-api-name": "register", "dep-api-table": "register", "dep-api-methods": ["upsert", "select"], "tbl-fields": [{"name": "id", "context": "pk", "type": "TEXT", "crud": "RI", "search-context": "text"}, {"name": "type", "context": "type", "type": "TEXT", "crud": "CRI", "search-context": "type"}, {"name": "form", "context": "form", "description": "JSON record", "type": "JSONB", "crud": "FR"}, {"name": "password", "context": "password", "description": "Passwords are stored in table row, but not in json row", "type": "TEXT", "crud": "Cu", "calculate": "encrypt(_password)"}, {"name": "active", "context": "active", "type": "BOOLEAN", "default": "true", "crud": "ru"}, {"name": "created", "context": "created", "type": "TIMESTAMP", "crud": "r"}, {"name": "updated", "context": "updated", "type": "TIMESTAMP", "crud": "r"}], "api-overwrite": "0", "api-name": "user", "api-table": "register", "api-methods": ["upsert", "select", "test"], "api-role": "anonymous", "api-version": "1.0.0", "api-privileges": [{"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, JSONB", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, TEXT", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, JSONB", "role": "api_user"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, TEXT", "role": "api_user"}], "api-form": [{"name": "id", "context": "pk", "type": "TEXT", "json": "RI", "search": "uuid", "calculated": "uuid_generate_v4()"}, {"name": "type", "context": "type", "type": "TEXT", "json": "CRI", "const": "user"}, {"name": "app_id", "context": "name", "type": "TEXT", "json": "CRI", "default": "my-test-app@1.0.0"}, {"name": "username", "context": "email", "type": "TEXT", "json": "Cru"}, {"name": "password", "context": "password", "description": ["Passwords are stored in table row, but not in json row", "Remove the password from form before inserting", "Remove the password from form before updating"], "type": "TEXT", "json": "CuD"}], "api-test-forms": [{"type": "insert", "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.user( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}})", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"type": "user", "app_id": "my-test-app@1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}, "expected": "'{\"status\": \"200\", \"msg\": \"ok\"}'::JSONB", "description": "'user - insert test'::TEXT"}, {"type": "select", "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.user( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}} )", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"id": "my-test-app@1.0.0"}, "expected": "'[a-zA-Z\\.0-9_]+'", "description": "'user - select from {{tbl-name}} by id and check token'::TEXT"}]}
        
##########
##########
##########
 
class Template_RegisterAppInterfaceTestPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'interface-test.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '99.register-app.interface-test.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

BEGIN;
  SELECT plan(2);

  -- insert
  SELECT [[api-test-forms..type:insert..is ( {{LB_PROJECT_prefix}}_schema.{{api-name}}( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]

  -- select
  SELECT [[api-test-forms..type:select..matches( {{LB_PROJECT_prefix}}_schema.{{api-name}}( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]

  SELECT * FROM finish();

ROLLBACK;
'''.split('\n')
 
    def getDictionary(self):
        return \
			{"description": ["Single table multiple interfaces"], "type": "interface", "db-prefix": "reg", "tbl-name": "register", "tbl-prefix": "reg", "tbl-tests": ["api"], "tbl-roles": ["registrant"], "dep-api-overwrite": "0", "dep-api-name": "register", "dep-api-table": "register", "dep-api-methods": ["upsert", "select"], "tbl-fields": [{"name": "id", "context": "pk", "type": "TEXT", "crud": "RI", "search-context": "text"}, {"name": "type", "context": "type", "type": "TEXT", "crud": "CRI", "search-context": "type"}, {"name": "form", "context": "form", "description": "JSON record", "type": "JSONB", "crud": "FR"}, {"name": "password", "context": "password", "description": "Passwords are stored in table row, but not in json row", "type": "TEXT", "crud": "Cu", "calculate": "encrypt(_password)"}, {"name": "active", "context": "active", "type": "BOOLEAN", "default": "true", "crud": "ru"}, {"name": "created", "context": "created", "type": "TIMESTAMP", "crud": "r"}, {"name": "updated", "context": "updated", "type": "TIMESTAMP", "crud": "r"}], "api-overwrite": "0", "api-name": "app", "api-table": "register", "api-methods": ["upsert", "select", "test"], "api-role": "anonymous", "api-version": "1.0.0", "api-privileges": [{"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "JSONB", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "JSONB", "role": "api_user"}], "api-form": [{"name": "id", "context": "pk", "type": "TEXT", "json": "RI", "search": "uuid", "calculated": "uuid_generate_v4()"}, {"name": "type", "context": "type", "type": "TEXT", "json": "CRI", "const": "app"}, {"name": "app-name", "context": "name", "type": "TEXT", "json": "CRI", "default": "my-app"}, {"name": "version", "context": "version", "type": "TEXT", "default": "1.0.0", "json": "CR"}, {"name": "username", "context": "email", "type": "TEXT", "json": "Cru"}, {"name": "password", "context": "password", "description": ["Passwords are stored in table row, but not in json row", "Remove the password from form before inserting", "Remove the password from form before updating"], "type": "TEXT", "json": "CuD"}, {"name": "token", "context": "token", "type": "TEXT", "json": "r", "function": "sign(_payload, _secret)"}], "api-test-forms": [{"type": "insert", "description": "'app - insert test'::TEXT", "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.app( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}})", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}, "expected": "'{\"msg\": \"OK\", \"status\": \"200\"}'::JSONB"}, {"type": "select", "description": "'app - select from {{tbl-name}} by id and check token'::TEXT", "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.app( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}} )", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"id": "my-test-app@1.0.0"}, "expected": "'[a-zA-Z\\.0-9_]+'"}]}
        
##########
##########
##########
 
class Template_RegisterAppInterfaceUpsertPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'register-app.interface-upsert.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '09.register-app.interface-upsert.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db
-- custom
-- gen from default tmpl
CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.[[api-name]](_token TEXT, _json JSONB) RETURNS JSONB
AS $$
  Declare rc jsonb;
  Declare _cur_row JSONB;
  Declare _model_user JSONB;

  [[tbl-fields.*:*.Declare _{{name}} {{type}};]]

  BEGIN

    _model_user := current_setting('app.lb_register_[[api-role]]')::jsonb;

    -- figure out which token: app-token or user-token
    if not([[LB_PROJECT_prefix]]_schema.is_valid_token(_token, _model_user ->> 'role')) then
        return '{"status": "401", "msg":"Unauthorized bad token"}'::JSONB;
    end if;

    -- INSERT only

    BEGIN

        -- confirm all required attributes are in form
        if not([[api-form.json:(C)._json ? '{{name}}'. and ]]) then
           return '{"status":"400","msg":"Bad Request, missing form attribute"}'::JSONB;
        end if;

        -- make sure type is expected value
        if not(_json ->> '[[api-form.context:type.{{name}}]]' = '[[api-form.context:type.{{const}}]]') then
           return '{"status":"400", "msg":"Bad Request, type."}'::JSONB;
        end if;

        -- extract values needed for wrapper record

        _[[api-form.context:type.{{name}}]] := _json ->> '[[api-form.context:type.{{name}}]]';

        -- never store password in form
        _[[api-form.context:password.{{name}}]] := _json ->> '[[api-form.context:password.{{name}}]]';

        _[[tbl-fields.context:form.{{name}}]] := _json - '[[api-form.context:password.{{name}}]]';

        -- validate
        if length(_[[api-form.context:password.{{name}}]]) < 8 then
            return '{"status":"400", "msg":"Bad Request, validation error"}'::JSONB;
        end if;

        rc := '{"status":"200", "msg":"OK"}'::JSONB;

        INSERT INTO [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
            ([[tbl-fields.crud:(CF).{{tbl-prefix}}_{{name}}., ]])
          VALUES
            ([[tbl-fields.crud:(CF)._{{name}}., ]] );

    EXCEPTION
        WHEN unique_violation THEN
            rc := '{"status":"400", "msg":"Bad Request, duplicate error"}'::JSONB;
        WHEN check_violation then
            rc := '{"status":"400", "msg":"Bad Request, validation error"}'::JSONB;
        WHEN others then
            rc := format('{"status":"500", "msg":"unknown insertion error", "form":%s}',_form)::JSONB;
    END;

    RETURN rc;
  END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.[[api-name]](_json JSONB) RETURNS JSONB
AS $$
DECLARE _token TEXT;
DECLARE _jwt TEXT;
DECLARE _anonymous JSONB;
BEGIN
    -- this is an INSERT function special case
    -- remove password
    _anonymous := current_setting('app.lb_register_anonymous')::JSONB-'password';
    -- inject the type attribute
    _anonymous := _anonymous || '{"type": "[[api-name]]"}'::JSONB;
    -- get pw from model user
	_jwt := current_setting('app.lb_register_jwt')::JSONB ->> 'password';
	-- make the token
	_token := sign(_anonymous::JSON, _jwt) ;
	return [[LB_PROJECT_prefix]]_schema.[[api-name]](_token, _json);
END;
$$ LANGUAGE plpgsql;

[[api-privileges..type:FUNCTION..GRANT {{privilege}} ON {{type}} {{LB_PROJECT_prefix}}_schema.{{api-name}} ({{parameters}}) TO {{role}};]]
-- END XXXXXXXX
'''.split('\n')
 
    def getDictionary(self):
        return \
			{"description": ["Single table multiple interfaces"], "type": "interface", "db-prefix": "reg", "tbl-name": "register", "tbl-prefix": "reg", "tbl-tests": ["api"], "tbl-roles": ["registrant"], "dep-api-overwrite": "0", "dep-api-name": "register", "dep-api-table": "register", "dep-api-methods": ["upsert", "select"], "tbl-fields": [{"name": "id", "context": "pk", "type": "TEXT", "crud": "RI", "search-context": "text"}, {"name": "type", "context": "type", "type": "TEXT", "crud": "CRI", "search-context": "type"}, {"name": "form", "context": "form", "description": "JSON record", "type": "JSONB", "crud": "FR"}, {"name": "password", "context": "password", "description": "Passwords are stored in table row, but not in json row", "type": "TEXT", "crud": "Cu", "calculate": "encrypt(_password)"}, {"name": "active", "context": "active", "type": "BOOLEAN", "default": "true", "crud": "ru"}, {"name": "created", "context": "created", "type": "TIMESTAMP", "crud": "r"}, {"name": "updated", "context": "updated", "type": "TIMESTAMP", "crud": "r"}], "api-overwrite": "0", "api-name": "app", "api-table": "register", "api-methods": ["upsert", "select", "test"], "api-role": "anonymous", "api-version": "1.0.0", "api-privileges": [{"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "JSONB", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "JSONB", "role": "api_user"}], "api-form": [{"name": "id", "context": "pk", "type": "TEXT", "json": "RI", "search": "uuid", "calculated": "uuid_generate_v4()"}, {"name": "type", "context": "type", "type": "TEXT", "json": "CRI", "const": "app"}, {"name": "app-name", "context": "name", "type": "TEXT", "json": "CRI", "default": "my-app"}, {"name": "version", "context": "version", "type": "TEXT", "default": "1.0.0", "json": "CR"}, {"name": "username", "context": "email", "type": "TEXT", "json": "Cru"}, {"name": "password", "context": "password", "description": ["Passwords are stored in table row, but not in json row", "Remove the password from form before inserting", "Remove the password from form before updating"], "type": "TEXT", "json": "CuD"}, {"name": "token", "context": "token", "type": "TEXT", "json": "r", "function": "sign(_payload, _secret)"}], "api-test-forms": [{"type": "insert", "description": "'app - insert test'::TEXT", "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.app( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}})", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}, "expected": "'{\"msg\": \"OK\", \"status\": \"200\"}'::JSONB"}, {"type": "select", "description": "'app - select from {{tbl-name}} by id and check token'::TEXT", "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.app( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}} )", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"id": "my-test-app@1.0.0"}, "expected": "'[a-zA-Z\\.0-9_]+'"}]}
        
##########
##########
##########
 
class Template_RegisterAppInterfaceSelectPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'interface-select.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '09.register-app.interface-select.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

-------------------------------
-- Select
---------

CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.[[api-name]](_token TEXT, _form_text TEXT) RETURNS JSONB
AS $$
  DECLARE rc TEXT;
  DECLARE secret TEXT;
  DECLARE rc_form JSONB;
  DECLARE _model_user JSONB;

  [[tbl-fields.*:*.Declare _{{name}} {{type}};]]

BEGIN

    _model_user := current_setting('app.lb_register_anonymous')::jsonb;

    -- figure out which token: app-token or user-token
    if not([[db-prefix]]_schema.is_valid_token(_token, _model_user ->> 'role')) then
        return '{"status": "401"}'::JSONB;
    end if;

    -- convert Text to JSONB to ref
    _form := _form_text::JSONB;

    -- confirm proper attributes in _form
    if not(_form ? 'id') then
        return '{"status":"400", "msg":"Bad Request id"}'::JSONB;
    end if;

    -- set where clause
    _id = _form ->> 'id';

    -- go get the data

    select [[tbl-prefix]]_[[tbl-fields.context:form.{{name}}]]
    into rc_form
    from [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
    where [[tbl-prefix]]_[[api-form.context:uuid-TEXT.{{name}}]]= _id;

    if rc_form is NULL then
      rc_form := '{"status":"204", "msg":"No Content","result": {}}'::JSONB;
    else
      rc_form :=  format('{"status":"200", "result":%s}',rc_form::TEXT)::JSONB;
    end if;

    RETURN rc_form;
END;  $$ LANGUAGE plpgsql;

GRANT EXECUTE ON FUNCTION
  [[LB_PROJECT_prefix]]_schema.[[api-name]](
  TEXT, TEXT
  ) TO anonymous;

[[api-privileges..type:FUNCTION..GRANT {{privilege}} ON {{type}} {{LB_PROJECT_prefix}}_schema.{{api-name}} ({{parameters}}) TO {{role}};]]

'''.split('\n')
 
    def getDictionary(self):
        return \
			{"description": ["Single table multiple interfaces"], "type": "interface", "db-prefix": "reg", "tbl-name": "register", "tbl-prefix": "reg", "tbl-tests": ["api"], "tbl-roles": ["registrant"], "dep-api-overwrite": "0", "dep-api-name": "register", "dep-api-table": "register", "dep-api-methods": ["upsert", "select"], "tbl-fields": [{"name": "id", "context": "pk", "type": "TEXT", "crud": "RI", "search-context": "text"}, {"name": "type", "context": "type", "type": "TEXT", "crud": "CRI", "search-context": "type"}, {"name": "form", "context": "form", "description": "JSON record", "type": "JSONB", "crud": "FR"}, {"name": "password", "context": "password", "description": "Passwords are stored in table row, but not in json row", "type": "TEXT", "crud": "Cu", "calculate": "encrypt(_password)"}, {"name": "active", "context": "active", "type": "BOOLEAN", "default": "true", "crud": "ru"}, {"name": "created", "context": "created", "type": "TIMESTAMP", "crud": "r"}, {"name": "updated", "context": "updated", "type": "TIMESTAMP", "crud": "r"}], "api-overwrite": "0", "api-name": "app", "api-table": "register", "api-methods": ["upsert", "select", "test"], "api-role": "anonymous", "api-version": "1.0.0", "api-privileges": [{"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "JSONB", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "JSONB", "role": "api_user"}], "api-form": [{"name": "id", "context": "pk", "type": "TEXT", "json": "RI", "search": "uuid", "calculated": "uuid_generate_v4()"}, {"name": "type", "context": "type", "type": "TEXT", "json": "CRI", "const": "app"}, {"name": "app-name", "context": "name", "type": "TEXT", "json": "CRI", "default": "my-app"}, {"name": "version", "context": "version", "type": "TEXT", "default": "1.0.0", "json": "CR"}, {"name": "username", "context": "email", "type": "TEXT", "json": "Cru"}, {"name": "password", "context": "password", "description": ["Passwords are stored in table row, but not in json row", "Remove the password from form before inserting", "Remove the password from form before updating"], "type": "TEXT", "json": "CuD"}, {"name": "token", "context": "token", "type": "TEXT", "json": "r", "function": "sign(_payload, _secret)"}], "api-test-forms": [{"type": "insert", "description": "'app - insert test'::TEXT", "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.app( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}})", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}, "expected": "'{\"msg\": \"OK\", \"status\": \"200\"}'::JSONB"}, {"type": "select", "description": "'app - select from {{tbl-name}} by id and check token'::TEXT", "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.app( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}} )", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"id": "my-test-app@1.0.0"}, "expected": "'[a-zA-Z\\.0-9_]+'"}]}
        
##########
##########
##########
 
class Template_RegisterUserInterfaceTestPgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'interface-test.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '99.register-user.interface-test.pg.sql'
    def getTemplateList(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

BEGIN;
  SELECT plan(2);

  -- insert
  SELECT [[api-test-forms..type:insert..is ( {{LB_PROJECT_prefix}}_schema.{{api-name}}( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]

  -- select
  SELECT [[api-test-forms..type:select..matches( {{LB_PROJECT_prefix}}_schema.{{api-name}}( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]

  SELECT * FROM finish();

ROLLBACK;
'''.split('\n')
 
    def getDictionary(self):
        return \
			{"description": ["Single table multiple interfaces"], "type": "interface", "db-prefix": "reg", "tbl-name": "register", "tbl-prefix": "reg", "tbl-tests": ["api"], "tbl-roles": ["registrant"], "dep-api-overwrite": "0", "dep-api-name": "register", "dep-api-table": "register", "dep-api-methods": ["upsert", "select"], "tbl-fields": [{"name": "id", "context": "pk", "type": "TEXT", "crud": "RI", "search-context": "text"}, {"name": "type", "context": "type", "type": "TEXT", "crud": "CRI", "search-context": "type"}, {"name": "form", "context": "form", "description": "JSON record", "type": "JSONB", "crud": "FR"}, {"name": "password", "context": "password", "description": "Passwords are stored in table row, but not in json row", "type": "TEXT", "crud": "Cu", "calculate": "encrypt(_password)"}, {"name": "active", "context": "active", "type": "BOOLEAN", "default": "true", "crud": "ru"}, {"name": "created", "context": "created", "type": "TIMESTAMP", "crud": "r"}, {"name": "updated", "context": "updated", "type": "TIMESTAMP", "crud": "r"}], "api-overwrite": "0", "api-name": "user", "api-table": "register", "api-methods": ["upsert", "select", "test"], "api-role": "anonymous", "api-version": "1.0.0", "api-privileges": [{"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, JSONB", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, TEXT", "role": "anonymous"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, JSONB", "role": "api_user"}, {"privilege": "EXECUTE", "type": "FUNCTION", "parameters": "TEXT, TEXT", "role": "api_user"}], "api-form": [{"name": "id", "context": "pk", "type": "TEXT", "json": "RI", "search": "uuid", "calculated": "uuid_generate_v4()"}, {"name": "type", "context": "type", "type": "TEXT", "json": "CRI", "const": "user"}, {"name": "app_id", "context": "name", "type": "TEXT", "json": "CRI", "default": "my-test-app@1.0.0"}, {"name": "username", "context": "email", "type": "TEXT", "json": "Cru"}, {"name": "password", "context": "password", "description": ["Passwords are stored in table row, but not in json row", "Remove the password from form before inserting", "Remove the password from form before updating"], "type": "TEXT", "json": "CuD"}], "api-test-forms": [{"type": "insert", "template": "SELECT [[api-test-forms..type:insert..is ( reg_schema.user( {{token}}, '{{form}}'::JSONB )::JSONB, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}})", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"type": "user", "app_id": "my-test-app@1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}, "expected": "'{\"status\": \"200\", \"msg\": \"ok\"}'::JSONB", "description": "'user - insert test'::TEXT"}, {"type": "select", "template": "SELECT [[api-test-forms..type:select..matches( reg_schema.user( {{token}}, '{{form}}'::JSONB )::TEXT, {{expected}}, {{description}} );]]", "token": "sign('{{pattern}}'::json, {{password}} )", "pattern": {"username": "testuser@register.com", "role": "anonymous"}, "password": "current_setting('app.jwt_secret')", "form": {"id": "my-test-app@1.0.0"}, "expected": "'[a-zA-Z\\.0-9_]+'", "description": "'user - select from {{tbl-name}} by id and check token'::TEXT"}]}
        
##########
##########
##########
 
class Template_DbDatabasePgJson(Template):
 
    def __init__(self):
        super().__init__({})
 
    def process(self):
        super().process()
        print('{}'.format('\n'.join(self)))
        self.copy(self.getOutputFolder(), self.getOutputName())
        self.permissions(self.getOutputFolder(), self.getOutputName())
        return self
 
    def getInputTemplate(self): return 'database.pg.tmpl'
    def getOutputFolder(self): return '/Users/jameswilfong/..LyttleBit/dev/code/00-zadopt-a-drain/#21.refactor.reorganize.folders/zadopt-a-drain/db/sql'
    def getOutputName(self): return '01.db.database.pg.sql'
    def getTemplateList(self):
        return '''
\c postgres

DROP DATABASE IF EXISTS [[LB_PROJECT_prefix]]_db;

CREATE DATABASE [[LB_PROJECT_prefix]]_db;

-- SET DB

\c [[LB_PROJECT_prefix]]_db

create schema if not exists [[LB_PROJECT_prefix]]_schema;
[[db-extensions.*:*.CREATE EXTENSION IF NOT EXISTS {{name}};.; ]]
-- db-extensions

SET search_path TO [[LB_PROJECT_prefix]]_schema, public; -- put everything in [[LB_PROJECT_prefix]]_schema;

-- the following should be set by the admin manually, it is set here for convenience
-- models
[[models.*:*.ALTER DATABASE {{LB_PROJECT_prefix}}_db SET "{{app-key}}" TO \'{{model}}\';]]

ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.jwt_secret" TO '[[LB_REGISTER_JWT_MODEL_password]]';
/*
x ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_register_jwt" TO '[[LB_REGISTER_JWT_MODEL]]';
x ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_register_anonymous" TO '[[LB_REGISTER_GUEST_MODEL]]';
x ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_register_editor" TO '[[LB_REGISTER_EDITOR_MODEL]]';
x ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_register_registrant" TO '[[LB_REGISTER_REGISTRANT_MODEL]]';
x ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_register_registrar" TO '[[LB_REGISTER_REGISTRAR_MODEL]]';
x ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_register_testuser" TO '[[LB_TEST_USER]]';

ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_web_anonymous" TO 'LB_WEB_ANONYMOUS]]';
ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_web_anonymous_role" TO 'LB_WEB_ANONYMOUS_ROLE]]';
ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_web_anonymous_password" TO 'LB_WEB_ANONYMOUS_PASSWORD]]';
ALTER DATABASE [[LB_PROJECT_prefix]]_db SET "app.lb_admin_registrar_password" TO 'LB_ADMIN_REGISTRAR_PASSWORD]]';
*/

/*
CREATE OR REPLACE FUNCTION log_last_name_changes()
  RETURNS trigger AS
$BODY$
BEGIN
   IF NEW.last_name <> OLD.last_name THEN
       INSERT INTO employee_audits(employee_id,last_name,changed_on)
       VALUES(OLD.id,OLD.last_name,now());
   END IF;

   RETURN NEW;
END;
$BODY$
*/
'''.split('\n')
 
    def getDictionary(self):
        return \
			{
			    "db-type": "postgres",
			    "db-type-abbr": "pg",
			    "type": "database",
			    "db-extensions": [{"name": "pgcrypto"}, {"name": "pgtap"}, {"name": "pgjwt"}, {"name": "\"uuid-ossp\""}],
			    "model-template": "[[models.*:*.ALTER DATABASE {{LB_PROJECT_prefix}}_db SET \"{{app-key}}\" TO '{{model}}';]]",
			
			    "models": [
			
			        {
			            "type": "model",
			            "env-key": "LB_REGISTER_JWT_MODEL",
			            "app-key": "app.lb_register_jwt",
			            "description": ["JSON WEB Token"],
			            "model": {
			                "username": "jwt@register.com",
			                "email": "jwt@register.com",
			                "password": "PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG",
			                "role": "jwt"
			            }
			        },
			        {
			            "type": "model",
			            "env-key": "LB_REGISTER_ANONYMOUS",
			            "app-key": "app.lb_register_anonymous",
			            "description": ["define me"],
			            "model":{"username":"anonymous@register.com",
			                     "email":"anonymous@register.com",
			                     "password":"g1G!gggg",
			                     "role":"anonymous"}
			        },
			        {
			            "type": "model",
			            "env-key": "LB_REGISTER_EDITOR_MODEL",
			            "app-key": "app.lb_register_editor",
			            "description": ["define me"],
			            "model": {"username":"editor@register.com",
			                      "email":"editor@register.com",
			                      "password":"g1G!gggg",
			                      "role":"editor"}
			        },
			        {
			            "type": "model",
			            "env-key": "LB_REGISTER_REGISTRANT_MODEL",
			            "app-key": "app.lb_register_registrant",
			            "description": ["define me"],
			            "model": {"username":"registrant@register.com",
			                      "email":"registrant@register.com",
			                      "password":"g1G!gggg",
			                      "role":"registrant"}
			        },
			        {
			            "type": "model",
			            "env-key": "LB_REGISTER_REGISTRAR_MODEL",
			            "app-key": "app.lb_register_registrar",
			            "description": ["define me"],
			            "model": {"username":"registrar@register.com",
			                      "email":"registrar@register.com",
			                      "password":"g1G!gggg",
			                      "role":"registrar"}
			        },
			        {
			            "type": "model",
			            "env-key": "LB_TEST_USER",
			            "app-key": "app.lb_register_testuser",
			            "description": ["define me"],
			            "model": {"type":"app",
			                      "app-name":"my-app",
			                      "version": "1.0.0",
			                      "username":"testuser@register.com",
			                      "email":"testuser@register.com",
			                      "password":"g1G!gggg",
			                      "role":"registrar"}
			        }
			    ]
			}
			
        
##########
##########
##########
def main():
    appSettings = AppSettings()
    if 'LB-TESTING' in os.environ:
        appSettings = AppSettingsTest()
    Template_DockerfileWebDockerfileWebDkJson()
    Template_DockerComposeDockerComposeDcJson()
    Template_DockerfileDbDockerfileDbDkJson()
    Template_PgEnvironmentEnvJson()
    Template_DockerfileAdminDockerfileAdminDkJson()
    Template_TestJwtTokenTestPgJson()
    Template_RegisterTablePgJson()
    Template_NuxtjsWebScriptShShJson()
    Template_DownScriptShShJson()
    Template_NuxtjsAdminScriptShShJson()
    Template_UpScriptShShJson()
    Template__confScriptShShJson()
    Template_DbScriptShShJson()
    Template_AuthenticatorRolePgJson()
    Template_AnonymousRolePgJson()
    Template_EditorRolePgJson()
    Template_Api_userRolePgJson()
    Template_Get_idFunctionPgJson()
    Template_Is_valid_tokenFunctionPgJson()
    Template_Get_app_idFunctionPgJson()
    Template_Validate_passwordValidateFunctionPgJson()
    Template_Get_roleFunctionPgJson()
    Template_Get_usernameFunctionPgJson()
    Template_RegisterUserInitializePgJson()
    Template_RegisterAppInitializePgJson()
    Template_RegisterUserInterfaceSelectPgJson()
    Template_RegisterUserInterfaceUpsertPgJson()
    Template_RegisterAppInterfaceTestPgJson()
    Template_RegisterAppInterfaceUpsertPgJson()
    Template_RegisterAppInterfaceSelectPgJson()
    Template_RegisterUserInterfaceTestPgJson()
    Template_DbDatabasePgJson()
if __name__ == "__main__":
    main()
