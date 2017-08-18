import requests, os
class GSEPROXY:     
    def __init__(self, proxy_file):
        self.proxy_file = proxy_file

    def requestDELETEWithProxy(self, endpoint, **kwargs):
        if not os.path.isfile("./NO_PROXY"):
            kwargs["timeout"]=5    
            with open(self.proxy_file) as f:
                proxies = f.readlines()
                for proxy in proxies:
                    print("setting proxy: ", proxy)
                    os.environ['http_proxy'] = "http://" + proxy.strip()
                    os.environ['https_proxy'] = "https://" + proxy.strip()
                    try:
                        call = requests.post(endpoint, **kwargs)
                    except Exception:
                        print(proxy, "didn't work")
                    else:
                        return call
        else: 
            call = requests.post(endpoint, **kwargs)
            return call

    def requestPOSTWithProxy(self, endpoint, **kwargs):
        if not os.path.isfile("./NO_PROXY"):
            kwargs["timeout"]=5    
            with open(self.proxy_file) as f:
                proxies = f.readlines()
                for proxy in proxies:
                    print("setting proxy: ", proxy)
                    os.environ['http_proxy'] = "http://" + proxy.strip()
                    os.environ['https_proxy'] = "https://" + proxy.strip()
                    try:
                        call = requests.post(endpoint, **kwargs)
                    except Exception:
                        print(proxy, "didn't work")
                    else:
                        return call
        else: 
            call = requests.post(endpoint, **kwargs)
            return call

    def requestGETWithProxy(self, endpoint, **kwargs):
        if not os.path.isfile("./NO_PROXY"):
            kwargs["timeout"]=5    
            with open(self.proxy_file) as f:
                proxies = f.readlines()
                for proxy in proxies:
                    print("setting proxy: ", proxy)
                    os.environ['http_proxy'] = "http://" + proxy.strip()
                    os.environ['https_proxy'] = "https://" + proxy.strip()
                    try:
                        call = requests.get(endpoint, **kwargs)
                    except Exception:
                        print(proxy, "didn't work")
                    else:
                        return call
        else: 
            call = requests.post(endpoint, **kwargs)
            return call
 
 
    def requestPUTWithProxy(self, endpoint, **kwargs):
        if not os.path.isfile("./NO_PROXY"):
            kwargs["timeout"]=5    
            with open(self.proxy_file) as f:
                proxies = f.readlines()
                for proxy in proxies:
                    print("setting proxy: ", proxy)
                    os.environ['http_proxy'] = "http://" + proxy.strip()
                    os.environ['https_proxy'] = "https://" + proxy.strip()
                    try:
                        call = requests.put(endpoint, **kwargs)
                    except Exception:
                        print(proxy, "didn't work")
                    else:
                        return call
        else: 
            call = requests.post(endpoint, **kwargs)
            return call