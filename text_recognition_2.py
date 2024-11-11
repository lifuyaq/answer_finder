import easyocr
import os
import pandas as pd
from rapidfuzz import fuzz, process


def pic_getter():
    return pic_path


def text_reader(pic_path):
    reader = easyocr.Reader(['ja'])
    result = reader.readtext(pic_path)
    strr = result[0][1]
    return strr


# 定义一个快速模糊匹配的函数
def fuzzy_match(target, candidates, limit=1):
    # 使用 rapidfuzz 的 process.extractOne 或 process.extract 进行模糊匹配
    return process.extract(target, candidates, limit=limit)


def answer(sheet, target):
    result = fuzzy_match(target, sheet.candidates)[0][0]
    index = sheet.candidates.index(result)
    key = sheet.keys[index]
    return key


class ExcelReader(object):

    def __init__(self, file_path):
        self.path = file_path
        self.workbook = pd.ExcelFile(self.path)
        self.sheetnames = self.workbook.sheet_names


class SheetReader(object):

    def __init__(self, father, sheet_name):
        """father should be a excel workbook"""
        self.father = father
        self.sheetname = sheet_name
        self.sheet = father.parse(sheet_name)
        self.colunmnames = self.sheet.columns.tolist()
        self.candidates = self.sheet[self.colunmnames[0]].tolist()
        self.candidates = list(map(lambda x: str(x) if x is not None else '', self.candidates))     # change format into string
        self.keys = self.sheet[self.colunmnames[1]].tolist()


if __name__ == '__main__':
    pic_path = pic_getter()
    text_reader(pic_path)

