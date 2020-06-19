
class MethodList(list):
    def __init__(self, tbl_dictionary, interface):
        self.tbl_dictionary = tbl_dictionary


        for i in self.tbl_dictionary['interfaces'][interface]['methods']:
            self.append(i)


def main():
    import pprint
    import os
    from test_func import test_table

    os.environ['LB-TESTING'] = '1'
    methods = MethodList(test_table(), 'app')

    assert type(methods) == MethodList
    #print('methond', methods)
    assert methods == ['upsert', 'select']

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()

