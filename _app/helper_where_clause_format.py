'''
from helper import Helper
from app_settings import AppSettings
import json
from context_dict import ContextDict, ContextKey
from templatize import Templatize
from list_fields import FieldList
from pprint import pprint
# [[where-clause]]
class HelperWhereClauseFormat(Helper):
    def __init__(self, step=None):
        super().__init__(step)
        self.object_types = ['JSONB']
        self.unquoted_types = ['INTEGER', 'BOOLEAN']
        self.quoted_types = ['TEXT', 'TIMESTAMP']
        self.dictionary = None
        self.lines=[]
        self.context_dictionary = None

    def search_context_key(self, field):
        return '{}-{}'.format(field['context'], field['type'])

    def get_context_dictionary(self):
        if self.context_dictionary == None:
            self.context_dictionary = ContextDict().read()

        return self.context_dictionary

    def set_dictionary(self, table_dictionary ):
        self.dictionary = table_dictionary
        return self

    def format(self):
        self.process()
        return self.lines

    def get_template(self, contextKey):
        # the key might be code
        #rc = self.get_context_dictionary().getTemplateList(key)
        #print('get_context_dictionary()')
        #print('contextKey', contextKey)
        #pprint(self.get_context_dictionary())
        rc = self.get_context_dictionary().get(contextKey)

        if rc == None: # key might be code so return it if not found
            return 'context-key {} {} not found!'.format(contextKey['name'], contextKey['key'])

        return rc

    #def template(self, tmpl, key_pairs):
    #    return
    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')
        #template = Templatize().set_dictionary(f).templatize(self.get_template(f['search']))
        #search_clauses = [self.get_template(f['search']) for f in self.dictionary['tbl-fields'] if 'search' in f]
        search_clauses = [Templatize().set_dictionary(f).templatize(self.get_template(ContextKey('search-context',f)))
                          for f in FieldList(self.dictionary, ['I']) ]


        #print('search_clauses',search_clauses)
        #self.lines.append(' and '.join(search_clauses))
        self.lines.append('            {}'.format(' and '.join(search_clauses)))

        # the closing ; has to be added in template
        self.lines.append('            ;')
        return self

def main():
    import pprint
    import os
    from test_func import test_table

    os.environ['LB-TESTING'] = '1'

    helper = HelperWhereClauseFormat().set_dictionary(test_table())
    lines = helper.format()
    assert (type(lines)==list) # is a list

    print('xxxtemplate', helper.get_template(ContextKey('search-context','uuid')))
    assert '' in helper.get_template(ContextKey('search-context','uuid'))
    #pprint.pprint(lines)
    print('lines','\n'.join(lines))

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()
'''