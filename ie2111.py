##todo
'''
--calculations--
continual compounding on the interestTables

--cash flow analysis--
b/c analysis
irr and mirr

'''




#some thing just don't need to be improved
from numpy import irr,mirr,nper,rate
from matplotlib.pyplot import subplots
from interestTableFunctions import *
from interestTableFunctions import _sanitize_rate
import monteCarlo as mc

def effectiveInterestConverter(interest = 0, old = 1, new = 1):
    #ratio between old and new interest rate
    return interest **(new/old)

class CashFlow(object):
    def __init__(self, rate=0.1,seq=None,seq2=None):
        #seq and seq2 to account for positive and negative flows
        self.set_rate(rate)
        self.set_sequence(seq,seq2)

    def set_sequence(self,seq,seq2):
        if seq == None and seq2 == None:
            raise SyntaxError("No seq provided")
        elif seq2 == None:
            seqs = [self.__validateSeq(seq)]
        elif seq == None:
            seqs  = [self.__validateSeq(seq2)]
        else:
            seqs  = [self.__validateSeq(seq)
                    ,self.__validateSeq(seq2)]
        pos = [0]*len(seqs[0])
        neg = [0]*len(seqs[0])
        for seq in seqs:
            for i in range(len(seqs[0])):
                if seq[i]>0:
                    pos[i] += seq[i]
                elif seq[i]<0:
                    neg[i] += seq[i]
        self.pos = pos
        self.neg = neg

    def __validateSeq(self,seq):
        if type(seq) not in (list,tuple):
            raise SyntaxError("invalid seq type")
        if False in [type(i) in (float,int) for i in seq]:
            raise SyntaxError("invalid values in seq")
        return (list(seq) if type(seq)==tuple else seq)
        
    def __equalize(self,a,b):
        if len(a)<len(b):
            a += [0]*(len(b)-len(a))
        elif len(b)<len(a):
            b += [0]*(len(a)-len(b))
        return(a,b)
    
    def __add__(self,other):
        #adding two cash flows assuming they start at the same time
        if self.rate == other.rate:
            posA,posB = self.__equalize(self.pos,other.pos)
            negA,negB = self.__equalize(self.neg,other.neg)
            newPos = [i+j for i,j in zip(posA,posB)]
            newNeg = [i+j for i,j in zip(negA,negB)]
            return CashFlow(rate=self.rate,seq=newPos,seq2=newNeg)
        else:
            #raise error when rates are mismatched to remove ambiguity
            raise SyntaxError("mismatched rates")
    def __radd__(self,other):
        #needed for sum() to work
        return self

    def get_PW(self):
        return sum([PF(self.rate,i)*(self.pos[i]+self.neg[i]) for i in range(len(self.pos))])
    def get_AW(self):
        return self.get_PW() * AP(self.rate,len(self.pos)-1)
    def get_FW(self):
        return self.get_PW() * FP(self.rate,len(self.pos)-1)
    def get_mergedSeries(self):
        return [self.pos[i]+self.neg[i] for i in range(len(self.pos))]
    def set_rate(self,rate):
        #interest rate is per period
        self.rate = _sanitize_rate(rate)
    def rebase(self, newBase=1):
        if newBase<=1:
            raise SyntaxError("rebase can only be increased sorry :(")
        elif float(newBase) != int(newBase):
            raise SyntaxError("rebase has to be an integer")
        for i in self.pos:
            newPos += [i] + [0]*newBase-1
        for i in self.neg:
            newNeg += [i] + [0]*newBase-1
        newRate = (1+self.rate)**(1/newBase)-1
        return CashFlow(rate=newRate,seq=newPos,seq2=newNeg)
    
    def IRR(self, other=False):
        if other:
            if len(self.pos) != len(other.pos):
                raise SyntaxError("mismatched study periods, cannot calculate IRR")
            toCheck = [j-i for i,j in zip(self.get_mergedSeries(),other.get_mergedSeries())]
        else:
            toCheck = self.get_mergedSeries()
        return irr(toCheck)
    '''
    def MIRR(self, other=False):  #DO from scratch
        if other:
            toCheck = [j-i for i,j in zip(self.get_mergedSeries,other.get_mergedSeries)]
        else:
            toCheck = self.get_mergedSeries()
        #MIRR(toCheck)
        return "MIRR"
    def BC(self, other=False): #Do from scratch
        if other:
            #comparative
            return "compare"
        return "self BC"
    '''
    def draw(self,labels=False,merge=False):
        fig,ax = subplots()
        xAxis = range(len(self.pos))
        if merge:
            merge = [i+j for i,j in zip(self.pos,self.neg)]
            up    = [i if i>0 else None for i in merge]
            down  = [i if i<0 else None for i in merge]
        else:
            up    =  [None if i== 0 else i for i in self.pos]
            down  =  [None if i== 0 else i for i in self.neg]
        try:
            ax.stem(xAxis,up,markerfmt="^",use_line_collection=True)
        except:
            ax.stem(xAxis,up,markerfmt="^")
        if labels:
            for i in range(len(xAxis)):
                if up[i]== None:
                    continue
                # ax.annotate(
                #     s=" $ {0:0.2f}".format(up[i]),
                #     xy=(xAxis[i],up[i]/20),
                #     rotation=90,
                #     ha = "right",
                #     va='bottom'
                #     )
                ax.text(xAxis[i],up[i]/20," $ {0:0.2f}".format(up[i]),
                    rotation=90,ha = "right",va='bottom')
        try:
            ax.stem(xAxis,down,markerfmt="rv",linefmt='r',use_line_collection=True)
        except:
             ax.stem(xAxis,down,markerfmt="rv",linefmt='r')
        if labels:
            for i in range(len(xAxis)):
                if down[i] == None:
                    continue
                # ax.annotate(
                #     s="$ {0:0.2f} ".format(down[i]),
                #     xy=(xAxis[i],down[i]),
                #     rotation=90,
                #     ha='right',
                #     va='top'
                #     )
                ax.text(xAxis[i],down[i]/20," $ {0:0.2f}".format(down[i]),
                    rotation=90,ha = "right",va='top')
        #returning fig and subplot object for manual editing if desired
        return fig,ax

#general instantiators
def createA(rate=0.1,pmt=0,length=0):
    #raise error if length<0
    seq = [0]+[pmt]*length
    return CashFlow(rate=rate,seq=seq)

def createB(rate=0.1,pmt=0,length=0):
    #raise Error if length <0
    seq = [pmt]*length+[0]
    return CashFlow(rate=rate,seq=seq)
                    
def createG(rate = 0.1,g=0,length=0):
    seq = [0]+[i*g for i in range(length)]
    return CashFlow(rate=rate,seq=seq)

def createGeo(rate = 0.1,start=1,f=0,length=0):
    seq = [0]+[start*(1+f)**i for i in range(length)]
    return CashFlow(rate=rate,seq=seq)

def createSingle(rate = 0.1,pos=0,value=0,length=0):
    seq = [0] *max(length+1,pos+1)
    seq[pos] = value
    return CashFlow(rate=rate,seq=seq)

def createRepeat(rate = 0.1,pattern=[0],length=0):
    seq = [0] + (1+length//len(pattern))*pattern
    seq = seq[:length+1]
    return CashFlow(rate=rate,seq=seq)

# other art pro

def drawCashFlows(*args):
    #take in a series of lists/tuples and draw a cash flow for them
    maxLen = max([len(i)for i in args])
    rebased = [i+[0]*(maxLen-len(i)) for i in args]
    pos = [0]*maxLen
    neg = [0]*maxLen
    for i in range(maxLen):
        for series in rebased:
            if series[i]>0:
                pos[i] += series[i]
            elif series[i]<0:
                neg[i] += series[i]
    print(pos,neg)
    fig,ax = CashFlow(seq=pos,seq2=neg).draw()
    return fig,ax