import GetData as gd


getData = gd.GetData()
# Instance variables 테스트
# print(f"{gd.GetData.file_list}")
print(f"Instance variables: {getData.file_list}")
print(f"Class variables: {gd.GetData.test_list}")