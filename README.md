# Turbowarp-Font-Printer
### 这是什么?
Fonts Printer.sb3 - 可以在 Turbowarp 上运行的文字打印插件  
TTF2Png.py - 提取 .TTF 文件中每个字形的 png 图片  

### 作者是谁?
Fonts Printer.sb3  
EarthsOnline  
  
TTF2Png.py  
DeepSeek 🐋 基于 [@CSDN_拜阳](https://blog.csdn.net/bby1987/article/details/142371889) 的程序编写并进行了修改  

### 运行环境?
Fonts Printer 使用了大量的 Turbowarp 拓展库。因此它 **完全不能** 在 Scratch 3.0 上运行。  
  
TTF2Png.py 需要安装 **依赖库** Fonttools 和 Pillow, 您可以通过: **`pip install Fonttools pillow`** 进行安装。

### 更新日志
> Fonts Printer.sb3

| S.N. | | Changes |
|:-:|:-:|:-|
|1|+|对不存在对应造型的文字的处理|
||+|对 Unicode 范围重叠的文字的处理|
||+|动态调节文本的间隔|
||+|超出边框自动换行|
||+|按 X 瞬间完成生成|
||+|通过 is_generating 变量判断是否处于生成中避免冲突|
|2|-|完全删除了方正像素 16 字体|
||+|分离了前缀和正文|
||+|自动缩进正文|
||+|自定义文字右边界|
||+|使用了更为常用的方正基础像素字体|
|3|-|使用迭代方式优化了大量冗余代码|
||-|为适配迭代移除了 is_generating|

> TTF2Png.py

| S.N. | | Changes |
|:-:|:-:|:-|
|1|+|可视化的 UI|
||+|对英文/汉字/数字/特殊符号的分类提取|
|2|+|处理了 Windows 不区分文件名大小写的问题|
||+|增加了控制台输出进行调试|
|3|-|删除了非英文字母提取时产生的 upper 和 lower 文件夹
||+|常用汉字提取
|4|-|优化了 precise_chinese_3500[] 格式
||+|提取特定字符的图片|
||+|批量提取特定字符的图片|
