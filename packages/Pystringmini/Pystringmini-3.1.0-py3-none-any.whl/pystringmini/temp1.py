def minimum(string):
    cnt=[]
    for i in string.strip():
        if ord(i)>=97 and ord(i)<=122:
            temp=int(ord(i))
            cnt.append(temp)
        elif ord(i)>=65 and ord(i)<=90: #caps
            temp=int(ord(i))
            cnt.append(temp)
        else:
            continue
    cnt.sort()
    return chr(cnt[0])
print(minimum("https://pypi.org/project/Pystringmini/"))

def maximum(string):
    cnt=[]
    for i in string.strip():
        if ord(i)>=97 and ord(i)<=122:
            temp=int(ord(i))
            cnt.append(temp)
        elif ord(i)>=65 and ord(i)<=90: #caps
            temp=int(ord(i))
            cnt.append(temp)
        else:
            continue
    cnt.sort()
    return chr(cnt[len(cnt)-1])

print(maximum("https://pypi.org/project/Pystringmini/"))
