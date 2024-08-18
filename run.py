from flask import Flask, request, send_from_directory, jsonify, abort, render_template
import os
import socket
import qrcode
from colorama import init, Fore
from PIL import Image
import psutil

# 初始化 Colorama
init(autoreset=True)

app = Flask(__name__)

# 设置文件存储的根目录
FILE_DIRECTORY = os.path.join(os.getcwd(), 'files')

@app.route('/')
def index():
    # 使用 render_template 渲染 index.html
    return render_template('index.html')

# 设置文件上传和下载的路由
@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'error': '无文件'}), 400

    files = request.files.getlist('file')  # 获取所有上传的文件列表
    for file in files:
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        if file:
            filename = file.filename
            # 检查文件是否已存在，并添加序号
            counter = 1
            file_path = os.path.join(FILE_DIRECTORY, filename)
            while os.path.exists(file_path):
                file_name, file_ext = os.path.splitext(filename)
                new_filename = f"{file_name}_{counter}{file_ext}"
                file_path = os.path.join(FILE_DIRECTORY, new_filename)
                counter += 1
            file.save(file_path)
    return jsonify({'message': '文件上传成功'}), 200

@app.route('/download/<filename>')
def download_file(filename):
    # 拼接完整的文件路径
    file_path = os.path.join(FILE_DIRECTORY, filename)
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        print(f"文件不存在: {file_path}")  # 打印日志
        abort(404)  # 如果文件不存在，返回 404 错误
    return send_from_directory(FILE_DIRECTORY, filename, as_attachment=True)

@app.route('/list')
def list_files():
    # 获取请求的目录路径
    requested_path = request.args.get('path', '')
    full_path = os.path.join(FILE_DIRECTORY, requested_path)

    # 确保请求的路径是存在的目录
    if not os.path.isdir(full_path):
        return jsonify({'error': '目录不存在'}), 404

    # 遍历目录
    files = []
    for item in os.listdir(full_path):
        item_path = os.path.join(full_path, item)
        if os.path.isfile(item_path):
            files.append(item)

    # 返回文件列表
    return jsonify(files)

'''
获取局域网 IP 地址
@return: 局域网 IP 地址
'''

def get_lan_ip():
    try:
        # 获取所有网络接口的详细信息
        interfaces = psutil.net_if_addrs()
        # 遍历接口，寻找名称中包含"WLAN"的接口
        for interface_name, addrs in interfaces.items():
            if "WLAN" in interface_name:
                # 遍历地址信息，寻找IPv4地址
                for addr in addrs:
                    if addr.family == socket.AF_INET:   # 使用socket的AF_INET来检查IPv4地址
                        return addr.address
        # 如果没有找到非回环地址，返回 '127.0.0.1'
        return '127.0.0.1'
    except Exception as e:
        # 如果发生异常，打印错误信息并返回 '127.0.0.1'
        print(f"获取局域网 IP 地址时发生错误: {e}")
        return '127.0.0.1'


'''
创建二维码
@param url: 二维码链接
@param filename: 二维码文件名
'''
def create_qr_code(url, filename):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 检查文件是否存在，如果存在则覆盖
    if os.path.exists(filename):
        os.remove(filename)  # 删除已存在的文件
        
    img.save(filename)

'''
打印二维码到控制台
@param data: 二维码数据
@param fill_char: 填充字符
@param back_char: 背景字符
@param fill_color: 填充颜色
@param back_color: 背景颜色
'''
def print_qr_code_console(data, fill_char='█', back_char=' ', box_size=1, version=1):
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=1
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    pil_img = qr_img.convert('1')

    for y in range(pil_img.size[1]):
        for x in range(pil_img.size[0]):
            color = pil_img.getpixel((x, y))
            char = fill_char if color else back_char
            print(Fore.BLUE + char, end='')
        print()

if __name__ == '__main__':
    # 获取局域网 IP 地址
    local_ip = get_lan_ip()
    # 构建访问 Flask 应用的 URL
    flask_url = f"http://{local_ip}:5001"
    print("获取的url是:"+ flask_url)
    # 定义二维码图片的文件名
    qr_code_filename = 'qr_code.png'
    # 生成并保存二维码图片
    create_qr_code(flask_url, qr_code_filename)
    print_qr_code_console(flask_url)
    app.run(host='0.0.0.0', port=5001)  # 监听所有可用的网络接口
