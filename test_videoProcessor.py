from videoProcessor import video_process

# 最简单的方法：原样输出
def process(img_in):
    #  在此处修改代码
    img_out = img_in
    return img_out

## 测试原样输出，相当于mp4转avi
print('processed {} frames in total.'.format( video_process('work/throwingfootball.mp4','data',proc=process) ))

# 把颜色通道打乱输出：
def jamColor(img_in):
    #  在此处修改代码
    colors = img_in.split()
    r = colors[0]
    g = colors[1]
    b = colors[2]
    img_out = Image.merge( 'RGB',( b,r,g ) )
    return img_out


## 颜色通道打乱,proc是处理用的函数rgb入rgb出，sample是每过几帧取1帧（注意只有是整数时才有效），有个隐藏的参数bar用于控制是否打印进度
print('processed {} frames in total.'.format( video_process('work/throwingfootball.mp4','data',proc=jamColor,sample=5) ))
