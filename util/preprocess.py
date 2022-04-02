import pandas as pd
import os
import sys


class getDataframe:
    test_list = ['jungwoo', 'esji']

    def __init__(self):
        '''
        한번에 모든 파일을 읽어서 가지고 올 수 있는 방안 마련
        '''
        self.file_list = []
        self.concated_list = []
        self.except_list = ['.DS_Store', 'README.md']

        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        root_path = os.path.join(root_path, "data")

        for filename in os.listdir(root_path):
            if filename not in self.except_list:
                self.file_list.append(filename)

        for item in self.file_list:
            print(os.path.join(root_path, item))
            tempframe = pd.read_csv(os.path.join(root_path, item), encoding='UTF-8')
            self.concated_list.append(tempframe)

    def getpreprocessed(self):

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

        '''
        one-hot encoding
        '''
        main_onehot = pd.get_dummies(df['main'])
        mid_onehot = pd.get_dummies(df['mid'])
        sub_onehot = pd.get_dummies(df['sub'])
        name_onehot = pd.get_dummies(df['name'])
        platform_onehot = pd.get_dummies(df['platform'])

        # 노트북 중복에 따른 Rename
        mid_onehot = mid_onehot.rename(columns={'노트북':'notebook'})

        pre_df = pd.concat([main_onehot, mid_onehot, sub_onehot, name_onehot, platform_onehot, df], axis=1)
        pre_df = pre_df.drop('main', axis=1)
        pre_df = pre_df.drop('mid', axis=1)
        pre_df = pre_df.drop('sub', axis=1)
        pre_df = pre_df.drop('name', axis=1)
        pre_df = pre_df.drop('platform', axis=1)

        num_price = pd.to_numeric(pre_df['price'])
        num_ship = pd.to_numeric(pre_df['ship'])
        num_label = pd.to_numeric(pre_df['label'])
        pre_df = pre_df.drop('price', axis=1)
        pre_df = pre_df.drop('ship', axis=1)
        pre_df = pre_df.drop('label', axis=1)

        df = pd.concat([pre_df, num_price, num_ship, num_label], axis=1)

        return df


if __name__ == "__main__":
    '''
    Debug function
    '''
    print("Debugging function")
    gdf = getDataframe()
    print('=' * 100)
    df = gdf.getpreprocessed()
    # Instance variables 테스트
    # print(f"{gd.GetData.file_list}")
    print(f"Instance variables: {gdf.file_list}")
    print(f"Class variables: {gdf.test_list}")

    print(df.describe())
    print(df.head())

    print(df['label'].describe())