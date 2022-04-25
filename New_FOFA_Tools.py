import requests,urllib3
import sys
import argparse
import configparser
import base64
import time


class fofa(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('fofa.ini', encoding="utf-8")
        self.email = config.get("userinfo", "email")
        self.key = config.get("userinfo", "key")
        self.base_url = config.get("userinfo", "FOFA_URL")
    def parse_args(self):
        parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -fofa title=\"泛微\"")
        parser.add_argument("-fofa", "--FOFA", help="title=\"泛微\"")
        parser.add_argument("-p", "--proxy", help="default 127.0.0.1:7777")
        parser.add_argument("-o", "--outputurl", help="Output file name. ")
        parser.add_argument("-v", "--particulars", help="Output particulars ")
        parser.add_argument("-f", "--file", help="in file")
        return parser.parse_args()
    def FOFA_Search(self,Value):
        Value =base64.b64encode(Value.encode('utf-8'))
        #title,domain,province,city,country_name,server,banner,isp,icp,
        API = self.base_url+"/api/v1/search/all?email={0}&key={1}&qbase64={2}&page=1&size=9999&fields=ip,host".format(self.email,self.key,str(Value,'utf-8'))
        # print("API:%s"%API)
        response = requests.get(url=API,timeout=15,verify=False).json()
        # print(response)
        try:
            result = response['results']
        except:
            return None
        INFO_LIST = []
        for INFO in result:
            Info = {
                "HOST":INFO[-1],
                "IP": INFO[0],
            }
            INFO_LIST.append(Info)
        return INFO_LIST
    def Xray_Scan(self,FOFAHOST,outfile=None,proxy="127.0.0.1:7777"):
        outfile = self.parse_args().outputurl
        if self.parse_args().proxy != None:
            proxy = self.parse_args().proxy
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        try:

            INFO = requests.get(url=FOFAHOST, proxies=proxies, timeout=5, verify=False)
            if outfile != None:
                with open(outfile,'a+') as f:
                    f.write(FOFAHOST+"\n")
            time.sleep(1)
        except:
            pass
    def Run_Start(self):
        urllib3.disable_warnings()
        PROXY = self.parse_args().proxy
        if self.parse_args().proxy == None:
            PROXY = "127.0.0.1:7777"
        print("\033[4;32m -Console output-\033[0m")
        print("\033[4;32m proxy：%s\n\n\n\033[0m"%(PROXY))
        print("\033[4;32m --------------------------------- \033[0m")
        if self.parse_args().FOFA != None:#-fofa
            FOFA_Value = self.parse_args().FOFA
            FOFA_return_INFO = self.FOFA_Search(FOFA_Value)
            for URL in FOFA_return_INFO:
                URL = URL["HOST"]
                if URL[0:4] != 'http':
                    URL = 'http://' + URL
                print("\033[4;32m"+URL+"\033[0m")
                self.Xray_Scan(URL)
                time.sleep(3)
        elif self.parse_args().file != None and self.parse_args().FOFA == None:
            file = self.parse_args().file
            IP_file = open(file,'r').readlines()
            for ip in IP_file:
                IP = "ip="+'"'+ip.strip()+'"'
                FOFA_return_INFO = self.FOFA_Search(IP)
                if FOFA_return_INFO == None:
                    continue
                else:
                    for URL in FOFA_return_INFO:
                        URL = URL["HOST"]
                        if URL[0:4] != 'http':
                            URL = 'http://' + URL
                        print("\033[4;32m"+URL+"\033[0m")
                        self.Xray_Scan(URL)
                        time.sleep(3)
        else:
            print("error!")
    def Logo(self):
            print("""
            ____  ___.________.    ____.   _____ 联动XRAY
    \   \/  /\_   __   \  /  _  \  \__  |   |       
     \     /  |    _  _/ /  /_\  \  /   |   |    
     /     \  |    |   \/    |    \ \____   |        
    \___/\  \ |____|   /\____|_   / / _____/    
          \_/       \_/        \_/  \/                           By SecI302
    默认代理：127.0.0.1：7777
            """)

if __name__ == '__main__':
    Obj = fofa()
    Obj.Logo()
    Obj.Run_Start()