import pandas as pd
import os


class getDataframe:
    test_list = ['jungwoo', 'esji']

    def __init__(self):
        '''
        한번에 모든 파일을 읽어서 가지고 올 수 있는 방안 마련
        '''
        self.file_list = []
        self.concated_list = []
        self.except_list = ['.DS_Store', 'README.md']

        for filename in os.listdir('data'):
            if filename not in self.except_list:
                self.file_list.append(filename)

        for item in self.file_list:
            tempFrame = pd.read_csv('./data/'+item, encoding='UTF-8')
            self.concated_list.append(tempFrame)

    def getPreprocessedData(self):
        df = pd.concat(self.concated_list, axis=0, ignore_index=True)
        '''
        NaN Value 전처리, 결측시 제거
        Labeling이 되지 않은 데이터이기 때문에 다른 기법을 사용하지 않고 삭제 처리
        '''
        df = df.dropna(axis='index', how='any')

        # Feature Selection
        df = df.drop('link', axis=1)

        '''
        가격비교 전처리가 정확히 int형으로 변경이 잘 안되는데 확인이 필요할 듯 함.
        '''
        pre_ship = df['ship'].replace( value='0', regex='[^0-9]')
        pre_ship = pre_ship.replace('', '0')
        df['ship'] = pre_ship

        pre_price = df['price']
        pre_price = pre_price.replace('[\$,]', '', regex=True)
        df['price'] = pre_price

        return df


if __name__=="__main__":
    '''
    Debug function
    '''
    print("Debugging function")
    gdf = getDataframe()
    # Instance variables 테스트
    # print(f"{gd.GetData.file_list}")
    print(f"Instance variables: {gdf.file_list}")
    print(f"Class variables: {gdf.test_list}")

    print(gdf.getPreprocessedData())