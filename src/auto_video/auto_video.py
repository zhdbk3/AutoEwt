#
# Created by 着火的冰块nya (zhdbk3) on 2025/1/23
#

import time
import logging
import traceback
from typing import Literal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from utils import click, click_and_switch, close_and_switch


class AutoVideo:
    def __init__(self, driver, config):
        """
        自动看课程序的主体
        :param driver: 浏览器驱动实例
        :param config: 读取的配置文件
        """
        self.mode: Literal['watch'] = config['mode']
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
            "//div[contains(@class, 'btn-3dDLy') "
            "and .//text()[contains(., '学')] "
            "and not(.//text()[contains(., '已学完')])]")
        unit = '节课'
        logging.info(f'该天还剩 {len(btns)} {unit}')
        for i in range(len(btns)):
            logging.info(f'第 {i + 1} / {len(btns)} {unit}')
            try:
                self.finish_a_lesson(btns[i])
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
                close_and_switch(self.driver)

    def finish_a_lesson(self, btn: WebElement) -> None:
        """
        完成一节课，应对各种突发情况
        :param btn: “学”按钮
        :return: None
        """
        click_and_switch(self.driver, btn)

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
                click(self.driver, self.driver.find_element(
                    By.XPATH, "//*[contains(text(), '点击通过检查') or contains(text(), 'A')]"
                ))
                logging.info('点击了检查点')
            except NoSuchElementException:
                pass

            time.sleep(1)

        logging.info('好诶~完成啦~')

        close_and_switch(self.driver)
