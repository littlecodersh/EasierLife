#coding = utf8
'''
getData()    returns a LIST contains a row in order
storeData()  stores a LIST contains a row in order
'''
import xlrd, xlwt

class ExcelClient:
    def __init__(self, sourceDir = None, outputDir = None, sourceIndex = None, outputHeader = None):
        self.sourceDir = sourceDir
        self.outputDir = outputDir if outputDir else 'DemoExcelClientOutput.xls'
        self.source = self.getSource(sourceIndex) if sourceIndex else None
        self.output = self.setOutput()
        self.storeData(outputHeader)
    def getSource(self, dataRange): # content will be the first
        with xlrd.open_workbook(self.sourceDir) as workbook:
            table = workbook.sheets()[0]
            for i in range(1, table.nrows): # ignore header
                yield [table.row_values(i)[j] for j in dataRange]
    def setOutput(self):
        workbook = xlwt.Workbook()
        table = workbook.add_sheet('metaData')
        row = 0
        while True:
            if self.outputData:
                for col in range(len(self.outputData)): table.write(row, col, self.outputData[col])
                row += 1
                workbook.save(self.outputDir)
                yield True
            else:
                yield False
    def getData(self): # returns a LIST contains a row in order
        try:
            return self.source.next()
        except StopIteration, AttributeError:
            return None
    def storeData(self, data): # stores a LIST contains a row in order
        self.outputData = data
        return self.output.next()

if __name__ == '__main__':
    iec = ExcelClient(sourceDir = '1.xlsx', sourceIndex = (0,1))
    oec = ExcelClient(outputDir = '1.xlsx', outputHeader = ['subject', 'time'])
    for i in range(3):
        data = iec.getData()
        oec.storeData(data)

