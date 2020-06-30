import cv2
import numpy as np
import codecs
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
# 讀取圖片檔禎數
m1=cv2.imread("image/01.png",1)
print(m1)
print(m1.shape)
cv2.imshow("m1", m1)
m2=cv2.cvtColor(m1, cv2.COLOR_BGR2GRAY)
cv2.imshow("m2", m2)
cv2.imwrite("image/m2.png", m2, [cv2.IMWRITE_JPEG_QUALITY, 100])
cv2.waitKey(0)
cv2.destroyAllWindows()

# # 自製圖片
m3 = np.full((300,350 ,3),(190,160,60), np.uint8)
# 在圖片上標記
cv2.line(m3, (0,0), (120,120), (255,255,255), 2)
cv2.rectangle(m3, (50,50), (170,170), (160,50,120), 3)
cv2.circle(m3, (170,170), 80, (50,150,30), 4)
cv2.imshow("m3", m3)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 自製動畫
# 存檔
w1 = cv2.VideoWriter(
	"video/03.mp4",
	cv2.VideoWriter_fourcc(*'MP4V'),
	30,
	(350,300)
)
i = 30
j = 220
x = 5
while True:
	m3 = np.full((300,350 ,3),255, np.uint8)
	cv2.circle(m3, (170,150), i, [150,150-i,30], -1)
	cv2.circle(m3, (170,150), j, (j,60,j+30), 3)
	cv2.imshow("m3", m3)
	w1.write(m3)
	i=i+x
	j=j-5
	if i>200 | j<10:
		x=-x
		j=220
	if cv2.waitKey(33) != -1:
		break
w1.release()
cv2.destroyAllWindows()

# 影片讀取
v1 = cv2.VideoCapture("video/01.mp4")
print("高度:", v1.get(4))
print("寬度:", v1.get(3))
print("每秒撥放影格數:", v1.get(5))
v1.set(1,1000)

# 影片寫入
w1 = cv2.VideoWriter(
	"video/02.mp4",
	cv2.VideoWriter_fourcc(*"MP4V"),
	30,
	(int(v1.get(3)),int(v1.get(4)))
)
while v1.isOpened()==True:
	r, m1=v1.read()
	if r==True:
		cv2.imshow("m1",m1)
		w1.write(m1)
	if cv2.waitKey(33)!=-1:
		break
w1.release()
cv2.destroyAllWindows()

# 啟用攝影機
cap = cv2.VideoCapture(1)
w1 = cv2.VideoWriter(
	"video/05.mp4",
	cv2.VideoWriter_fourcc(*'MP4V'),
	30,
	(int(cap.get(3)),int(cap.get(4)))
)
cap.open(1)
print(cap.isOpened())
while(True):
  	# 從攝影機擷取一張影像
  	ret, frame = cap.read()

  	# 顯示圖片
  	cv2.imshow('frame', frame)
  	
	while(cap.isOpened() == True):
		r, m1=cap.read()
		if r==True:
			cv2.imshow("m1",m1)
			w1.write(m1)
		if cv2.waitKey(33)!=-1:
			break
	# 若按下 q 鍵則離開迴圈
	if cv2.waitKey(1) & 0xFF == ord('q'):
    	break
w1.release()
cv2.destroyAllWindows()

# 寫字, 浮水印
from PIL import ImageFont, ImageDraw, Image
m3 = np.full((300,350 ,3),220, np.uint8)
m3 = Image.fromarray(m3)
ImageDraw.Draw(m3).text(
	(0,60),
	"今天天氣好晴朗",
	(90,50,160),
	ImageFont.truetype("study/msjh.ttc", 50))
m3 = np.array(m3)
cv2.imshow("m3", m3)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 圖像BGR加減 
m1 = cv2.imread("image/02.png",1)
m2 = np.full(m1.shape, 90, np.uint8)
m3 = cv2.add(m1,m2)
m3 = cv2.subtract(m1,m2)
m3 = cv2.absdiff(m1,m2)
m4 = cv2.bitwise_not(m1)
m3 = m1+200
cv2.imshow("m1", m1)
cv2.imshow("m2", m2)
cv2.imshow("m3", m3)
cv2.imshow("m4", m4)
# 大小比列縮放
m4 = cv2.resize(m1,(500,500))
h = 500
w = int((h/m1.shape[0])*m1.shape[1])
m3 = cv2.resize(m1,(w,h))
# 翻轉 (1, 0, -1)
m3 = cv2.flip(m1, 1)
# 旋轉
m=cv2.getRotationMatrix2D((50,50), 45, 2)
m3=cv2.warpAffine(m1, m, (m1.shape[1],m1.shape[0]))
# 裁切
m3=m1[50:140,220:300]

# 篩選,複製貼上 [起始像素:終點像素:間格像素, 起始像素:終點像素:間格像素]
m3 = np.full((500, 600, 3), 190, np.uint8)
m3[100:200,50:250]=m1[60:160,15:215]
m4=m1[60:160:2,15:215:2]
# 色彩通道 0:B, 1:G, 2:R
m2 = np.full((300,350 ,3),(0,255,0), np.uint8)
m3 = m2[:,:,0]
m4 = m2[:,:,1]
m5 = m2[:,:,2]
cv2.imshow("m1", m1)
cv2.imshow("m2", m2)
cv2.imshow("m3", m3)
cv2.imshow("m4", m4)
cv2.imshow("m5", m5)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 0325hw2 作業解法提示
h1 = cv2.imread("image/homework2.png",1)
h2 = np.full(h1.shape,255, np.uint8)
for y in range(0,h1.shape[0],1):
	for x in range(0,h1.shape[1]):
		if h1[y,x,0]==255 and h1[y,x,1]==255 and h1[y,x,2]==255:
			h2[y,x]=0
h3=cv2.cvtColor(h2, cv2.COLOR_BGR2GRAY)
h4=cv2.cvtColor(h3, cv2.COLOR_GRAY2BGR)
cv2.imshow("h1", h1)
cv2.imshow("h2", h2)
cv2.imshow("h3", h3)
cv2.imshow("h4", h4)
cv2.waitKey(0)
cv2.destroyAllWindows()

