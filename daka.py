from selenium import webdriver
from selenium.webdriver.common.by import By
from chaojiying import Chaojiying_Client
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

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
        self.latitude = latitude  # 纬度
        self.longitude = longitude  # 经度

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

        # 使用 chrome
        driver = webdriver.Chrome(options=chrome_options)  # 创建chrome驱动
        driver.get(url)
        driver.maximize_window()

        return driver

    def login(self, driver):
        print("\n[Time] %s" %
              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("🚌 打卡任务启动")

        username_input = driver.find_element(by=By.ID, value="username")
        password_input = driver.find_element(by=By.ID, value="password")
        login_button = driver.find_element(by=By.ID, value="dl")

        print("登录到浙大统一身份认证平台...")

        try:
            username_input.send_keys(username)
            password_input.send_keys(password)
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

        school = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]/span[1]")))
        school.click()

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

        # 所在校区
        # driver.find_element(by=By.XPATH,
        #         value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]/span[1]/i").click()

        # # 今日申领健康码的状态？
        # driver.find_element(by=By.XPATH,
        #         value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[21]/div/div/div[1]/span[1]").click()

        # # 今日是否有发热症状（高于37.2 ℃）？
        # driver.find_element(by=By.XPATH,
        #         value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[22]/div/div/div[2]/span[1]").click()

        # # 今日是否有涉及涉疫情的管控措施
        # driver.find_element(by=By.XPATH,
        #         value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[22]/div/div/div[2]/span[1]").click()

        # # 是否有与新冠疫情确诊人员或密接人员有接触的情况?
        # driver.find_element(by=By.XPATH,
        #         value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[25]/div/div/div[2]/span[1]").click()

        # 获取验证码
        print("正在获取验证码...")
        img = driver.find_element(by=By.XPATH,
                                  value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/span/img").screenshot_as_png

        print("正在识别验证码")
        chaojiying = Chaojiying_Client('kalival', 'mlz123123', '928325')
        dic = chaojiying.PostPic(img, 1902)
        verify_code = dic['pic_str']

        print(f"验证码识别完成 验证码为{verify_code}")

        # 填入验证码
        driver.find_element(by=By.XPATH,
                            value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/input").send_keys(verify_code)

        # 本人承诺
        driver.find_element(by=By.XPATH,
                            value="/html/body/div[1]/div[1]/div/section/div[4]/ul/li[27]/div/div/div/span[1]").click()

        # 提交信息
        driver.find_element(by=By.XPATH,
                            value="/html/body/div[1]/div[1]/div/section/div[5]/div/a").click()

        time.sleep(5)
        tijiao = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="wapcf"]/div/div[2]/div[1]')))
        tijiao.click()
        time.sleep(5)
        

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
    密码）
    定位地点的经纬度
    """
    url = "https://healthreport.zju.edu.cn/ncov/wap/default/index"
    username = "3200103580"  # 用户名（学号）
    password = "mlz123123"  # 密码
    latitude = 30.27  # 虚拟位置纬度
    longitude = 120.13  # 经度
    daka = AutoDaka(url, username, password, latitude, longitude)
    daka.run()
