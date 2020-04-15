from pathlib import Path
from template_file import TemplateFile
# file: authenticator.role.pg.tmpl
class TemplateFileAuthenticatorRoleCreatePgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('authenticator.role.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            'CREATE ROLE [[role-name]] NOINHERIT LOGIN PASSWORD \'[[LB_SECRET_PASSWORD]]\';',
        ])
# file: credentials.api.insert.pg.tmpl
class TemplateFileCredentialsApiInsertPgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('credentials.api.insert.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '-------------------------------',
            '-- INSERT',
            '---------',
            '-- [[api-name]](TEXT, TEXT)',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.[[api-name]](username TEXT, password TEXT) RETURNS TEXT',
            'AS $$',
            '    Declare rc TEXT;',
            '    Declare id int;',
            '    Declare role TEXT;',
            '  BEGIN',
            '    rc := \'{"result":-1}\';',
            '    role := \'guest\';',
            '    -- guest should be',
            '    BEGIN',
            '          INSERT INTO [[db-prefix]]_schema.[[tbl-name]]',
            '            (crd_email, crd_password, crd_role)',
            '            VALUES',
            '            (username, crypt(password, gen_salt(\'bf\', 8)), role);',
            '',
            '      rc := \'{"result":1}\';',
            '    EXCEPTION WHEN unique_violation THEN',
            '      rc := \'{"result":2}\';',
            '    END;',
            '    RETURN rc;',
            '  END;',
            '$$ LANGUAGE plpgsql;',
        ])
# file: credentials.api.select.pg.tmpl
class TemplateFileCredentialsApiSelectPgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('credentials.api.select.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '--------------------------------------------',
            '-- Select AKA signin',
            '-- logged in version',
            '---------',
            '-- [[api-name]](TEXT,int,TEXT,TEXT)',
            '-- change while logged in',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.credential(_token TEXT, username TEXT, password TEXT) RETURNS TEXT',
            'AS $$',
            '  DECLARE rc TEXT;',
            '  DECLARE payload TEXT;',
            '  DECLARE secret varchar(500);',

            'BEGIN',
            '  -- requires a valid token',
            '  -- returns a token given a valid un and pw',
            '  -- secret needs to be moved to environment variable',
            '  secret := \'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG\';',
            '  rc := \'{"result":-1}\';',
            '  if [[db-prefix]]_schema.is_valid_token(_token, \'guest\') then',
            '    SELECT \'{"id":\' || [[tbl-prefix]]_id || \',"username":"\' || [[tbl-prefix]]_email || \'","role":"\' || [[tbl-prefix]]_role || \'"}\'',
            '      into payload FROM [[db-prefix]]_schema.[[tbl-name]]',
            '      WHERE [[tbl-prefix]]_email = lower(username)',
            '      AND [[tbl-prefix]]_password = crypt(password, [[tbl-prefix]]_password);',
            '    if FOUND then',
            '      rc := format(\'{"token":"%s"}\',  sign(payload::json, secret));',
            '    else',
            '      rc := \'{"result":-2}\';',
            '    end if;',
            '  end if;',
            '  RETURN rc;',
            'END;  $$ LANGUAGE plpgsql;',
        ])
# file: credentials.api.update.pg.tmpl
class TemplateFileCredentialsApiUpdatePgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('credentials.api.update.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '--------------------------------------------',
            '-- Update',
            '-- logged in version',
            '---------',
            '-- [[api-name]](TEXT,int,TEXT,TEXT)',
            '-- change while logged in',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.[[api-name]](_token text, id int, email text, password text) RETURNS TEXT',
            'AS $$',
            '    Declare rc TEXT;',
            '  BEGIN',
            '    rc := \'{"result":-1}\';',
            '    rc := format(\'{"result":%s}\', id);',
            '    if [[db-prefix]]_schema.is_valid_token(_token, \'[[api-role]]\') then',
            '      rc := \'{"result":-2}\';',
            '      update [[db-prefix]]_schema.[[api-db-api-table-table]]',
            '        set',
            '          crd_email=email,',
            '          crd_password=crypt(password, gen_salt(\'bf\', 8))',
            '        where crd_id=id',
            '        and crd_email=[[db-prefix]]_schema.get_username(_token);',
            '      if FOUND then',
            '        rc := \'{"result":1}\';',
            '      end if;',
            '    end if;',
            '    RETURN rc;',
            '  END;',
            '$$ LANGUAGE plpgsql;',
        ])
# file: credentials.db-api-table-table.pg.tmpl._DEP
class TemplateFileCredentialsTablePgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('credentials.db-api-table-table.pg.tmpl._DEP')
        self.add([
            '---- SET DB',
            '\c [[db-prefix]]_db',
            'create db-api-table-table if not exists',
            '[[db-prefix]]_schema.[[tbl-name]] (',
            '  [[fields]]',
            ');',
            'CREATE UNIQUE INDEX IF NOT EXISTS [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[db-prefix]]_schema.[[tbl-name]]([[tbl-prefix]]_id int4_ops);',
            'CREATE UNIQUE INDEX IF NOT EXISTS index_[[tbl-name]]_on_[[tbl-prefix]]_email ON [[db-prefix]]_schema.[[tbl-name]]([[tbl-prefix]]_email text_ops);',
        ])
# file: database.pg.tmpl
class TemplateFileDatabasePgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('database.pg.tmpl')
        self.add([
            '\c postgres',
            'DROP DATABASE IF EXISTS [[db-prefix]]_db;',
            'CREATE DATABASE [[db-prefix]]_db;',
            '-- SET DB',
            '\c [[db-prefix]]_db',
            '',
            'create schema if not exists [[db-prefix]]_schema;',
            '[[extensions]]',
            '',
            'SET search_path TO [[db-prefix]]_schema, public; -- put everything in [[db-prefix]]_schema;',
        ])
# file: docker-compose.pg.tmpl
class TemplateFileDockerComposePgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('docker-compose.pg.tmpl')
        self.add([
            'version: \'3\'',
            '# docker-compose up',
            '# ref: http://postgrest.org/en/v6.0/install.html#docker',
            '# ref: https://github.com/mattddowney/compose-postgrest/blob/master/docker-compose.yml',
            '',
            'services:',
            '  #web:',
            '  #  container_name: [[app-name]]',
            '  #  image: [[app-owner]]/[[app-name]]',
            '  #  build:',
            '  #    context: ./[[app-name]]-web/',
            '  #  command: >',
            '  #    bash -c "npm install && npm run dev"',
            '  #  volumes:',
            '  #    - ./[[app-name]]-web:/usr/src',
            '  #  ports:',
            '  #    - "3000:3000"',
            '',
            '  #############',
            '  # POSTGRES',
            '  #########',
            '  db-api-table:',
            '    build: ./pg-database',
            '    ports:',
            '      - "5433:5432"',
            '    environment:',
            '      - POSTGRES_USER=postgres',
            '      - POSTGRES_PASSWORD=[[LB_SECRET_PASSWORD]]',
            '      - POSTGRES_DB=[[db-prefix]]_db',
            '      - DB_ANON_ROLE=guest',
            '      - DB_SCHEMA=[[db-prefix]]_schema',
            '      - DB_NAME=postgres',
            '      - DB_USER=postgres',
            '      - DB_PASS=[[LB_JWT_PASSWORD]]',
            '',
            '    volumes:',
            '      # anything in initdb directory is created in the database',
            '      # see "How to extend this image" section at https://hub.docker.com/r/_/postgres/',
            '      - "./[[db-prefix]]-db-api-table/pg-database/db-api-table-script/compiled-script:/docker-entrypoint-initdb.d"',
            '      # Uncomment this if you want to persist the data.',
            '      - "~/.data/[[db-prefix]]_db/pgdata:/var/lib/postgresql/data"',
            '    networks:',
            '      - postgrest-backend',
            '    restart: always',
            '  ##########',
            '  # POSTGRREST',
            '  #####',
            '  api:',
            '    container_name: postgrest',
            '    image: postgrest/postgrest:latest',
            '    ports:',
            '      - "3100:3000"',
            '    environment:',
            '      # The standard connection URI format, documented at',
            '      # https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING',
            '      PGRST_DB_URI: postgres://postgres:[[LB_SECRET_PASSWORD]]@db-api-table:5432/[[db-prefix]]_db',
            '      PGRST_DB_SCHEMA: [[db-prefix]]_schema',
            '      PGRST_DB_ANON_ROLE: guest',
            '',
            '    depends_on:',
            '      - db-api-table',
            '    links:',
            '      - db-api-table:db-api-table',
            '',
            '    networks:',
            '      - postgrest-backend',
            '    restart: always',
            'networks:',
            '  postgrest-backend:',
            '    driver: bridge',
        ])
# file: dockerfile.pg.tmpl
class TemplateFileDockerfilePgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('dockerfile.pg.tmpl')
        self.add([
            'FROM postgres:11',
            '# build postres container with jwt included',
            '',
            'RUN apt-get update && apt-get install -y make git postgresql-server-dev-11 postgresql-11-pgtap',
            '',
            '# set up jwt tokens',
            'RUN mkdir "/postgres-jwt"',
            'WORKDIR "/postgres-jwt"',
            'COPY . .',
            'RUN make && make install',
            '',
            '# fire up postres with new config file',
            'CMD ["postgres"]',
        ])
# file: get_id.function.pg.tmpl
class TemplateFileGet_idFunctionPgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('get_id.function.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '----------------------------------------------',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.get_id(_token text) RETURNS TEXT',
            'AS $$',
            '  DECLARE data TEXT;',
            '  DECLARE secret TEXT;',
            'BEGIN',
            '',
            '  -- this is bad but ok for dev. Need to figure out how to enable the environment variables in postgres',
            '  secret := \'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG\';',
            '  select payload ->> \'id\' as id into data  from verify(_token, secret);',
            '  -- parce data',
            '',
            '  RETURN data;',
            'END;  $$ LANGUAGE plpgsql;',
        ])
# file: get_role.function.pg.tmpl
class TemplateFileGet_roleFunctionPgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('get_role.function.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '----------------------------------------------',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.get_role(_token text) RETURNS TEXT',
            'AS $$',
            '  DECLARE data TEXT;',
            '  DECLARE secret TEXT;',
            'BEGIN',
            '  ',
            '  -- this is bad but ok for dev. Need to figure out how to enable the environment variables in postgres',
            '  secret := \'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG\';',
            '  select payload ->> \'role\' as role into data  from verify(_token, secret);',
            '  -- parce data',
            '',
            '  RETURN data;',
            'END;  $$ LANGUAGE plpgsql;',
        ])
# file: get_username.function.pg.tmpl
class TemplateFileGet_usernameFunctionPgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('get_username.function.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '----------------------------------------------',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.get_username(_token text) RETURNS TEXT',
            'AS $$',
            '  DECLARE data TEXT;',
            '  DECLARE secret TEXT;',
            'BEGIN',
            '',
            '  -- this is bad but ok for dev. Need to figure out how to enable the environment variables in postgres',
            '  secret := \'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG\';',
            '  select payload ->> \'username\' as username into data  from verify(_token, secret);',
            '  -- parce data',
            '',
            '  RETURN data;',
            'END;  $$ LANGUAGE plpgsql;',
        ])
# file: is_valid_token.function.pg.tmpl
class TemplateFileIs_valid_tokenFunctionPgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('is_valid_token.function.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '---------------------------------------------',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.is_valid_token(_token text) RETURNS Boolean',
            'AS $$',
            '  DECLARE good Boolean;',
            '  DECLARE secret TEXT;',
            'BEGIN',
            '  -- cloak the secret',
            '  -- process the token',
            '  -- return true/false',
            '  good:=false;',
            '  -- this is bad but ok for dev. Need to figure out how to enable the environment variables in postgres',
            '  secret := \'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG\';',
            '  select valid into good from verify(_token, secret);',
            '  RETURN good;',
            'END;  $$ LANGUAGE plpgsql;',
            '--------------------------------------------',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.is_valid_token(_token TEXT, role TEXT) RETURNS Boolean',
            'AS $$',
            '  DECLARE good Boolean;',
            '  DECLARE actual_role TEXT;',
            '  DECLARE secret TEXT;',
            'BEGIN',
            '  -- cloak the secret',
            '  -- process the token',
            '  -- return true/false',
            '  good:=false;',
            '  -- this is bad but ok for dev. Need to figure out how to enable the environment variables in postgres',
            '  secret := \'PASSWORD.must.BE.AT.LEAST.32.CHARS.LONG\';',
            '  select valid into good from verify(_token, secret);',
            '',
            '  select payload ->> \'role\' as role into actual_role  from verify(_token, secret);',
            '',
            '  if good and role != actual_role then',
            '    good := false;',
            '  end if;',
            '',
            '  RETURN good;',
            'END;  $$ LANGUAGE plpgsql;',
        ])
# file: role-create.pg.tmpl._DEP
class TemplateFileRoleCreatePgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('role-create.pg.tmpl._DEP')
        self.add([
            '\c [[db-prefix]]_db',
            'CREATE ROLE [[role-name]];',
        ])
# file: db-api-table-table-api-insert.pg.tmpl
class TemplateFileTableApiInsertPgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('db-api-table-table-api-insert.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '-------------------------------',
            '-- INSERT',
            '---------',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.[[api-name]](',
            '  _token TEXT,',
            '  [[insert-parameters]]',
            ') RETURNS TEXT',
            'AS $$',
            '    Declare rc TEXT;',
            '    Declare role TEXT;',
            '    Declare id int;',
            '  BEGIN',
            '    rc := \'{"result",-1}\';',
            '    role := [[db-prefix]]_schema.get_role(_token);',
            '',
            '    BEGIN',
            '      if [[db-prefix]]_schema.is_valid_token(_token,\'[[tbl-role]]\') then',
            '        rc := \'{"result",-2}\';',
            '        INSERT INTO api_schema.users',
            '          ([[insert-columns]])',
            '          VALUES',
            '          ([[insert-values]]);',
            '          rc := \'{"result":1}\';',
            '      end if;',
            '    EXCEPTION WHEN unique_violation THEN',
            '      rc := \'{"result",-3}\';',
            '    END;',
            '    RETURN rc;',
            '  END;',
            '$$ LANGUAGE plpgsql;',
        ])
# file: db-api-table-table-api-select.pg.tmpl
class TemplateFileTableApiSelectPgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('db-api-table-table-api-select.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '-------------------------------',
            '-- Select',
            '---------',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.[[tbl-name]](_token text, id int) RETURNS TEXT',
            'AS $$',
            '  DECLARE rc TEXT;',
            '  DECLARE secret TEXT;',
            'BEGIN',
            '  -- returns a single user\'s info',
            '  -- need to figure out postgres environment variables',
            '',
            '  rc := \'{"result":-1}\';',
            '',
            '  if [[db-prefix]]_schema.is_valid_token(_token) then',
            '    select',
            '    \'{\' || [[select-columns]] || \'}\'',
            '    into rc from',
            '    [[db-prefix]]_schema.[[tbl-name]]',
            '    where [[tbl-prefix]]_id=id;',
            '    if rc is NULL then',
            '      rc := \'{"result":-1}\';',
            '    end if;',
            '  end if;',
            '',
            '  RETURN rc;',
            'END;  $$ LANGUAGE plpgsql;',
        ])
# file: db-api-table-table-api-update.pg.tmpl
class TemplateFileTableApiUpdatePgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('db-api-table-table-api-update.pg.tmpl')
        self.add([
            '\c [[db-prefix]]_db',
            '-------------------------------',
            '-- Update',
            '---------',
            'CREATE OR REPLACE FUNCTION',
            '[[db-prefix]]_schema.[[api-name]](_token text, [[update-parameters]]) RETURNS TEXT',
            'AS $$',
            '    Declare rc TEXT;',
            '  BEGIN',
            '    rc := \'{"result":-1}\';',
            '    if [[db-prefix]]_schema.is_valid_token(token, \'[[tbl-role]]\') then',
            '      rc := \'{"result":-2}\';',
            '      rc := format(\'{"result":"%s"}\',[[db-prefix]]_schema.get_username(token));',
            '      update [[db-prefix]]_schema.[[tbl-name]]',
            '        set',
            '          [[update-columns]]',
            '          ,[[tbl-prefix]]_updated=CURRENT_DATE',
            '        where [[tbl-prefix]]_id=id;',
            '      if FOUND then',
            '        rc := \'{"result":1}\';',
            '      end if;',
            '    end if;',
            '    RETURN rc;',
            '  END;',
            '$$ LANGUAGE plpgsql;',
        ])
# file: db-api-table-table.pg.tmpl
class TemplateFileTablePgConfigTmplMock(TemplateFile):
    def __init__(self, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.default_folder = '{}/temp'.format(str(Path.home()))
        if foldername == None:
            self.setFolderName(self.default_folder)
        if filename == None:
            self.setFileName('db-api-table-table.pg.tmpl')
        self.add([
            '-- Default Table Template',
            '---- SET DB',
            '\c [[db-prefix]]_db',
            'create db-api-table-table if not exists',
            '[[db-prefix]]_schema.[[tbl-name]] (',
            '  [[fields]]',
            ');',
            'CREATE UNIQUE INDEX IF NOT EXISTS [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[db-prefix]]_schema.[[tbl-name]]([[tbl-prefix]]_id int4_ops);',
            '--CREATE UNIQUE INDEX IF NOT EXISTS index_[[tbl-name]]_on_[[tbl-prefix]]_email ON [[db-prefix]]_schema.[[tbl-name]]([[tbl-prefix]]_email text_ops);',
        ])
 
def main():
     TemplateFileAuthenticatorRoleCreatePgConfigTmplMock().write()
     TemplateFileCredentialsApiInsertPgConfigTmplMock().write()
     TemplateFileCredentialsApiSelectPgConfigTmplMock().write()
     TemplateFileCredentialsApiUpdatePgConfigTmplMock().write()
     TemplateFileCredentialsTablePgConfigTmplMock().write()
     TemplateFileDatabasePgConfigTmplMock().write()
     TemplateFileDockerComposePgConfigTmplMock().write()
     TemplateFileDockerfilePgConfigTmplMock().write()
     TemplateFileGet_idFunctionPgConfigTmplMock().write()
     TemplateFileGet_roleFunctionPgConfigTmplMock().write()
     TemplateFileGet_usernameFunctionPgConfigTmplMock().write()
     TemplateFileIs_valid_tokenFunctionPgConfigTmplMock().write()
     TemplateFileRoleCreatePgConfigTmplMock().write()
     TemplateFileTableApiInsertPgConfigTmplMock().write()
     TemplateFileTableApiSelectPgConfigTmplMock().write()
     TemplateFileTableApiUpdatePgConfigTmplMock().write()
     TemplateFileTablePgConfigTmplMock().write()
 
if __name__ == "__main__":
    main()
