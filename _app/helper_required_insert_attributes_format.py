
from helper import Helper
from app_settings import AppSettings

class HelperRequiredInsertAttributesFormat(Helper):
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

    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        required_attributes = ['_json ? \'{}\''.format( f['name']) for f in self.dictionary['fields'] if 'json' in f and 'c' in f['json']]

        self.lines.append('    not (')
        self.lines.append(' and '.join(required_attributes))
        self.lines.append('    )')

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
    lines = HelperRequiredInsertAttributesFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
if __name__ == "__main__":
    main()