import fme
import fmeobjects
# Template Function interface:
# When using this function, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
def processFeature(feature):
	row = feature.getAttribute('Add_Number')
	try:
		valid = int(row)
		if "%s" % row[0] == "0":
			feature.setAttribute("AddNum_Pre","0")
		pass
	except:
		if "-" not in row and " " not in row:
			fnl = [row]
		if "  " in row:
			row.replace("  "," ")
		if "-" in row and " " not in row:
			fnl = row.split("-")
		if " " in row and "-" not in row:
			fnl = row.split(" ")
		if " " in row and "-" in row:
			for a in row:
				if a == " ":
					fnl = row.split(" ")
					break
				if a == "-":
					fnl = row.split(" ")
					break
		if len(fnl) == 2:
			c = fnl[0]
			for a, b in enumerate(c):
				try:
					int(b)
					feature.setAttribute("Add_Number", c)
				except:
					feature.setAttribute("Add_Number", c[:a])
					feature.setAttribute("Unit", c[a:])
			if "/" in fnl[1]:
				d = fnl[1]
				for a, b in enumerate(d):
					if b == "/":
						feature.setAttribute("AddNum_Suf", d)
					else:
						try:
							int(b)
						except:
							feature.setAttribute("AddNum_Suf", d[:a])
							feature.setAttribute("Unit", d[a:])
			else:
				
				feature.setAttribute("Unit", fnl[1])
		if len(fnl) == 3:
			feature.setAttribute("Add_Number", fnl[0])
			feature.setAttribute("AddNum_Suf", fnl[1])
			feature.setAttribute("Unit", fnl[2])
		if len(fnl) == 1:
			c = fnl[0]
			for a, b in enumerate(c):
				try:
					int(b)
				except:
					feature.setAttribute("Add_Number", c[:a])
					feature.setAttribute("Unit", c[a:])
	pass