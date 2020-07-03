from templates import Template
from templatize import TemplatizedLine

class TemplateSelect(Template):
    """
    this is a template debuging class
    dont use in process
    Use ProjectCompile instead
    """
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.run()

    def process(self):

        for tmpl_line in self.getTemplate():
            tmpl_line = self.templatize(tmpl_line)
            self.apply_line_functions(tmpl_line)
            #print('last', self[len(self)-1])

        return self

    def postProcess(self):
        self.validate()
        return self


    def validate(self):
        for line in self:
            if '[[' in line:
                raise Exception('Validate failed, undefined tag in dictionary. "{}"'.format(line))
        return self

    def getTemplate(self):
        return '''
\c [[LB_PROJECT_prefix]]_db

-------------------------------
-- Select
---------

CREATE OR REPLACE FUNCTION
[[LB_PROJECT_prefix]]_schema.[[api-name]](_token text, id uuid) RETURNS TEXT
AS $$
  DECLARE rc TEXT;
  DECLARE secret TEXT;
BEGIN

  -- returns a single user's info
  -- need to figure out postgres environment variables

  rc := '{"result":-1}';

  if [[LB_PROJECT_prefix]]_schema.is_valid_token(_token) then

    select [[tbl-prefix]]_[[tbl-fields.context:form.{{name}}]]
    into rc_form
    from [[LB_PROJECT_prefix]]_schema.[[tbl-name]]
	where [[tbl-prefix]]_[[api-form.context:uuid.{{name}}]]= id;
    
    if rc is NULL then
      rc := '{"result":-1}'::JSONB;
    else
      rc :=  format('{"result":%s}',rc_form::TEXT)::JSONB 
    end if;
  end if;

  RETURN rc;
END;  $$ LANGUAGE plpgsql;

GRANT EXECUTE ON FUNCTION
  [[LB_PROJECT_prefix]]_schema.[[api-name]](
  TEXT, UUID
  ) TO anonymous;

 '''.split('\n')

def main():
    from test_func import test_table, test_db
    from configuration_interface import InterfaceConfiguration
    from pprint import pprint
    import os

    os.environ['LB-TESTING'] = '1'
    dictionary_tbl = InterfaceConfiguration('app').load(test_table())
    print('dictionary_tbl',dictionary_tbl)
    tmpl = TemplateSelect(dictionary_tbl)
    print('list upsert')
    print('\n'.join(tmpl))

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()