# 虎粮自动发放

## 本脚本经过修改增加了一些自用功能

-   自动打开二维码图片
-   增加送全部虎粮功能
-   失败重试功能
-   每天自动赠送功能
-   requirements.txt
-   时间记录功能
-   and more...

---

用于虎牙直播平台，自动发放用户虎粮。

> 由与虎牙前端更新等情况，有可能会出现误送礼物，请谨慎使用！出现不可控情况概不负责！

## 使用说明

```python
hy.login(username="", password="")  #  填写账号
hy.into_room(518512, 70)			#  房间号， 发放虎粮数目
hy.into_room(518511, 20)			#  房间号， 发放虎粮数目
```

-   建议第一次使用的时候，将`debug = True`
-   第一次登陆会需要进行扫码登陆，二维码保存在代码路径下，名为`qr-username.png`，打开扫码登陆即可；或者打开输出的`QR-code url:xxxxx`也可以。

-   如果需要多个账号登陆，需要把这里的代码。(自己看着改吧

    ```python
    path_chrome_data = os.getcwd() + '/chromeData'
    if not Path(path_chrome_data).exists():
        os.mkdir(path_chrome_data)
    chrome_options.add_argument(r'user-data-dir=' + path_chrome_data)
    ```

-   运行需要[`chromedriver`](https://registry.npmmirror.com/binary.html?path=chromedriver/)(选择符合你浏览器的版本下载)。

-   定时使用`crontab`， `0 8 * * * python main.py >> huya.log 2>&1`。

-   linux 下 selenium 环境

    ```sh
    # 安装 google-chrome
    yum install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
    yum install -y mesa-libOSMesa-devel gnu-free-sans-fonts wqy-zenhei-fonts
    # 这里根据安装的chrome版本选择chromedriver
    wget https://npm.taobao.org/mirrors/chromedriver/94.0.4606.41/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    mv chromedriver /usr/bin/
    chmod +x /usr/bin/chromedriver
    #安装selenium
    pip install selenium
    ```

    > [**518512 nb**](https://huya.com/518512)

## 更新

-   修复了由于 selenium 新版本，导致的代码不可用的错误。（所有元素查找都已用 js 重写）
-   修复了虎牙网页更新导致虎粮找不到或误送礼物的错误。
