
from helper import Helper
from app_settings import AppSettings

class HelperRequiredInputAttributesFormat(Helper):
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

        #required = ['if not (_json ? \'%s\') then return \'{"result":"-1.3"}\'::JSONB; end if;'.format(f['name'])
        #            for f in self.dictionary['fields'] if 'crud' in f and 'c' in f['crud']]

        required = ['if not(_json ? \'{}\') then return \'{{"result":"-1.3"}}\'::JSONB; end if;'.format(f['name'])
                    for f in self.dictionary['fields'] if 'crud' in f and 'json' in f and 'c' in f['crud']]

        self.lines.append('\n'.join(required))

        return self

def test_table():
    return {
    "type": "table",
    "tbl-name": "credentials",
    "tbl-prefix": "crd",
    "tbl-role": "guest",
    "api-overwrite": "0",
    "api-name": "credential",
    "api-table": "credentials",
    "api-methods": ["upsert", "select"],
    "fields": [{
            "name": "id",
            "context": "pk",
            "type": "INTEGER",
            "crud": "r",
            "json": "ru",
            "required": "ru",
            "search": "confirm-id"
        },{
            "name": "username",
            "context": "email",
            "type": "TEXT",
            "crud": "cru",
            "json": "cru",
            "required": "cru",
            "search": "confirm-token-username"
        },{
            "name": "password",
            "context": "password",
            "description": "Passwords are stored in table row, but not in json row",
            "type": "TEXT",
            "crud": "cru",
            "json": "",
            "required": "cru"
        },{
            "name": "row",
            "context": "row",
            "description": "json to define role access to multiple apps.",
            "type": "JSONB",
            "crud": "ru",
            "required": "cru"
        },{
            "name": "email",
            "context": "email",
            "type": "TEXT",
            "json": "cru",
            "required": "cru"
        },{
            "name": "roles",
            "context": "roles",
            "description": "User can have multiple roles",
            "type": "JSONB",
            "default": ["registrant"],
            "crud": "",
            "json": "cr",
            "required": "r"
        },{
            "name": "created",
            "context": "created",
            "type": "TIMESTAMP",
            "crud": "r",
            "required": "r"
        },{
            "name": "updated",
            "context": "updated",
            "type": "TIMESTAMP",
            "crud": "r",
            "required": "r"
        },{
            "name": "active",
            "context": "active",
            "type": "BOOLEAN",
            "default": "true",
            "crud": "r",
            "json": "ru",
            "required": "r"
        }]
}

def main():
    import pprint
    lines = HelperRequiredInputAttributesFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
if __name__ == "__main__":
    main()