import os
import time
import requests
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class HuYa:
    def __init__(self, dri: webdriver.Chrome):
        self.url_userIndex = "https://i.huya.com/"
        self.driver = dri

    def login_check(self):
        try:
            js = '''
                return document.getElementsByClassName("uesr_n")
            '''
            status = self.driver.execute_script(js)
        except:
            status = []
        if len(status) == 1:
            username = status[0].get_attribute("textContent")
            print("user:{} has logged in.".format(username))
            return True
        return False

    def login(self, username, password):
        self.driver.get(self.url_userIndex)
        print("user:{} start to login.".format(username))
        self.driver.implicitly_wait(2)  # 等待跳转
        if self.login_check():
            return True

        self.driver.switch_to.frame('UDBSdkLgn_iframe')
        js = '''
            document.getElementsByClassName("input-login")[0].click();
            document.getElementsByClassName("udb-input-account")[0].value = "''' + str(username) + '''";
            document.getElementsByClassName("udb-input-pw")[0].value = "''' + str(password) + '''";
            document.getElementById("login-btn").click();
        '''
        self.driver.execute_script(js)
        self.driver.implicitly_wait(2)  # 等待跳转
        if not self.login_check():
            self.driver.get(self.url_userIndex)
            self.driver.switch_to.frame('UDBSdkLgn_iframe')
            self.driver.execute_script('document.getElementsByClassName("quick-icon")[0].click();')
            time.sleep(1)
            qr_url = self.driver.execute_script('return document.getElementById("qr-image").src;')
            print("user:{} login requires authentication, you have to scan the QR code to sign in.\nQR-code url:{}".format(username, qr_url))
            self.get_qr(username, qr_url)
            while not self.login_check():
                print(self.login_check())
                time.sleep(0.1)

    def into_room(self, room_id, n):
        s = int(self.get_hul())
        print("The remaining HL is {}".format(s))
        if s < n and s != 0:
            n = s
            print('The remaining HL is not enough for room:{}.'.format(room_id))
        elif s == 0:
            print('The remaining HL is 0. \nroom:{} send failure'.format(room_id))
            return False
        self.driver.get("https://huya.com/{}".format(room_id))
        self.driver.implicitly_wait(2)  # 等待跳转
        print("Enter room:{}".format(room_id))
        time.sleep(2)

        self.driver.execute_script("document.getElementsByClassName('player-face-arrow')[0].click()")
        time.sleep(0.5)
        try_times = 5
        while True:
            gift_hl_id = self.driver.execute_script('''
                gifts = document.getElementsByClassName("gift-panel-item");
                var gift_hl_id = 0;
                for(var i=0;i<gifts.length;i++){
                    propsid = gifts[i].getAttribute("propsid");
                    if(propsid === "4"){
                        gift_hl_id = i;
                        break;
                    }
                }
                return gift_hl_id;
            ''')
            if gift_hl_id != 0:
                break
            else:
                try_times -= 1
                time.sleep(1)
            if try_times == 0:
                print("room:{} send failure".format(room_id))
                return False
        print("gift_hl_id", gift_hl_id)

        for i in range(n):
            self.driver.execute_script('''
                gifts[''' + str(gift_hl_id) + '''].click();
                if(document.getElementsByClassName("btn confirm").length != 0){
                    document.getElementsByClassName("btn confirm")[0].click();
                }
            ''')
            print('Room:{} send out the {}th HL.'.format(room_id, i))
            time.sleep(1)

    def get_hul(self):
        # 进入充值页面查询虎粮
        self.driver.get("https://hd.huya.com/pay/index.html?source=web")
        self.driver.implicitly_wait(2)  # 等待跳转
        self.driver.execute_script('document.getElementsByClassName("nav")[0].getElementsByTagName("li")[4].click();')
        time.sleep(1)
        n = self.driver.execute_script('''
            lis = document.getElementsByTagName("li");
            for(var i=0;i<lis.length;i++){
                if(lis[i].title.search("虎粮") != -1){
                    return lis[i].getAttribute("data-num");
                }
            } 
            return 0;
        ''')

        print("number of HL:{}".format(n))
        return n

    def get_qr(self, usn, url, attach_cookie=False):
        sess = requests.Session()
        # 将selenium的cookies放到session中, 虎牙的验证码不带cookie也能访问, 绝绝子
        if attach_cookie:
            cookies = self.driver.get_cookies()
            sess.headers.clear()
            for cookie in cookies:
                sess.cookies.set(cookie['name'], cookie['value'])

        ret = sess.get(url)
        with open('qr-{}.png'.format(usn), 'wb') as f:
            print("qr-code saved success.")
            f.write(ret.content)


if __name__ == '__main__':
    debug = False
    chrome_options = Options()
    if not debug:
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
        chrome_options.add_argument("--disable-popup-blocking")  # 禁用弹出拦截
        chrome_options.add_argument("no-sandbox")  # 取消沙盒模式
        chrome_options.add_argument("no-default-browser-check")  # 禁止默认浏览器检查
        chrome_options.add_argument("disable-extensions")  # 禁用扩展
        chrome_options.add_argument("disable-glsl-translator")  # 禁用GLSL翻译
        chrome_options.add_argument("disable-translate")  # 禁用翻译
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--hide-scrollbars")  # 隐藏滚动条, 应对一些特殊页面
        chrome_options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片, 提升速度

    path_chrome_data = os.getcwd() + '/chromeData'
    if not Path(path_chrome_data).exists():
        os.mkdir(path_chrome_data)
    chrome_options.add_argument(r'user-data-dir=' + path_chrome_data)
    count = 0
    while True:
        
        driver = webdriver.Chrome(options=chrome_options)

        hy = HuYa(driver)

        hy.login(username="", password="")


        hy.into_room(950827, 45)
        driver.quit()
        count += 1
        print(f"已执行完成{count}次")
        time.sleep(86400)  # 一天的时间间隔，以秒为单位


