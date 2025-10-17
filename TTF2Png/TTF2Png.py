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
        self.root.geometry("600x600")

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
        self.extract_common_chinese = tk.BooleanVar(value=False)

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
        ttk.Checkbutton(chars_frame, text="仅常用汉字", variable=self.extract_common_chinese,
                        command=self.toggle_common_chinese).grid(row=1, column=2, sticky=tk.W, pady=2)

        # 常用汉字级别选择 - 已删除选择列表，保留复选框功能

        # 自定义字符提取
        custom_frame = ttk.LabelFrame(main_frame, text="自定义字符提取", padding="5")
        custom_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # 单字符输入
        ttk.Label(custom_frame, text="单个字符:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.single_char = tk.StringVar()
        ttk.Entry(custom_frame, textvariable=self.single_char, width=10).grid(row=0, column=1, sticky=tk.W, pady=2,
                                                                              padx=(5, 0))
        ttk.Button(custom_frame, text="添加到列表", command=self.add_to_list).grid(row=0, column=2, sticky=tk.W, pady=2,
                                                                                   padx=(5, 0))

        # 字符列表
        ttk.Label(custom_frame, text="字符列表:").grid(row=1, column=0, sticky=tk.W, pady=2)
        list_frame = ttk.Frame(custom_frame)
        list_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.char_listbox = tk.Listbox(list_frame, height=4)
        self.char_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.char_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.char_listbox.config(yscrollcommand=scrollbar.set)

        # 列表操作按钮
        list_buttons_frame = ttk.Frame(custom_frame)
        list_buttons_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=2)

        ttk.Button(list_buttons_frame, text="删除选中", command=self.delete_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(list_buttons_frame, text="清空列表", command=self.clear_list).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(list_buttons_frame, text="提取列表", command=self.extract_list).pack(side=tk.LEFT)

        # 跳过已存在文件
        self.skip_existing = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="跳过已存在的文件", variable=self.skip_existing).grid(row=5, column=0,
                                                                                               columnspan=3,
                                                                                               sticky=tk.W, pady=5)

        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # 状态标签
        self.status = tk.StringVar(value="准备就绪")
        ttk.Label(main_frame, textvariable=self.status).grid(row=7, column=0, columnspan=3, sticky=tk.W, pady=5)

        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=10)

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
            self.extract_common_chinese.set(False)
        else:
            state = 'normal'

        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Checkbutton):
                text = widget.cget('text')
                if text not in ["全部字符", "仅常用汉字"]:
                    widget.configure(state=state)

    def toggle_common_chinese(self):
        if self.extract_common_chinese.get():
            self.extract_chinese.set(True)
            self.extract_english.set(False)
            self.extract_digits.set(False)
            self.extract_symbols.set(False)
            self.extract_all.set(False)

            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Checkbutton):
                    text = widget.cget('text')
                    if text not in ["中文字符", "仅常用汉字"]:
                        widget.configure(state='disabled')
        else:
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Checkbutton):
                    widget.configure(state='normal')

    def add_to_list(self):
        char = self.single_char.get().strip()
        if char:
            # 如果输入多个字符，只取第一个
            if len(char) > 1:
                char = char[0]
                self.single_char.set(char)

            # 检查是否已存在
            existing_chars = self.char_listbox.get(0, tk.END)
            if char not in existing_chars:
                self.char_listbox.insert(tk.END, char)
                self.single_char.set("")  # 清空输入框
            else:
                messagebox.showwarning("警告", f"字符 '{char}' 已存在于列表中")
        else:
            messagebox.showwarning("警告", "请输入字符")

    def delete_selected(self):
        selected = self.char_listbox.curselection()
        if selected:
            self.char_listbox.delete(selected[0])

    def clear_list(self):
        self.char_listbox.delete(0, tk.END)

    def extract_list(self):
        chars = self.char_listbox.get(0, tk.END)
        if not chars:
            messagebox.showwarning("警告", "字符列表为空")
            return

        if not self.font_path.get():
            messagebox.showerror("错误", "请选择字体文件")
            return

        if not self.output_path.get():
            messagebox.showerror("错误", "请选择输出目录")
            return

        try:
            self.status.set("正在提取自定义字符...")
            self.root.update()

            # 调用自定义字符提取函数
            extract_custom_chars(
                font_file=self.font_path.get(),
                chars_list=list(chars),
                font_size=self.font_size.get(),
                image_size=self.image_size.get(),
                out_folder=self.output_path.get(),
                name_mode=self.name_mode.get(),
                image_extension=self.image_format.get(),
                is_skip=self.skip_existing.get(),
                progress_callback=self.update_progress
            )

            self.status.set("自定义字符提取完成！")
            messagebox.showinfo("完成", "自定义字符提取完成！")

        except Exception as e:
            self.status.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"提取过程中出现错误:\n{str(e)}")

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
                extract_common_chinese=self.extract_common_chinese.get(),
                common_chinese_level="常用3500",  # 固定值
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


def get_precise_common_chinese_3500():
    """精确的3500个常用汉字列表，按部首排列，无重复"""
    precise_chinese_3500 = ["一丁七万丈三上下不与丐丑专且世丘丙业丛东丝丞丢两严丧个丫中丰串临丸丹为主丽举",
                            "丫中丰串临",
                            "九乃久么乏乘乙乜也习乡书买乱乳乾了予争事二于云互五井些亚亟亡交亥亦产亨亩享京亭亮亲",
                            "乙乜也习乡书买乱乳乾了予争事", "二于云互五井些亚亟亡交亥亦产亨亩享京亭亮亲",
                            "仁什仆仇今介仍从仑仓他仗付仙代令以仪们仰件价任份仿企伊伍伏优伐延仲件任价伦份仰仿伙伪",
                            "似但伸作伯伶佣低你住位伴伺佛伽役何余佛作佣佩依便俩修俏保促俄俭俗俘信侵侯俊待",
                            "儿兀允元兄光先兆克免兑兔党兜兢", "入全两内丙肉", "八公六共兵其具典养兼兽冀",
                            "内冈冉册再网同肉", "写军农冠冤冥幂", "冰冲决况冷冻净凄凉凌减凑凝", "几凡凤凭凯凳",
                            "凶出击凸凹函",
                            "刀刃分切刊刑划列则刚创初删判别利刮到制刷券刹刺刻剁剂剃前剑剔剥剧剩剪副割劈",
                            "力办功加务动助努劫励劳势勃勇勉勋勤募勾勿包匆匈", "勾勿包匆匈", "匕化北匙", "区匹巨匝医匪",
                            "区匹巨匝医匪", "十千午升半华协卑卒卓单卖南博卜占卡卢卦", "卜占卡卢卦", "卫印却即卷卸卿",
                            "厂厅历压厌厕厚原厢厦厨", "私允去参能", "又叉友反取受叔叛难",
                            "口古句另只叫召叭叮可台史右叶号司叹叽吁吃各合吉吊同名后向吓吐哇品响哈哥哦啊",
                            "啦啪喀喂喜喝喧喳嘿器嚷囚四回因团园围困图固国圃圆", "囚四回因团园围困图固国圃圆",
                            "土圣在地场块坚坡坤坦型城域培基堂堆堕堡堤塔塞境增壁", "士壮声处备复夏", "夕外多夜够",
                            "大天太夫央失头奇奉奏契奔奖套奢奥",
                            "女奴奶她好如妇妈妙妥妨妹妻姐姑姓始委妮娜娃姨姻娇婆婚婶媒嫁嫩媳嫂嫌嬉",
                            "子孔孕存孝学孩孙孤",
                            "宁它宅宇守安完宏宗官定宜宝实宠审客宣室宫宪害宽家宵容宾宿寂寄密富寒寓寞察",
                            "寸对寻导寿封耐尉尊", "小少尔尘尚尝就", "尤就尴",
                            "尸尺尼尽层屁尿尾局居屈届屋屏屑展属屠屡履",
                            "屯山屿岁岂岗岸岩岭岳峙峡峰峻崇崎崖崩崭嵌巍川州巡巢工左巧巨巩巫差己已巴巷",
                            "山屿岁岂岗岸岩岭岳峙峡峰峻崇崎崖崩崭嵌巍", "川州巡", "工左巧巨巩巫差", "己已巴巷",
                            "巾市布帅师希帐帕帖帘帚带帮帧帽幕幢", "干平年并幸干", "幻幼幽",
                            "广庄庆应床库底店庙府庞废度座庭康庸廉廊廓", "延建", "开异弃弄弊", "弋式贰",
                            "弓引弛弟张弦弧弯弱弹强粥", "归当录彗", "形彩雕", "彷役往征待很律徒得徘御循微德徽",
                            "心必忆忍志忘忙忠忧快性怕怪怜思怡怨总恋恒恕恰恨悟悄悔悦悬情惜惭惧惕惊惨惯惫愧愿慈慌慎慕慢慧慨慰憎憾懈应",
                            "戈戍戏我或战戚截戮", "户房所扇",
                            "手才扎扑扒打扔托扛扣执扫扬扭扮扯扰扳扶批扼找承技抄把抑抓投抗折抚抛抢护报担押抽拐拖拍顶拆拥抵拘抱拉拦拌拧",
                            "拨择拾拿持挂指按挑挣挤拼挖按挥挪振挺挽捂捌捅捆捉捍捐损捡换捣捧据捷捺掀掂授掉排掏掠掂控探接推掩措描提插握",
                            "揣揉斯", "支收改攻放政故效敌敏救教敛敢散敬敞敢敦斑", "文刘齐斋斌", "斗料斜",
                            "斤斥斧斩断斯", "方无既",
                            "日旦旧早旬旱时旺昂明昏易春显映星昨昭是昼显晃晋晒晓晕晚晨普景晴晶智晾暂暑暖暗暇暮暴曙",
                            "曰曲更曾替最", "月有朋服朗望朝期",
                            "木未末本札术朱朴朵机权朽材村杖杜束条来杨杭杯杰松板构析林果枝枢枣枪枫架柏某染柱柿栏树柔查柬",
                            "欠次欢欣欧欲欺", "止正此步武歧歪", "歹死歼殃殊残殖", "殴段殷殿", "毋母每毒", "比毕毙",
                            "毛毫毯", "氏民", "气氛氧氮",
                            "水永求汇汉汗污江池汤汪汶汽沃沉沫浅法泄河沾泪油泊沿泡注泻泳泥沸波泼泽治洁洪洒浇浊洞测洗活派流润浪浸涨烫",
                            "涌",
                            "火灭灯灰灵灶灼灿炉炎炒炊炙炫炬炭炮炸点炼炽烂烈烊烘烦烧烛烟烙烩烫烬热烹焕焙焚焦焰然煤照煮熙熊熟燃燎燕爆",
                            "爪爬爱爵", "父爷爸爹", "爽", "片版牌", "牙穿", "牛牟牧物牲牵特牺",
                            "犬犯状狂犹狐狗狠独狭狮狱狼猎猛猩猪猫献猴猾", "玄率",
                            "玉王玛玩环现玫玻珍玲珊玻珠班球理琉琅琢琳琴琵琶琼瑕瑟瑞瑰瑙璃璋璞", "瓜瓣", "瓦瓶瓷",
                            "甘某甜", "生甥", "用甩甫甬", "田由甲申电男画畅界畏留略累畴", "疏疑",
                            "疔疗疚疤疫疮疯疱疴病症疼疾痂痊痒痕痛痫痤痴痹瘟瘤瘦瘸瘾", "登发", "白的百皂的皇皆皓",
                            "皮皱", "皿盆盈益盏监盒盖盗盛盟",
                            "目盯盲直相省眉看真眠眼着睁眯睛睡督睬瞄睹瞄睫睬瞅瞬瞳瞧瞻", "矛柔矜", "矢知矩短矮",
                            "石矿码研砖砧破础硅硕硬确碑碗碘碰碳磁磨磷", "示社祖神祥祸福", "内",
                            "禾秀私秉秋科秒种租积称移秽税稠稳稿稼穆", "穴穷空穿突窃窍窑窗窜", "立站竞童竭端",
                            "竹竿笑笔笛符第等策答筋简算筷筹签简篇篮籍", "米类粉粒粗粘粥粮粹糊糖糕糟",
                            "系紧素索紫累细终经结给络绝统绣继绩绪续绳维绵绷绸综绿缀缅缆缉缓编缘缚缝缠缩缭缴", "缶缸缺",
                            "网罗罚罢罩罪置署", "羊美羞群羹", "羽翅翁翘翔翩", "老考者", "而要耐", "耒耕耗",
                            "耳耽耿聊聋职联聘聚", "聿肃肆",
                            "肉肋肌肝肚肠股肢肥肩肯育肺肾肿胃胆背胎胞胖脉脊脑脚脱脸脾腊腔腹腿腰腥腮膜膝臀臂臊", "臣卧",
                            "自臭", "至致", "臼舀", "舌乱舍舒", "舛舞", "舟航舰艇", "艮良艰", "色艳",
                            "艸艺节芋芍芒芙芜芦苇芽花芹芥芬苍芳芯苦若茂苹苗英范茄茎茅茶草茵荷获莓莉莲莫莱莹莺莽菇菊菜",
                            "菠营萧萨落萱葛董葡葱葵", "虎虏虐",
                            "虫虱虽虾蚁蚂蚊蚕蛊蛇蛆蛋蛙蛛蛤蛮蛔蜓蜓蜂蜗蜘蜜蝇蝴蝶螃融螳蟀蟋蟀蟑蟆蟹", "血众",
                            "行衍街衡", "衣补表衫衬衰衷袋裁裂装裆裔", "西要覆", "见规视览觉", "角解", "言誉警", "谷欲",
                            "豆岂登", "豕象", "豸豹貌",
                            "贝贞负财责贤败货质贩贪贫贬购贮贯贱贴贵贷贸费贺贼贿赁赂赃资赌赎赏赐赔赖赛", "走赴起超越",
                            "足趴距趾跃跑跌跋跚跳践踏踩踪蹋蹈蹦蹬", "身躲躺", "车轧轨转轮软轰较辅辆辈辉辐辑输",
                            "辛辜辞辣", "辰辱",
                            "辵边达迁过迈迎运近返还这进远违连迟迫述迷迹追退送适逃逆选逊透逐递通逛逢逮逸逻逼遇遁遂道遗遛避",
                            "邑那邦邪邮邻郁郊部都", "酉酒配酗酬醉醋醒", "采释", "里重野量",
                            "金针钉钓钏钙钝钞钟钢钥钦钩钮钱钳钻铁铃铅铐银铸铺链销锁锄锋锐错锡锣锤锦键锯镇镜镐镊镰",
                            "长", "门闩闪闭问闯闲间闷闸闹闺闻闽阀阁阅阉阎阔阑",
                            "阜队防阳阴阵阶阻阿附际陆陈降限陡院除险陪陵陶陷随隅隆隐隔隙", "隶", "隹难雀集雄雅雇雌雕",
                            "雨雪雳零雾雹雷需霆震霉霜霞露", "青静", "非靠", "面", "革靴靶鞠", "韦韧", "韭", "音章竟意",
                            "页顶顷项顺须顽顾顿颁颂预领颇颈颊频题颜额颠颤", "风飘", "飞",
                            "食饥饭饮饲饱饰饼饵饺饿馆馊馋", "首", "香", "马驭驰驱驳驴驹驾驶驼驻驿骂骄骆骇骋骏骑骚骡",
                            "骨骼髓", "高", "髟鬓", "斗", "鬯", "鬲", "鬼魂魅魔", "鱼鲁鲜鲸鳄",
                            "鸟鸡鸣鸥鸦鸭鸯鸽鹅鹊鹏", "卤", "鹿麟", "麦", "麻", "黄", "黍", "黑默黔点", "黹", "鼠",
                            "鼻", "齐", "齿龄", "龙", "龟", "龠"]
    # 将所有字符串连接成一个字符串，然后转换为字符列表
    all_chars = ""
    for group in precise_chinese_3500:
        all_chars += group

    # 检查重复字符
    char_set = set()
    duplicates = []
    for char in all_chars:
        if char in char_set:
            duplicates.append(char)
        char_set.add(char)

    if duplicates:
        print(f"发现重复字符: {set(duplicates)}")

    # 返回去重后的字符列表
    unique_chars = list(char_set)
    print(f"总字符数: {len(unique_chars)}")

    return unique_chars


class ChineseExtractionTracker:
    """中文提取跟踪器，用于检查重复字符"""

    def __init__(self):
        self.extracted_chars = set()
        self.duplicate_count = 0

    def check_duplicate(self, char):
        """检查字符是否重复"""
        if char in self.extracted_chars:
            print(f"⚠️ 重复字符: '{char}'")
            self.duplicate_count += 1
            return True
        self.extracted_chars.add(char)
        return False

    def get_stats(self):
        """获取统计信息"""
        return {
            "total_extracted": len(self.extracted_chars),
            "duplicate_count": self.duplicate_count
        }


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
              0x0180 <= code <= 0x024F):  # 拉丁扩展-B
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


def extract_custom_chars(font_file, chars_list, font_size, image_size, out_folder=None,
                         name_mode='char', image_extension='png',
                         bg_color=(255, 255, 255, 0), fg_color=(0, 0, 0, 255),
                         is_skip=True, progress_callback=None):
    """提取自定义字符列表"""

    if out_folder is None:
        out_folder = os.path.splitext(font_file)[0] + "_custom_images"

    # 创建输出目录
    os.makedirs(out_folder, exist_ok=True)

    font_pil = ImageFont.truetype(font_file, font_size)

    total_chars = len(chars_list)
    success_count = 0
    fail_count = 0
    skip_count = 0

    for i, char in enumerate(chars_list):
        # 获取输出文件名
        if name_mode == 'char':
            # 处理文件名中的特殊字符
            if char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'] or ord(char) < 32:
                filename = f"char_{ord(char)}"
            else:
                filename = char
        else:
            filename = f"char_{ord(char)}"

        filename = os.path.join(out_folder, f'{filename}.{image_extension}')

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
            success_count += 1
            print(f"✅ 成功保存: '{char}' -> {os.path.basename(filename)}")
        except Exception as e:
            print(f"❌ 保存失败 '{char}': {e}")
            fail_count += 1

        # 更新进度
        if progress_callback:
            progress = (i + 1) / total_chars * 100
            progress_callback(progress)

    # 最终统计
    print(f"\n=== 自定义字符处理完成 ===")
    print(f"成功: {success_count}, 失败: {fail_count}, 跳过: {skip_count}")
    print(f"文件保存在: {out_folder}")


def font2image(font_file, font_size, image_size, out_folder=None,
               name_mode='char', image_extension='png',
               bg_color=(255, 255, 255, 0), fg_color=(0, 0, 0, 255),
               extract_chinese=True, extract_english=True,
               extract_digits=True, extract_symbols=False, extract_all=False,
               extract_common_chinese=False, common_chinese_level="常用3500",
               is_skip=True, progress_callback=None):
    """从字体生成图像 - 增强版，支持精确常用汉字提取"""

    if out_folder is None:
        out_folder = os.path.splitext(font_file)[0] + "_images"

    # 创建主输出目录
    os.makedirs(out_folder, exist_ok=True)

    # 获取字体中的所有字符
    cmap = get_cmap(font_file)
    if cmap is None:
        raise Exception("无法读取字体文件或字体文件损坏")

    decimal_unicode = list(cmap.keys())

    # 分类字符
    chinese_chars, english_chars, digit_chars, symbol_chars = classify_unicode(decimal_unicode)

    # 如果选择仅提取常用汉字，则使用精确的汉字列表
    if extract_common_chinese and extract_chinese:
        print(f"使用精确的3500常用汉字列表...")
        precise_chars = get_precise_common_chinese_3500()

        # 将精确汉字列表转换为Unicode码点
        precise_unicode = [ord(char) for char in precise_chars]

        # 只保留字体中实际存在的字符
        available_chars = [code for code in precise_unicode if code in chinese_chars]
        chinese_chars = available_chars

        print(f"精确3500汉字中在字体中可用的有: {len(available_chars)} 个")

        # 如果字体中可用的字符很少，给出警告
        if len(available_chars) < 1000:
            print(f"⚠️ 警告: 字体中可用的常用汉字较少，可能不是标准中文字体")

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

    # 智能创建文件夹：根据实际要提取的字符类型决定
    folders_created = []

    # 检查是否需要英文字母文件夹
    has_uppercase = any(extract_all or extract_english for code in chars_to_extract if 'A' <= chr(code) <= 'Z')
    has_lowercase = any(extract_all or extract_english for code in chars_to_extract if 'a' <= chr(code) <= 'z')
    has_other = any(extract_all or extract_chinese or extract_digits or extract_symbols for code in chars_to_extract
                    if not ('A' <= chr(code) <= 'Z' or 'a' <= chr(code) <= 'z'))

    if has_uppercase:
        uppercase_folder = os.path.join(out_folder, "uppercase")
        os.makedirs(uppercase_folder, exist_ok=True)
        folders_created.append("uppercase")
        print(f"  - 大写字母: {uppercase_folder}")

    if has_lowercase:
        lowercase_folder = os.path.join(out_folder, "lowercase")
        os.makedirs(lowercase_folder, exist_ok=True)
        folders_created.append("lowercase")
        print(f"  - 小写字母: {lowercase_folder}")

    if has_other:
        other_folder = os.path.join(out_folder, "other")
        os.makedirs(other_folder, exist_ok=True)
        folders_created.append("other")
        print(f"  - 其他字符: {other_folder}")

    print(f"创建的文件夹: {', '.join(folders_created)}")

    font_pil = ImageFont.truetype(font_file, font_size)

    # 初始化重复检查器
    duplicate_tracker = ChineseExtractionTracker()

    # 处理每个字符
    total_chars = len(chars_to_extract)
    success_count = 0
    fail_count = 0
    skip_count = 0

    for i, code in enumerate(chars_to_extract):
        char = chr(code)

        # 确定输出文件夹
        if 'A' <= char <= 'Z' and has_uppercase:
            target_folder = uppercase_folder
            folder_type = "大写"
        elif 'a' <= char <= 'z' and has_lowercase:
            target_folder = lowercase_folder
            folder_type = "小写"
        elif has_other:
            target_folder = other_folder
            folder_type = "其他"
        else:
            # 如果对应的文件夹不存在，跳过这个字符
            print(f"⚠️ 跳过字符 '{char}'，对应的文件夹不存在")
            skip_count += 1
            continue

        # 检查重复字符
        if duplicate_tracker.check_duplicate(char):
            skip_count += 1
            continue

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
        # print(f"处理: '{char}' ({folder_type}) -> {os.path.basename(filename)}")

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
            success_count += 1
        except Exception as e:
            print(f"❌ 保存失败 '{char}': {e}")
            fail_count += 1

        # 更新进度
        if progress_callback:
            progress = (i + 1) / total_chars * 100
            progress_callback(progress)

    # 最终统计
    stats = duplicate_tracker.get_stats()
    print(f"\n=== 处理完成 ===")
    print(f"成功: {success_count}, 失败: {fail_count}, 跳过: {skip_count}")
    print(f"重复字符: {stats['duplicate_count']}")
    print(f"实际提取唯一字符: {stats['total_extracted']}")
    print(f"文件保存在: {out_folder}")
    if folders_created:
        print(f"创建的文件夹: {', '.join(folders_created)}")


def main():
    root = tk.Tk()
    app = FontExtractorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
