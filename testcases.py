#testCases to be created
import enginecon as ie
from numpy import irr



#ATCF test case based on assignment
annual = ie.createA(-10000,15)
salvage = ie.createSingle(10,5000) + ie.createSingle(15,30000)
BTCF = annual+salvage
cap = ie.tax.createDepreciation(-100000,0,3) + ie.tax.createDepreciation(-100000,10,3)
ATCF = ie.tax.AfterTaxCashFlow(BTCF,cap,lambda x:0.17*x)
assert [round(i,2) for i in ATCF.get_mergedSeries()] == [-100000.0, -2633.33, -2633.33, -2633.33, -8300.0, -8300.0, -8300.0, -8300.0, -8300.0, -8300.0, -104150.0, -2633.33, -2633.33, -2633.33, -8300.0, 16600.0]
assert round(ATCF.get_PW("5%"),2) == -208111.93

print('ALL CLEAR')