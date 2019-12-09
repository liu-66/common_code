#!/usr/bin/env python
# coding=utf-8

# 需要xlwt库的支持 pip install xlwt
import xlwt

# 指定file以utf-8的格式打开
file = xlwt.Workbook(encoding = 'utf-8')
# 添加表
table = file.add_sheet('data')

# 存入数据，格式(x,y,数据值)
table.write(0,0,1)
table.write(0,1,2)

# 保存文件
file.save('data.xls')
