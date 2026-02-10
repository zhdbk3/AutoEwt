#
# Created by 着火的冰块nya (zhdbk3) on 2025/1/23
#

import time
import logging
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from auto_base import AutoBase


class AutoVideo(AutoBase):
    def finish_a_day(self, day: WebElement) -> None:
        """
        完成一天的任务
        :param day: 该天在网页上的标签
        :return: None
        """
        self.click(day)
        time.sleep(2*self.config.get('delay_multiplier'))
        btns = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'btn-AoqsA') "
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
                self.close_and_switch()

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
            time.sleep(3*self.config.get('delay_multiplier'))
            self.driver.find_element(By.CLASS_NAME, 'vjs-big-play-button').click()
            logging.info('手动开始播放视频')
        except:
            pass

        while not video.get_attribute('ended'):
            # 老师敲黑板，帮你暂停一下
            # 看看你在不在认真听课~
            els: list[WebElement] = self.driver.find_elements(
                By.XPATH, "//*[contains(text(), '点击通过检查') or contains(text(), 'A')]"
            )
            els = [e for e in els if e.is_displayed()]
            for e in els:
                self.click(e)

            time.sleep(1*self.config.get('delay_multiplier'))

        logging.info('好诶~完成啦~')

        self.close_and_switch()
