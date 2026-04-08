


def ifLetter(c):
    if( (c<='Z' and c>='A') or (c<='z' and c>='a') ):
        return True
    return False

def ifNumber(c):
    if(c<='9'and c>='0'):
        return True
    return False

def ifChinese(c):
    if ('\u4e00' <= c <= '\u9fff'):
        return True
    return False

def ifSymbol(c):
    if (    c == '!' or c == '@' or c == '$' or c == '%' or c == '^' or c == '&' or c == '*' or
            c == '(' or c == ')' or c == '[' or c == ']' or c == '{' or c == '}' or c == ':' or
            c == ';' or c == '\'' or c == '\"' or c == ',' or c == '.' or c == '<' or c == '>' or
            c == '+' or c == '=' or c == '-' or c == '_' or c == '/' or c == '?'
    ):
        return True
    return False

def getWord(s,p):
    ret=''
    n=len(s)
    while(p<n and not ifLetter(s[p]) and not ifChinese(s[p]) ):
        p+=1
    while (p < n and (ifLetter(s[p]) or ifChinese(s[p]) ) ):
        ret+=s[p]
        p+=1

    return ret



def getString(s,p):
    ret=''
    n=len(s)
    while(p<n and not ifLetter(s[p]) and not ifChinese(s[p]) and not ifNumber(s[p]) and not ifSymbol(s[p]) ):
        p+=1
    while (p < n and (ifLetter(s[p]) or ifChinese(s[p]) or ifNumber(s[p]) or ifSymbol(s[p]) ) ):
        ret+=s[p]
        p+=1

    return ret


def getString2(s,p):
    ret=''
    n=len(s)
    while(p<n and not ifLetter(s[p]) and not ifChinese(s[p]) and not ifNumber(s[p]) and not ifSymbol(s[p]) ):
        p+=1
    while (p < n and (ifLetter(s[p]) or ifChinese(s[p]) or ifNumber(s[p]) or ifSymbol(s[p]) ) ):
        ret+=s[p]
        p+=1

    return (ret,p)



def getNumber(s, p):
    ret = 0
    ok=0
    n = len(s)
    while (p < n and not ifNumber(s[p]) ):
        p+=1
    while (p < n and ifNumber(s[p]) ):
        ok=1
        ret*=10
        ret += int(s[p])
        p+=1
    if(ok==0):
        return -1
    return ret

def getNumber2(s, p):
    ret = 0
    ok=0
    n = len(s)
    while (p < n and not ifNumber(s[p]) ):
        p+=1
    while (p < n and ifNumber(s[p]) ):
        ok=1
        ret*=10
        ret += int(s[p])
        p+=1
    if(ok==0):
        return (-1,n)
    return (ret,p)


def getAny(s,p):
    ret=''
    n=len(s)
    
    while (p < n and s[p] == ' ' ):
        p+=1
    
    while (p < n):
        ret+=s[p]
        p+=1

    return ret