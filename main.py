import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import json
import os


class ChordConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("音乐和弦转换工具")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # 定义音符和调式
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        # 当前选择的调式
        self.current_key = tk.StringVar(value='C')

        # 和弦数据 - 存储级数和后缀信息，或者 'newline' 表示换行
        self.chords = []  # 存储 {'degree': int, 'suffix': str} 或 None (空白) 或 'newline'
        self.selected_chord_index = None

        # 每行显示的和弦数量
        self.chords_per_row = 10

        # 构建界面
        self.setup_ui()
        self.update_scale_chords()

    def setup_ui(self):
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 顶部框架 - 调式选择和调式和弦显示
        top_frame = tk.Frame(main_frame, bg='#f0f0f0')
        top_frame.pack(fill=tk.X, pady=(0, 20))

        # 调式选择区域
        key_frame = tk.LabelFrame(top_frame, text="调式选择", bg='#f0f0f0', font=('Arial', 12, 'bold'))
        key_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        # 主音选择
        tk.Label(key_frame, text="主音:", bg='#f0f0f0', font=('Arial', 10)).pack(anchor=tk.W, padx=10, pady=5)
        key_combo = ttk.Combobox(key_frame, textvariable=self.current_key, values=self.notes,
                                 state='readonly', width=10)
        key_combo.pack(padx=10, pady=5)
        key_combo.bind('<<ComboboxSelected>>', self.on_key_change)

        # 调式类型显示（只显示大调）
        tk.Label(key_frame, text="调式: 大调", bg='#f0f0f0', font=('Arial', 10)).pack(anchor=tk.W, padx=10,
                                                                                      pady=(5, 10))

        # 调式和弦显示区域
        scale_frame = tk.LabelFrame(top_frame, text="调式和弦", bg='#f0f0f0', font=('Arial', 12, 'bold'))
        scale_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scale_chords_frame = tk.Frame(scale_frame, bg='#f0f0f0')
        self.scale_chords_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 输入区域
        input_frame = tk.LabelFrame(main_frame, text="和弦输入", bg='#f0f0f0', font=('Arial', 12, 'bold'))
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # 创建滚动框架
        self.input_canvas = tk.Canvas(input_frame, bg='#f0f0f0', height=200)
        self.input_scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=self.input_canvas.yview)
        self.input_chords_frame = tk.Frame(self.input_canvas, bg='#f0f0f0')

        self.input_canvas.configure(yscrollcommand=self.input_scrollbar.set)
        self.input_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.input_canvas.create_window((0, 0), window=self.input_chords_frame, anchor="nw")

        # 级数转换区域
        degree_frame = tk.LabelFrame(main_frame, text="级数显示", bg='#f0f0f0', font=('Arial', 12, 'bold'))
        degree_frame.pack(fill=tk.X, pady=(0, 20))

        # 创建滚动框架
        self.degree_canvas = tk.Canvas(degree_frame, bg='#f0f0f0', height=200)
        self.degree_scrollbar = ttk.Scrollbar(degree_frame, orient="vertical", command=self.degree_canvas.yview)
        self.degree_chords_frame = tk.Frame(self.degree_canvas, bg='#f0f0f0')

        self.degree_canvas.configure(yscrollcommand=self.degree_scrollbar.set)
        self.degree_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.degree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.degree_canvas.create_window((0, 0), window=self.degree_chords_frame, anchor="nw")



        # 文件操作区域 - 固定在底部
        file_frame = tk.LabelFrame(main_frame, text="文件操作", bg='#f0f0f0', font=('Arial', 12, 'bold'))
        file_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        file_control_frame = tk.Frame(file_frame, bg='#f0f0f0')
        file_control_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(file_control_frame, text="保存和弦谱", command=self.save_chord_progression,
                  bg='#28a745', fg='white', font=('Arial', 10), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(file_control_frame, text="打开和弦谱", command=self.load_chord_progression,
                  bg='#007bff', fg='white', font=('Arial', 10), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(file_control_frame, text="新建和弦谱", command=self.new_chord_progression,
                  bg='#6c757d', fg='white', font=('Arial', 10), width=12).pack(side=tk.LEFT, padx=5)

        # 绑定鼠标滚轮事件
        self.bind_mousewheel()

        # 初始化和弦列表
        self.chords = []  # 开始时为空
        self.update_chord_display()

    def bind_mousewheel(self):
        """绑定鼠标滚轮事件"""

        def on_mousewheel(event):
            canvas = event.widget
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            # 同步级数显示的滚动
            if canvas == self.input_canvas:
                self.degree_canvas.yview_moveto(canvas.yview()[0])

        self.input_canvas.bind("<MouseWheel>", on_mousewheel)
        # 移除级数显示的独立滚轮事件，让它跟随输入框
        # self.degree_canvas.bind("<MouseWheel>", on_mousewheel)

    def get_chord_options_for_degree(self, degree):
        """根据级数获取和弦选项（只考虑大调）"""
        chord_options = {
            1: ['', 'm', 'maj7', '7'],
            2: ['m', '', '7', 'm7', 'm9'],
            3: ['m', '', '7', 'm7', 'm9'],
            4: ['', 'm', 'maj7', '7'],
            5: ['', 'm', 'maj7', '7'],
            6: ['m', '', '7', 'm7', 'm9'],
            7: ['dim', '', '7', 'm', 'm7(b5)']
        }
        return chord_options.get(degree, [])



    def chord_data_to_string(self, chord_data):
        """将和弦数据转换为字符串"""
        if chord_data is None:
            return ''

        # 获取当前调式的根音
        key_index = self.notes.index(self.current_key.get())

        # 大调音阶间隔
        intervals = [0, 2, 4, 5, 7, 9, 11]
        root_note_index = (key_index + intervals[chord_data['degree'] - 1]) % 12
        root_note = self.notes[root_note_index]

        return root_note + chord_data['suffix']

    def get_scale_chords(self, key):
        """获取大调的基本三和弦"""
        key_index = self.notes.index(key)

        # 大调音阶间隔：全全半全全全半
        intervals = [0, 2, 4, 5, 7, 9, 11]
        chord_types = ['', 'm', 'm', '', '', 'm', 'dim']

        chords = []
        for i, (interval, chord_type) in enumerate(zip(intervals, chord_types)):
            note_index = (key_index + interval) % 12
            chord = self.notes[note_index] + chord_type
            chords.append(f"{i + 1}级: {chord}")

        return chords

    def update_scale_chords(self):
        """更新调式和弦显示"""
        for widget in self.scale_chords_frame.winfo_children():
            widget.destroy()

        scale_chords = self.get_scale_chords(self.current_key.get())

        # 创建网格布局显示调式和弦
        for i, chord in enumerate(scale_chords):
            row = i // 4
            col = i % 4

            chord_label = tk.Label(self.scale_chords_frame, text=chord,
                                   bg='#e8e8e8', relief=tk.RAISED, borderwidth=2,
                                   font=('Arial', 10), width=12, height=2)
            chord_label.grid(row=row, column=col, padx=5, pady=5, sticky='ew')

        # 配置列权重
        for i in range(4):
            self.scale_chords_frame.columnconfigure(i, weight=1)

    def create_chord_box(self, parent, chord_data, index, is_add_button=False):
        """创建和弦方框"""
        if is_add_button:
            # 添加新和弦的虚线方框
            frame = tk.Frame(parent, bg='#f0f0f0', relief=tk.SOLID, borderwidth=2,
                             highlightbackground='gray', highlightcolor='gray')
            frame.configure(highlightthickness=2)

            label = tk.Label(frame, text="+", font=('Arial', 12),
                             bg='#f0f0f0', fg='gray', width=8, height=2)
            label.pack()

            frame.bind("<Button-1>", lambda e: self.show_add_options_menu())
            label.bind("<Button-1>", lambda e: self.show_add_options_menu())
        else:
            # 普通和弦方框
            bg_color = '#d4edda' if index == self.selected_chord_index else '#e8e8e8'

            frame = tk.Frame(parent, bg=bg_color, relief=tk.RAISED, borderwidth=2)

            # 显示和弦 - 空白时不显示文字
            if chord_data is None:
                display_text = ''
            else:
                display_text = self.chord_data_to_string(chord_data)

            label = tk.Label(frame, text=display_text, font=('Arial', 12),
                             bg=bg_color, width=8, height=2)
            label.pack()

            # 绑定事件
            frame.bind("<Button-1>", lambda e: self.select_chord(index))
            label.bind("<Button-1>", lambda e: self.select_chord(index))
            frame.bind("<Button-3>", lambda e: self.edit_chord(index))
            label.bind("<Button-3>", lambda e: self.edit_chord(index))

        return frame

    def layout_chords_in_grid(self, parent, chord_items, show_add_button=False):
        """在网格中布局和弦"""
        # 清空现有显示
        for widget in parent.winfo_children():
            widget.destroy()

        current_row = 0
        current_col = 0

        for i, chord_data in enumerate(chord_items):
            if chord_data == 'newline':
                # 遇到换行标记，跳到下一行
                current_row += 1
                current_col = 0
                continue

            # 创建和弦方框
            chord_frame = self.create_chord_box(parent, chord_data, i)
            chord_frame.grid(row=current_row, column=current_col, padx=5, pady=5, sticky='w')

            current_col += 1
            # 自动换行
            if current_col >= self.chords_per_row:
                current_row += 1
                current_col = 0

        # 添加新和弦按钮
        if show_add_button:
            add_frame = self.create_chord_box(parent, None, -1, is_add_button=True)
            add_frame.grid(row=current_row, column=current_col, padx=5, pady=5, sticky='w')

    def update_chord_display(self):
        """更新和弦显示"""
        # 输入区域
        self.layout_chords_in_grid(self.input_chords_frame, self.chords, show_add_button=True)

        # 级数显示区域
        degree_items = []
        for chord_data in self.chords:
            if chord_data == 'newline':
                degree_items.append('newline')
            else:
                degree_items.append(chord_data)

        self.layout_chords_in_grid(self.degree_chords_frame, degree_items, show_add_button=False)

        # 更新级数显示的文本
        current_row = 0
        current_col = 0
        for i, chord_data in enumerate(self.chords):
            if chord_data == 'newline':
                current_row += 1
                current_col = 0
                continue

            # 找到对应的widget并更新文本
            for widget in self.degree_chords_frame.grid_slaves(row=current_row, column=current_col):
                if isinstance(widget, tk.Frame):
                    label = widget.winfo_children()[0]
                    if chord_data is None:
                        label.configure(text='', bg='#fff3cd')
                    else:
                        label.configure(text=f"{chord_data['degree']}级", bg='#fff3cd')
                    break

            current_col += 1
            if current_col >= self.chords_per_row:
                current_row += 1
                current_col = 0



        # 更新滚动区域
        self.update_scroll_regions()

    def update_scroll_regions(self):
        """更新滚动区域"""

        def update_scroll_region(canvas, frame):
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.root.after(1, lambda: update_scroll_region(self.input_canvas, self.input_chords_frame))
        self.root.after(1, lambda: update_scroll_region(self.degree_canvas, self.degree_chords_frame))

    def add_chord(self):
        """添加新和弦 - 显示选项菜单"""
        self.show_add_options_menu()

    def show_add_options_menu(self):
        """显示添加选项菜单"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="添加和弦", command=self.add_new_chord)
        menu.add_command(label="换行", command=self.add_newline)
        
        # 获取鼠标位置
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        menu.post(x, y)

    def add_new_chord(self):
        """添加新和弦"""
        self.chords.append(None)  # 添加空白和弦
        new_index = len(self.chords) - 1
        self.show_chord_selection_dialog(new_index)

    def add_newline(self):
        """添加换行"""
        self.chords.append('newline')
        self.update_chord_display()

    def select_chord(self, index):
        """选择和弦"""
        self.selected_chord_index = index
        self.update_chord_display()

        # 绑定键盘事件
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()

    def on_key_press(self, event):
        """处理键盘事件"""
        if self.selected_chord_index is not None:
            if event.keysym in ['BackSpace', 'Delete']:
                self.delete_chord(self.selected_chord_index)

    def delete_chord(self, index):
        """删除和弦"""
        if 0 <= index < len(self.chords):
            if self.chords[index] == 'newline':
                # 删除换行标记
                self.chords.pop(index)
            else:
                # 删除和弦
                if len([c for c in self.chords if c != 'newline']) > 1:
                    self.chords.pop(index)
                else:
                    self.chords[index] = None
            self.selected_chord_index = None
            self.update_chord_display()

    def edit_chord(self, index):
        """编辑和弦"""
        if 0 <= index < len(self.chords) and self.chords[index] != 'newline':
            self.show_chord_selection_dialog(index)

    def show_chord_selection_dialog(self, index):
        """显示和弦选择对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("选择和弦")
        dialog.configure(bg='#f0f0f0')
        dialog.resizable(True, True)  # 允许调整大小

        # 创建主框架
        main_frame = tk.Frame(dialog, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 状态变量
        selected_degree = tk.StringVar()
        selected_chord = tk.StringVar()

        # 获取当前和弦信息用于预选
        current_chord_data = self.chords[index] if index < len(self.chords) else None
        if current_chord_data and current_chord_data != 'newline':
            selected_degree.set(f"{current_chord_data['degree']}级")
            current_chord_string = self.chord_data_to_string(current_chord_data)
            selected_chord.set(current_chord_string)
        else:
            selected_degree.set('空白')
            selected_chord.set('空白')

        # 一级选择：级数
        degree_frame = tk.LabelFrame(main_frame, text="第一步：选择级数", bg='#f0f0f0', font=('Arial', 12, 'bold'))
        degree_frame.pack(fill=tk.X, pady=(0, 20))

        degree_options = ['空白', '1级', '2级', '3级', '4级', '5级', '6级', '7级']

        degree_buttons_frame = tk.Frame(degree_frame, bg='#f0f0f0')
        degree_buttons_frame.pack(fill=tk.X, padx=20, pady=10)

        # 存储级数按钮以便更新样式
        self.degree_buttons = {}

        for i, degree in enumerate(degree_options):
            btn = tk.Button(degree_buttons_frame, text=degree,
                            command=lambda d=degree: self.select_degree(d, selected_degree, selected_chord,
                                                                        chord_buttons_frame),
                            font=('Arial', 10), width=8, height=2)
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.degree_buttons[degree] = btn

        # 二级选择：具体和弦
        chord_frame = tk.LabelFrame(main_frame, text="第二步：选择具体和弦", bg='#f0f0f0', font=('Arial', 12, 'bold'))
        chord_frame.pack(fill=tk.X, pady=(0, 20))

        chord_buttons_frame = tk.Frame(chord_frame, bg='#f0f0f0')
        chord_buttons_frame.pack(fill=tk.X, padx=20, pady=10)

        # 存储和弦按钮以便更新样式
        self.chord_buttons = {}

        # 初始化和弦选项
        self.update_chord_options(selected_degree.get(), selected_chord, chord_buttons_frame)

        # 更新按钮样式
        self.update_button_styles(selected_degree.get(), selected_chord.get())

        # 按钮框架
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(20, 0))

        def confirm_selection():
            degree_str = selected_degree.get()
            chord_str = selected_chord.get()

            if degree_str == '空白' or chord_str == '空白':
                self.chords[index] = None
            else:
                degree_num = int(degree_str[0])
                # 从和弦字符串中提取后缀
                key_index = self.notes.index(self.current_key.get())
                intervals = [0, 2, 4, 5, 7, 9, 11]
                root_note_index = (key_index + intervals[degree_num - 1]) % 12
                root_note = self.notes[root_note_index]
                suffix = chord_str[len(root_note):]

                self.chords[index] = {'degree': degree_num, 'suffix': suffix}

            self.update_chord_display()
            dialog.destroy()

        def cancel_selection():
            # 如果是新添加的和弦且取消了，则删除它
            if index == len(self.chords) - 1 and self.chords[index] is None:
                self.chords.pop()
            dialog.destroy()

        tk.Button(button_frame, text="确定", command=confirm_selection,
                  bg='#007bff', fg='white', font=('Arial', 12), width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="取消", command=cancel_selection,
                  bg='#6c757d', fg='white', font=('Arial', 12), width=10).pack(side=tk.LEFT)

        # 让对话框居中
        dialog.transient(self.root)
        dialog.grab_set()

        # 设置初始大小并确保内容可见
        dialog.update_idletasks()  # 确保所有组件都已布局
        dialog.geometry("600x500")  # 设置一个足够的初始高度

        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")

    def select_degree(self, degree, degree_var, chord_var, chord_buttons_frame):
        """选择级数"""
        degree_var.set(degree)
        chord_var.set('')  # 清空和弦选择
        self.update_chord_options(degree, chord_var, chord_buttons_frame)
        self.update_button_styles(degree, '')

    def select_chord_in_dialog(self, chord, chord_var):
        """在对话框中选择和弦"""
        chord_var.set(chord)
        self.update_button_styles(None, chord)

    def update_button_styles(self, selected_degree, selected_chord):
        """更新按钮样式"""
        # 更新级数按钮样式
        for degree, btn in self.degree_buttons.items():
            if degree == selected_degree:
                btn.configure(bg='#007bff', fg='white', relief=tk.RAISED, bd=3)
            else:
                btn.configure(bg='#f8f9fa', fg='black', relief=tk.RAISED, bd=1)

        # 更新和弦按钮样式
        for chord, btn in self.chord_buttons.items():
            if chord == selected_chord:
                btn.configure(bg='#28a745', fg='white', relief=tk.RAISED, bd=3)
            else:
                btn.configure(bg='#f8f9fa', fg='black', relief=tk.RAISED, bd=1)

    def update_chord_options(self, degree, chord_var, chord_buttons_frame):
        """更新二级选择选项"""
        # 清空现有选项
        for widget in chord_buttons_frame.winfo_children():
            widget.destroy()

        self.chord_buttons = {}

        if degree == '空白':
            # 如果选择空白，只显示空白选项
            btn = tk.Button(chord_buttons_frame, text='空白',
                            command=lambda: self.select_chord_in_dialog('空白', chord_var),
                            font=('Arial', 10), width=8, height=2)
            btn.grid(row=0, column=0, padx=5, pady=5)
            self.chord_buttons['空白'] = btn
        elif degree and degree != '':
            # 获取级数
            degree_num = int(degree[0])

            # 获取当前调式的根音
            key_index = self.notes.index(self.current_key.get())

            # 大调音阶间隔
            intervals = [0, 2, 4, 5, 7, 9, 11]
            root_note_index = (key_index + intervals[degree_num - 1]) % 12
            root_note = self.notes[root_note_index]

            # 获取和弦后缀选项
            chord_suffixes = self.get_chord_options_for_degree(degree_num)

            # 创建具体和弦选项
            for i, suffix in enumerate(chord_suffixes):
                chord_name = root_note + suffix
                btn = tk.Button(chord_buttons_frame, text=chord_name,
                                command=lambda c=chord_name: self.select_chord_in_dialog(c, chord_var),
                                font=('Arial', 10), width=8, height=2)
                btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
                self.chord_buttons[chord_name] = btn

        # 更新对话框大小以适应新内容
        chord_buttons_frame.update_idletasks()
        # 获取对话框窗口
        dialog = chord_buttons_frame.winfo_toplevel()
        dialog.update_idletasks()

        # 计算所需的最小高度
        required_height = max(500, dialog.winfo_reqheight() + 50)
        current_geometry = dialog.geometry()
        width = current_geometry.split('x')[0]
        x_pos = current_geometry.split('+')[1] if '+' in current_geometry else '0'
        y_pos = current_geometry.split('+')[2] if '+' in current_geometry else '0'

        # 更新窗口大小，保持位置不变
        dialog.geometry(f"{width}x{required_height}+{x_pos}+{y_pos}")

    def on_key_change(self, event):
        """调式主音改变 - 按级数转调所有和弦"""
        self.update_scale_chords()
        self.update_chord_display()



    def save_chord_progression(self):
        """保存和弦谱"""
        if not self.chords:
            messagebox.showwarning("警告", "没有和弦数据可保存")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            title="保存和弦谱"
        )
        
        if file_path:
            try:
                # 准备保存的数据
                save_data = {
                    'key': self.current_key.get(),
                    'chords': self.chords
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("成功", f"和弦谱已保存到:\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")

    def load_chord_progression(self):
        """加载和弦谱"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            title="打开和弦谱"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    load_data = json.load(f)
                
                # 恢复数据
                self.current_key.set(load_data.get('key', 'C'))
                self.chords = load_data.get('chords', [])
                
                # 更新显示
                self.update_scale_chords()
                self.update_chord_display()
                
                messagebox.showinfo("成功", f"和弦谱已加载:\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"加载失败: {str(e)}")

    def new_chord_progression(self):
        """新建和弦谱"""
        if self.chords:
            result = messagebox.askyesno("确认", "当前和弦谱将被清空，是否继续？")
            if not result:
                return
        
        # 清空数据
        self.chords = []
        self.current_key.set('C')
        self.selected_chord_index = None
        
        # 更新显示
        self.update_scale_chords()
        self.update_chord_display()
        
        messagebox.showinfo("成功", "已创建新的和弦谱")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChordConverter(root)
    root.mainloop()