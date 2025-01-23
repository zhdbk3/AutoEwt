#
# Created by MC着火的冰块(zhdbk3) on 2025/1/23
#

import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class Viewer:
    def __init__(self, browser: str, driver_path: str, username: str, password: str):
        """
        自动刷课程序的主体
        :param browser: 浏览器名称
        :param driver_path: 浏览器驱动路径
        :param username: 用户名
        :param password: 密码
        """
        self.username = username
        self.password = password

        self.driver: webdriver.Chrome = getattr(webdriver, browser)(
            service=getattr(webdriver, browser.lower()).service.Service(driver_path)
        )
        self.driver.maximize_window()
        self.driver.get('https://www.ewt360.com')
        self.driver.implicitly_wait(10)

        self.login()
        self.my_holiday()
        self.get_days_list()

    def login(self) -> None:
        logging.info('登录账号……')
        self.driver.find_element(By.ID, 'login__password_userName').send_keys(self.username)
        self.driver.find_element(By.ID, 'login__password_password').send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, 'ant-btn-block').submit()

    def my_holiday(self) -> None:
        logging.info('进入我的假期……')
        self.driver.find_element(By.CLASS_NAME, 'myHoliday').click()
        # 关闭第一页
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])
        self.driver.close()
        self.driver.switch_to.window(handles[1])
        # 即刻开启
        self.driver.find_element(By.CLASS_NAME, 'ant-btn-primary').click()

    def click(self, btn: WebElement) -> None:
        """
        通过调用 .click(); 事件点击一个按钮，这比直接在 Python 中 .click() 更稳定
        对于可能被遮挡而无法点击的按钮，应使用此方法
        :param btn: 要点击的按钮
        :return: None
        """
        self.driver.execute_script('arguments[0].click();', btn)

    def get_days_list(self) -> None:
        """获取所有天"""
        days = self.driver.find_elements(By.CLASS_NAME, 'day-card-container-19key')
        logging.info(f'一共有 {len(days)} 天的课程')
        for i in range(len(days)):
            logging.info(f'第 {i + 1} / {len(days)} 天')
            self.finish_a_day(days[i])

    def finish_a_day(self, day: WebElement) -> None:
        """
        完成一天的课程
        :param day: 该天在网页上的标签
        :return: None
        """
        self.click(day)
        time.sleep(1)
        btns_go = self.driver.find_elements(By.CLASS_NAME, 'operate-btn-2TCuM')
        logging.info(f'该天还剩 {len(btns_go)} 节课需学习')
        for i in range(len(btns_go)):
            logging.info(f'第 {i + 1} / {len(btns_go)} 节课')
            self.finish_a_lesson(btns_go[i])

    def finish_a_lesson(self, btn: WebElement) -> None:
        """
        完成一节课，应对各种突发情况
        :param btn: “去学习”按钮
        :return: None
        """
        self.click(btn)
        time.sleep(1)  # 给新页面反应一会
        # 切换到当前页面
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

        video = self.driver.find_element(By.TAG_NAME, 'video')
        while not video.get_attribute('ended'):
            # 老师敲黑板，帮你暂停一下
            # 看看你在不在认真听课~
            try:
                self.driver.find_element(By.XPATH, "//*[contains(text(), '点击通过检查')]").click()
                logging.info('点击了检查点')
            except NoSuchElementException:
                pass

            time.sleep(1)

        logging.info('好诶~完成啦~')
        # 关闭页面，返回首页
        self.driver.close()
        self.driver.switch_to.window(handles[0])
        time.sleep(1)  # 怎么每次换页面都得等一会
