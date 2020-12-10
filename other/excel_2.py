# -*- coding=utf-8 -*-

import xlrd  #导入读excel的模块
import xlwt
#打开excel
filename='1.xlsx'
data=xlrd.open_workbook(filename,"rb")

#获取excel工作表
mysheets=data.sheets() #获取工作表list

#通过索引获取第一个sheet
mysheet=mysheets[0]

#通过索引顺序获取
#mysheet=data.sheet_by_index(0)

#通过名称获取
#mysheet=data.sheet_by_name(u'Sheet1')


#获取行数和列数
nrows=mysheet.nrows
print (nrows)
ncols=mysheet.ncols
print (ncols)

#获取一行和一列
#myRowValues=mysheet.row_values(0)
#print myRowValues
#myColValues=mysheet.col_values(0)
#print myColValues
myWorkbook = xlwt.Workbook()
my = myWorkbook.add_sheet('a')
m = 0
#读取单元格数据
for i in range(int(65536/3)):
    for j in range(ncols):
        myCell=mysheet.cell(i,j)
        myCellValue=myCell.value
        if j == 2:
            myCellValue = 2
        #print(myCellValue)
        my.write(m, j, myCellValue)
    m += 1
    my.write(m, 0, '')
    my.write(m, 1, '')
    my.write(m, 2, '')
    m += 1
myWorkbook.save('2.xlsx')