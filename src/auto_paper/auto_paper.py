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
from .get_corret_answer_v2 import get_answer
from .get_info_by_current_url import get_info_from_url


class AutoPaper(AutoBase):
    def finish_a_day(self, day: WebElement) -> None:
        self.click(day)
        time.sleep(2*self.config.get('delay_multiplier'))
        btns = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'btn-AoqsA')][contains(., '测一测') or contains(., '继续答')]")
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

        # 获取当前 URL 各参数
        params = get_info_from_url(self.driver.current_url)
        biz_code = params['bizCode']
        paper_id = params['paperId']

        # 统一获取答案
        # API 无法直接获取母题的子题的答案，故在此统一获取
        answers: dict[str, list[str]] = {}
        questions = self.driver.find_elements(By.CSS_SELECTOR, '.pm-question > .pm-question-content')
        for q in questions:
            q_id = q.get_attribute('id')[13:]  # 截断前面的 ewt-question-
            answers |= get_answer(biz_code, paper_id, str(self.config['report_id']), q_id, self.token)
            time.sleep(0.2*self.config.get('delay_multiplier'))

        # 完成选择题
        options_uls = self.driver.find_elements(By.CLASS_NAME, 'pm-question-options')
        for ul in options_uls:
            if not self.config['choose_correctly']:
                # 随机选一个选项
                items = ul.find_elements(By.CSS_SELECTOR, 'li')
                self.click(random.choice(items))
            else:
                # 选择正确答案
                q_id = ul.find_element(By.XPATH, './ancestor::*[2]').get_attribute('id')[13:]
                for letter in answers[q_id]:
                    self.click(ul.find_element(
                        By.XPATH, f".//span[contains(@class, 'pm-tag-letter') and text()='{letter}']"
                    ))
            time.sleep(0.2*self.config.get('delay_multiplier'))

        time.sleep(1*self.config.get('delay_multiplier'))

        # 提交
        self.click(self.driver.find_element(By.CLASS_NAME, 'ant-btn-primary'))
        time.sleep(1*self.config.get('delay_multiplier'))
        self.click(self.driver.find_element(By.CLASS_NAME, 'confirm-right'))
        time.sleep(5*self.config.get('delay_multiplier'))

        # 自批满分（不一定有此环节）
        n = len(self.driver.find_elements(By.CSS_SELECTOR, '.content-left-scroll > ul > li'))
        if n != 0:
            for i in range(n):
                self.click(self.driver.find_element(By.CSS_SELECTOR, '.content-right-scroll > ul > li:last-child'))
                time.sleep(2*self.config.get('delay_multiplier'))
            self.click(self.driver.find_element(By.CLASS_NAME, 'content-main-footer_submit_btn_full'))
            time.sleep(1*self.config.get('delay_multiplier'))
            self.click(self.driver.find_element(By.CLASS_NAME, 'confirm-right'))
            time.sleep(3*self.config.get('delay_multiplier'))

        self.close_and_switch()
