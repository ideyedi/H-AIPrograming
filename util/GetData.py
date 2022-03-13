import pandas as pd
import os


class GetData():

    def __init__(self):
        '''
        한번에 모든 파일을 읽어서 가지고 올 수 있는 방안 마련
        '''
        self.file_list = []
        self.except_list = ['.DS_Store', 'README.md']
        #df2144 = pd.read_csv('../data/220117.2144.csv', encoding='UTF-8')
        #df2204 = pd.read_csv('../data/220117.2204.csv', encoding='UTF-8')
        for filename in os.listdir('data'):
            if filename not in self.except_list:
                self.file_list.append(filename)

        #print(f"{self.file_list}")