import math
import turtle

def drawCIrcleTurtle(x,y,r):
    turtle.up()
    turtle.setpos(x+r,y)
    turtle.down()

    for i in range(0,365,1):
        a = math.radians(i)
        turtle.setpos(r+r*math.cos(a),y+r*math.sin(a))

drawCIrcleTurtle(100,100,50)
turtle.mainloop()
