import lux
LUX = lux.LUX("lux.xml")

while(True):
	target = raw_input("Color: ")
	color = LUX.getColor(target)
	print color.dim_models[0].broadness(360)
