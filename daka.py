from selenium import webdriver
from selenium.webdriver.common.by import By
from chaojiying import Chaojiying_Client
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import os
from DingRobot import dingpush

# 使用代理的方法 ，可以直接windows使用代理，不用这么麻烦
# browserOptions = webdriver.ChromeOptions()
# browserOptions.add_argument('--proxy-server=ip:port)
# browser = webdriver.Chrome(chrome_options=browserOptions)

# 自动打卡
class AutoDaka:
    # 初始化
    def __init__(self, url, username, password, latitude, longitude):
        self.url = url
        self.username = username  # 用户名(学号)
        self.password = password  # 密码 
        self.latitude = latitude  # 纬度 默认是杭州市西湖区，可以在main函数里进行修改
        self.longitude = longitude  # 经度
        self.DD_BOT_TOKEN = os.getenv("DD_BOT_TOKEN") # 钉钉机器人token
        self.DD_BOT_SECRET=os.getenv("DD_BOT_SECRET") # 钉钉机器人secret

    # 获得Chrome驱动，并访问url
    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")

        # 使用headless无界面浏览器模式，因为要放在linux服务器上运行，无法显示界面，调试的时候需要把下面五行注释掉，显示chrome界面
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--headless')

        # 创建chrome驱动
        driver = webdriver.Chrome(options=chrome_options) 
        # 访问url 
        driver.get(url)
        # 将窗口最大化
        driver.maximize_window()

        return driver

    def login(self, driver):
        print("\n[Time] %s" %
              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("🚌 打卡任务启动")

        # 找到输入框,发送要输入的用户名和密码,模拟登陆
        username_input = driver.find_element(by=By.ID, value="username")
        password_input = driver.find_element(by=By.ID, value="password")
        login_button = driver.find_element(by=By.ID, value="dl")

        print("登录到浙大统一身份认证平台...")

        try:
            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            print("已登录到浙大统一身份认证平台")
            login_button.click()
            time.sleep(1)
        except Exception as err:
            print(str(err))
            raise Exception

    def daka(self, driver):
        print("打卡任务启动...")
        print("正在获得虚拟地理位置信息...")
        
        # 获取虚拟地理位置信息
        driver.execute_cdp_cmd(
            "Browser.grantPermissions",  # 授权地理位置信息
            {
                "origin": self.url,
                "permissions": ["geolocation"]
            },
        )

        driver.execute_cdp_cmd(
            "Emulation.setGeolocationOverride",  # 虚拟位置
            {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "accuracy": 50,
            },
        )

        time.sleep(2)  # 等待位置信息

        print("基本信息填写中...")

        # 是否在校
        inSchool = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]/span[1]")))
        inSchool.click()

        time.sleep(1)

        try:  # 提交位置信息
            area_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[9]/div/input"))
            )
            area_element.click()
            print("地理位置信息已提交")
        except Exception as error:
            print('get location wrong...\n', error)

        time.sleep(3)

        # 获取验证码
#         print("正在获取验证码...")
#         img = driver.find_element(by=By.XPATH,
#                                   value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/span/img").screenshot_as_png

#         print("正在识别验证码")
#         # 输入chaojiying的用户名，密码和软件ID
#         chaojiying = Chaojiying_Client('kalival', 'mlz123123', '928325')
#         # 设定验证码类型为4位全英文
#         dic = chaojiying.PostPic(img, 3004)
#         verify_code = dic['pic_str']

#         print(f"验证码识别完成 验证码为{verify_code}")

#         # 填入验证码
#         driver.find_element(by=By.XPATH,
#                             value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/input").send_keys(verify_code)

        # 本人承诺
        try:
            commit = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, 
                                    '/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/div/div/span[1]/i'))) 
            commit.click()
        except Exception as error:
            print('commit wrong...\n', error)

        # 提交信息
        driver.find_element(by=By.XPATH, 
                            value="/html/body/div[1]/div[1]/div/section/div[5]/div/a").click()

        time.sleep(2)
        
        # 弹出的确认提交窗口，点击确定
        try:  
            submit = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="wapcf"]/div/div[2]/div[2]')))
            submit.click()
            print("确认提交")
            self.Reminder("今天的打卡完成了🚌，耶！")
        except Exception as error:
            print('您已经提交过一次了.\n', error)
            self.Reminder("您今天已经提交过一次了")

        time.sleep(1)
    
    def Reminder(self, content):
        if self.DD_BOT_TOKEN:
            ding= dingpush('浙江大学每日健康打卡小助手', content, self.DD_BOT_TOKEN,self.DD_BOT_SECRET)
            ding.SelectAndPush()
        else:
            print("钉钉推送未配置，请自行查看签到结果")
        print("推送完成！")
        

    def run(self):
        driver = self.init_driver()
        self.login(driver)
        self.daka(driver)
        driver.close()
        print("打卡完成")
        

if __name__ == "__main__":

    """
    用户输入区：
    学号
    密码
    定位地点的经纬度
    """
    url = "https://healthreport.zju.edu.cn/ncov/wap/default/index"
    account = os.getenv("account")
    password = os.getenv("password")
    latitude = 30.27  # 虚拟位置纬度
    longitude = 120.13  # 经度
    daka = AutoDaka(url, account, password, latitude, longitude)
    daka.run()
