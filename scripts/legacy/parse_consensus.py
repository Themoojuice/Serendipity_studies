import json,re,sys
d=json.load(open(sys.argv[1]))
txt="".join(x.get('text','') for x in d)
items=re.split(r'\n\[(\d+)\] ',txt)
for i in range(1,len(items)-1,2):
    n=items[i]; body=items[i+1]
    m=re.match(r'\[(.*?)\]\((.*?)\) \((.*?)\)',body)
    if m:
        title,url,meta=m.groups()
        print(f"{n}|{meta[:55]}|{title[:140]}")
