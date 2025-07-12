import json

import requests
from urllib.parse import urlparse


paperId='1969526514235999045'
reportId='2040881795217891454'
homeworkId='10389626'
userId='151028179'
token = '151028179-1-89663793316a648f'


def get_answer(paperId:str, reportId:str, homeworkId:str, userId:str, token:str):
    # 创建会话对象
    session = requests.Session()

    # 设置 User-Agent
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    })

    # 只添加 token cookie
    session.cookies.set(
        name="token",
        value=token,
        domain=".ewt360.com",
        path="/"
    )

    # 请求 URL

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
        # "referurl": "https://web.ewt360.com/mystudy/#/report?bizCode=205&homeworkId=10389626&paperId=1969526514235999045&platform=1&reportId=2040881795217891454",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "token": token,
        "x-requested-with": "XMLHttpRequest"
    }

    try:
        # 发送 GET 请求
        response = session.get(
            url,
            headers=headers,
            timeout=15
        )


        # 尝试解析 JSON
        try:
            # open('response.json','w',encoding='utf-8').write(response.text)
            json2 = json.loads(response.text)['data']['groups'][0]['questions'][0]['rightAnswer']
            return json2  


        except ValueError:
            pass
            return 'json解析失败'

    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            return f'请求失败，错误响应{e.response.text}'
        else:
            return f"请求失败: {str(e)}"

if __name__ == '__main__':
    print(get_answer(paperId,reportId,homeworkId,userId,token))