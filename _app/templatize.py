
from helper import Helper
from app_settings import AppSettings
import json

class Templatize(Helper):
    def __init__(self, step=None):
        super().__init__(step)

        self.lines=[]
        self.template=None

    def set_dictionary(self, table_dictionary):
        self.dictionary = table_dictionary
        return self

    def set_template(self, template):
        self.template = template
        return self

    def templatize(self,template):
        self.set_template(template)
        self.process()
        return self.lines[0]

    def process(self):
        # tempatize
        for key_ in self.dictionary:
            v = self.dictionary[key_]
            if type(v) != list:
                self.template = self.template.replace('[[{}]]'.format(key_), v)
        self.lines.append(self.template)
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
    tmpl = Templatize().set_dictionary(test_table()).templatize('im a little ([[tbl-name]]) template ')
    assert (type(tmpl)==str) # is a list
    print(tmpl)

    tmpl = Templatize().set_dictionary(test_table()['fields'][0]).templatize('im a little ([[name]]) template ')
    assert (type(tmpl) == str)  # is a list
    print(tmpl)

if __name__ == "__main__":
    main()