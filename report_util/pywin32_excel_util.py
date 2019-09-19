#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
   适用条件:安装pywin32和office excel
"""

import os
import time
import glob
import shutil
import string

import win32com.client as win32

PROJECT = os.path.dirname(os.path.realpath(__file__))

SRC_PATH = ""  # 需处理的excel文件目录
DST_PATH = ""  # 处理后的excel存放目录

SKIP_FILE_LIST = []  # 需要跳过的文件列表
MAX_SHEET_INDEX = 1  # 每个excel文件的前几个表需要处理
DELETE_ROW_LIST = []  # 需要删除的行号


def dealPath(pathname=''):
    '''deal with windows file path'''
    if pathname:
        pathname = pathname.strip()
    if pathname:
        pathname = r'%s' % pathname
        pathname = string.replace(pathname, r'/', '\\')
        pathname = os.path.abspath(pathname)
        if pathname.find(":\\") == -1:
            pathname = os.path.join(os.getcwd(), pathname)
    return pathname


class EasyExcel(object):
    """
       class of pywin32 for excel
    """

    def __init__(self):
        '''initial excel application'''
        self.app_type = 'Excel.Application'
        self.xlfilename = ''
        self.xlexists = False
        self.xlapp = win32.gencache.EnsureDispatch(self.app_type)
        self.xlapp.EnableEvents = False  # 禁用事件
        self.xlapp.DisplayAlerts = False  # 禁止弹窗
        self.xlbook.Checkcompatibility = False  # 屏蔽弹窗
        self.xlbook.RunAutoMacros(2)  # 1:打开宏，2:禁用宏

    def open(self, filename=''):
        '''open excel file'''
        if getattr(self, 'xlbook', False):
            self.xlbook.Close()
        self.xlfilename = dealPath(filename) or ''
        self.xlexists = os.path.isfile(self.xlfilename)
        if not self.xlfilename or not self.xlexists:
            self.xlbook = self.xlapp.Workbooks.Add()
        else:
            self.xlbook = self.xlapp.Workbooks.Open(self.xlfilename, False)

    def reset(self):
        '''reset'''
        self.xlapp = None
        self.xlbook = None
        self.xlfilename = ''

    def save(self, newfile=''):
        '''save the excel content'''
        newfile = dealPath(newfile) or self.xlfilename
        if not newfile or (self.xlexists and newfile == self.xlfilename):
            self.xlbook.Save()
            return
        pathname = os.path.dirname(newfile)
        if not os.path.isdir(pathname):
            os.makedirs(pathname)
        self.xlfilename = newfile
        self.xlbook.SaveAs(newfile)

    def close(self):
        '''close the application'''
        self.xlbook.Close(SaveChanges=1)
        self.xlapp.Quit()
        time.sleep(2)
        self.reset()

    def addSheet(self, sheetname=None):
        '''add new sheet, the name of sheet can be modify,but the workbook can't '''
        sht = self.xlbook.Worksheets.Add()
        sht.Name = sheetname if sheetname else sht.Name
        return sht

    def getSheet(self, sheet=1):
        '''get the sheet object by the sheet index'''
        assert isinstance(sheet, int), 'the sheet index must be int'
        assert sheet > 0, 'the sheet index must bigger then 0'
        return self.xlbook.Worksheets(sheet)

    def getSheetByName(self, name):
        '''get the sheet object by the sheet name'''
        for i in xrange(1, self.getSheetCount() + 1):
            sheet = self.getSheet(i)
            if name == sheet.Name:
                return sheet
        return None

    def getCell(self, sheet=1, row=1, col=1):
        '''get the cell object'''
        assert isinstance(
            row, int) or isinstance(
            col, int), 'the row and col  must be int'
        assert row > 0 and col > 0, 'the row and column index must bigger then 0'
        return self.getSheet(sheet).Cells(row, col)

    def getRow(self, sheet=1, row=1):
        '''get the row object'''
        assert isinstance(row, int), 'the row  must be int'
        assert row > 0, 'the row index must bigger then 0'
        return self.getSheet(sheet).Rows(row)

    def getCol(self, sheet, col):
        '''get the column object'''
        assert isinstance(col, int), 'the col  must be int'
        assert col > 0, 'the column index must bigger then 0'
        return self.getSheet(sheet).Columns(col)

    def getRange(self, sheet, row1, col1, row2, col2):
        '''get the range object'''
        sht = self.getSheet(sheet)
        return sht.Range(
            self.getCell(
                sheet, row1, col1), self.getCell(
                sheet, row2, col2))

    def getCellValue(self, sheet, row, col):
        '''Get value of one cell'''
        return self.getCell(sheet, row, col).Value

    def setCellValue(self, sheet, row, col, value):
        '''set value of one cell'''
        self.getCell(sheet, row, col).Value = value

    def getRowValue(self, sheet, row):
        '''get the row values'''
        return self.getRow(sheet, row).Value

    def setRowValue(self, sheet, row, values):
        '''set the row values'''
        self.getRow(sheet, row).Value = values

    def getColValue(self, sheet, col):
        '''get the row values'''
        return self.getCol(sheet, col).Value

    def setColValue(self, sheet, col, values):
        '''set the row values'''
        self.getCol(sheet, col).Value = values

    def getRangeValue(self, sheet, row1, col1, row2, col2):
        '''return a tuples of tuple)'''
        return self.getRange(sheet, row1, col1, row2, col2).Value

    def setRangeValue(self, sheet, row1, col1, data):
        '''set the range values'''
        row2 = row1 + len(data) - 1
        col2 = col1 + len(data[0]) - 1
        range = self.getRange(sheet, row1, col1, row2, col2)
        range.Clear()
        range.Value = data

    def getSheetCount(self):
        '''get the number of sheet'''
        return self.xlbook.Worksheets.Count

    def getMaxRow(self, sheet):
        '''get the max row number, not the count of used row number'''
        return self.getSheet(sheet).Rows.Count

    def getMaxCol(self, sheet):
        '''get the max col number, not the count of used col number'''
        return self.getSheet(sheet).Columns.Count

    def clearCell(self, sheet, row, col):
        '''clear the content of the cell'''
        self.getCell(sheet, row, col).Clear()

    def deleteCell(self, sheet, row, col):
        '''delete the cell'''
        self.getCell(sheet, row, col).Delete()

    def clearRow(self, sheet, row):
        '''clear the content of the row'''
        self.getRow(sheet, row).Clear()

    def deleteRow(self, sheet, row):
        '''delete the row'''
        self.getRow(sheet, row).Delete()

    def clearCol(self, sheet, col):
        '''clear the col'''
        self.getCol(sheet, col).Clear()

    def deleteCol(self, sheet, col):
        '''delete the col'''
        self.getCol(sheet, col).Delete()

    def clearSheet(self, sheet):
        '''clear the hole sheet'''
        self.getSheet(sheet).Clear()

    def deleteSheet(self, sheet):
        '''delete the hole sheet'''
        self.getSheet(sheet).Delete()

    def deleteRows(self, sheet, fromRow, count=1):
        '''delete count rows of the sheet'''
        maxRow = self.getMaxRow(sheet)
        maxCol = self.getMaxCol(sheet)
        endRow = fromRow + count - 1
        if fromRow > maxRow or endRow < 1:
            return
        self.getRange(sheet, fromRow, 1, endRow, maxCol).Delete()

    def deleteCols(self, sheet, fromCol, count=1):
        '''delete count cols of the sheet'''
        maxRow = self.getMaxRow(sheet)
        maxCol = self.getMaxCol(sheet)
        endCol = fromCol + count - 1
        if fromCol > maxCol or endCol < 1:
            return
        self.getRange(sheet, 1, fromCol, maxRow, endCol).Delete()

    def setCellformat(self, sheet, row, col):
        '''set value of one cell'''
        sht = self.getSheet(sheet)
        sht.Cells(row, col).Font.Size = 15  # 字体大小
        sht.Cells(row, col).Font.Bold = True  # 是否加粗
        sht.Cells(row, col).Name = "Calibri"  # 字体类型
        sht.Cells(row, col).Interior.ColorIndex = 3  # 表格背景
        sht.Cells(row, col).BorderAround(1, 4)  # 表格边框
        sht.Rows(3).RowHeight = 30  # 行高
        sht.Cells(row, col).HorizontalAlignment = -4131  # 水平居中
        sht.Cells(row, col).VerticalAlignment = -4160  # 竖直居中

    def addPicture(self, sheet, pictureName, Left, Top, Width, Height):
        '''insert a picture in sheet'''
        sht = self.getSheet(sheet)
        sht.Shapes.AddPicture(pictureName, 1, 1, Left, Top, Width, Height)

    def cpSheet(self, before):
        '''copy sheet'''
        shts = self.xlbook.Worksheets
        shts(1).Copy(None, shts(1))

    def pivotRefresh(self, pivot_sheet_name, pivotname='PivotTable1'):
        '''open excel and refresh Pivot table'''
        sheet_pivot = self.xlbook.Worksheets(pivot_sheet_name)
        sheet_pivot.PivotTables(
            pivotname).PivotCache().Refresh()  # 修改excel中pivotname

    def create_pivot_table(self,df_excel):
        win32c = win32.constants
        sheet_data = self.xlbook.Worksheets("raw_data")
        cl1 = sheet_data.Cells(1, 1)
        cl2 = sheet_data.Cells(df_excel.shape[0] + 1, df_excel.shape[1])

        PivotSourceRange = sheet_data.Range(cl1, cl2)
        PivotSourceRange.Select()

        Sheet2 = wb.Sheets.Add(After=self.xlbook.Sheets(1))
        Sheet2.Name = 'summary'
        cl3 = Sheet2.Cells(4, 1)
        PivotTargetRange = Sheet2.Range(cl3, cl3)
        PivotTableName = 'Report PivotTable'

        PivotCache = self.xlbook.PivotCaches().Create(SourceType=win32c.xlDatabase, SourceData=PivotSourceRange, Version=win32c.xlPivotTableVersion14)
        PivotTable = PivotCache.CreatePivotTable(TableDestination=PivotTargetRange, TableName=PivotTableName, DefaultVersion=win32c.xlPivotTableVersion14)

        PivotTable.PivotFields('Team').Orientation = win32c.xlRowField
        PivotTable.PivotFields('Team').Position = 1
        PivotTable.PivotFields('AM').Orientation = win32c.xlRowField
        PivotTable.PivotFields('AM').Position = 2
        PivotTable.PivotFields('Client Name').Orientation = win32c.xlRowField
        PivotTable.PivotFields('Client Name').Position = 3

        PivotTable.PivotFields('OC Name').Orientation = win32c.xlPageField
        PivotTable.PivotFields('OC Name').Position = 1

        PivotTable.PivotFields('Invoice Status').Orientation = win32c.xlPageField
        PivotTable.PivotFields('Invoice Status').Position = 2

        PivotTable.PivotFields('Month').Orientation = win32c.xlColumnField
        PivotTable.PivotFields('Month').Position = 1

        DataField = PivotTable.AddDataField(PivotTable.PivotFields('Commission'))
        DataField.NumberFormat = '###0.00'

        self.xlbook.Save()
        self.xlapp.Quit()

def echo(msg):
    '''echo message'''
    print msg


def dealSingle(excel, sfile, dfile):
    '''deal with single excel file'''
    echo("deal with %s" % sfile)
    basefile = os.path.basename(sfile)
    excel.open(sfile)
    sheetcount = excel.getSheetCount()
    if not (basefile in SKIP_FILE_LIST):
        for sheet in range(1, sheetcount + 1):
            if sheet > MAX_SHEET_INDEX:
                continue
            reduce = 0
            for row in DELETE_ROW_LIST:
                excel.deleteRow(sheet, row - reduce)
                reduce += 1
                # excel.deleteRows(sheet, 2, 2)
    excel.save(dfile)


def dealExcel(spath, dpath):
    '''deal with excel files'''
    start = time.time()
    # check source path exists or not
    spath = dealPath(spath)
    if not os.path.isdir(spath):
        echo("No this directory :%s" % spath)
        return
        # check destination path exists or not
    dpath = dealPath(dpath)
    if not os.path.isdir(dpath):
        os.makedirs(dpath)
    shutil.rmtree(dpath)
    # list the excel file
    filelist = glob.glob(os.path.join(spath, '*.xlsx'))
    if not filelist:
        echo('The path of %s has no excel file' % spath)
        return
        # deal with excel file
    excel = EasyExcel()
    for file in filelist:
        basefile = os.path.basename(file)
        destfile = os.path.join(dpath, basefile)
        dealSingle(excel, file, destfile)
    echo('Use time:%s' % (time.time() - start))
    excel.close()


def main():
    if SRC_PATH and DST_PATH and MAX_SHEET_INDEX:
        dealExcel(SRC_PATH, DST_PATH)


if __name__ == "__main__":
    main()
