基于flask写的局域网传输文件不限速很快，也可以通过内网穿透实时给外网上传下载。
默认的地址端口号: http://当前ip地址:5001

克隆本仓库到本地
git clone https://github.com/sunweisu/LAN-file-transfer.git
然后修改index.html里面的电脑背景图片手机背景与logo图片为自己的
然后下载对应的python包
运行run.py即可
局域网内的人可以通过输出的连接/扫描生成的二维码即可上传下载文件

如果需要限制文件大小上传可以在run.py中的app = Flask(name_)下面添加代码：

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为16MB
```

如果需要限制文件类型上传可以在run.py中的app = Flask(name)下面添加代码：

```python
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # 允许上传的文件类型

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

然后在upload()函数中添加代码：


```python
if not allowed_file(file.filename):
    flash('不允许上传该类型的文件')
    return redirect(request.url)
```
