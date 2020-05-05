# 环境准备：
#【1】安装paddleHub： pip install paddlehub==1.6.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
#【2】安装抠图模型 ：hub download deeplabv3p_xception65_humanseg

# 生成红蓝立体图
import paddlehub as hub
import matplotlib.pyplot as plt
from PIL import Image , ImageOps

_DELTA_=5
humanseg = hub.Module( name="deeplabv3p_xception65_humanseg" )

def make_3d_image( o_img ):
    # 存储临时文件
	tmp_png_file='0.tmp_png_file.png'
	o_img.save( tmp_png_file )
	# 人像抠图，读出
	result = humanseg.segmentation( data={"image": [tmp_png_file]} )
	hub_img = Image.open( result[0]['processed'] )
	h_w,h_h=hub_img.size
	h_r,h_g,h_b,h_a = hub_img.split( )

	# 制作人像重影遮罩
	img_mask_1 = ImageOps.invert( h_a )#.convert( '1' )
	img_mask_2 = Image.new( 'RGB', ( h_w + _DELTA_,h_h ), ( 255, 255, 255 ) )
	img_mask_2.paste( img_mask_1,( _DELTA_ + 0,0,_DELTA_ + h_w,h_h ) )
	img_mask_2.paste( img_mask_1,( 0,0,h_w,h_h ),mask=h_a )
	#img_mask_2 = ImageOps.invert( img_mask_2 )
	img_mask_2 = img_mask_2.crop( box=( 0,0,h_w,h_h ) )

	#前景画布
	img_Front = Image.new( 'RGB', ( h_w + _DELTA_,h_h ), ( 255, 255, 255 ) )
	img_Front.paste( o_img,( 0,0,h_w,h_h ),mask=img_mask_2.convert( 'L' ) )
	## 方法1：立体感好，但左侧有黑边
	#img_Front.paste( ImageOps.invert( h_a ),( 0,0,h_w,h_h ),mask=h_a ) 
	## 方法2：左侧衔接好，但左侧无立体感
	#img_Front.paste( o_img,( 0,0,h_w,h_h ),mask=h_a )
	## 方法3：结合上面两种左侧1px黑边，衔接基本还好
	img_Front.paste( ImageOps.invert( h_a ),( 0,0,h_w,h_h ),mask=h_a )
	img_Front.paste( o_img,( 1,0,h_w + 1,h_h ),mask=h_a )

	img_Front.paste( o_img,( 0 + _DELTA_,0,h_w + _DELTA_,h_h ),mask=ImageOps.invert( img_mask_2 ).convert( 'L' ) ) 
	img_Front = img_Front.crop( box=( 0,0,h_w,h_h ) )
	f_r,f_g,f_b = img_Front.split( )

	#背景用原画r通道，前景用g + b通道
	#return Image.merge( 'RGB',( h_r,f_g,f_b ) )
	return Image.merge( 'RGB',( f_r,h_g,h_b ) )
	#return ImageOps.invert( img_mask_2 )
	#return o_img


#【1】图片测试：
src_image=Image.open( 'video/throwingfootball/0.png' )
#plt.figure( figsize=( 15,15 ) )
#plt.axis( 'off' )
plt.imshow( src_image )
plt.show( src_image )
tgt_image = make_3d_image( src_image )
print( tgt_image )
plt.imshow( tgt_image ) 
plt.show( tgt_image ) 

#【2】视频测试：
from videoProcessor import video_process
print('processed {} frames in total.'.format( video_process('video/throwingfootball.mp4','video',proc=make_3d_image) ))
print('processed {} frames in total.'.format( video_process('video/White_15.2019.mp4','video',proc=make_3d_image,sample=9.0) ))
