#some thing just don't need to be improved
from numpy import irr,mirr,nper,rate

###Interest table stuff##################################################################3

#Doing a start/end of period variable following numpy convention

#A series
def FP(i,n,when=0):
    n = (n-1 if when == 1 else n)
    return (1+i)**n

def PF(i,n,when=0):
    n = (n-1 if when == 1 else n)
    return (1+i)**-n

def FA(i,n,when=0):
    n = (n-1 if when == 1 else n)
    return ((1+i)**n-1)/i

def PA(i,n,when=0):
    n = (n-1 if when == 1 else n)
    return ((1+i)**n-1)/(i*(1+i)**n)

def AF(i,n,when=0):
    n = (n-1 if when == 1 else n)
    return FA(i,n)**-1

def AP(i,n,when=0):
    n = (n-1 if when == 1 else n)
    return PA(i,n)**-1

#G series
def PG(i,n,when=0):
    n = (n-1 if when == 1 else n)
    return (1/i)*(((1+i)**n-1)/(i*(1+i)**n) - (n/(1+i)**n))

def AG(i,n,when=0):
    n = (n-1 if when == 1 else n)
    return 1/i - n/((1+i)**n-1)

def PGEO(i,n,f,when=0):
    n = (n-1 if when == 1 else n)
    return 1/(i-f) * (1-PF(i,n)*FP(f,n))
###########################################################################################################################
def effectiveInterestConverter(interest = 0, old = 1, new = 1):
    #ratio between old and new interest rate
    return interest **(new/old)

from matplotlib.pyplot import subplots
class CashFlow(object):
    def __init__(self, rate=0.1,sequence=[]):
        self.set_rate(rate)
        if type(sequence) in (list,tuple):
            if False not in [type(i) in (float,int) for i in sequence]:
                self.sequence = list(sequence)
            else:
                raise SyntaxError("invalid values in sequence")
        else:
            raise SyntaxError("invalid sequence type")

    def __equalize(self,a,b):
        if len(a)<len(b):
            a += [0]*(len(b)-len(a))
        elif len(b)<len(a):
            b += [0]*(len(a)-len(b))
        return(a,b)
    def __add__(self,other):
        #adding two cash flows assuming they start at the same time
        if self.rate == other.rate:
            a,b = self.__equalize(self.sequence,other.sequence)
            newseq = [i+j for i,j in zip(a,b)]
            return CashFlow(rate=self.rate,sequence=newseq)
        else:
            #raise error when rates are mismatched to remove ambiguity
            raise SyntaxError("mismatched rates")
    def __radd__(self,other):
        #needed for sum() to work
        return self
    def get_PW(self):
        return sum([PF(self.rate,i)*self.sequence[i] for i in range(len(self.sequence))])
    def get_AW(self):
        return self.get_PW() * AP(self.rate,len(self.sequence)-1)
    def get_FW(self):
        return self.get_PW() * FP(self.rate,len(self.sequence)-1)
    def set_rate(self,rate):
        #interest rate is per period
        if type(rate) == str and "%" in rate: 
            self.rate = float(rate.split("%")[0].strip())/100
        elif type(rate) in (int,float):
            self.rate = rate
        else:
            raise SyntaxError("invalid rate")
    def rebase(self, newBase=1):
        if newBase<=1:
            raise SyntaxError("rebase can only be increased sorry :(")
        elif float(newBase) != int(newBase):
            raise SyntaxError("rebase has to be an integer")
        newSeq = []
        for i in self.sequence:
            newSeq+=[i] + [0]*newBase-1
        newRate = (1+self.rate)**(1/newBase)-1
        return CashFlow(rate=newRate,sequence=newSeq)

        
        

    def draw(self,labels=False):
        fig,ax = subplots()
        xAxis = range(len(self.sequence))
        up =    [i if i>0 else None for i in self.sequence]
        down =  [i if i<0 else None for i in self.sequence]
        if False in [True if i == None else False for i in up]:
            ax.stem(xAxis,up,markerfmt="^",use_line_collection=True)
            if labels:
                for i in range(len(xAxis)):
                    if up[i]== None:
                        continue
                    ax.annotate(
                        s=" $ {0:0.2f}".format(up[i]),
                        xy=(xAxis[i],up[i]),
                        rotation=90,
                        ha = "right",
                        va='bottom'
                        )
        if False in [True if i==None else False for i in down]:
            ax.stem(xAxis,down,markerfmt="rv",linefmt='r',use_line_collection=True)
            if labels:
                for i in range(len(xAxis)):
                    if down[i] == None:
                        continue
                    ax.annotate(
                        s="$ {0:0.2f} ".format(down[i]),
                        xy=(xAxis[i],down[i]),
                        rotation=90,
                        ha='right',
                        va='top'
                        )
        #returning fig and subplot object for manual editing if desired
        return fig,ax

#general instantiators
def createA(rate=0.1,pmt=0,length=0):
    #raise error if length<0
    seq = [0]+[pmt]*length
    return CashFlow(rate=rate,sequence=seq)

def createB(rate=0.1,pmt=0,length=0):
    #raise Error if length <0
    seq = [pmt]*length+[0]
    return CashFlow(rate=rate,sequence=seq)
                    
def createG(rate = 0.1,g=0,length=0):
    seq = [0]+[i*g for i in range(length)]
    return CashFlow(rate=rate,sequence=seq)

def createGeo(rate = 0.1,start=1,f=0,length=0):
    seq = [0]+[start*(1+f)**i for i in range(length)]
    return CashFlow(rate=rate,sequence=seq)

def createSingle(rate = 0.1,pos=0,value=0,length=0):

    seq = [0] *max(length+1,pos+1)
    seq[pos] = value
    return CashFlow(rate=rate,sequence=seq)

def createRepeat(rate = 0.1,pattern=[0],length=0):
    seq = [0] + (1+length//len(pattern))*pattern
    seq = seq[:length+1]
    return CashFlow(rate=rate,sequence=seq)

# other art pro

def drawCashFlows(*args):
    #take in a series of lists/tuples and draw a cash flow for them

    #rebase
    maxLen = max([len(i)for i in args])
    rebased = [i+[0]*(maxLen-len(i)) for i in args]
    print(rebased)
    pos = [0]*maxLen
    neg = [0]*maxLen
    for i in range(maxLen):
        for series in rebased:
            if series[i]>0:
                pos[i] += series[i]
            elif series[i]<0:
                neg[i] += series[i]
    pos = [None if i ==0 else i for i in pos]
    neg = [None if i ==0 else i for i in neg]
    fig,ax=subplots()
    ax.stem(pos)
    ax.stem(neg)

    
    #sum positives
    #sum negatives


'''
X = []
Y = []
for lines in fig.gca().get_lines():
    for x,y in lines.get_xydata():
        X.append(x)
        Y.append(y)
        print(x,y)
fig2,ax2 = subplots()
ax2.scatter(X,Y)

'''