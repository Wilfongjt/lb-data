from templates import Template
#from templatize import TemplatizedLine

class Template_Test(Template):
    """
    this is a template debuging class
    dont use in process
    Use ProjectCompile instead

    """

    def __init__(self, dictionary):
        super().__init__(dictionary)
        # self.dictionary = dictionary
        # self.run()

    def process(self):
        super().process()
        return self

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


def main():
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os

    os.environ['LB-TESTING'] = '1'
    dictionary_tbl = InterfaceConfiguration('app').load(test_table())
    print('dictionary_tbl',dictionary_tbl)
    tmpl = Template_Test(dictionary_tbl)
    print('list upsert')
    print('\n'.join(tmpl))

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()