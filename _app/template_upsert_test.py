from templates import Template
#from function_anchor import Function_Anchor

#from function_simple_templatize import Function_SimpleTemplatize
#from function_update_combination_code import Function_UpdateCombinationCode
"""
load template one line at a time
evaluate each line for << aka a template key that calls function
evaluate each line for [[ aka an inline template
"""
# interface-test.pg.json
class Template_InterfaceTest(Template):
    """
    this is a template debuging class
    dont use in process
    Use ProjectCompile instead
    """

    def getTemplateList(self):
        return ''''
\c [[LB_PROJECT_prefix]]_db

select '##### [[tbl-name]] TESTS';
BEGIN;
  SELECT plan(1);
  select '###### [[tbl-name]]';
  select '############################################## Upsert ';
  select '######################################## A UPDATE {}';
  /*
  select '############ INSERT need to write this test'
  */
  SELECT is (
    [[LB_PROJECT_prefix]]_schema.[[api-name]](
      sign('{"username":"testuser@register.com","role":"[[api-role]]"}'::json, current_setting('app.jwt_secret')),
      '{"type": "[[api-name]]", "app_id": "my-app", "version": "[[api-version]]", "username": "abc@xyx.com", "password": "t1T!tttt"}'::JSONB
      '[[api-test-forms.type:insert.{{form}}]]'::JSONB
    )::JSONB,
    '{"result": "1"}'::JSONB,
    '[[tbl-name]] testuser@request.com UPSERT'::TEXT
  );
  /*
  select '############ xxxSELECT need to write this test'
  */
  select '#############################################';
  SELECT * FROM finish();
  select '##### [[tbl-name]] TESTS Done';
ROLLBACK;
 '''.split('\n')

def main():
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os

    os.environ['LB-TESTING'] = '1'
    dictionary_tbl = InterfaceConfiguration('app').load(test_table())
    # print('dictionary_tbl',dictionary_tbl)
    tmpl = Template_InterfaceTest(dictionary_tbl)#.run() # have to run for test

    print('list upsert')
    print(tmpl.toString())
    #print('\n'.join(tmpl))

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()