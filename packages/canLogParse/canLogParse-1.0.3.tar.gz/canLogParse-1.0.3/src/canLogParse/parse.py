import utils
import csv

# Take a raw packet line and format it into something more useful
def parsePacket(rawPacket, outputFormat="array"):
	packet = rawPacket.split()

	# There's always a "logging stopped" line at the end
	if packet[0] == "Logging":
		return None

	# The leading zero at the start of the packet
	leadingZero = int(packet[0])
	# The ID of the packet
	id = packet[1]
	# The length of the actual data
	dataLength = int(packet[2])
	# The transmit/receive byte
	tr = packet[-1]
	# The timestamp of the packet
	timeStamp = float(packet[-2])
	# The actual bytes of data
	data = utils.extractDataFromPacket(packet)

	formattedPacket = utils.formatPacket(leadingZero, id, dataLength, data, tr, timeStamp, outputFormat=outputFormat)
	
	return formattedPacket

# Take the contents of a CAN log and format it into something more useful
def parseCanData(rawData, outputFormat="array"):
	# The output array
	output = []

	# Loop through every packet logged
	for rawPacket in rawData:
		formattedPacket = parsePacket(rawPacket, outputFormat=outputFormat)
		if formattedPacket == None:
			return output
		output.append(formattedPacket)

	return output

# Given a 2D array of packets, finds all unique IDs
def findUniqueIDs(packets):
	allIDs = []
	# Loop through all of the packets
	for packet in packets:
		# Append the ID to allIDs
		allIDs.append(packet[1])
	
	uniqueIDs = set(allIDs)
	return list(uniqueIDs)

# Export a log in 2D array format to a csv file
def exportLogToCSV(log, filename):
	with open(filename, "w") as csvfile:
		logWriter = csv.writer(csvfile)
		for i in log:
			logWriter.writerow(i)

# Take a CAN log file and format it into something more useful
def importCanLogFile(file, outputFormat="array"):
	rawCanData = utils.fileToList(file)
	output = parseCanData(rawCanData, outputFormat=outputFormat)
	return output
