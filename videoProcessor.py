# 视频逐帧处理：输入MP4，输出avi
from PIL import Image
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 

def video_process(src_file,dst_path='',proc=lambda x:x,sample=None,bar=True):
    src_video = cv2.VideoCapture(src_file)
    f_name=os.path.join(dst_path,src_file.split(os.sep)[-1].split('.')[0]+('.sample_%d'%sample if type(sample)==int else '')+'.avi')
    frame_size = ( int(src_video.get(3)),int(src_video.get(4)))
    frame_rate =int(src_video.get(5))
    frame_cnt =int(src_video.get(7))
    # 进度条
    def process_bar(percent, start_str='', end_str='', total_length=0):
        bar = ''.join(["="] * int(percent * total_length)) + ''
        bar = '\r' + start_str +' ['+ bar.ljust(total_length) + ']{:0>4.1f}% '.format(percent*100) + end_str
        print(bar, end='', flush=True)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.VideoWriter_fourcc('I','4','2','0')
    #fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    dst_video = cv2.VideoWriter( f_name, fourcc, frame_rate, frame_size , True )
    count = 0 
    while True: 
        flag, frame = src_video.read() 
        if flag: 
            if (type(sample)==int and count%sample==0) or type(sample)!=int:
                _frm_ = frame
                _frm_ =  cv2.cvtColor(_frm_, cv2.COLOR_BGR2RGB)
                _frm_ = Image.fromarray(_frm_)
                _frm_ = proc(_frm_)
                _frm_ = np.array(_frm_)
                _frm_ =  cv2.cvtColor(_frm_, cv2.COLOR_RGB2BGR)
                dst_video.write(_frm_)
            count = count + 1 
            if bar:
                process_bar(count/frame_cnt, start_str=f_name, end_str='', total_length=50)
        else:
            dst_video.release()
            src_video.retrieve()
            if bar:
                print()
            return count
