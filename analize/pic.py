import cv2
import os


def get_pic_size(path):
	filelist = os.listdir(path)  # 获取该目录下的所有文件名
	for item in filelist:
		if item.endswith('.jpg'):  # 判断图片后缀是否是.png
			item = path + '/' + item
			img = cv2.imread(item)
			size = str(img.shape)
			if "320" in size:
				return (320,240)
			else:
				return (640,480)


print(get_pic_size("E:\\3a61c8c61327e87c4929fe\\"))