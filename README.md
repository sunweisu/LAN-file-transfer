基于flask写的局域网传输文件不限速很快，也可以通过内网穿透实时给外网上传下载。
默认的地址端口号: http://当前ip地址:5001

克隆本仓库到本地
git clone https://github.com/sunweisu/LAN-file-transfer.git
然后修改index.html里面的电脑背景图片手机背景与logo图片为自己的
然后下载对应的python包
运行run.py即可
局域网内的人可以通过输出的连接/扫描生成的二维码即可上传下载文件

如果需要限制文件大小上传可以添加代码：

# 设置最大文件大小为 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # 这里可以添加处理文件的代码
        return 'File successfully uploaded', 200

    # 如果文件大小超过限制，将触发一个 413 错误
    return abort(413, description="File size exceeds the limit")
