import random

proxies_list =[]
with open('proxy.txt') as f:
        for line in f:
                proxies_list.append(line.strip())
f.close()

def get_proxy():
        proxy_chosen = random.choice(proxies_list)
        proxy_ditails = proxy_chosen.split(":")
        proxy = proxy_ditails
        pelneproxy = proxy[2]+":"+proxy[3]+"@"+proxy[0]+":"+proxy[1]
        proxies = {
                'http': 'http://'+pelneproxy,
                'https': 'http://'+pelneproxy}
        return proxies