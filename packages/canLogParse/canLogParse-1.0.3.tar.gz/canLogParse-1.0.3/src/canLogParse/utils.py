def fileToList(file):
	with open(file) as readFile:
		lines = readFile.readlines()
	return lines

# Takes a part-formed packet array and returns the data
def extractDataFromPacket(packet):
	dataLength = int(packet[2])
	# Remove all non-data bytes
	# I know this is janky, but I'm doing this quickly
	npacket = packet
	npacket.pop(0)
	npacket.pop(0)
	npacket.pop(0)
	npacket.pop(-1)
	npacket.pop(-1)
	
	# Convert the array of strings to an array of bytes
	dataArray = []
	for i in npacket:
		dataArray.append(str(i))

	return dataArray

# Turns the packet into a nice dictionary
def formatPacketDict(leadingZero, id, dataLength, data, tr, timeStamp):
	outputDict = {}
	outputDict["leadingZero"] = leadingZero
	outputDict["id"] = id
	outputDict["dataLength"] = dataLength
	outputDict["data"] = data
	outputDict["T/R"] = tr
	outputDict["timeStamp"] = timeStamp

	return outputDict

# Turns the data into a nice list
def formatPacketList(leadingZero, id, dataLength, data, tr, timeStamp):
	outputArr = []
	outputArr.append(leadingZero)
	outputArr.append(id)
	outputArr.append(dataLength)
	outputArr.append(data)
	outputArr.append(tr)
	outputArr.append(timeStamp)

	return outputArr

# Turns the data into a nice tuple
def formatPacketTuple(leadingZero, id, dataLength, data, tr, timeStamp):
	packetArray = formatPacketList(leadingZero, id, dataLength, data, tr, timeStamp)
	packetTuple = tuple(packetArray)

	return packetTuple

# Formats the packet into a nice format
def formatPacket(leadingZero, id, dataLength, data, tr, timeStamp, outputFormat="2dArray"):
	if outputFormat == "dict":
		# Construct a dictionary with all of the data
		output = formatPacketDict(leadingZero, id, dataLength, data, tr, timeStamp)
	elif outputFormat == "array":
		# Construct an array with all of the data
		output = formatPacketList(leadingZero, id, dataLength, data, tr, timeStamp)
	elif outputFormat == "tuple":
		# Construct a tuple with all of the data
		output = formatPacketTuple(leadingZero, id, dataLength, data, tr, timeStamp)
	
	return output