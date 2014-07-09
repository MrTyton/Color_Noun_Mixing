import lux
print "Importing LUX"
LUX = lux.LUX('lux.xml')
import matplotlib.pyplot as plt
import dataManip


print "Grabbing Colors"
green_blue = LUX.getColor("green-blue")
blue_green = LUX.getColor("blue-green")

for x in [green_blue, blue_green]:
    x.dim_models[0].auc(360)
    x.dim_models[1].auc(100)
    x.dim_models[2].auc(100)
print "Testing"

print dataManip.r2test("green-blue", green_blue, green_blue)
print dataManip.r2test("green-blue", green_blue, blue_green)
print dataManip.r2test("blue-green", blue_green, green_blue)

    
#dataManip.plotData("green-blue", green_blue, blue_green, "H")
#dataManip.plotData("green-blue", green_blue, blue_green, "S")
#dataManip.plotData("green-blue", green_blue, blue_green, "V")


    

