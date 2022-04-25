# XRAY-F
FOFA联动XRAY
需要安装的库 requests,urllib3,argparse,configparser,base64
python3 -m pip install *




使用前要先开启xray然后运行脚本即可

-fofa 通过fofa自定义查询 使用fofa语法即可

-f 导入IP进行批量跑fofa 格式：192.168.0.0

-v 没卵用

-o 输出fofa爬取的url 格式：http[s]://xxx.xxx.xxx

-h 帮助信息




推荐食用方法
代理道Burp然后Burp再代理到Xray这样既可以联动Burp的插件如Shiro，FastJson插件也可以使用Burp的爬虫这样Xray扫得更加透彻

main.py -fofa 标题="泛微" -p 【Burp代理端口】 -o out.txt


-o格式主要是为了能够再次联动AWVS因为AWVS需要导入URL
