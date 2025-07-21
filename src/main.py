#
# Created by  着火的冰块nya (zhdbk3) on 2025/1/23
#

import os
import datetime
import logging
import traceback

import yaml
from selenium.common.exceptions import StaleElementReferenceException

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

'''
配置文件样例：
# 修改时不要删掉冒号后的空格
browser: 浏览器名称（首字母大写），如 Chrome, Edge 等
driver_path: 浏览器驱动路径
username: 用户名
password: 密码
list_url: 课程列表页面的链接
# 浏览器启动时的参数，这里给了个静音
options: --mute-audio
# AutoEwt 模式，选填 watch（看课）/ test（做试卷）
mode: watch
'''
with open('config.yml', encoding='utf-8') as f:
    config = yaml.load(f, yaml.FullLoader)
    # 密码可能是纯数字
    config['password'] = str(config['password'])
    logging.info('成功读取到配置文件')

logging.info('启动！')

num_abnormal_collapse = 0
while True:
    try:
        viewer = Viewer(config)
    except StaleElementReferenceException:
        logging.error(traceback.format_exc())
        logging.info('程序崩溃，正在自动重启……')
        logging.info('这是由于页面自动刷新导致的元素查找错误，是正常现象')
    except:
        logging.critical(traceback.format_exc())
        logging.critical('程序异常崩溃，请报告 bug，正在自动重启……')
        num_abnormal_collapse += 1
        if num_abnormal_collapse >= 5:
            logging.critical('异常崩溃次数过多，已停止程序')
            break
