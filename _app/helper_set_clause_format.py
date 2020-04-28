
from helper import Helper
from app_settings import AppSettings
import json

class HelperSetClauseFormat(Helper):
    def __init__(self, step=None):
        super().__init__(step)
        self.object_types = ['JSONB']
        self.unquoted_types = ['INTEGER', 'BOOLEAN']
        self.quoted_types = ['TEXT', 'TIMESTAMP']
        self.dictionary = None
        self.lines=[]

    def set_dictionary(self, table_dictionary ):
        self.dictionary = table_dictionary
        return self

    def format(self):
        self.process()
        return self.lines

    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        set_fields = ['{}_{}=_{}'.format(self.dictionary['tbl-prefix'],f['name'], f['name']) for f in self.dictionary['fields']
                      if f['context'] != 'pk' and 'crud' in f and 'u' in f['crud']]

        #self.lines.append(' and '.join(set_fields))
        self.lines.append('            {}'.format(', '.join(set_fields)))

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
    lines = HelperSetClauseFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
if __name__ == "__main__":
    main()