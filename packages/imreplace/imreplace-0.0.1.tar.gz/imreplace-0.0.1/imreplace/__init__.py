class trp:
    def replace(t,i,v):
        t2=list(t)
        print(t2)
        t2[i]=v
        t3=tuple(t2)
        print(t3)
class srp:
    def replace(s,x,v):
        for i in s[x]:
            i=v
            h=s[:x]+i+s[x+1:]
        print(h)
        s=h








