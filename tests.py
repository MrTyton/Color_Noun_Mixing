import matplotlib.pyplot as plt
print "Importing Data Manip"
import dataManip
LUX = dataManip.LUX


print "Grabbing Colors"
green_blue = LUX.getColor("green-blue")
blue_green = LUX.getColor("blue-green")

green_blue([0, 0, 0])
blue_green([0, 0, 0])
print "Testing"

print dataManip.klDivergance("green-blue", green_blue, green_blue)
print dataManip.klDivergance("blue-green", blue_green, blue_green)
print dataManip.klDivergance("green-blue", green_blue, blue_green)
print dataManip.klDivergance("blue-green", blue_green, green_blue)

    
#dataManip.plotData("green-blue", green_blue, blue_green, "H")
#dataManip.plotData("green-blue", green_blue, blue_green, "S")
#dataManip.plotData("green-blue", green_blue, blue_green, "V")


    

