import requests
import json


def get_question_ids(paperId: str, token: str):
    """获取试卷中的题目ID信息
    
    通过调用EWT360 API获取指定用户的试卷信息，解析并返回题目ID列表
    
    :param paperId: 试卷ID
    :param token: 用户认证令牌
    
    :returns: 
        - 成功时返回题目ID列表
        - 发生错误时返回错误描述字符串
    
    :raises ValueError: 当JSON解析失败时返回错误字符串
    :raises requests.exceptions.RequestException: 网络请求失败时返回错误字符串
    """
    # 创建会话对象并设置User-Agent
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
    })

    # 设置token cookie
    session.cookies.set("token", token, domain=".ewt360.com", path="/")

    url = f"https://web.ewt360.com/api/answerprod/common/paper/getPaperQuestionByPaperId?paperId={paperId}"

    # 请求头信息
    headers = {
        "authority": "web.ewt360.com",
        "method": "GET",
        "path": url,
        "scheme": "https",
    }


    try:
        response = session.get(url,headers=headers,)
        
        # 检查HTTP状态码
        if response.status_code != 200:
            return f"API请求失败，状态码: {response.status_code}"
        
        if response.json()['code'] == '2001106':
            return f'请求失败，登陆状态异常，请检查token是否过期或无效'
        
        if json.loads(response.text)['code'] != '200':
            return f"API请求失败，ewt状态码：{json.loads(response.text)['code']},消息：{json.loads(response.text)['msg']} "


        # 解析JSON响应
        json_data = response.json()
        
        # print(response.text)
        # 检查响应是否包含data字段
        if 'data' not in json_data:
            return f"请求失败，API响应缺少data字段，完整响应: {response.text[:200]}"
        
        def extract_ids(question_list):
            ids = []
            if not isinstance(question_list, list):
                return ids
            for q in question_list:
                if not isinstance(q, dict):
                    continue
                sub_list = q.get('subQuestionList')
                if isinstance(sub_list, list) and sub_list:
                    # 有子题时只递归子题，不添加母题id
                    ids.extend(extract_ids(sub_list))
                else:
                    # 无子题时添加当前题id
                    ids.append(q.get('questionId'))
            return ids

        data = json_data['data']
        question_list = data.get('questionList', [])
        question_ids = extract_ids(question_list)
        return question_ids

    except json.JSONDecodeError:
        return f"响应解析失败，原始内容: {response.text[:200]}"  # 只返回前200个字符避免过长
    except requests.exceptions.RequestException as e:
        return f"网络请求失败: {type(e).__name__} - {str(e)}"
    except Exception as e:
        return f"处理失败，处理过程中发生未预期错误: {type(e).__name__} - {str(e)}"

if __name__ == '__main__':
    # 测试参数
    # paperId = '1996206103754744180' # 语文
    paperId = '1986397841559642844' # 数学
    token = ''
    result = get_question_ids(paperId, token)
    print("获取到的题目ID列表:", result)