
from helper import Helper
from app_settings import AppSettings
import itertools
from helper_where_clause_format import HelperWhereClauseFormat

class HelperUpdateCombosFormat(Helper):
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
        rc = []
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        fieldname_combos = self.get_fieldname_combos()

        rows = self.get_rownames()

        i = 0
        for name_list in fieldname_combos:
            d = ['_json ? \'{}\''.format(n) for n in name_list]

            if i == 0:
                self.lines.append('            if {} then'.format(' and '.join(d)))
            else:
                self.lines.append('            elsif {} then'.format(' and '.join(d)))

            self.add_update_template(list(name_list)+rows)
            i += 1

        for name_list in rows[::-1]:
            self.lines.append('            else')
            self.add_update_template([name_list])
        self.lines.append('            end if;')

        return self

    def get_rownames(self):
        row_names = [f['name'] for f in self.dictionary['fields'] if 'crud' in f and 'row' in f['context']]
        if len(row_names) < 1:
            raise Exception('No json role defined!')
        if len(row_names) > 1:
            raise Exception('Only 1 "row" field allowed!')
        return row_names

    def get_fieldname_combos(self):

        #names = ['_json ? \'{}\''.format(f['name']) for f in self.dictionary['fields'] if 'crud' in f and 'json' in f and 'c' in f['crud']]
        names = [f['name'] for f in self.dictionary['fields'] if
                 'crud' in f and 'json' in f and 'c' in f['crud']]

        all_combinations = []
        for r in range(len(names) + 1):
            combinations_object = itertools.combinations(names, r)
            combinations_list = list(combinations_object)
            all_combinations += combinations_list

        r = [f for f in reversed(all_combinations)]
        r = r[:len(r)-1]
        return r

    def add_update_template(self, name_list):
        tblpfx = self.dictionary['tbl-prefix']
        set_names = [' {}_{} = _{}'.format(tblpfx, nm,nm) for nm in name_list]
        #set_rows = [' {}_{} = _{}'.format(tblpfx, nm, nm) for nm in self.get_rownames() ]
        #set_names.append('{}_{} = _{}'.format(tblpfx, ))
        #set_names = set_names + set_rows
        pfx = self.dictionary['db-prefix']
        tblname = self.dictionary['tbl-name']
        #where_lines = HelperWhereClauseFormat().set_dictionary(self.getConfigFile()).format()
        where_lines = HelperWhereClauseFormat().set_dictionary(self.dictionary).format()

        self.lines.append('              update ')
        self.lines.append('                  {}_schema.{}'.format(pfx, tblname))
        self.lines.append('                set ')
        self.lines.append('                  {} '.format(', '.join(set_names)))
        self.lines.append('                where ')

        for w in where_lines:
            self.lines.append('       {}'.format(w))

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
        }],
        "db-prefix":"reg"
}

def main():
    import pprint
    lines = HelperUpdateCombosFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
if __name__ == "__main__":
    main()