from urllib.parse import parse_qs

def get_info_from_url(paper_url):
    """
    从给定的 URL 中提取查询参数并返回一个字典。

    :param paper_url: 包含查询参数的 URL 字符串
    :return: 包含 URL 中所有查询参数的字典
    """
    # 找到 ? 的索引位置
    query_start_index = paper_url.find('?')
    if query_start_index == -1:
        # 如果没有找到 ?，说明没有查询参数，返回空字典
        return {}
    # 提取 ? 后面的查询字符串
    query_string = paper_url[query_start_index + 1:]
    # 解析查询字符串为字典
    query_params = parse_qs(query_string)
    # 将字典的值从列表转换为单个值
    return {key: value[0] for key, value in query_params.items()}

if __name__ == '__main__':
    test_urls = [
        "https://web.ewt360.com/mystudy/#/exam/answer?paperId=1990849016816197771&bizCode=205&platform=1&videoPoint=1&homeworkId=10389626",
    ]

    for url in test_urls:
        result = get_info_from_url(url)
        print(f"测试 URL: {url}")
        print(f"解析结果: {result}")
        print("-" * 50)