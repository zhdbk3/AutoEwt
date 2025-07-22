#
# Created by  着火的冰块nya (zhdbk3) on 2025/1/23
#

import traceback
from utils import init_logging, read_config, init_driver, login
from auto_video.auto_video import AutoVideo
from auto_paper.auto_paper import AutoPaper
from selenium.common.exceptions import StaleElementReferenceException
import logging
import time

init_logging()

config = read_config()

logging.info('启动！')

retry_count = 0
retry_interval = 3  # 初始重试间隔为 3 秒

while True:
    try:
        driver = init_driver(config)
        # 登录并获取 token
        token = login(driver, config['username'], config['password'])
        print(f"登录成功，Token: {token}")
        if config['mode'] == 'watch':
            AutoVideo(driver, config)
        elif config['mode'] == 'test':
            AutoPaper(driver, config)
        break  # 如果程序正常执行完毕，退出循环
    except StaleElementReferenceException:
        logging.error(traceback.format_exc())
        logging.info('程序崩溃，正在自动重启……')
        logging.info('这是由于页面自动刷新导致的元素查找错误，是正常现象')
    except Exception as e:
        logging.critical(traceback.format_exc())
        logging.critical(f'程序异常崩溃，错误信息: {str(e)}，正在自动重启……')
    finally:
        if 'driver' in locals():
            driver.quit()

    retry_count += 1
    logging.info(f'第 {retry_count} 次重试，将在 {retry_interval} 秒后进行')
    time.sleep(retry_interval)
    retry_interval *= 2  # 每次重试间隔时间翻倍