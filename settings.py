import os
#from pathlib import Path
from dotenv import load_dotenv
import sys
# sys.path.insert(0, '{}/__classes__'.format(os.getcwd()))
print('app', '{}/_app'.format(os.getcwd()) )
#sys.path.insert(0, '{}'.format(os.getcwd().replace('/pg-dev','')))

sys.path.insert(0, '{}/_app'.format(os.getcwd()))

load_dotenv()

#print('WORKING_FOLDER_NAME',os.getenv('WORKING_FOLDER_NAME'))
#print(sys.path)
#print('settings')

