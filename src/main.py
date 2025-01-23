#
# Created by MC着火的冰块(zhdbk3) on 2025/1/23
#

import sys

import yaml

from viewer import Viewer, log

if len(sys.argv) == 1:
    with open('config.yml', encoding='utf-8') as f:
        config = yaml.load(f, yaml.FullLoader)
        log('成功读取到配置文件')
else:
    # 传入了参数
    config = {
        'username': sys.argv[1],
        'password': sys.argv[2],
        'driver_path': sys.argv[3]
    }
    log('接收到了传入的参数')

log('启动！')
viewer = Viewer(**config)
