import easyocr
import os
import pandas as pd
from rapidfuzz import fuzz, process

path = os.getcwd()
print(path)
path2 = path + '/pic'
os.chdir(path2)
file_list = os.listdir(path2)
print(file_list)
try:
    os.rename(file_list[0], 'img.png')
except:
    pass

reader = easyocr.Reader(['ja'])
result = reader.readtext('img.png')
strr = result[0][1]

os.chdir(path)
filename = '../answers/Webテスト解答集.xlsx'
workbook = pd.ExcelFile(filename)
sheet_names = workbook.sheet_names
sheet = workbook.parse(sheet_names[1])
column_names = sheet.columns.tolist()

target_string = strr


# 定义一个快速模糊匹配的函数
def fuzzy_match(target, candidates, limit=1):
    # 使用 rapidfuzz 的 process.extractOne 或 process.extract 进行模糊匹配
    return process.extract(target, candidates, limit=limit)

# 将候选字符串列表（例如某列）定义为候选池
candidates = sheet[column_names[0]].tolist()
keys = sheet[column_names[1]].tolist()
candidates = list(map(lambda x: str(x) if x is not None else '', candidates))
result_f = fuzzy_match(target_string, candidates)[0][0]
index = candidates.index(result_f)
key = keys[index]





# 批量进行模糊匹配
# df['匹配结果'] = df['待匹配列'].apply(lambda x: fuzzy_match(x, candidates, limit=1))
# print(df)






