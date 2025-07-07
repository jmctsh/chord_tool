# 音乐和弦转换工具 (Chord Converter)

一个基于Python和Tkinter开发的音乐和弦转换工具，支持和弦级数显示、换行编辑、文件保存和加载等功能。

## 功能特性

### 🎵 核心功能
- **调式选择**：支持12个调式（C, C#, D, D#, E, F, F#, G, G#, A, A#, B）
- **和弦输入**：支持1-7级和弦，包含多种和弦类型（大三和弦、小三和弦、七和弦等）
- **级数显示**：实时显示和弦对应的级数
- **换行编辑**：支持多行和弦谱编辑

### 📁 文件操作
- **保存和弦谱**：将当前和弦谱保存为JSON格式文件
- **加载和弦谱**：从JSON文件加载之前保存的和弦谱
- **新建和弦谱**：清空当前和弦谱，开始新的编辑

### 🎹 和弦类型支持
- **1级和弦**：C, Cm, Cmaj7, C7
- **2级和弦**：Dm, D, D7, Dm7, Dm9
- **3级和弦**：Em, E, E7, Em7, Em9
- **4级和弦**：F, Fm, Fmaj7, F7
- **5级和弦**：G, Gm, Gmaj7, G7
- **6级和弦**：Am, A, A7, Am7, Am9
- **7级和弦**：Bdim, B, B7, Bm, Bm7(b5)

## 系统要求

- Windows 10/11
- Python 3.7 或更高版本
- Tkinter（通常随Python一起安装）

## 安装和运行

### 方法1：直接运行Python文件
```bash
# 克隆或下载项目
git clone https://github.com/your-username/chord-converter.git
cd chord-converter

# 运行程序
python main.py
```

### 方法2：运行可执行文件
1. 下载最新版本的 `ChordConverter.exe`
2. 双击运行即可

## 使用说明

### 基本操作
1. **选择调式**：在左上角选择当前调式（默认为C大调）
2. **添加和弦**：点击虚线框（+号），选择"添加和弦"
3. **选择和弦**：在弹出的对话框中选择级数和具体和弦
4. **换行**：点击虚线框，选择"换行"选项
5. **编辑和弦**：右键点击和弦框进行编辑
6. **删除和弦**：选中和弦后按Delete键

### 文件操作
- **保存**：点击"保存和弦谱"按钮，选择保存位置
- **加载**：点击"打开和弦谱"按钮，选择要加载的文件
- **新建**：点击"新建和弦谱"按钮，清空当前内容

### 快捷键
- `Delete` / `Backspace`：删除选中的和弦
- 鼠标滚轮：在输入区域上下滚动

## 文件格式

程序使用JSON格式保存和弦谱文件，包含以下信息：
```json
{
  "key": "C",
  "chords": [
    {"degree": 1, "suffix": ""},
    {"degree": 4, "suffix": ""},
    {"degree": 5, "suffix": ""},
    "newline",
    {"degree": 1, "suffix": ""}
  ]
}
```

## 开发环境

- **语言**：Python 3.8+
- **GUI框架**：Tkinter
- **依赖**：仅使用Python标准库

## 项目结构

```
chord-converter/
├── main.py              # 主程序文件
├── README.md            # 项目说明文档
├── requirements.txt     # 依赖列表（空，仅使用标准库）
└── build/              # 打包输出目录
    └── ChordConverter.exe
```

## 打包为可执行文件

使用PyInstaller打包：

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包程序
pyinstaller --onefile --windowed --name ChordConverter main.py

# 可执行文件将生成在 dist/ 目录中
```

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 支持基本和弦转换功能
- 支持文件保存和加载
- 支持多行编辑
- 删除转调功能，简化界面

## 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

**注意**：本工具仅用于学习和音乐创作参考，请根据实际需要调整和弦进行。 