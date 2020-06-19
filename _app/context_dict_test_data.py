'''
import json
import os.path
#from copy_file import CopyFile
from context_dict import ContextDict
from app_settings import AppSettings, AppSettingsTest

class ContextDictTestData(ContextDict):
    def __init__(self, foldername=None, filename='context.test-data.list.json'):
        super().__init__(foldername, filename)
        print('* ContextDictTestData')

    def get(self, key):
        val = None

        if key in self:
            val = self[key]
        return val

    def getTemper(self, key, temper):
        val = "TBD"

        if key in self:
            val = self[key][temper]
        #print('gettemper', key, val)
        return val

def main():
    import pprint as pprint
    os.environ['LB-TESTING'] = '1'
    print('* Test ContextDictTestData')
    #res_folder = AppSettingsTest().getResourceFolder('shared')
    #temp_folder = AppSettingsTest().getFolder('temp-folder')

    AppSettingsTest().createFolders()

    contextDict = ContextDictTestData().read()

    print('contextDict', contextDict)

    assert len(contextDict) > 0
    #print('get',contextDict.get('created'))
    assert contextDict.get('created') == {"good":"2020-04-30 22:34:25.919433", "bad": "a"}
    assert contextDict.get('active') == {"good":"true", "bad": "a"}

    #print('type', type(contextDict))
    #print('getTemper',contextDict.getTemper('active','good'))
    assert contextDict.getTemper('active','good') == "true"
    assert contextDict.getTemper('active', 'bad') != "true"

    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()


'''