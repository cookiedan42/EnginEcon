import scipy.stats as st
import numpy as np

# distributions return a array of size n if count=n
# else return an object
# object.rvs(n) to get an array of size n
def discretePMF(values,probs,count=None):
    if count:
        return st.rv_discrete(values=(values,probs)).rvs(size=count)
    else:
        return st.rv_discrete(values=(values,probs))

def uniform(lower,upper,count=None):
    if count:
        return st.uniform(loc=lower,scale = upper-lower).rvs(size=count)
    else:
        return st.uniform(loc=lower,scale = upper-lower)

def uniform_int(lower,upper,count=None):
    if count:
        return st.randint(low=lower,high=upper+1).rvs(size=count)
    else:
        return st.randint(low=lower,high=upper+1)

def triangle(lower,mode,upper,count=None):
    if count:
        return st.triang(loc=lower,c=(mode-lower)/(upper-lower),scale=upper-lower).rvs(size=count)
    else:
        return st.triang(loc=lower,c=(mode-lower)/(upper-lower),scale=upper-lower)

def normal(mean,stdvar,count=None):
    if count:
        return st.norm(loc=mean,scale=stdvar).rvs(size=count)
    else:
        return st.norm(loc=mean,scale=stdvar)

def trunc_normal(mean,stdvar,lower,upper,count=None):
    a,b = (lower - mean)/stdvar , (upper - mean)/stdvar
    if count:
        return st.truncnorm(a,b,loc=mean,scale=stdvar).rvs(size=count)
    else:
        return st.truncnorm(a,b,loc=mean,scale=stdvar)

def fixed(value,count=None):
    if count:
        return st.uniform(loc=value,scale = 0).rvs(size=count)
    else:
        return st.uniform(loc=value,scale = 0)

def lognormal(mean,stdvar,count=None):
    a_mean = 0.5* np.log(mean**4/(stdvar**2+mean**2))
    a_stdvar = np.sqrt(np.log(stdvar**2/mean**2+1))
    if count:
        return st.lognorm(s=a_stdvar,scale=np.exp(a_mean)).rvs(size=count)
    else:
        return st.lognorm(s=a_stdvar,scale=np.exp(a_mean))

class risk(object):
    #so basically this is a template for slotting in functions and data
    def __init__(self,func,data,counts=None):
        self.func = func
        self.data = data
        self.seq  = self.updateSeq(counts)
    def updateSeq(self,counts=None):
        self.errorCount = 0
        self.errorLog = []
        variables = self.func.__code__.co_varnames[:self.func.__code__.co_argcount]
        if not counts:
            countsList = []
            for i in self.data.values():
                try:
                    countsList += [len(i)]
                except:
                    countsList += [0]
            counts = max(countsList)        
        sortedvars = ()
        for i in range(counts):
            ith = ()
            for key in variables:
                if type(self.data[key]) not in (list,tuple,np.ndarray):
                    ith += (self.data[key],)
                else:
                    ith += (self.data[key][i],)
            sortedvars+=(ith,)
        out = ()
        for i in sortedvars:
            try:
                out+=(self.func(*i),)
            except Exception as e:
                self.errorLog +=[e]
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

    # return st.percentile updated version?
    # def valueAtRisk(self,percentile):
    #     if type(percentile) == str:
    #         percentile = float(percentile.split('%')[0])
    #     return st.scoreatpercentile(self.seq,100-percentile)

    # def upsidePotential(self,value):
    #     return 1 - st.percentileofscore(self.seq,value,kind='strict')

    # def downsideRisk(self):
    #     st.percentileofscore(self.seq,0,kind='weak')

    # def tornado(self):
    #     if seq:
    #         seqStats = st.describe(seq)
    #         maxS,minS = seqStats.minmax
    #         meanS = seqStats.mean
    #     else:
    #         pass
        #pseduocode
        # subplot
        # for i in factors:
        #     a = [func(all expected values, linspace 10 i)]
        #     ax.plot(a)
        # # return fig,ax
        # return "This function is incomplete"