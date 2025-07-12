#
# Created by 着火的冰块nya (zhdbk3) on 2025/1/23
#

import time
import logging
import traceback
from typing import Literal
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class Viewer:
    def __init__(self, config: dict):
        """
        自动刷课程序的主体
        :param config: 读取的配置文件
        """
        self.mode: Literal['watch', 'test'] = config['mode']
        if self.mode not in ['watch', 'test']:
            logging.error('mode 只能是 watch 或 test，请检查配置文件！')
            exit(1)
        if self.mode == 'test':
            logging.warning('由于技术限制，请保持焦点在浏览器窗口上！')

        self.username = config['username']
        self.password = config['password']

        browser = config['browser']

        options = getattr(webdriver, browser.lower()).options.Options()
        options.add_argument(config['options'])
        self.driver: webdriver.Edge = getattr(webdriver, browser)(
            service=getattr(webdriver, browser.lower()).service.Service(config['driver_path']),
            options=options
        )
        self.driver.maximize_window()
        self.driver.get(config['list_url'])
        self.driver.implicitly_wait(3)

        self.login()
        self.finish_days_list()

    def login(self) -> None:
        logging.info('登录账号……')
        self.driver.find_element(By.ID, 'login__password_userName').send_keys(self.username)
        self.driver.find_element(By.ID, 'login__password_password').send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, 'ant-btn-block').submit()

    def click(self, btn: WebElement) -> None:
        """
        通过调用 .click(); 事件点击一个按钮，这比直接在 Python 中 .click() 更稳定
        对于可能被遮挡而无法点击的按钮，应使用此方法
        :param btn: 要点击的按钮
        :return: None
        """
        self.driver.execute_script('arguments[0].click();', btn)

    def finish_days_list(self) -> None:
        """完成所有天"""
        time.sleep(5)
        days = self.driver.find_elements(By.CSS_SELECTOR, 'li[data-active="true"], li[data-active="false"]')
        logging.info(f'一共有 {len(days)} 天的任务')
        for i in range(len(days)):
            logging.info(f'================ 第 {i + 1} / {len(days)} 天 ================')
            self.finish_a_day(days[i])

    def finish_a_day(self, day: WebElement) -> None:
        """
        完成一天的任务
        :param day: 该天在网页上的标签
        :return: None
        """
        self.click(day)
        time.sleep(2)
        if self.mode == 'watch':
            btns = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'btn-3dDLy') "
                "and .//text()[contains(., '学')] "
                "and not(.//text()[contains(., '已学完')])]")
            unit = '节课'
        else:
            btns = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'btn-3dDLy')][contains(., '测一测') or contains(., '继续答')]")
            unit = '张试卷'
        logging.info(f'该天还剩 {len(btns)} {unit}')
        for i in range(len(btns)):
            logging.info(f'第 {i + 1} / {len(btns)} {unit}')
            try:
                if self.mode == 'watch':
                    self.finish_a_lesson(btns[i])
                else:
                    self.finist_a_test(btns[i])
            except:
                # 似乎现在不存在这种特殊情况了，但这些逻辑还是留着吧，防止看一半程序暴毙
                # # 出现特殊情况，则跳过，不影响其他课程的完成
                # # 并不是所有课都是视频，还有 FM、试卷等
                # # 对于 FM，只要点进去了就是完成
                # # 对于试卷，留给人来处理
                logging.error(traceback.format_exc())
                logging.warning('该课已跳过')
                logging.warning('如果这是视频课，请报告 bug')
                # 关闭页面，返回首页
                self.close_and_switch()

    def click_and_switch(self, btn: WebElement):
        """
        点击按钮并切换到新页面
        :param btn: 要点击的按钮
        """
        self.click(btn)
        time.sleep(1)  # 给新页面反应一会
        # 切换到当前页面
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

    def close_and_switch(self):
        """关闭当前页面并返回到首页"""
        handles = self.driver.window_handles
        self.driver.close()
        self.driver.switch_to.window(handles[0])
        time.sleep(1)

    def finish_a_lesson(self, btn: WebElement) -> None:
        """
        完成一节课，应对各种突发情况
        :param btn: “学”按钮
        :return: None
        """
        self.click_and_switch(btn)

        video = self.driver.find_element(By.TAG_NAME, 'video')

        # 有时需要手动点播放
        try:
            time.sleep(3)
            self.driver.find_element(By.CLASS_NAME, 'vjs-big-play-button').click()
            logging.info('手动开始播放视频')
        except:
            pass

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

        self.close_and_switch()

    def finist_a_test(self, btn: WebElement):
        """
        完成一张试卷
        选择题随机选一个，大题传一个占位图片文件，并自批为满分
        """
        self.click_and_switch(btn)

        # 完成选择题
        options_uls = self.driver.find_elements(By.CLASS_NAME, 'pm-question-options')
        for ul in options_uls:
            items = ul.find_elements(By.CSS_SELECTOR, 'li')
            # 随机选一个选项
            self.click(random.choice(items))
            time.sleep(0.2)

        time.sleep(1)

        # # 完成大题
        # 完成个蛋，我研究了一整天怎么上传图片，结果偶然发现其实不需要上传图片也可以自批 qwq
        # 气笑了

        # 提交
        self.click(self.driver.find_element(By.CLASS_NAME, 'ant-btn-primary'))
        time.sleep(1)
        self.click(self.driver.find_element(By.CLASS_NAME, 'confirm-right'))
        time.sleep(5)

        # 自批满分（不一定有此环节）
        n = len(self.driver.find_elements(By.CSS_SELECTOR, '.content-left-scroll > ul > li'))
        if n != 0:
            for i in range(n):
                self.click(self.driver.find_element(By.CSS_SELECTOR, '.content-right-scroll > ul > li:last-child'))
                time.sleep(2)
            self.click(self.driver.find_element(By.CLASS_NAME, 'content-main-footer_submit_btn_full'))
            time.sleep(1)
            self.click(self.driver.find_element(By.CLASS_NAME, 'confirm-right'))
            time.sleep(3)

        self.close_and_switch()
