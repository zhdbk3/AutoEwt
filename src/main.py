#
# Created by  着火的冰块nya (zhdbk3) on 2025/1/23
#

import traceback
import logging
import time
import os
import datetime

from selenium.common.exceptions import StaleElementReferenceException

from auto_base import read_config
from auto_video.auto_video import AutoVideo
from auto_paper.auto_paper import AutoPaper

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

config = read_config()

logging.info('启动！')

retry_count = 0
retry_interval = 3  # 初始重试间隔为 3 秒

while True:
    try:
        match read_config()['mode']:
            case 'watch':
                auto = AutoVideo()
            case 'test':
                auto = AutoPaper()
            case _:
                logging.error('mode 只能是 watch 或 test，请检查配置文件！')
                exit(1)
        break  # 如果程序正常执行完毕，退出循环
    except StaleElementReferenceException:
        logging.error(traceback.format_exc())
        logging.info('程序崩溃，正在自动重启……')
        logging.info('这是由于页面自动刷新导致的元素查找错误，是正常现象')
    except Exception as e:
        logging.critical(traceback.format_exc())
        logging.critical(f'程序异常崩溃，错误信息: {str(e)}，正在自动重启……')
    finally:
        auto.driver.quit()

    retry_count += 1
    logging.info(f'第 {retry_count} 次重试，将在 {retry_interval} 秒后进行')
    time.sleep(retry_interval)
    retry_interval *= 2  # 每次重试间隔时间翻倍
