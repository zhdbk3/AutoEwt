import requests
import json


def get_answer(bizCode:str, homeworkId:str, userId:str, paperId:str, reportId:str, questionId:str, token:str):
    """获取指定试卷的单选题和多选题正确答案
    
    通过调用EWT360 API获取指定用户的作业报告，解析并返回题目ID与正确答案的映射
    
    很多地方写的很不规范，一部分是不得不和 ewt 统一，还其它的看到就改一下吧qwq

    :param bizCode: 业务ID，见于url
    :param homeworkId: 作业ID
    :param userId: 用户唯一标识
    :param paperId: 试卷ID
    :param reportId: 报告ID
    :param questionId: 问题ID
    :param token: 用户认证令牌
    
    :returns: 
        - 成功时返回格式为 {题目ID: 正确答案} 的字典
        - 没有找到答案时返回'未找到正确答案'字符串
        - 发生错误时返回错误描述字符串
    
    :raises ValueError: 当JSON解析失败时返回错误字符串
    :raises requests.exceptions.RequestException: 网络请求失败时返回错误字符串
    """
    # 创建会话对象并设置User-Agent
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
    })

    # 仅添加token cookie
    session.cookies.set("token", token, domain=".ewt360.com", path="/")

    url = "https://web.ewt360.com/api/answerprod/web/answer/simple/question/info"


    # 请求头信息
    headers = {
        "authority": "web.ewt360.com",
        "method": "POST",
        "path": url,
        "scheme": "https",
    }

    # 请求体数据
    payload = {
        "questionId": questionId,
        "paperId": paperId,
        "reportId": reportId,
        "platform": "1",
        "bizCode": bizCode
    }

    url = "https://web.ewt360.com/api/answerprod/web/answer/simple/question/info"
    

    try:
        response = session.post(
            url,
            headers=headers,
            json=payload
        )
        data = json.loads(response.text)['data']

        answer_dict = {}

        def parse_questions(questions):
            """递归解析题目和子题"""
            for question in questions:
                # 先提取当前题目答案（无论是否有子题）
                if question.get('rightAnswer'):
                    answer_dict[question['id']] = question['rightAnswer']
                # 然后处理子题
                if question.get('childQuestions'):
                    parse_questions(question['childQuestions'])

        # 先处理根节点题目自身答案
        if data.get('rightAnswer'):
            answer_dict[data['id']] = data['rightAnswer']
        
        # 无论是否有子题都尝试解析
        if data.get('childQuestions'):
            parse_questions(data['childQuestions'])
        
        return answer_dict if answer_dict else '未找到正确答案'

    except ValueError:
        print("响应解析失败，原始内容:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")




if __name__ == '__main__':
    bizCode = '205'
    homeworkId='10389626'
    userId='151028179'
    paperId='1969526514235999045'
    reportId='2040988842982768934'
    questionId='1176211251046524293'
    token = '151028179-1-af93b7cbfc70ad17'
    print(get_answer(bizCode,homeworkId,userId,paperId,reportId,questionId,token))