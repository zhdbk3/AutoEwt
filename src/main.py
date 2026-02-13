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
        logging.info('开源项目：https://github.com/zhdbk3/AutoEwt')
        logging.info('如您是通过购买方式获得的本软件，请退款并举报卖家')
        logging.info('使用即视为同意项目README.md中的相关条款')
        logging.info('本软件不能处理练习和试卷，请自行处理上述内容')
        match read_config()['mode']:
            case 'video':
                auto = AutoVideo()
            case 'paper':
                auto = AutoPaper()
            case _:
                logging.error('mode 只能是 video 或 paper，请检查配置文件！')
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
        if 'auto' in locals():
            auto.driver.quit()

    retry_count += 1
    logging.info(f'第 {retry_count} 次重试，将在 {retry_interval} 秒后进行')
    time.sleep(retry_interval)
    retry_interval = min(retry_interval * 2, 300)  # 300s 熔断
