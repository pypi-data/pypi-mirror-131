
# canLogParse

This is a library for importing and parsing data from Kvaser CAN files when you don't have a DBC file. The code should be fairly simple and self-documenting, and all other information should be contained within this file. You can install the library on pip via `pip3 install canLogParse`.

  

## Functions

### `parseCanPacket(rawPacket, outputFormat="2dArray")`
Takes a raw, unformatted CAN packet and returns it in a more useful format. The possible formats are `array` (the default), `tuple`, and `dict`. 

#### Output data

The data is structured as follows:

`leadingZero`: The zero at the start of the packet.

`id`: The packet ID.

`dataLength`: The number of data bytes.

`data`: The data bytes in an array of strings.

`T/R`: It is assumed that this is transmit/receive, but so far it has only been observed as `R`.

`timeStamp`: The packet timestamp.  

In `array` and `tuple` formats, the data is in the order above. In `dict	` format, the keys are as stated above and 

### `parseCanData(rawData, outputFormat="array")`
Parses an array of CAN packets in the same way as `parseCanPacket`. Formats are the same as `parseCanPacket`, but put together in an array.

### `importCanLogFile(file, outputFormat="array")`

The same as `parseCanData`, but taking the data from a file.

### `findUniqueIDs(packets)`

Takes a 2D array (or array of tuples) of packets, returns a list of all unique packet IDs.

### `exportLogToCSV(log, filename)`

Takes a 2D array of packets and writes the data in CSV format to the specified file.

### `_formatPacket(leadingZero, id, dataLength, data, tr, timeStamp, outputFormat="2dArray")`

This function takes the given data and formats it in the specified way.

### `_formatPacketList(leadingZero, id, dataLength, data, tr, timeStamp)`, `_formatPacketDict`, and `_formatPacketTuple`

These functions take in the packet data and format it into either a list, a dictionary, or a tuple.

### `_extractDataFromPacket(packet)`

This function takes a packet array and returns the data bytes as an array of strings. It does this by removing all known non-data bytes, which is a terrible way to do it. This function should be updated to extract it using the included `dataLength` byte.

### `_fileToList(file)`

This takes a file name, and returns its rows in a list.

## TODO

- Update `_extractDataFromPacket` to use the `dataLength` byte
