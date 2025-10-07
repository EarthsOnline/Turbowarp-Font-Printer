# Turbowarp-Font-Printer
### 这是什么?
Fonts Printer.sb3 - 可以在 Turbowarp 上运行的文字打印插件
TTF2Png.py - 提取 .TTF 文件中每个字形的 png 图片
### 作者是谁?
Fonts Printer.sb3  
EarthsOnline 导入了 6000+ 造型并手动编写了程序  
  
TTF2Png.py  
DeepSeek 🐋 基于 [@CSDN_拜阳](https://blog.csdn.net/bby1987/article/details/142371889) 的程序编写并进行了 3 次修改  
### 支持什么功能?
> Fonts Printer
1. 对不存在对应造型的文字的处理
2. 对 Unicode 范围重叠的文字的处理
3. 动态调节文本的间隔
4. 超出边框自动换行
5. 按 X 瞬间完成生成
6. 通过 is_generating 变量判断是否处于生成中, 避免出现冲突
> TTF2Png
1. 便于使用的 UI
2. 对英文/汉字/数字/特殊符号的分类提取
3. 正确地处理大小写
4. 可以在控制台追踪生成结果
