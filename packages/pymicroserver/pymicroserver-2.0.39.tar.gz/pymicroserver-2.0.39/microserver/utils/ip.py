# @Time    : 2018/7/19 15:50
# @Author  : Niyoufa
import requests
from lxml import etree

def get_ip_info(ip):
    ip_url = "https://ip.cn/index.php?ip=%s"%ip
    response = requests.get(ip_url)
    html = etree.HTML(response.text)
    location = html.xpath("//div[@id='result']/div/p/code/text()")
    if location:
        location = location[-1].strip()
    else:
        location = ""
    return location
