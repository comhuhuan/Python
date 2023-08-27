import re
import json
import requests

url_map = {"http://walletservice": "https://mesh-walletservice.qa.ejeokvv.com",
           "http://userservice": "https://mesh-userservice.qa.ejeokvv.com",
           "http://adminservice": "https://mesh-adminservice.qa.ejeokvv.com"
           }

def request_info(response, *args, **kwargs):
    print("Request URL:", response.request.url)
    print("Request method:", response.request.method)
    print("Request headers:", response.request.headers)
    print("Request body:", response.request.body)


# 从 detail.txt 文件中提取 HTTP 方法、URL、headers 和 Query String 或 Payload
def extract_request_details(file_content):
    method_pattern = r"Method: (.*)"
    url_pattern = r"URL: (.*)"
    headers_pattern = r"Headers\n-+\n(.*?\n-+\n)"
    query_string_pattern = r"Query String: (.*)"
    payload_pattern = r"Payload\n-+\n(.*\n)"

    method = re.search(method_pattern, file_content).group(1)
    bbb = re.search(url_pattern, file_content).group(1)
    url = bbb.replace("http://walletservice", "https://mesh-walletservice.qa.ejeokvv.com")
    print()
    headers_text = re.search(headers_pattern, file_content, flags=re.S).group(1).strip()

    headers_list = headers_text.split("\n")
    headers = {}
    for header in headers_list:
        if "host" in header:
            continue

        if ": " in header:
            key, value = header.split(": ", 1)
            headers[key] = value
        else:
            print(f"Warning: Invalid header format: '{header}', ignoring.")

    query_string_text = re.search(query_string_pattern, file_content, flags=re.S)
    if query_string_text:
        query_string_text = query_string_text.group(1).strip()
        query_string_list = query_string_text.split("\n")
        query_string = {}
        for query in query_string_list:
            if ": " in query:
                key, value = query.split(": ", 1)
                query_string[key] = value
            else:
                print(f"Warning: Invalid query string format: '{query}', ignoring.")
    else:
        query_string = {}

    payload_text = re.search(payload_pattern, file_content)
    if payload_text:
        payload = json.loads(payload_text.group(1).strip())
    else:
        payload = {}

    return method, url, headers, query_string, payload

# 读取 detail.txt 文件内容
with open("detail.txt", "r") as detail_file:
    file_content = detail_file.read()

# 解析请求详细信息
method, url, headers, query_string, payload = extract_request_details(file_content)

# 根据提取到的 HTTP 方法发送相应的请求
if method.upper() == "GET":
    print(url)
    response = requests.get(url, params=query_string, headers=headers, hooks={'response': request_info})
elif method.upper() == "POST":
    print(url)

    response = requests.post(url, json=payload, headers=headers, hooks={'response': request_info})
else:
    raise ValueError(f"Unsupported HTTP method '{method}' in detail.txt")

# 打印响应内容及状态码
print("Response status code:", response.status_code)
print("\nResponse content:\n", response.text)