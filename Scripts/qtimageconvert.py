import os
from PyQt4.QtGui import QImage

for file in os.walk('.').next()[2]:
    if not file.endswith('.png'): continue
    i = QImage()
    i.load(file)
    i.save(file)
    print('%s is successfully converted' % file)
