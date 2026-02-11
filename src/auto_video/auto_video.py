# auto_video.py
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

    # 查找"学"按钮的 XPATH（提取为常量，方便重新获取时复用）
    BTN_XPATH = (
        "//div[contains(@class, 'btn-AoqsA') "
        "and .//text()[contains(., '学')] "
        "and not(.//text()[contains(., '已学完')])]"
    )

    def finish_a_day(self, day: WebElement) -> None:
        """
        完成一天的任务
        :param day: 该天在网页上的标签
        :return: None
        """
        self.click(day)
        time.sleep(2 * self.config.get('delay_multiplier'))
        btns = self.driver.find_elements(By.XPATH, self.BTN_XPATH)
        total = len(btns)
        unit = '节课'
        logging.info(f'该天还剩 {total} {unit}')
        for i in range(total):
            logging.info(f'第 {i + 1} / {total} {unit}')
            try:
                # 每次重新获取按钮列表，避免页面切换后元素引用失效（StaleElementReferenceException）
                btns = self.driver.find_elements(By.XPATH, self.BTN_XPATH)
                if i >= len(btns):
                    logging.info('剩余按钮数量已变化，该天任务可能已完成')
                    break
                self.finish_a_lesson(btns[i])
            except Exception:
                # 似乎现在不存在这种特殊情况了，但这些逻辑还是留着吧，防止看一半程序暴毙
                # # 出现特殊情况，则跳过，不影响其他课程的完成
                # # 并不是所有课都是视频，还有 FM、试卷等
                # # 对于 FM，只要点进去了就是完成
                # # 对于试卷，留给人来处理
                logging.error(traceback.format_exc())
                logging.warning('该课已跳过')
                logging.warning('如果这是视频课，请报告 bug')
                # 如果有多余窗口，关闭页面，返回首页
                try:
                    if len(self.driver.window_handles) > 1:
                        self.close_and_switch()
                except Exception:
                    pass

    def _handle_checkpoint(self) -> None:
        """
        处理防挂机检查点弹窗（"点击通过检查"）
        """
        try:
            els: list[WebElement] = self.driver.find_elements(
                By.XPATH, "//*[contains(text(), '点击通过检查')]"
            )
            els = [e for e in els if e.is_displayed()]
            for e in els:
                self.click(e)
                logging.info('点击了检查点')
        except Exception:
            pass

    def _handle_interactive_question(self) -> None:
        """
        处理视频中弹出的互动题（选择题、判断题等）
        策略：
        1. 如果有"跳过"按钮且可见，直接跳过
        2. 否则随机选一个选项并提交（答错了也没关系，可以跳过重试）
        3. 如果出现重试界面，点击跳过
        """
        try:
            # 检查互动题层是否存在且可见
            interactive_layers = self.driver.find_elements(
                By.CSS_SELECTOR, '.video-interactive-layer'
            )
            if not interactive_layers:
                return

            layer = interactive_layers[0]
            # 检查互动层是否实际可见（通过尺寸判断）
            if not layer.is_displayed():
                return

            # ===== 优先尝试点击跳过按钮 =====
            skip_btns = layer.find_elements(
                By.CSS_SELECTOR, '.action-skip'
            )
            for btn in skip_btns:
                if btn.is_displayed():
                    self.click(btn)
                    logging.info('互动题：点击了跳过按钮')
                    time.sleep(0.5)
                    return

            # ===== 处理重试界面：点击跳过 =====
            retry_skip_btns = layer.find_elements(
                By.CSS_SELECTOR, '.retry-container .action-skip'
            )
            for btn in retry_skip_btns:
                if btn.is_displayed():
                    self.click(btn)
                    logging.info('互动题：重试界面点击了跳过')
                    time.sleep(0.5)
                    return

            # ===== 处理选择题：选第一个选项然后提交 =====
            option_btns = layer.find_elements(
                By.CSS_SELECTOR, '.action-btn.btn'
            )
            visible_options = [btn for btn in option_btns if btn.is_displayed()]
            if visible_options:
                # 选择第一个选项
                self.click(visible_options[0])
                logging.info('互动题：选择了一个选项')
                time.sleep(0.3)

                # 点击提交按钮
                submit_btns = layer.find_elements(
                    By.CSS_SELECTOR, '.action-submit'
                )
                for btn in submit_btns:
                    if btn.is_displayed():
                        self.click(btn)
                        logging.info('互动题：点击了提交按钮')
                        time.sleep(0.5)
                        break

                # 提交后可能出现重试界面，再尝试跳过
                time.sleep(1)
                retry_skip_btns = layer.find_elements(
                    By.CSS_SELECTOR, '.retry-container .action-skip'
                )
                for btn in retry_skip_btns:
                    if btn.is_displayed():
                        self.click(btn)
                        logging.info('互动题：答错后点击了跳过')
                        time.sleep(0.5)
                        return
                return

            # ===== 处理判断题 =====
            judge_btns = layer.find_elements(
                By.CSS_SELECTOR, '.action-judge'
            )
            visible_judges = [btn for btn in judge_btns if btn.is_displayed()]
            if visible_judges:
                # 选第一个（如"对"）
                self.click(visible_judges[0])
                logging.info('互动题：选择了判断题选项')
                time.sleep(0.3)

                # 点击提交
                submit_btns = layer.find_elements(
                    By.CSS_SELECTOR, '.action-submit'
                )
                for btn in submit_btns:
                    if btn.is_displayed():
                        self.click(btn)
                        logging.info('互动题：点击了提交按钮')
                        time.sleep(0.5)
                        break

                # 答错后尝试跳过重试
                time.sleep(1)
                retry_skip_btns = layer.find_elements(
                    By.CSS_SELECTOR, '.retry-container .action-skip'
                )
                for btn in retry_skip_btns:
                    if btn.is_displayed():
                        self.click(btn)
                        logging.info('互动题：答错后点击了跳过')
                        time.sleep(0.5)
                        return
                return

        except Exception:
            logging.debug(f'互动题处理异常: {traceback.format_exc()}')

    def _resume_if_paused(self, video: WebElement) -> None:
        """
        检查视频是否被暂停（可能被检查点或互动题暂停），如果暂停则恢复播放
        """
        try:
            paused = self.driver.execute_script('return arguments[0].paused;', video)
            if paused:
                self.driver.execute_script('arguments[0].play();', video)
                logging.info('视频被暂停，已恢复播放')
        except Exception:
            pass

    def finish_a_lesson(self, btn: WebElement) -> None:
        """
        完成一节课，应对各种突发情况
        :param btn: "学"按钮
        :return: None
        """
        self.click_and_switch(btn)

        video = self.driver.find_element(By.TAG_NAME, 'video')

        # 有时需要手动点播放
        try:
            time.sleep(3 * self.config.get('delay_multiplier'))
            self.driver.find_element(By.CLASS_NAME, 'vjs-big-play-button').click()
            logging.info('手动开始播放视频')
        except Exception:
            pass

        # 使用 JS 获取 ended 属性，返回真正的布尔值，避免字符串 "false" 被当作 True 的问题
        while not self.driver.execute_script('return arguments[0].ended;', video):
            # 1. 处理防挂机检查点弹窗
            self._handle_checkpoint()

            # 2. 处理视频中的互动题
            self._handle_interactive_question()

            # 3. 检查视频是否被暂停，如果暂停则恢复播放
            self._resume_if_paused(video)

            time.sleep(1 * self.config.get('delay_multiplier'))

        logging.info('好诶~完成啦~')

        self.close_and_switch()
