import pyscreenshot as ImageGrab
from PIL import Image
import pytesseract

def main():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #指定tesseract.exe執行檔位置
    img = ImageGrab.grab(bbox=(100, 100, 150, 150))  # X1, Y1, X2, Y2
    img.show()
    text = pytesseract.image_to_string(img, lang='eng') #讀英文
    #text = pytesseract.image_to_string(img, lang='chi_sim') #簡體中文
    #text = pytesseract.image_to_string(img, lang='chi_tra') #繁體中文
    print(text)
if __name__ == '__main__':
    main()
