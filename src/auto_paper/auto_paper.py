#
# Created by 着火的冰块nya (zhdbk3) on 2025/1/23
#

import time
import logging
import traceback
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from auto_base import AutoBase


class AutoPaper(AutoBase):
    def finish_a_day(self, day: WebElement) -> None:
        self.click(day)
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
                self.close_and_switch()

    def finish_a_test(self, btn: WebElement):
        """
        完成一张试卷
        选择题随机选一个，大题**并不**传一个占位图片文件[doge]，并自批为满分
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
