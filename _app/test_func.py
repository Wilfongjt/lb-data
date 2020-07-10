def test_db():
    return {
    "db-type": "postgres",
    "db-type-abbr": "pg",
    "type": "database",
    "db-extensions": [{"name": "pgcrypto"}, {"name": "pgtap"}, {"name": "pgjwt"}, {"name": "\"uuid-ossp\""}],
    "model-template": "[[models.*:*.ALTER DATABASE {{LB_PROJECT_prefix}}_db SET \"{{app-key}}\" TO '{{model}}';]]",
    "models": [
        {
            "type": "role",
            "env-key": "LB_JWT_MODEL",
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
            "type": "role",
            "env-key": "LB_REGISTER_GUEST_MODEL",
            "app-key": "app.lb_register_anonymous",
            "description": ["define me"],
            "model":{"username":"anonymous@register.com",
                     "email":"anonymous@register.com",
                     "password":"g1G!gggg",
                     "role":"anonymous"}
        },
        {
            "type": "role",
            "env-key": "LB_REGISTER_REGISTRANT_MODEL",
            "app-key": "app.lb_register_editor",
            "description": ["define me"],
            "model": {"username":"registrant@register.com",
                      "email":"registrant@register.com",
                      "password":"g1G!gggg",
                      "role":"registrant"}
        },
        {
            "type": "role",
            "env-key": "LB_REGISTER_EDITOR_MODEL",
            "app-key": "app.lb_register_registrant",
            "description": ["define me"],
            "model": {"username":"editor@register.com",
                      "email":"editor@register.com",
                      "password":"g1G!gggg",
                      "role":"editor"}
        },
        {
            "type": "role",
            "env-key": "LB_REGISTER_REGISTRAR_MODEL",
            "app-key": "app.lb_register_registrar",
            "description": ["define me"],
            "model": {"username":"registrar@register.com",
                      "email":"registrar@register.com",
                      "password":"g1G!gggg",
                      "role":"registrar"}
        },
        {
            "type": "role",
            "env-key": "LB_TEST_USER",
            "app-key": "app.lb_register_testuser",
            "description": ["define me"],
            "model": {"type":"app",
                      "app-name":"my-app",
                      "version": "1.0.0",
                      "username":"testuser@register.com",
                      "email":"testuser@register.com",
                      "password":"g1G!gggg"}
        }
    ]
}

def test_table():
    return {
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
            "methods": ["upsert", "select", "test"],
            "role": "anonymous",
            "version": "1.0.0",
            "privileges": [
                {
                    "privilege": "EXECUTE",
                    "type": "FUNCTION",
                    "parameters": "JSONB",
                    "role": "anonymous"
                }
            ],
            "form":[
                {
                    "name": "id",
                    "context": "pk",
                    "type": "TEXT",
                    "json": "RI",
                    "search": "uuid",
                    "calculated": "uuid_generate_v4()"
                }, {
                    "name": "type",
                    "context": "type",
                    "type": "TEXT",
                    "json": "CRI",
                    "const": "app"
                }, {
                    "name": "app-name",
                    "context": "name",
                    "type": "TEXT",
                    "json": "CRI",
                    "default": "my-app"
                }, {
                    "name": "version",
                    "context": "version",
                    "type": "TEXT",
                    "default": "1.0.0",
                    "json": "CR"
                }, {
                    "name": "username",
                    "context": "email",
                    "type": "TEXT",
                    "json": "Cru"
                }, {
                    "name": "password",
                    "context": "password",
                    "description": ["Passwords are stored in table row, but not in json row",
                                    "Remove the password from form before inserting",
                                    "Remove the password from form before updating"],
                    "type": "TEXT",
                    "json": "CuD"
                }, {
                    "name": "token",
                    "context": "token",
                    "type": "TEXT",
                    "json": "r",
                    "function": "sign(_payload, _secret)"
                }
            ],

            "test-forms": [
                {"type": "insert",
                    "template": "is ( {{LB_PROJECT_prefix}}_schema.{{api-name}}( {{token}}, {{form}} ), {{expected}}, {{description}} )",
                    "token":"sign('{{pattern}}', {{password}})",
                    "pattern":   {
                        "username":"testuser@register.com",
                        "role":"anonymous"
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
                    "expected": "'{\"status\": \"200\", \"msg\": \"ok\"}'::JSONB",
                    "description": "'app - insert test'::TEXT"
                },
                {"type": "select",
                    "template": "( matches( {{LB_PROJECT_prefix}}_schema.{{api-name}}( {{token}}, {{form}} )::JSONB, {{expected}}, {{description}} )::JSONB ->> 'result' ) ->> 'token'",
                    "token":"sign('{{pattern}}', {{password}} )",
                    "pattern": {
                        "username":"testuser@register.com",
                        "role":"anonymous"
                    },
                    "password": "current_setting('app.jwt_secret')",
                    "form": {
                        "id": "my-test-app@1.0.0"
                    },
                    "expected": "[a-zA-Z\\.0-9_]+",
                    "description": "app - select and check token"
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
                    "expected": "'{\"status\": \"200\", \"msg\": \"ok\" }'::JSONB",
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
def test_table_template():
    return '''
---- SET DB
\c [[LB_PROJECT_prefix]]_db
-- TABLE
create table if not exists
[[LB_PROJECT_prefix]]_schema.[[tbl-name]] (
  <<table-fields>>
);

-- INDEXxxx
--CREATE UNIQUE INDEX IF NOT EXISTS [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[LB_PROJECT_prefix]]_schema.[[tbl-name]]([[tbl-prefix]]_id int4_ops);
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

def test_upsert_template():
    return '''
\c [[LB_PROJECT_prefix]]_db

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
    if [[LB_PROJECT_prefix]]_schema.is_valid_token(_token, _model_user ->> 'role') then
		rc := '{"result":"1"}'::JSONB;
    else
        return '{"result": "0"}'::JSONB;
    end if;

    -- UPDATE or INSERT
    if _json ? '[[api-form.context:uuid.{{name}}]]' then
    	rc := '{"result":"-2"}'::JSONB;

		-- get current json object
		select [[tbl-prefix]]_[[tbl-fields.context:form.{{name}}]] as _usr
		  into _cur_row
		  from [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
		  where [[tbl-prefix]]_[[api-form.context:uuid.{{name}}]]= cast(_json::jsonb ->> '[[api-form.context:uuid.{{name}}]]' as UUID) and [[tbl-prefix]]_[[api-form.context:type.{{name}}]]= cast(_json::jsonb ->> '[[api-form.context:type.{{name}}]]' as TEXT);

        rc := '{"result":"-2.1"}'::JSONB;

		-- update existing json object with input values
        BEGIN
            -- sync-json-values to table values

            -- update_combos_format
            <<update-combination-code>>
            -- update_combos_format end

        EXCEPTION
		    WHEN check_violation then
		        rc := '{"result":"-2.2"}'::JSONB;
		    WHEN others then
		        rc := '{"result":"-2.2"}'::JSONB;
        END;
		if not FOUND then
		  return format('{"result":"-2.2"}')::JSONB;
		end if;
	    rc := '{"result":"2"}'::JSONB;
    else
    	BEGIN
    	    -- check required attributes
            if _json ? '[[api-form.context:type.{{name}}]]' then
              if _json ->> '[[api-form.context:type.{{name}}]]' = 'app' then
                  -- expected form values on insert
                  if not([[api-form.json:(C)._json ? '{{name}}'.and]]) then
                    return '{"result":"-2"}'::JSONB;
                  end if;
              else
                 return '{"result":"-4"}'::JSONB;
              end if;
            else
                 return '{"result":"-5"}'::JSONB;
            end if;
    	    -- set defaults just in case

            _active = true;

            -- required sync assignments
            if _json ? '[[api-form.context:type.{{name}}]]' then
                _[[api-form.context:type.{{name}}]] := _json ->> '[[api-form.context:type.{{name}}]]';
            else
                return '{"result":"-21"}'::JSONB;
            end if;

            if _json ? '[[api-form.context:password.{{name}}]]' then
                _[[api-form.context:password.{{name}}]] := _json ->> '[[api-form.context:password.{{name}}]]';
            else
                return '{"result":"-22"}'::JSONB;
            end if;

            -- sync attributes to object
            _[[tbl-fields.context:form.{{name}}]] := _json - '[[api-form.context:password.{{name}}]]';

            -- validate
            if length(_[[api-form.context:password.{{name}}]]) < 8 then
                return '{"result":"-1.4"}'::JSONB;
            end if;

			rc := '{"result":"1"}'::JSONB;

			INSERT INTO [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
                ([[tbl-fields.crud:(CF).{{tbl-prefix}}_{{name}}., ]])
              VALUES
                ([[tbl-fields.crud:(CF)._{{name}}., ]] );

		EXCEPTION
		    WHEN unique_violation THEN
		        rc := '{"result":"-1.1"}'::JSONB;
		    WHEN check_violation then
		        rc := '{"result":"-1.2"}'::JSONB;
		    WHEN others then
		        rc := '{"result":"-1.3"}'::JSONB;
		END;
    end if;
    RETURN rc;
  END;
$$ LANGUAGE plpgsql;

GRANT EXECUTE ON FUNCTION
  [[LB_PROJECT_prefix]]_schema.[[api-name]](
  TEXT, JSONB
  ) TO anonymous;    
    '''

def main():
    from app_settings import AppSettingsTest
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os

    os.environ['LB-TESTING'] = '1'
    dictionary_tbl = InterfaceConfiguration('app').load(test_table())
    print('dictionary')
    pprint(dictionary_tbl)

    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()