import os
import cv2

import moviepy.editor as mpe


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


def picvideo(path):
	filelist = os.listdir(path)  # 获取该目录下的所有文件名

	fps = 6
	size = get_pic_size(path) #图片的分辨率片
	file_path = r"D:\data\xxxy.mp4"  # 导出路径
	fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')  # 不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）

	video = cv2.VideoWriter(file_path, fourcc, fps, size)

	for item in filelist:
		if item.endswith('.jpg'):  # 判断图片后缀是否是.png
			item = path + '/' + item
			img = cv2.imread(item)  # 使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。
			video.write(img)  # 把图片写进视频

	video.release()  # 释放

picvideo("D:\data\pic")

# my_clip = mpe.VideoFileClip('D:\data\\xxx.mp4')
# my_clip.write_videofile("D:\data\\yyy.mp4",audio="D:\data\music\\0011.mp3")