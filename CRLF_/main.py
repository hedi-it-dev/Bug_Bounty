import requests

urls=['url']
injection=open("crlf-payload-full.txt",'r').readlines()

for url in urls:
    for i in injection:
        response=requests.get(
            url=f"{url}/{i}"
        ).status_code
        print(f" [ {response} ] {url}/{i} ")