import scipy.stats as st
import numpy as np

def discretePMF(values,probs,count):
    return st.rv_discrete(values=(values,probs)).rvs(size=count)

def uniform(lower,upper,count):
    return st.uniform.rvs(loc=lower,scale = upper-lower,size=count)

def uniform_int(lower,upper,count):
    return st.randint.rvs(low=lower,high=upper,size=count)

def triangle(lower,mode,upper,count):
    return st.triang.rvs(loc=lower,c=(mode-lower)/(upper-lower),scale=upper-lower,size=count)

def trunc_normal(mean,stdvar,lower,upper):
    #need to check this one more
    return False

class risk(object):
    #so basically this is a template for slotting in functions and data
    def __init__(self,func,data):
        self.func = func
        self.data = data
        self.seq  = self.updateSeq()
    def updateSeq(self):
        self.errorCount = 0
        variables = self.func.__code__.co_varnames[:self.func.__code__.co_argcount]
        sortedvars =  tuple(tuple(self.data[k][i]for k in variables) for i in range(len(self.data[list(self.data.keys())[0]])))
        out = ()
        for i in sortedvars:
            try:
                out+=(self.func(*i),)
            except:
                self.errorCount+=1
        return np.array(out)
    def updateData(self,data):
        self.data = data
        self.seq = self.updateSeq()
    def updateFunc(self,func):
        self.func = func
        self.seq = self.updateSeq()
    def stats(self):
        return st.describe(self.seq)

    def tornado(self):
        #pseduocode
        # subplot
        # for i in factors:
        #     a = [func(all expected values, linspace 10 i)]
        #     ax.plot(a)
        # return fig,ax
        return "This function is incomplete"