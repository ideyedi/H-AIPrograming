import pandas as pd

class GetData():
    def __init__(self):
        '''
        한번에 모든 파일을 읽어서 가지고 올 수 있는 방안 마련
        '''
        df2144 = pd.read_csv('../data/220117.2144.csv', encoding='UTF-8')
        df2204 = pd.read_csv('../data/220117.2204.csv', encoding='UTF-8')

