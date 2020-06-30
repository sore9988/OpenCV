import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

m1 = cv2.imread("image/01.png",1)
cv2.imshow("m1", m1)
m2 = m1.copy()
# 二值化
# cv2.THRESH_OTSU (整張處理) 只能用灰階圖片 要處理彩色 => 分三張處理
th, m2[:,:,0]=cv2.threshold(m1[:,:,0], 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print(th)
th, m2[:,:,1]=cv2.threshold(m1[:,:,1], 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print(th)
th, m2[:,:,2]=cv2.threshold(m1[:,:,2], 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print(th)
cv2.imshow("m2", m2)
cv2.imshow("m2 B", m2[:,:,0])
cv2.imshow("m2 G", m2[:,:,1])
cv2.imshow("m2 R", m2[:,:,2])

# adaptiveThreshold (小區塊處理) 只能用灰階圖片 要處理彩色 => 分三張處理
# 區塊越小(只能用奇數) => 線條越細 , 微調值(0, 1) 影響
m2=cv2.adaptiveThreshold(m1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,51,50)
m2[:,:,0]=cv2.adaptiveThreshold(m1[:,:,0],255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,0)
m2[:,:,1]=cv2.adaptiveThreshold(m1[:,:,1],255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,)
m2[:,:,2]=cv2.adaptiveThreshold(m1[:,:,2],255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,)
cv2.imshow("m2", m2)

# 影像邊緣偵測 辨識
m2=cv2.Canny(m1,200,100)
cv2.imshow("m2", m2)

# 模糊化 : 美肌功能
# (平均數)
m2=cv2.blur(m1,(25,25))
cv2.imshow("m2", m2)

# 中值模糊化 + 奇數 => 字會直接消失
m3=cv2.medianBlur(m1,25)
cv2.imshow("m3", m3)

# 銳利化 : 顏色貝拉到 255 或 0 , 只能用餘灰階
m2 = cv2.equalizeHist(m1)
cv2.imshow("m2", m2)

# 侵蝕 色彩高的下降 , 色彩低的上升 , ((高,寬))
m2 = cv2.erode(m1, np.ones((5,5)))
cv2.imshow("m2", m2)
# 膨脹 與 侵蝕 相反
m3 =cv2.dilate(m2, np.ones((5,5)))
cv2.imshow("m3", m3)

# 侵蝕與膨脹結合的參數 
cv2.MORPH_OPEN：先執行侵蝕後執行膨脹
cv2.MORPH_CLOSE：先執行膨脹後執行侵蝕
cv2.MORPH_GRADIENT：執行膨脹與侵蝕產生的變化差
m2 = cv2.morphologyEx(m1, cv2.MORPH_GRADIENT, np.ones((4,4)))
cv2.imshow("m2", m2)

# 色彩篩選 回傳為灰階
m2=cv2.inRange(m1, (0,0,0), (200,200,200))
cv2.imshow("m2", m2)
m3=cv2.inRange(m1, (150,150,150), (255,255,255))
cv2.imshow("m3", m3)
# 利用色彩篩選選出要得圖像 , 搭配 膨脹, 模糊等去除小喳喳再+m1 =>變彩色了
m4=cv2.add(m2,m3)
m4=cv2.cvtColor(m4,cv2.COLOR_GRAY2BGR)
m4=cv2.add(m4,m1)
m4=cv2.dilate(m4, np.ones((5,5)))
cv2.imshow("m4", m4)
# 
m1 = cv2.imread("image/g3.jpg",1)
cv2.imshow("m1", m1)

m2=np.full(m1.shape, 0, np.uint8)
m2[230:300,180:260,0]=cv2.inRange(m1[230:300,180:260,0], (0,0,0), (200,200,200))
m2[230:300,180:260,1]=cv2.inRange(m1[230:300,180:260,1], (0,0,0), (200,200,200))
m2[230:300,180:260,2]=cv2.inRange(m1[230:300,180:260,2], (0,0,0), (200,200,200))
cv2.imshow("m2", m2)

# **抓圖像輪廓** => 先轉灰階圖片 => 再二值化 => 再抓輪廓
m2 = cv2.cvtColor(m1,cv2.COLOR_BGR2GRAY)
th, m2=cv2.threshold(m2, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# 先用侵蝕再用輪廓偵測 => 使文字連在一起, 方便擷取
# m2 = cv2.erode(m2, np.ones((1,25)))
cv2.imshow("m2", m2)
c, t=cv2.findContours(m2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(c)

# 繪製輪廓
m3 = np.full(m1.shape,255,np.uint8)
cv2.drawContours(m3, c, -1, (0,0,0), 1)
# 快一點, 快速過濾出想要的
for d in range(0, len(c),1):
	if len(c[d])>1:
		cv2.drawContours(m3, c, d, (0,0,0), 1)

# 取得包覆指定輪廓點的最小正矩形：
x, y, w, h=cv2.boundingRect(c[18])
cv2.rectangle(m3, (x,y), (x+w, y+h), (0,255,0), 2)

m3=m1.copy()
# 抓 LOGO
for d in range(0, len(c),1):
	x, y, w, h=cv2.boundingRect(c[d])
	if w>m1.shape[1]*0.08 and w<m1.shape[1]*0.6:
		cv2.drawContours(m3, c, d, (0,0,0), 2)
		cv2.rectangle(m3, (x,y), (x+w, y+h), (0,255,0), 2)
		# m3 = m1[y:y+h, x:x+w]
m3 = cv2.add(m3,m1)
cv2.imshow("m3", m1)
cv2.imwrite("image/m3.png", m3)

# 抓文字
for d in range(0, len(c),1):
	x, y, w, h=cv2.boundingRect(c[d])
	if w>h*3:
		cv2.drawContours(m3, c, d, (0,0,0), -1)
		cv2.rectangle(m3, (x,y), (x+w, y+h), (0,255,0), 2)
		m3 = m1[y:y+h, x:x+w]
		cv2.imshow("m3"+str(d), m3)
		cv2.imwrite("image/01/m3_"+ str(d) +".png", m3)



cv2.waitKey(0)
cv2.destroyAllWindows()