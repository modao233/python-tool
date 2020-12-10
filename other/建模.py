# -*- coding=utf-8 -*-

import xlrd  #导入读excel的模块
import xlwt
#打开excel
filename='建模.xlsx'
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
for i in range(nrows):
    e = []
    for j in range(ncols):
        myCell=mysheet.cell(i,j)
        e.append(myCell.value)
    Q1 = (e[5]-e[3])*e[0] - (e[3]-e[2])*e[1]
    Q2 = (e[5]-e[4])*e[0] - (e[4]-e[2])*e[1] - e[6]
    print(Q1)
    print(Q2)
myWorkbook.save('2.xlsx')