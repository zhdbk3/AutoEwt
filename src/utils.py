#
# 此模块用于存储通用的工具函数
#

import os
import datetime
import logging
import time
import yaml
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

def init_logging():
    # 如果不存在 log 文件夹，则创建
    if not os.path.exists('log'):
        os.makedirs('log')
    # 初始化日志
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s %(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler(), logging.FileHandler(f'log/log_{now}.txt', encoding='utf-8')],
    )

def read_config():
    '''
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
    '''
    if not os.path.exists('config.yml'):
        logging.error('配置文件 config.yml 不存在，请检查！')
        exit(1)
    with open('config.yml', encoding='utf-8') as f:
        config = yaml.load(f, yaml.FullLoader)
        # 密码可能是纯数字
        config['password'] = str(config['password'])
        logging.info('成功读取到配置文件')
    return config

def init_driver(config):
    browser = config['browser']

    options = getattr(webdriver, browser.lower()).options.Options()
    options.add_argument(config['options'])
    driver = getattr(webdriver, browser)(
        service=getattr(webdriver, browser.lower()).service.Service(config['driver_path']),
        options=options
    )
    driver.maximize_window()
    driver.get(config['list_url'])
    driver.implicitly_wait(3)
    return driver

def login(driver, username, password):
    from selenium.webdriver.common.by import By  # 导入 By 类
    logging.info('登录账号……')
    # 使用新的定位方式 By.ID
    driver.find_element(By.ID, 'login__password_userName').send_keys(username)
    driver.find_element(By.ID, 'login__password_password').send_keys(password)
    # 使用新的定位方式 By.CLASS_NAME
    driver.find_element(By.CLASS_NAME, 'ant-btn-block').submit()


def click(driver, btn: WebElement) -> None:
    """
    通过调用 .click(); 事件点击一个按钮，这比直接在 Python 中 .click() 更稳定
    对于可能被遮挡而无法点击的按钮，应使用此方法
    :param driver: 浏览器驱动实例
    :param btn: 要点击的按钮
    :return: None
    """
    driver.execute_script('arguments[0].click();', btn)

def click_and_switch(driver, btn: WebElement):
    """
    点击按钮并切换到新页面
    :param driver: 浏览器驱动实例
    :param btn: 要点击的按钮
    """
    click(driver, btn)
    time.sleep(1)  # 给新页面反应一会
    # 切换到当前页面
    handles = driver.window_handles
    driver.switch_to.window(handles[1])

def close_and_switch(driver):
    """关闭当前页面并返回到首页"""
    handles = driver.window_handles
    driver.close()
    driver.switch_to.window(handles[0])
    time.sleep(1)