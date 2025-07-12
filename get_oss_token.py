import json
import requests
import time


def get_token():
    # 创建会话对象并设置 User-Agent
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
    })

    # 构造请求 URL（使用当前时间戳，或固定值 1752300940171）
    ts = int(time.time() * 1000)  # 当前毫秒级时间戳
    # ts = 1752300940171  # 或使用原固定值
    url = f"https://gateway.ewt360.com/fs/credentials/token?appName=mystudy&bucket=ewt-infrastructure&expire=3600&ts={ts}"

    # 定义请求头
    headers = {
        "authority": "gateway.ewt360.com",
        "method": "GET",
        "path": f"/fs/credentials/token?appName=mystudy&bucket=ewt-infrastructure&expire=3600&ts={ts}",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "origin": "https://web.ewt360.com",
        "priority": "u=1, i",
        "referer": "https://web.ewt360.com/",
        "sec-ch-ua": '""',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '""',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }

    # 发送 GET 请求
    response = session.get(
        url,
        headers=headers,
        verify=True  # 验证 SSL 证书（默认）
    )

    json2=json.loads(response.text)
    return json2["data"]["credentials"]["securityToken"]



if __name__=="__main__":
    print(get_token())
