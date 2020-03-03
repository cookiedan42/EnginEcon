#testCases to be created
import ie2111 as ie

a = ie.createA(pmt=5,length=11)
b = ie.createG(g=-2,length=5)
c = a+b
fig,ax = c.draw()
fig2,bx = c.draw(merge=True)
fig.show()
fig2.show()