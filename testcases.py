#testCases to be created
import ie2111 as ie

#interestTables
assert round(ie.FP  (0.05,5),4) == 1.2763
assert round(ie.PF  (0.05,5),4) == 0.7835
assert round(ie.FA  (0.05,5),4) == 5.5256
assert round(ie.PA  (0.05,5),4) == 4.3295
assert round(ie.AF  (0.05,5),4) == 0.1810
assert round(ie.AP  (0.05,5),4) == 0.2310
assert round(ie.PG  (0.05,5),3) == 8.237
assert round(ie.AG  (0.05,5),4) == 1.9025
#assert round(ie.PGEO(0.05,5),4) == #ok IDK how to test case this

A = ie.createA(rate=0.1,pmt=5,length=5) 
B = ie.createB(rate=0.1,pmt=-5,length=5)
G = ie.createG(rate=0.1,g=5,length=5)
F = ie.createGeo(rate=0.1,start=1,f=1,length=5)
R = ie.createRepeat(rate=0.1,pattern=[0,1],length=5)
S = ie.createSingle(rate=0.1,pos=5,value=5)
I = ie.createSingle(rate=0.1,pos=0,value=-5)

assert A.get_mergedSeries() == [0,5,5,5,5,5]
assert B.get_mergedSeries() == [-5,-5,-5,-5,-5,0]
assert G.get_mergedSeries() == [0,0,5,10,15,20]
assert F.get_mergedSeries() == [0,1,2,4,8,16]
assert R.get_mergedSeries() == [0,0,1,0,1,0]
assert S.get_mergedSeries() == [0,0,0,0,0,5]
assert I.get_mergedSeries() == [-5]
assert (A+B).get_mergedSeries() == [-5,0,0,0,0,5]

assert F.get_PW() == sum(F.get_mergedSeries()[i]*ie.PF(0.1,i) for i in range(len(F.get_mergedSeries())))
assert F.get_AW() == F.get_PW() * ie.AP(0.1,5)
assert F.get_FW() == F.get_PW() * ie.FP(0.1,5)