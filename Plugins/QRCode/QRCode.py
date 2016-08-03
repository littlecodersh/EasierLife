from PIL import Image 
import sys, os

QR_DIR = '.'
try:
    b = u'\u2588'
    sys.stdout.write(b + '\r')
    sys.stdout.flush()
except UnicodeEncodeError:
    BLOCK = 'MM'
else:
    BLOCK = b

class QRCode():
    pass
def print_cmd_qr(fileDir, size = 37, padding = 3,
        white = BLOCK, black = '  '):
    img     = Image.open(fileDir)
    times   = img.size[0] / (size + padding * 2)
    rgb     = img.convert('RGB')
    sys.stdout.write(' '*50 + '\r')
    sys.stdout.flush()
    qr = white * (size + 2) + '\n'
    startPoint = padding + 0.5
    for y in range(size):
        qr += white
        for x in range(size):
            r,g,b = rgb.getpixel(((x + startPoint) * times, (y + startPoint) * times))
            qr += white if r > 127 else black
        qr += white + '\n'
    qr += white * (size + 2) + '\n'
    sys.stdout.write(qr)

if __name__ == '__main__':
    # 37 is for picture size without padding, 3 is padding
    # q = QRCode(os.path.join(QR_DIR, 'QR.jpg'), 37, 3, 'BLACK')
    print_cmd_qr(os.path.join(QR_DIR, 'QR.jpg'))
