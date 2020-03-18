import  xlrd

class ExcelData:

    def __init__(self,path):
        self.path=path

    def get_data(self):
        workbook = xlrd.open_workbook(self.path)
        sheet_obj=workbook.sheet_by_index(0)#通过表单名来获取对象
        return sheet_obj

#test-coding
'''tester=ExcelData("../../data/testdata/test_data.xlsx")
sheet_obj=tester.get_data()
t=sheet_obj.row_values(1)
print(t)'''