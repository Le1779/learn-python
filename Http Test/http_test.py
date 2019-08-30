import requests

my_data = {'testString': 'python send'}

# 將資料加入 POST 請求中
r = requests.post('http://dfo.dynacw.com:57555/Home/TestApi2', data = my_data)
print(r)