import pytesseract
import cv2
# img = cv2.imread("image.jpg")

# ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)  #二值化
# print(pytesseract.image_to_string(img))
# cv2.imshow("1",img)
# cv2.waitKey(0)
from PIL import Image, ImageFilter

# 開啟影像檔案
image = Image.open('haaa.png')

gray_image = image.convert('L')

# 進行二值化處理
threshold = 150  # 二值化閾值，可根據需要調整
binary_image = gray_image.point(lambda p: p > threshold and 255)
#進行降噪處理
denoised_image = binary_image.filter(ImageFilter.MedianFilter)

print(pytesseract.image_to_string(binary_image))
# 顯示處理後的影像
