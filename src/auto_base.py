#
# 此模块用于存储通用的工具函数
#

import os
import logging
import time
from abc import ABC, abstractmethod
from functools import cache

import yaml
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


@cache
def read_config() -> dict:
    """
    配置文件样例：
    # 修改时不要删掉冒号后的空格
    browser: 浏览器名称（首字母大写），如 Chrome, Edge 等
    driver_path: 浏览器驱动路径
    username: 用户名
    password: 密码
    list_url: 课程列表页面的链接
    # 浏览器启动时的参数，这里给了个静音
    options: --mute-audio
    # AutoEwt 模式，选填 watch（看课）/ test（做试卷）
    mode: watch
    """
    if not os.path.exists('config.yml'):
        logging.error('配置文件 config.yml 不存在，请检查！')
        exit(1)
    with open('config.yml', encoding='utf-8') as f:
        config = yaml.load(f, yaml.FullLoader)
        # 密码可能是纯数字
        config['password'] = str(config['password'])
        logging.info('成功读取到配置文件')
    return config


class AutoBase(ABC):
    def __init__(self):
        self.config = read_config()
        self.mode = self.config['mode']
        self.driver = self.init_driver()

        self.token = self.login()
        self.finish_days_list()

    def init_driver(self) -> webdriver.Edge:
        browser = self.config['browser']

        options = getattr(webdriver, browser.lower()).options.Options()
        options.add_argument(self.config['options'])
        driver = getattr(webdriver, browser)(
            service=getattr(webdriver, browser.lower()).service.Service(self.config['driver_path']),
            options=options
        )
        driver.maximize_window()
        driver.get(self.config['list_url'])
        driver.implicitly_wait(3)
        return driver

    def login(self) -> str:
        """
        登录
        :return: token
        """
        logging.info('登录账号……')
        self.driver.find_element(By.ID, 'login__password_userName').send_keys(self.config['username'])
        self.driver.find_element(By.ID, 'login__password_password').send_keys(self.config['password'])
        self.driver.find_element(By.CLASS_NAME, 'ant-btn-block').submit()
        # 等待一段时间，确保页面加载完成并生成 token
        time.sleep(3)
        # 获取所有 cookie
        cookies = self.driver.get_cookies()
        token = None
        for cookie in cookies:
            if cookie['name'] == 'token':
                token = cookie['value']
                break
        return token

    def click(self, btn: WebElement) -> None:
        """
        通过调用 .click(); 事件点击一个按钮，这比直接在 Python 中 .click() 更稳定
        对于可能被遮挡而无法点击的按钮，应使用此方法
        :param btn: 要点击的按钮
        :return: None
        """
        self.driver.execute_script('arguments[0].click();', btn)

    def click_and_switch(self, btn: WebElement) -> None:
        """
        点击按钮并切换到新页面
        :param btn: 要点击的按钮
        """
        self.click(btn)
        time.sleep(1)  # 给新页面反应一会
        # 切换到当前页面
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

    def close_and_switch(self) -> None:
        """关闭当前页面并返回到首页"""
        handles = self.driver.window_handles
        self.driver.close()
        self.driver.switch_to.window(handles[0])
        time.sleep(1)

    def finish_days_list(self) -> None:
        """完成所有天"""
        time.sleep(5)
        days = self.driver.find_elements(By.CSS_SELECTOR, 'li[data-active="true"], li[data-active="false"]')
        logging.info(f'一共有 {len(days)} 天的任务')
        for i in range(self.config['day_to_start_on'] - 1, len(days)):
            logging.info(f'================ 第 {i + 1} / {len(days)} 天 ================')
            self.finish_a_day(days[i])

    @abstractmethod
    def finish_a_day(self, day: WebElement) -> None:
        """
        完成一天的任务
        :param day: 该天在网页上的标签
        """
        ...
