from file import ListFile

class TextFile(ListFile):
    def __init__(self, folder, filename):
        super().__init__(folder, filename)


def main():
    from pathlib import Path
    from util import Util
    import os
    from app_settings import AppSettings, AppSettingsTest

    os.environ['LB-TESTING'] = '1'

    appSettings = AppSettingsTest()
    foldername = appSettings.getFolder('temp-folder')
    filename = 'test.tmpl'
    filename2 = 'test2.tmpl'

    textFile = TextFile(foldername, filename)

    textFile.append('line A')
    textFile.append('line B')
    textFile.append('line C')

    assert textFile[0] == 'line A'
    assert textFile[1] == 'line B'
    assert textFile[2] == 'line C'
    assert textFile == ['line A', 'line B', 'line C']

    textFile.write()                                    # write orignial

    assert textFile.exists()
    textFile.copy(foldername, filename2)                # copy
    textFile2 = TextFile(foldername, filename2).read()  # read
    assert textFile2 == ['line A', 'line B', 'line C']

    # cleanup
    textFile.delete()                                   # delete original
    assert not textFile.exists()
    textFile2.delete()                                  # delete copy
    assert not textFile2.exists()

if __name__ == "__main__":
    main()