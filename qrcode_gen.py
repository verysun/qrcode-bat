import qrcode
from PIL import Image, ImageDraw, ImageFont
import platform

OS = platform.system() # Windows, Linux

# 打开文件并读取内容
file = open('qrcode_contents.txt', 'r')
contents = file.read().splitlines()

# 计算二维码图片大小和间距
qr_size = 200  # 每个二维码图片大小为200 x 200像素
qr_padding = 40  # 二维码图片之间的间距为40像素

# 定义每行每列的二维码数量和A4纸张大小
a4_width = 2480  # A4纸张宽度，单位是像素，Pillow默认的dpi为72
a4_height = 3508  # A4纸张高度，单位是像素，Pillow默认的dpi为72
row_qr_count = (int)(a4_width / (qr_size + qr_padding))  # 每一行二维码数量

# 计算画布大小
canvas_width = row_qr_count * (qr_size + qr_padding) - qr_padding
canvas_height = -(-len(contents) // row_qr_count) * (qr_size + qr_padding)

# 创建白色底的全局画布
global_canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')

# 设置字体
fontname = 'Ubuntu-RI.ttf' if OS == 'Linux' else 'arial.ttf'
font = ImageFont.truetype(fontname, 48)

# 定义变量控制二维码图片的位置
x = 0
y = 0

# 循环处理每个字符串
for i, content in enumerate(contents):
    # 创建QRCode对象，设置二维码大小和边距等属性
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4)
    
    print(i)
    # 添加数据并生成二维码
    qr.add_data(content)
    qr.make(fit=True)

    # 获取二维码图片，并调整大小为qr_size x qr_size像素
    img_qr = qr.make_image(fill_color='black', back_color='white')
    img_qr = img_qr.resize((qr_size, qr_size), Image.ANTIALIAS)

    # 判断二维码是否越界
    if x + qr_size > global_canvas.width:
        # 如果越界了就移到下一行，同时重置x的值
        y += qr_size + qr_padding
        x = 0

    if y + qr_size > global_canvas.height:
        # 如果越界了就退出循环
        break


    # 在全局画布上添加二维码图片
    global_canvas.paste(img_qr, (x, y))

    # 添加字符串
    draw = ImageDraw.Draw(global_canvas)
    draw.text((x, y + qr_size - 20), content, font=font, fill='black')

    # 控制图片位置
    if i % row_qr_count == row_qr_count - 1:  # 如果到达行末尾，换行
        x = 0
        y += qr_size + qr_padding + 10
    else:  # 否则移到下一列
        x += qr_size + qr_padding

# 计算需要拆分成几张A4纸张
canvas_count = -(-global_canvas.height // a4_height)  # 对高度向上取整，计算出需要的画布数量

# 循环处理每个A4画布
for i in range(canvas_count):
    # 创建白色底的单张A4画布
    canvas = Image.new('RGB', (a4_width, a4_height), 'white')

    # 设置要粘贴的全局画布区域
    paste_x = 0
    paste_y = i * a4_height
    paste_width = global_canvas.width
    paste_height = min(a4_height, global_canvas.height - paste_y)

    # 粘贴全局画布上对应区域的内容到单张A4画布上
    canvas.paste(global_canvas.crop((paste_x, paste_y, paste_x + paste_width, paste_y + paste_height)))

    # 保存单张A4画布为文件
    canvas.save('qrcodes_{}.png'.format(i+1))
