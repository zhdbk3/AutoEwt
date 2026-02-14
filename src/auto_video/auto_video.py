#
# Created by 着火的冰块nya (zhdbk3) on 2025/1/23
#

import time
import logging
import traceback
import warnings

import selenium
from selenium.common import StaleElementReferenceException
from tqdm import tqdm, TqdmWarning


from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from auto_base import AutoBase

warnings.filterwarnings('ignore', category=TqdmWarning)

class AutoVideo(AutoBase):
    def finish_a_day(self, day: WebElement) -> None:
        """
        完成一天的任务
        :param day: 该天在网页上的标签
        :return: None
        """
        self.click(day)
        time.sleep(2 * self.config.get('delay_multiplier'))
        btns = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'btn-AoqsA') "
            "and .//text()[contains(., '学')] "
            "and not(.//text()[contains(., '已学完')])]")
        btns_one_click = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'btn-AoqsA') "
            "and (.//text()[contains(., '去收听')] "
            " or .//text()[contains(., '去查看')]) "
            "and not(.//text()[contains(., '已学完')])]")
        unit = '节课'
        unit_one_click = "个"
        logging.info(f'该天还剩 {len(btns)} {unit}')
        logging.info(f'该天还剩 {len(btns_one_click)} {unit_one_click} 非视频课程')
        for i in range(len(btns)):
            logging.info(f'第 {i + 1} / {len(btns)} {unit}')
            try:
                self.finish_a_lesson(btns[i])
            except StaleElementReferenceException:
                self.close_and_switch()
                logging.warning('重新播放视频')
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
        for i in range(len(btns_one_click)):
            logging.info(f'第 {i + 1} / {len(btns_one_click)} {unit_one_click} 非视频课程')
            try:
                self.finish_a_click(btns_one_click[i])
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

    def _get_duration(self):  # <-- CHANGED: 原 tqdm_start() 拆分为只获取时长
        """获取视频总时长（秒），获取失败返回 None"""
        try:  # <-- CHANGED
            duration_text = self.driver.find_element(
                By.CSS_SELECTOR, ".vjs-duration-display"
            ).get_attribute("textContent")
            parts = duration_text.split(":")
            duration = int(parts[0]) * 60 + int(parts[1])
            if duration <= 0:  # <-- FIX
                return None
            return duration
        except Exception:
            return None


    def _create_pbar(self, duration):
            return tqdm(total=duration, desc='播放进度', ncols=100, unit_scale=True,
                        bar_format='{l_bar}{bar}| {n_fmt}秒/{total_fmt}秒')


    def finish_a_lesson(self, btn: WebElement, duration=None) -> None:
        """
        完成一节课，应对各种突发情况
        :param btn: “学”按钮
        :return: None
        """

        self.click_and_switch(btn)
        video = self.driver.find_element(By.TAG_NAME, 'video')
        time.sleep(3 * self.config.get('delay_multiplier'))
        try:
            self.driver.find_element(By.CLASS_NAME, 'vjs-big-play-button').click()
        except:
            pass
        logging.info(f"播放视频")
        duration = self._get_duration()
        with self._create_pbar(duration) as pbar:
            while True:
                ended = False
                try:  # <-- FIX
                    ended = video.get_attribute('ended')  # <-- FIX
                except:  # <-- FIX
                    raise # <-- FIX
                if ended:  # <-- FIX
                    break

                # 老师敲黑板，帮你暂停一下
                # 看看你在不在认真听课~
                els: list[WebElement] = self.driver.find_elements(
                    By.XPATH, "//*[contains(text(), '点击通过检查') or contains(text(), '跳过')]"
                )
                els = [e for e in els if e.is_displayed()]
                for e in els:
                    self.click(e)
                    logging.info('点击了检查点或答题点')
                    new_duration = self._get_duration()
                    if new_duration is not None:
                        pbar.total = new_duration
                        pbar.refresh()

                # zhdbk3的防止意外暂停
                self._resume_if_paused(video, pbar)

                try:
                    #从页面上已显示的时长文本解析（最简单可靠）
                    current_time_text = self.driver.find_element(
                        By.CSS_SELECTOR, ".vjs-current-time-display"
                    ).get_attribute("textContent")
                    # 转换为秒数
                    parts_current = current_time_text.split(":")
                    current_time = int(parts_current[0]) * 60 + int(parts_current[1])
                    pbar.n = current_time
                    pbar.refresh()
                except:
                    try:
                        current_time = self.driver.execute_script(
                            "return videojs('vjs_video_3').currentTime()"
                        )
                        pbar.n = current_time
                        pbar.refresh()
                    except:
                        pass
                time.sleep(1 * self.config.get('delay_multiplier'))


                els: list[WebElement] = self.driver.find_elements(
                    By.CLASS_NAME, 'vjs-big-play-button'
                )
                els = [e for e in els if e.is_displayed()]
                for e in els:
                    try:
                        logging.info('正在尝试以方式2重新播放视频')
                        self.driver.find_element(By.CLASS_NAME, 'vjs-big-play-button').click()
                        new_duration = self._get_duration()
                        if new_duration is not None:
                            pbar.total = new_duration
                            pbar.refresh()
                    except:

                        logging.error(f"呜...软件出现问题，请报告bug")

            if duration is not None:  # <-- CHANGED: 增加 None 检查
                pbar.n = duration
                pbar.refresh()
        logging.info('好诶~完成啦~')

        self.close_and_switch()

    def finish_a_click(self, btn: WebElement):
        self.click_and_switch(btn)
        logging.info('好诶~完成啦~')
        self.close_and_switch()

    def _resume_if_paused(self, video: WebElement, pbar):
        """
        检查视频是否被暂停，如果暂停则恢复播放
        https://github.com/zhdbk3/AutoEwt/pull/12/changes/46ac6a7e68f0724df552be6081b241e2f09173c7#diff-7e8f19105f96cbaa19843e7461b4b68b16d6cfedf1629ca0fc37772a4bb3936dR193-R203
        """
        try:
            # 视频结束时 paused 也为 true，但不应该恢复播放                            # <-- FIX

            ended = video.get_attribute('ended')  # <-- FIX
            if ended:
                return

            paused = self.driver.execute_script('return arguments[0].paused;', video)
            if paused:
                self.driver.execute_script('arguments[0].play();', video)
                logging.info('正在尝试以方式3重新播放视频')
                pbar.refresh()
        except:
            pass
