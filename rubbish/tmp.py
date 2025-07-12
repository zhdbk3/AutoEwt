import json
import os
import requests

common_header_json = {
    "content-type": "application/json", "access-control-allow-origin": "*",
    "origin": "https://teacher.ewt360.com", "referer": "https://teacher.ewt360.com/",
    "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
    "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site",
    "token": "151028179-1-fca9a702344e7836",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.30",
}


def get_paper_answer_by_questionid(paper_info,b_questionid):
    contentUrl = paper_info['contentUrl']
    query_info = contentUrl[contentUrl.find('?')+1:]
    url = "https://web.ewt360.com/customerApi/api/studyprod/web/answer/quesiton/analysis?"+query_info+"&questionId="+str(b_questionid)
    try:
        Response = requests.get(url,headers=common_header_json)
        json2=json.loads(Response.text)
        if(json2["code"]=="200"):
            return json2["data"]
        else:
            print("get answer_by_questionid ERROR")
            print(Response.text)
            raise Exception("Error")
    except:
        os.system("pause")


homeworkId = "10389626"
paperId = "1996206103754744180"
item = {"contentUrl":f"//web.ewt360.com/mystudy/#/exam/answer?paperId={paperId}&bizCode=205&platform=1&videoPoint=1&homeworkId={homeworkId}"}
b_questionid = 3244399719505180405

get_paper_answer_by_questionid(item,b_questionid)