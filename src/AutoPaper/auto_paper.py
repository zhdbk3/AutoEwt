#
# Created by 着火的冰块nya (zhdbk3) on 2025/1/23
#

import time
import logging
import traceback
from typing import Literal
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils import click, click_and_switch, close_and_switch

class AutoPaper:
    def __init__(self, driver, config):
        """
        自动刷试卷程序的主体
        :param driver: 浏览器驱动实例
        :param config: 读取的配置文件
        """
        self.mode: Literal['test'] = config['mode']
        if self.mode != 'test':
            logging.error('mode 只能是 test，请检查配置文件！')
            exit(1)

        self.driver = driver
        self.finish_days_list()

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
        click(self.driver, day)
        time.sleep(2)
        btns = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'btn-3dDLy')][contains(., '测一测') or contains(., '继续答')]")
        unit = '张试卷'
        logging.info(f'该天还剩 {len(btns)} {unit}')
        for i in range(len(btns)):
            logging.info(f'第 {i + 1} / {len(btns)} {unit}')
            try:
                self.finish_a_test(btns[i])
            except:
                logging.error(traceback.format_exc())
                logging.warning('该试卷已跳过')
                # 关闭页面，返回首页
                close_and_switch(self.driver)

    def finish_a_test(self, btn: WebElement):
        """
        完成一张试卷
        选择题随机选一个，大题传一个占位图片文件，并自批为满分
        """
        click_and_switch(self.driver, btn)

        # 完成选择题
        options_uls = self.driver.find_elements(By.CLASS_NAME, 'pm-question-options')
        for ul in options_uls:
            items = ul.find_elements(By.CSS_SELECTOR, 'li')
            # 随机选一个选项
            click(self.driver, random.choice(items))
            time.sleep(0.2)

        time.sleep(1)

        # 提交
        click(self.driver, self.driver.find_element(By.CLASS_NAME, 'ant-btn-primary'))
        time.sleep(1)
        click(self.driver, self.driver.find_element(By.CLASS_NAME, 'confirm-right'))
        time.sleep(5)

        # 自批满分（不一定有此环节）
        n = len(self.driver.find_elements(By.CSS_SELECTOR, '.content-left-scroll > ul > li'))
        if n != 0:
            for i in range(n):
                click(self.driver, self.driver.find_element(By.CSS_SELECTOR, '.content-right-scroll > ul > li:last-child'))
                time.sleep(2)
            click(self.driver, self.driver.find_element(By.CLASS_NAME, 'content-main-footer_submit_btn_full'))
            time.sleep(1)
            click(self.driver, self.driver.find_element(By.CLASS_NAME, 'confirm-right'))
            time.sleep(3)

        close_and_switch(self.driver)