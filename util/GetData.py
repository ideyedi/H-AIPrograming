import pandas as pd
import os


class GetData:
    test_list = ['jungwoo', 'esji']

    def __init__(self):
        '''
        한번에 모든 파일을 읽어서 가지고 올 수 있는 방안 마련
        '''
        self.file_list = []
        self.concated_list = []
        self.except_list = ['.DS_Store', 'README.md']
        #df2144 = pd.read_csv('../data/220117.2144.csv', encoding='UTF-8')
        #df2204 = pd.read_csv('../data/220117.2204.csv', encoding='UTF-8')
        for filename in os.listdir('data'):
            if filename not in self.except_list:
                self.file_list.append(filename)

        for item in self.file_list:
            tempFrame = pd.read_csv('./data/'+item, encoding='UTF-8')
            self.concated_list.append(tempFrame)

    def getResult(self):
        df = pd.concat(self.concated_list, axis=0, ignore_index=True)
        return df


if __name__=="__main__":
    '''
    Debug function
    '''
    print("Debugging function")
    getData = GetData()
    # Instance variables 테스트
    # print(f"{gd.GetData.file_list}")
    print(f"Instance variables: {getData.file_list}")
    print(f"Class variables: {GetData.test_list}")

    print(getData.getResult().describe())