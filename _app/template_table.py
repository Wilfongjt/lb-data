from templates import Template

from function_anchor import Function_Anchor
from function_simple_templatize import Function_SimpleTemplatize
from function_update_combination_code import Function_UpdateCombinationCode
"""
load template one line at a time
evaluate each line for << aka a template key that calls function
evaluate each line for [[ aka an inline template
"""
class Template_Table(Template):
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

---- SET DB
\c [[LB_DB_PREFIX]]_db
-- TABLE
create table if not exists
[[LB_DB_PREFIX]]_schema.[[tbl-name]] (
  <<table-fields>>
);

-- INDEXxxx
CREATE UNIQUE INDEX IF NOT EXISTS [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[LB_DB_PREFIX]]_schema.[[tbl-name]]([[tbl-prefix]]_id);

--CREATE UNIQUE INDEX IF NOT EXISTS [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[LB_DB_PREFIX]]_schema.[[tbl-name]]([[tbl-prefix]]_id text_pattern_ops);
--CREATE UNIQUE INDEX [[tbl-name]]_[[tbl-prefix]]_id_pkey ON [[LB_DB_PREFIX]]_schema.[[tbl-name]]([[tbl-prefix]]_id);
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
 BEFORE INSERT ON [[LB_DB_PREFIX]]_schema.[[tbl-name]]
 FOR EACH ROW
 EXECUTE PROCEDURE [[tbl-prefix]]_ins_upd_trigger_func();



 '''.split('\n')

def main():
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os

    os.environ['LB-TESTING'] = '1'
    dictionary_tbl = InterfaceConfiguration('app').load(test_table())
    print('dictionary_tbl',dictionary_tbl)
    tmpl = Template_Table(dictionary_tbl)
    print('list table')
    #print('\n'.join(tmpl))
    print('tmpl.toString()', tmpl.toString())
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()