import json

import requests
from urllib.parse import urlparse




def get_answer(paperId:str, reportId:str, homeworkId:str, userId:str, token:str):
    """获取指定试卷的单选题和多选题正确答案
    
    通过调用EWT360 API获取指定用户的作业报告，解析并返回题目ID与正确答案的映射

    参数除了token都包含在试卷页面的url里了
    
    很多地方写的很不规范，一部分是不得不和 ewt 统一，还其它的看到就改一下吧qwq

    :param paperId: 试卷唯一标识符
    :param reportId: 报告唯一标识符（也不知道这个报告指的是什么）
    :param homeworkId: 作业唯一标识符
    :param userId: 用户唯一标识
    :param token: 用户认证令牌
    
    :returns: 
        - 成功时返回格式为 {题目ID: 正确答案} 的字典
        - 没有找到答案时返回'未找到正确答案'字符串
        - 发生错误时返回错误描述字符串
    
    :raises ValueError: 当JSON解析失败时返回错误字符串
    :raises requests.exceptions.RequestException: 网络请求失败时返回错误字符串
    """
    # 创建会话对象
    session = requests.Session()

    # 设置 User-Agent
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    })

    # 添加 token cookie
    session.cookies.set(name="token",value=token,domain=".ewt360.com",path="/")

    # 请求 URL
    url = f"https://web.ewt360.com/api/answerprod/web/answer/webreport/questionGroup?paperId={paperId}&reportId={reportId}&platform=1&bizCode=205&homeworkId={homeworkId}&userId={userId}"

    # 请求头
    headers = {
        "authority": "web.ewt360.com",
        "method": "GET",
        "path": urlparse(url).path + "?" + urlparse(url).query,
        "scheme": "https",
        "token": token,
    }

    try:
        # 发送 GET 请求
        response = session.get(url,headers=headers,timeout=15)

        # open('tmp.json','w').write(response.text)

        # 尝试解析 JSON
        try:
            data = json.loads(response.text)['data']
            answer_dict = {}
            
            # 遍历所有题目组
            for group in data.get('groups', []):
                # 过滤条件：只处理单选题和多选题
                if group.get('groupName', '') in ['单选题', '多选题']:
                    # 遍历组中的每个题目
                    for question in group.get('questions', []):
                        # 同时获取题目ID和答案
                        q_id = question.get('id')
                        answer = question.get('rightAnswer')
                        if q_id and answer:
                            answer_dict[q_id] = answer
            
            return answer_dict if answer_dict else '未找到正确答案'

        except ValueError:
            return 'json解析失败'

    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            return f'请求失败，错误响应{e.response.text}'
        else:
            return f"请求失败: {str(e)}"




if __name__ == '__main__':
    paperId='1995378695485046992'
    reportId='2040988842982768934'
    homeworkId='10389626'
    userId='151028179'
    token = ''
    print(get_answer(paperId,reportId,homeworkId,userId,token))