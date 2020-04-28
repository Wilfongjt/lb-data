
from helper import Helper
from app_settings import AppSettings
import json
from context_dict import ContextDict
from templatize import Templatize
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

    def get_template(self, key):
        # the key might be code
        rc = self.get_context_dictionary().getTemplate(key)

        if rc == None: # key might be code so return it if not found
            return key
        return rc

    #def template(self, tmpl, key_pairs):
    #    return
    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')
        #template = Templatize().set_dictionary(f).templatize(self.get_template(f['search']))
        #search_clauses = [self.get_template(f['search']) for f in self.dictionary['fields'] if 'search' in f]
        search_clauses = [Templatize().set_dictionary(f).templatize(self.get_template(f['search'])) for f in self.dictionary['fields'] if 'search' in f]
        #print('search_clauses',search_clauses)
        #self.lines.append(' and '.join(search_clauses))
        self.lines.append('            {}'.format(' and '.join(search_clauses)))

        # the closing ; has to be added in template
        self.lines.append('            ;')
        return self

def test_table():
    return {
        "type": "table",
        "tbl-name": "test",
        "tbl-prefix": "tst",
        "tbl-role": "guest",
        "api-overwrite": "0",
        "api-name": "test",
        "api-table": "test",
        "api-methods": ["upsert", "select"],

    "fields": [{
            "name": "id",
            "context": "pk",
            "type": "INTEGER",
            "crud": "r",
            "json": "ru"
        },{
            "name": "username",
            "context": "email",
            "type": "TEXT",
            "crud": "cru",
            "json": "cru",
            "search": "confirm-token-username"
        },{
            "name": "email",
            "context": "email",
            "type": "TEXT",
            "json": "cru"
        },{
            "name": "password",
            "context": "password",
            "description": "Passwords are stored in table row, but not in json row",
            "type": "TEXT",
            "crud": "cru",
            "json": ""
        },{
            "name": "roles",
            "context": "roles",
            "description": "User can have multiple roles",
            "type": "JSONB",
            "default": ["registrant"],
            "crud": "",
            "json": "cr"
        },{
            "name": "row",
            "context": "row",
            "description": "json to define role access to multiple apps.",
            "type": "JSONB",
            "crud": "cru"
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
        },{
            "name": "active",
            "context": "active",
            "type": "BOOLEAN",
            "default": "true",
            "crud": "r",
            "json": "ru"

        }]
        ,
        "db-prefix":"db"

    }
def main():
    import pprint
    import os

    os.environ['LB-TESTING'] = '1'

    lines = HelperWhereClauseFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('lines','\n'.join(lines))
if __name__ == "__main__":
    main()