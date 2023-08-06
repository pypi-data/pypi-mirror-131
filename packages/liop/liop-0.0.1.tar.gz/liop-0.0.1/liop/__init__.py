
def ladd(l1,l2):
    l=[]
    if len(l1)>len(l2):
        for i in range(len(l2)):
            x=len(l2)
            l3=l1[i]+l2[i]
            l.append(l3)
        l.extend(l1[x::])
    elif len(l1)<len(l2):
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]+l2[i]
            l.append(l3)
        l.extend(l2[x::])
    else:
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]+l2[i]
            l.append(l3)
    return print(l)
def lsub(l1,l2):
    l=[]
    if len(l1)>len(l2):
        for i in range(len(l2)):
            x=len(l2)
            l3=l1[i]-l2[i]
            l.append(l3)
        l.extend(l1[x::])
    elif len(l1)<len(l2):
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]-l2[i]
            l.append(l3)
        l.extend(l2[x::])
    else:
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]-l2[i]
            l.append(l3)
    return print(l)
def lmulti(l1,l2):
    l=[]
    if len(l1)>len(l2):
        for i in range(len(l2)):
            x=len(l2)
            l3=l1[i]*l2[i]
            l.append(l3)
        l.extend(l1[x::])
    elif len(l1)<len(l2):
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]*l2[i]
            l.append(l3)
        l.extend(l2[x::])
    else:
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]*l2[i]
            l.append(l3)
    return print(l)
def ldiv(l1,l2):
    l=[]
    if len(l1)>len(l2):
        for i in range(len(l2)):
            x=len(l2)
            l3=l1[i]/l2[i]
            l.append(round(l3))
        l.extend(l1[x::])
    elif len(l1)<len(l2):
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]/l2[i]
            l.append(round(l3))
        l.extend(l2[x::])
    else:
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]/l2[i]
            l.append(round(l3))
    return print(l)
def lmod(l1,l2):
    l=[]
    if len(l1)>len(l2):
        for i in range(len(l2)):
            x=len(l2)
            l3=l1[i]%l2[i]
            l.append(l3)
        l.extend(l1[x::])
    elif len(l1)<len(l2):
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]%l2[i]
            l.append(l3)
        l.extend(l2[x::])
    else:
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]%l2[i]
            l.append(l3)
    return print(l)
def lpow(l1,l2):
    l=[]
    if len(l1)>len(l2):
        for i in range(len(l2)):
            x=len(l2)
            l3=l1[i]**l2[i]
            l.append(l3)
        l.extend(l1[x::])
    elif len(l1)<len(l2):
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]**l2[i]
            l.append(l3)
        l.extend(l2[x::])
    else:
        for i in range(len(l1)):
            x=len(l1)
            l3=l1[i]**l2[i]
            l.append(l3)
    return print(l)

