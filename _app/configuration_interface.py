import json
from configuration_file import ConfigurationDict
from pprint import pprint
class InterfaceConfiguration(ConfigurationDict):
    '''
    loads a single interface configuration file from the projects/project/config folder
    flattens the interface to a
    '''

    def __init__(self, interface_name, foldername=None, filename=None):
        super().__init__(foldername, filename)
        self.interface_name = interface_name
        #print('InterfaceConfiguration folder', foldername, filename )

    def read(self):
        path_filename = '{}/{}'.format(self.getFolderName(), self.getFileName())
        #print('open file', path_filename)
        with open(path_filename) as json_file:
            configuration_dict = json.load(json_file)

        self.load(configuration_dict)

        return self

    def load(self, dictionary):

        for key in dictionary:
            if key == 'interfaces':
                #self[key] = dictionary[key]
                #self['form']= dictionary['interfaces'][self.interface_name]['form']
                for fr_key in dictionary['interfaces'][self.interface_name]:
                    self['api-{}'.format(fr_key)] =  dictionary['interfaces'][self.interface_name][fr_key]
                    #print('configuration interfaces', 'api-{}'.format(fr_key))
            else:
                self[key] = dictionary[key]

        return self

def main():
    from pathlib import Path
    from util import Util
    import os
    from test_func import test_table
    from pprint import pprint

    #from app_settings import TestAppSettings

    os.environ['LB-TESTING']='1'
    #appSettings = TestAppSettings()
    flat = InterfaceConfiguration('app').load(test_table())
    #print('flat')
    pprint(flat)
    assert 'api-form' in flat
    assert 'api-name' in flat
    assert flat['api-name'] == 'user'
    assert flat['api-version'] == '1.0.0'


    os.environ['LB-TESTING']='0'

if __name__ == "__main__":
    main()