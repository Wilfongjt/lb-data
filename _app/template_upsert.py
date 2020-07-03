from templates import Template

#from function_anchor import Function_Anchor
#from function_simple_templatize import Function_SimpleTemplatize
#from function_update_combination_code import Function_UpdateCombinationCode
"""
load template one line at a time
evaluate each line for << aka a template key that calls function
evaluate each line for [[ aka an inline template
"""
class Template_Upsert(Template):
    """
    this is a template debuging class
    dont use in process
    Use ProjectCompile instead

    """
    def __init__(self, dictionary):
        super().__init__(dictionary)
        #self.dictionary = dictionary
        #self.run()

    def process(self):
        super().process()
        return self

    def getTemplateList(self):
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
		rc := '{"status":"200", "msg":"ok"}'::JSONB;
    else
        return '{"status": "401", "msg": "Bad Request, token."}'::JSONB;
    end if;

    if _json ? 'password' then
        _form = _json - 'password';
    else
        _form = _json;
    end if;

    -- UPDATE or INSERT
    -- is primary key in form
    if _json ? '[[api-form.context:pk.{{name}}]]' then
    	rc := '{"status":"400","msg": "Bad Request, missing id"}'::JSONB;

		-- get current json object
		select [[tbl-prefix]]_[[tbl-fields.context:form.{{name}}]] as _usr
		  into _cur_row
		  from [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
		  where [[tbl-prefix]]_[[api-form.context:pk.{{name}}]]= cast(_json::jsonb ->> '[[api-form.context:pk.{{name}}]]' as TEXT) and [[tbl-prefix]]_[[api-form.context:type.{{name}}]]= cast(_json::jsonb ->> '[[api-form.context:type.{{name}}]]' as TEXT);

		  -- where [[tbl-prefix]]_[[api-form.context:uuid.{{name}}]]= cast(_json::jsonb ->> '[[api-form.context:uuid.{{name}}]]' as UUID) and [[tbl-prefix]]_[[api-form.context:type.{{name}}]]= cast(_json::jsonb ->> '[[api-form.context:type.{{name}}]]' as TEXT);

        rc := '{"status":"-2", "msg": ""}'::JSONB;

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
		  return format('{"status":"404"}, "msg": "Not Found, on update."')::JSONB;
		end if;
	    rc := '{"status":"200", "msg": "ok"}'::JSONB;
    else
        -- start insert
    	BEGIN
    	    -- check required attributes
            if _json ? '[[api-form.context:type.{{name}}]]' then
              -- if _json ->> '[[api-form.context:type.{{name}}]]' = '[[api-name]]' then

              if _json ->> '[[api-form.context:type.{{name}}]]' = '[[api-form.context:type.{{const}}]]' then
                  -- expected form values on insert
                  if not([[api-form.json:(C)._json ? '{{name}}'. and ]]) then
                    return format('{"status":"400", "msg": "Bad Request, missing attribute.", "json":%s}',_json::TEXT)::JSONB;
                  end if;
              else
                 return '{"status":"400", "msg": "Bad Request, unknown type."}'::JSONB;
              end if;
            else
                 return '{"status":"400", "msg": "Bad Request, missing type."}'::JSONB;
            end if;
    	    -- set defaults just in case

            _active = true;

            -- required sync assignments
            if _json ? '[[api-form.context:type.{{name}}]]' then
                _[[api-form.context:type.{{name}}]] := _json ->> '[[api-form.context:type.{{name}}]]';
            else
                return '{"status":"400", "msg": "Bad Request, missing type."}'::JSONB;
            end if;

            if _json ? '[[api-form.context:password.{{name}}]]' then
                _[[api-form.context:password.{{name}}]] := _json ->> '[[api-form.context:password.{{name}}]]';
            else
                return '{"status":"401", "msg": "Unauthorized"}'::JSONB;
            end if;

            -- sync attributes to object
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

def main():
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os

    os.environ['LB-TESTING'] = '1'
    print('### A')
    dictionary_tbl = InterfaceConfiguration('user').load(test_table())
    print('### B')

    #print('dictionary_tbl',dictionary_tbl)

    tmpl = Template_Upsert(dictionary_tbl)
    print('### C')

    print('list upsert')
    print(tmpl.toString())
    #print('\n'.join(tmpl))
    print('### D')

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()