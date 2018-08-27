simbol=list('|&()')
N=50
pila=[]
EP=[]
tope=-1

def llena():
    if(tope==(N-1)):
        print 'STACKOVERFLOW'
        return True
    return False

def vacia():
    if(tope==-1):
        'STACKUNDERFLOW'
        return True
    return False

def push(dato):
    if(llena()!=True):
        global tope
        tope=tope+1
        pila.insert(tope,dato)

def pop():
    if(vacia()!=True):
        global tope
        aux=pila[tope]
        del pila[tope]
        tope=tope-1
        return aux
    else:
        return -9999

def infijo(i, EI):
    if(EI[i]=='&'):
        prioridadop=2
        return prioridadop
    elif(EI[i]=='|'):
        prioridadop=1
        return prioridadop
    elif(EI[i]=='('):
        prioridadop=5
        return prioridadop

def pripila(pila):
    if(pila[tope]=='&'):
        prioridadpi=2
        return prioridadpi
    elif(pila[tope]=='|'):
        prioridadpi=1
        return prioridadpi
    elif(pila[tope]=='('):
        prioridadpi=0
        return prioridadpi


def makeQuery(param):
    query = param.split("where")

    if (len(query) <= 1):
       return  "(&(objectClass={0}))".format(query[0].split()[-1])

    EI=query[1].replace('and','&').replace('or','|').replace("("," ( ").replace(")"," ) ").split()

    for i in range(len(EI)):
        if(not EI[i] in simbol):      #EI es operando
            EP.append("("+EI[i]+")")
        elif(EI[i]!=')'):                       #EI es diferente a ')'
            if (tope==-1):                      #Pila no esta vacia
                push(EI[i])
            else:
                if(infijo(i,EI)<=pripila(pila)):#operador de EI es <= a operador de pila
                    EP.append(pop())               
                    push(EI[i])
                elif(infijo(i,EI)>pripila(pila)):#operador de EI es > a operador de pila
                    push(EI[i])
        elif(EI[i]==')'):                       #EI es igual a ')'
            while (pila[tope]!='('):            #Pila es diferente a '('
                EP.append(pop())
            if(pila[tope]=='('):                #Pila es igual a '('
                pop()
            elif(tope!=-1):                     #Pila no esta vacia
                EP.append(pop())

    while (tope>-1):
        term = pop()
        EP.append(term)


    str=EP[0]
    stack = []
    for i,term in enumerate(EP):
        if EP[i] in simbol:
            stack[-1] = ("({0}{1}{2})".format(EP[i],stack[-1],stack[-2]))
            del(stack[-2])
        else:
            stack.append(EP[i])

    return "(&(objectClass={0}){1})".format(query[0].split()[-1],stack[-1])