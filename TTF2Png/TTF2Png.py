# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import re


class FontExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("字体字符提取工具")
        self.root.geometry("600x500")

        self.setup_ui()

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 字体文件选择
        ttk.Label(main_frame, text="字体文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.font_path = tk.StringVar()
        font_frame = ttk.Frame(main_frame)
        font_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Entry(font_frame, textvariable=self.font_path, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(font_frame, text="浏览", command=self.browse_font).pack(side=tk.RIGHT, padx=(5, 0))

        # 输出目录
        ttk.Label(main_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar()
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="浏览", command=self.browse_output).pack(side=tk.RIGHT, padx=(5, 0))

        # 参数设置
        params_frame = ttk.LabelFrame(main_frame, text="参数设置", padding="5")
        params_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # 字体大小
        ttk.Label(params_frame, text="字体大小:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.font_size = tk.IntVar(value=112)
        ttk.Entry(params_frame, textvariable=self.font_size, width=10).grid(row=0, column=1, sticky=tk.W, pady=2,
                                                                            padx=(5, 0))

        # 图片尺寸
        ttk.Label(params_frame, text="图片尺寸:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=(20, 0))
        self.image_size = tk.IntVar(value=128)
        ttk.Entry(params_frame, textvariable=self.image_size, width=10).grid(row=0, column=3, sticky=tk.W, pady=2,
                                                                             padx=(5, 0))

        # 命名模式
        ttk.Label(params_frame, text="命名模式:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.name_mode = tk.StringVar(value="char")
        ttk.Combobox(params_frame, textvariable=self.name_mode,
                     values=["char", "unicode"], width=10, state="readonly").grid(row=1, column=1, sticky=tk.W, pady=2,
                                                                                  padx=(5, 0))

        # 图片格式
        ttk.Label(params_frame, text="图片格式:").grid(row=1, column=2, sticky=tk.W, pady=2, padx=(20, 0))
        self.image_format = tk.StringVar(value="png")
        ttk.Combobox(params_frame, textvariable=self.image_format,
                     values=["png", "jpg", "bmp"], width=10, state="readonly").grid(row=1, column=3, sticky=tk.W,
                                                                                    pady=2, padx=(5, 0))

        # 字符类型选择
        chars_frame = ttk.LabelFrame(main_frame, text="提取字符类型", padding="5")
        chars_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        self.extract_chinese = tk.BooleanVar(value=True)
        self.extract_english = tk.BooleanVar(value=True)
        self.extract_digits = tk.BooleanVar(value=True)
        self.extract_symbols = tk.BooleanVar(value=False)
        self.extract_all = tk.BooleanVar(value=False)

        ttk.Checkbutton(chars_frame, text="中文字符", variable=self.extract_chinese).grid(row=0, column=0, sticky=tk.W,
                                                                                          pady=2)
        ttk.Checkbutton(chars_frame, text="英文字母", variable=self.extract_english).grid(row=0, column=1, sticky=tk.W,
                                                                                          pady=2)
        ttk.Checkbutton(chars_frame, text="数字", variable=self.extract_digits).grid(row=0, column=2, sticky=tk.W,
                                                                                     pady=2)
        ttk.Checkbutton(chars_frame, text="符号", variable=self.extract_symbols).grid(row=1, column=0, sticky=tk.W,
                                                                                      pady=2)
        ttk.Checkbutton(chars_frame, text="全部字符", variable=self.extract_all,
                        command=self.toggle_all_chars).grid(row=1, column=1, sticky=tk.W, pady=2)

        # 跳过已存在文件
        self.skip_existing = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="跳过已存在的文件", variable=self.skip_existing).grid(row=4, column=0,
                                                                                               columnspan=3,
                                                                                               sticky=tk.W, pady=5)

        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # 状态标签
        self.status = tk.StringVar(value="准备就绪")
        ttk.Label(main_frame, textvariable=self.status).grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=5)

        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="开始提取", command=self.start_extraction).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清空状态", command=self.clear_status).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="退出", command=self.root.quit).pack(side=tk.LEFT)

        # 配置权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def browse_font(self):
        filename = filedialog.askopenfilename(
            title="选择字体文件",
            filetypes=[("字体文件", "*.ttf *.otf *.TTF *.OTF"), ("所有文件", "*.*")]
        )
        if filename:
            self.font_path.set(filename)
            # 自动设置输出目录
            base_name = os.path.splitext(os.path.basename(filename))[0]
            output_dir = os.path.join(os.path.dirname(filename), f"{base_name}_images")
            self.output_path.set(output_dir)

    def browse_output(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_path.set(directory)

    def toggle_all_chars(self):
        if self.extract_all.get():
            state = 'disabled'
            self.extract_chinese.set(True)
            self.extract_english.set(True)
            self.extract_digits.set(True)
            self.extract_symbols.set(True)
        else:
            state = 'normal'

        # 更新其他复选框状态
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Checkbutton) and widget.cget('text') != "全部字符":
                widget.configure(state=state)

    def clear_status(self):
        self.status.set("准备就绪")
        self.progress['value'] = 0

    def start_extraction(self):
        if not self.font_path.get():
            messagebox.showerror("错误", "请选择字体文件")
            return

        if not self.output_path.get():
            messagebox.showerror("错误", "请选择输出目录")
            return

        try:
            self.status.set("正在提取字符...")
            self.root.update()

            font2image(
                font_file=self.font_path.get(),
                font_size=self.font_size.get(),
                image_size=self.image_size.get(),
                out_folder=self.output_path.get(),
                name_mode=self.name_mode.get(),
                image_extension=self.image_format.get(),
                extract_chinese=self.extract_chinese.get(),
                extract_english=self.extract_english.get(),
                extract_digits=self.extract_digits.get(),
                extract_symbols=self.extract_symbols.get(),
                extract_all=self.extract_all.get(),
                is_skip=self.skip_existing.get(),
                progress_callback=self.update_progress
            )

            self.status.set("提取完成！")
            messagebox.showinfo("完成", "字符提取完成！")

        except Exception as e:
            self.status.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"提取过程中出现错误:\n{str(e)}")

    def update_progress(self, value):
        self.progress['value'] = value
        self.status.set(f"处理进度: {value:.1f}%")
        self.root.update()


def get_cmap(font_file):
    """获取unicode cmap - 字符到字形索引映射表"""
    try:
        font = TTFont(font_file)
        cmap = font.getBestCmap()
        font.close()
        return cmap
    except Exception as e:
        print(f"读取字体文件错误: {e}")
        return None


def classify_unicode(decimal_unicode):
    """将Unicode字符分类 - 改进版本"""
    chinese_chars = []
    english_chars = []
    digit_chars = []
    symbol_chars = []

    for code in decimal_unicode:
        char = chr(code)

        # 中文字符 (包括CJK统一表意文字和扩展)
        if (0x4E00 <= code <= 0x9FFF or  # CJK统一表意文字
                0x3400 <= code <= 0x4DBF or  # CJK扩展A
                0x20000 <= code <= 0x2A6DF or  # CJK扩展B
                0x2A700 <= code <= 0x2B73F or  # CJK扩展C
                0x2B740 <= code <= 0x2B81F or  # CJK扩展D
                0x2B820 <= code <= 0x2CEAF or  # CJK扩展E
                0xF900 <= code <= 0xFAFF or  # CJK兼容象形文字
                0x2F800 <= code <= 0x2FA1F):  # CJK兼容补充
            chinese_chars.append(code)

        # 英文字母 - 扩展范围
        elif (0x0041 <= code <= 0x005A or  # 大写字母 A-Z
              0x0061 <= code <= 0x007A or  # 小写字母 a-z
              0x00C0 <= code <= 0x00FF or  # 带重音符号的拉丁字母
              0x0100 <= code <= 0x017F or  # 拉丁扩展-A
              0x0180 <= code <= 0x024F):   # 拉丁扩展-B
            english_chars.append(code)

        # 数字
        elif 0x0030 <= code <= 0x0039:
            digit_chars.append(code)

        # 符号 (更全面的排除控制字符)
        elif (code >= 0x0020 and code <= 0x007E) or (code >= 0x00A0 and code <= 0x00BF) or \
             (code >= 0x2000 and code <= 0x206F):  # 一般标点符号
            # 排除控制字符
            if code not in [0x007F, 0x0080, 0x0081, 0x0082, 0x0083, 0x0084, 0x0085, 0x0086, 0x0087,
                            0x0088, 0x0089, 0x008A, 0x008B, 0x008C, 0x008D, 0x008E, 0x008F, 0x0090,
                            0x0091, 0x0092, 0x0093, 0x0094, 0x0095, 0x0096, 0x0097, 0x0098, 0x0099,
                            0x009A, 0x009B, 0x009C, 0x009D, 0x009E, 0x009F]:
                symbol_chars.append(code)

    return chinese_chars, english_chars, digit_chars, symbol_chars


def get_bbox_offset(bbox, image_size):
    """获取偏移量以将边界框移动到图像中心"""
    if not isinstance(image_size, (list, tuple)):
        image_size = (image_size, image_size)

    center_x = image_size[0] // 2
    center_y = image_size[1] // 2
    xmin, ymin, xmax, ymax = bbox
    bbox_xmid = (xmin + xmax) // 2
    bbox_ymid = (ymin + ymax) // 2
    offset_x = center_x - bbox_xmid
    offset_y = center_y - bbox_ymid
    return offset_x, offset_y


def char_to_image(char, font_pil, image_size, bg_color=(255, 255, 255, 0), fg_color=(0, 0, 0, 255)):
    """生成包含单个字符的图像"""
    try:
        bbox = font_pil.getbbox(char)
    except Exception as e:
        print(f"获取字符边界框错误: {e}")
        return None

    if not isinstance(image_size, (list, tuple)):
        image_size = (image_size, image_size)

    offset_x, offset_y = get_bbox_offset(bbox, image_size)
    offset = (offset_x, offset_y)

    # 使用RGBA模式支持透明背景
    image = Image.new('RGBA', image_size, bg_color)
    draw = ImageDraw.Draw(image)
    draw.text(offset, char, font=font_pil, fill=fg_color)
    return image


def decimal_to_hex(decimal_unicode, prefix='uni'):
    """将十进制Unicode转换为十六进制Unicode"""

    def _regularize(single_decimal_unicode, prefix):
        h = hex(single_decimal_unicode)
        single_hex_unicode = prefix + h[2:].zfill(4)
        return single_hex_unicode

    is_single_code = False
    if not isinstance(decimal_unicode, (list, tuple)):
        decimal_unicode = [decimal_unicode]
        is_single_code = True

    hex_unicode = [_regularize(x, prefix) for x in decimal_unicode]

    if is_single_code:
        hex_unicode = hex_unicode[0]
    return hex_unicode


def font2image(font_file, font_size, image_size, out_folder=None,
               name_mode='char', image_extension='png',
               bg_color=(255, 255, 255, 0), fg_color=(0, 0, 0, 255),
               extract_chinese=True, extract_english=True,
               extract_digits=True, extract_symbols=False, extract_all=False,
               is_skip=True, progress_callback=None):
    """从字体生成图像"""

    if out_folder is None:
        out_folder = os.path.splitext(font_file)[0] + "_images"

    # 创建主输出目录
    os.makedirs(out_folder, exist_ok=True)

    # 创建子文件夹
    uppercase_folder = os.path.join(out_folder, "uppercase")
    lowercase_folder = os.path.join(out_folder, "lowercase")
    other_folder = os.path.join(out_folder, "other")

    os.makedirs(uppercase_folder, exist_ok=True)
    os.makedirs(lowercase_folder, exist_ok=True)
    os.makedirs(other_folder, exist_ok=True)

    print(f"输出目录结构:")
    print(f"  - 大写字母: {uppercase_folder}")
    print(f"  - 小写字母: {lowercase_folder}")
    print(f"  - 其他字符: {other_folder}")

    # 获取字体中的所有字符
    cmap = get_cmap(font_file)
    if cmap is None:
        raise Exception("无法读取字体文件或字体文件损坏")

    decimal_unicode = list(cmap.keys())

    # 分类字符
    chinese_chars, english_chars, digit_chars, symbol_chars = classify_unicode(decimal_unicode)

    # 根据选择确定要提取的字符
    chars_to_extract = []
    if extract_all or extract_chinese:
        chars_to_extract.extend(chinese_chars)
    if extract_all or extract_english:
        chars_to_extract.extend(english_chars)
    if extract_all or extract_digits:
        chars_to_extract.extend(digit_chars)
    if extract_all or extract_symbols:
        chars_to_extract.extend(symbol_chars)

    if not chars_to_extract:
        raise Exception("没有选择要提取的字符类型")

    print(f"总共找到 {len(chars_to_extract)} 个字符需要提取")
    print(
        f"中文字符: {len(chinese_chars)}, 英文字符: {len(english_chars)}, 数字: {len(digit_chars)}, 符号: {len(symbol_chars)}")

    font_pil = ImageFont.truetype(font_file, font_size)

    # 处理每个字符
    total_chars = len(chars_to_extract)
    success_count = 0
    fail_count = 0
    skip_count = 0

    for i, code in enumerate(chars_to_extract):
        char = chr(code)

        # 确定输出文件夹
        if 'A' <= char <= 'Z':
            target_folder = uppercase_folder
            folder_type = "大写"
        elif 'a' <= char <= 'z':
            target_folder = lowercase_folder
            folder_type = "小写"
        else:
            target_folder = other_folder
            folder_type = "其他"

        # 获取输出文件名 - 保持原始字符命名
        if name_mode == 'char':
            # 处理文件名中的特殊字符
            if char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'] or ord(char) < 32:
                filename = f"char_{code}"
            else:
                filename = char
        else:
            filename = f"char_{code}"

        filename = os.path.join(target_folder, f'{filename}.{image_extension}')

        # 调试信息
        print(f"处理: '{char}' ({folder_type}) -> {os.path.basename(filename)}")

        # 跳过已存在的文件
        if is_skip and os.path.exists(filename):
            print(f"⚠️ 跳过已存在: {os.path.basename(filename)}")
            skip_count += 1
            continue

        # 生成图像
        image = char_to_image(char, font_pil, image_size, bg_color, fg_color)
        if image is None:
            print(f"❌ 生成图像失败: '{char}'")
            fail_count += 1
            continue

        # 保存图像
        try:
            image.save(filename)
            print(f"✅ 成功保存: '{char}' -> {os.path.basename(filename)}")
            success_count += 1
        except Exception as e:
            print(f"❌ 保存失败 '{char}': {e}")
            fail_count += 1

        # 更新进度
        if progress_callback:
            progress = (i + 1) / total_chars * 100
            progress_callback(progress)

    # 最终统计
    print(f"\n=== 处理完成 ===")
    print(f"成功: {success_count}, 失败: {fail_count}, 跳过: {skip_count}")
    print(f"文件保存在: {out_folder}")


def main():
    root = tk.Tk()
    app = FontExtractorApp(root)
    root.mainloop()


if __name__ == '__main__':

    main()
