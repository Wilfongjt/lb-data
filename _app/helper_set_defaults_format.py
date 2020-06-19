"""
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
        unquoted_defaults = ['_{} = {};\n'.format(f['name'], f['default']) for f in self.dictionary['tbl-fields'] if 'default' in f and f['type'] in self.unquoted_types]
        quoted_defaults   = ['_{} = \'{}\'::{};\n'.format(f['name'], f['default'],f['type']) for f in self.dictionary['tbl-fields'] if 'default' in f and f['type'] in self.quoted_types]

        json_defaults = ['_{} = \'{}\'::{};\n'.format(f['name'], json.dumps(f['default']),f['type']) for f in self.dictionary['tbl-fields'] if 'default' in f and f['type'] in self.object_types]

        self.lines.append('            /*')
        self.lines.append('               -- unquoted types {}'.format(self.unquoted_types))
        self.lines.append('               -- quoted types   {}'.format(self.quoted_types))
        self.lines.append('               -- json types     {}'.format(self.object_types))

        combined = quoted_defaults + unquoted_defaults + json_defaults
        if len(combined)==0:
            self.lines.append('               -- No defaults configured')
            self.lines.append('               --  set default in field to include')
            self.lines.append('            */')
        else:
            self.lines.append('               --  set default in field to include')
            self.lines.append('            */')

        return combined

    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        defaults = self.get_defaults()
        #self.lines.append('            --')
        #self.lines.append('          '.join(defaults))
        self.lines.append('            {}'.format('            '.join(defaults)))


        return self

def main():
    import pprint
    import test_func
    import os
    os.environ['LB-TESTING'] = '1'
    lines = HelperSetDefaultsFormat().set_dictionary(test_func.test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()
"""