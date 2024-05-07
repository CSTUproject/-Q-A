#pip install requests
#pip install requests openpyxl

import pandas as pd
import requests
from bs4 import BeautifulSoup

# 定义要提取的网页范围
start_page = 28183
end_page = 36839

# 初始化 Excel 数据
data = []

for page_num in range(start_page, end_page + 1):
    url = f'https://gf.cabr-fire.com/article-{page_num}.htm'
    response = requests.get(url)
    html_content = response.content

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 获取网页标题
    title = soup.find('title').get_text().split('-')[0].strip()

    # 找到包含问题和答案的标签
    question_tags = soup.find_all(['strong', 'span'])
    for tag in question_tags:
        text = tag.get_text().strip()
        if text.startswith('★问题') or text.startswith('问题') or text.startswith('★'):
            question = text.split('：')[1].strip() if '：' in text else ''
            # 找到该问题对应的答案
            next_sibling = tag.next_sibling
            answer = ''
            while next_sibling and not next_sibling.name in ['strong', 'span']:
                if next_sibling.string:
                    answer += next_sibling.string.strip()
                next_sibling = next_sibling.next_sibling
            answer = answer.strip().strip("'")
            # 将问题和答案添加到 Excel 数据中
            data.append([url, page_num, title, question, answer])

# 创建 DataFrame 并写入 Excel 文件
df = pd.DataFrame(data, columns=['网页链接', '网页页数', '网页的标题', '爬取的问题', '爬取的答案'])
df.to_excel('output.xlsx', index=False)

import json

# 将数据转换为字典列表
data_dict = [{'网页链接': row[0], '网页页数': row[1], '网页的标题': row[2], '爬取的问题': row[3], '爬取的答案': row[4]} for row in data]

# 将字典列表保存为 JSON 文件
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)