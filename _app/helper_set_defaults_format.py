
from helper import Helper
from app_settings import AppSettings
import json

class HelperSetDefaultsFormat(Helper):
    def __init__(self, step=None):
        super().__init__(step)

        self.dictionary = None
        self.lines=[]

    def set_dictionary(self, table_dictionary ):
        self.dictionary = table_dictionary
        return self

    def format(self):

        self.process()

        return self.lines

    def get_defaults(self):
        # set defaults
        unquoted_defaults = ['_{} = {};\n'.format(f['name'], f['default']) for f in self.dictionary['fields'] if 'default' in f and f['type'] in self.unquoted_types]
        quoted_defaults   = ['_{} = \'{}\'::{};\n'.format(f['name'], f['default'],f['type']) for f in self.dictionary['fields'] if 'default' in f and f['type'] in self.quoted_types]

        json_defaults = ['_{} = \'{}\'::{};\n'.format(f['name'], json.dumps(f['default']),f['type']) for f in self.dictionary['fields'] if 'default' in f and f['type'] in self.object_types]

        return quoted_defaults + unquoted_defaults + json_defaults

    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        defaults = self.get_defaults()
        #self.lines.append('            --')
        #self.lines.append('          '.join(defaults))
        self.lines.append('            {}'.format('            '.join(defaults)))


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
            "crud": "r"
        }, {
            "name": "app_name",
            "context": "name",
            "type": "TEXT",
            "crud": "cru",
            "json": "cru"
        }, {
            "name": "version",
            "context": "version",
            "type": "TEXT",
            "crud": "cru",
            "default": "1.0.0",
            "json": "cru"
        },{
            "name": "token",
            "context": "token",
            "type": "TEXT",
            "json": "cru"
        },{
            "name": "row",
            "context": "row",
            "description": "JSON record",
            "type": "JSONB",
            "crud": "cru"
        },{
            "name": "created",
            "context": "created",
            "type": "timestamp",
            "crud": "r"
        }, {
            "name": "updated",
            "context": "updated",
            "type": "timestamp",
            "crud": "r"
        }, {
            "name": "active",
            "context": "active",
            "type": "BOOLEAN",
            "default": "true",
            "crud": "r"
        }],
        "db-prefix":"db"

    }
def main():
    import pprint
    lines = HelperSetDefaultsFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
if __name__ == "__main__":
    main()