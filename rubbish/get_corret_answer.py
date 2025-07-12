import json

import requests
from urllib.parse import urlparse

# 创建会话对象
session = requests.Session()

# 设置 User-Agent
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
})

# 只添加 token cookie
session.cookies.set(
    name="token",
    value="151028179-1-d65b0d54252a0394",
    domain=".ewt360.com",
    path="/"
)

# 请求 URL
paperId='1969526514235999045'
reportId='2040881795217891454'
homeworkId='10389626'
userId='151028179'
url = f"https://web.ewt360.com/api/answerprod/web/answer/webreport/questionGroup?paperId={paperId}&reportId={reportId}&platform=1&bizCode=205&homeworkId={homeworkId}&userId={userId}"

# 请求头 (保留所有原始头部)
headers = {
    "authority": "web.ewt360.com",
    "method": "GET",
    "path": urlparse(url).path + "?" + urlparse(url).query,
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "access-control-allow-origin": "*",
    "eagleeye-pappname": "aocb5mxsv0@c882b4be402630c",
    "eagleeye-sessionid": "y9mOadU00X19e3psalIpu5beRwUs",
    "eagleeye-traceid": "ef11d5e6175232609247810112630c",
    "ewt-contentstyle": "CamelCase",
    "ewt-requestsource": "web",
    "priority": "u=1, i",
    "referer": "https://web.ewt360.com/mystudy/",
    "referurl": "https://web.ewt360.com/mystudy/#/report?bizCode=205&homeworkId=10389626&paperId=1969526514235999045&platform=1&reportId=2040881795217891454",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "token": "151028179-1-d65b0d54252a0394",  # 头部中的token
    "x-requested-with": "XMLHttpRequest"
}

try:
    # 发送 GET 请求
    response = session.get(
        url,
        headers=headers,
        timeout=15
    )

    # 检查响应状态
    response.raise_for_status()

    # 输出结果
    print(f"请求成功! 状态码: {response.status_code}")

    # 尝试解析 JSON
    try:
        json_data = response.json()
        print("响应JSON内容:")
        print(json_data)
    except ValueError:
        print("响应文本内容:")
        # print(response.text[:1000])  # 显示前1000个字符
        json2 = json.loads(response.text)['data']['groups']['questions']
    # # 调试信息
    # print("\n调试信息:")
    # print(f"最终请求URL: {response.url}")
    # print(f"发送的Cookies: {session.cookies.get_dict()}")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"错误状态码: {e.response.status_code}")
        print(f"错误响应: {e.response.text[:500]}")

    # 输出请求详情以便调试
    print("\n请求详情:")
    print(f"URL: {url}")
    print(f"Headers: {headers}")