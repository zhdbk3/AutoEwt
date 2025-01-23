#
# Created by MC着火的冰块(zhdbk3) on 2025/1/23
#

import os
import datetime
import logging
import traceback

import yaml
from viewer import Viewer

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

with open('config.yml', encoding='utf-8') as f:
    config = yaml.load(f, yaml.FullLoader)
    logging.info('成功读取到配置文件')

logging.info('启动！')
try:
    viewer = Viewer(**config)
except:
    logging.critical(traceback.format_exc())
