
# Deprecated
"""
from helper import Helper
from app_settings import AppSettings
from field_list import FieldList

class dep_HelperExpandUpdateSettingsFormat(Helper):
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

        self.lines = ['[[tbl-prefix]]_{}=_{}'.format(f['name'], f['name'])
                      for f in FieldList(self.dictionary,['u','U'])
                      if 'pk-uuid' not in f['context'] and 'pk' not in f['context']]

        return self

def main():
    from test_func import test_table

    import pprint
    os.environ['LB-TESTING'] = '1'
    helper = HelperExpandUpdateSettingsFormat().set_dictionary(test_table())

    print('format', helper.format())

    assert '[[tbl-prefix]]_form=_form' in helper.format()

    #lines = HelperRequiredInsertAttributesFormat().set_dictionary(test_table()).format()
    lines = helper.format()
    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()
"""