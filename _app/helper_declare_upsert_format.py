'''
from helper import Helper
from app_settings import AppSettings

class HelperDeclareUpsertFormat(Helper):
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


        declarations = ['Declare _{} {};'.format(f['name'], f['type']) for f in self.dictionary['tbl-fields'] ]
        self.lines.append('\n'.join(declarations))

        return self

def main():
    import pprint
    from test_func import test_table
    import os

    os.environ['LB-TESTING'] = '1'
    lines = HelperDeclareUpsertFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()
'''