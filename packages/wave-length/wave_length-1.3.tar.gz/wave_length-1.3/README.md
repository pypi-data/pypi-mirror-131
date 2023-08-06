# 依赖库

1. numpy
2. pandas
3. matpltlib

# 介绍

该库使用步长为0.1 nm 的标准CIE色度匹配图进行光谱波长计算。

# 使用教程

work(file, start=380, end=780, draw=True, statr_line=8)

file文件须为 txt 文档，格式如下：

[nm]   ;[counts] ;[counts] ;[counts] 

143.968;  270.000;    0.000;    0.000

144.581;  295.000;    0.000;    0.000

145.194;  261.000;    0.000;    0.000

145.807;  292.429;    0.000;    0.000

# 参数使用规则

file：你的txt数据存储文件

start：计算波谱的起点——默认为 390nm。自定义值必须在区间 [390, 830]中，默认为390

end： 计算波谱的终点——默认为830nm。 自定义值必须在区间 [390, 830]中， 默认为830

draw：是否绘制展示图，默认为True

start_line：读取txt文档数据的起点，默认为8。如果你的txt文档有效数据是从第1行开始的，则将该参数设置为0。


# 返回的参数
x： CIE xy色度图的x值

y： CIE xy色度图的y值

result_lambda：你的波谱计算得到的波长

Lambda：CIE1931色彩空间色度图波长，步长为0.1nm —— array。 范围为 390——830

Lambda_x：CIE1931色彩空间色度图各波长对应的x —— array

Lambda_y：CIE1931色彩空间色度图各波长对应的y —— array


# 运行文件

运行需要两个关键文件，需要在下面网址去下载；

链接：https://pan.baidu.com/s/1CNjeEJy5hTK4IbnActwj2w 
提取码：cg2q

将里面的两个文件放在你自己代码的同级目录下。然后运行如下代码即可

from wavelength import wavelength

wavelength.work("file_path")