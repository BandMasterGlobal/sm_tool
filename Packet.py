import struct
import binascii

class Packet:	
	def __init__ (self, data = ''):
		self.data = data
		self.position = 0
		self.size = len (data)
	
	def getShort (self):
		short = struct.unpack ("H", self.data[self.position:self.position+2])[0]
		self.position += 2
		return short
	
	def getInt (self):
		int = struct.unpack ("I", self.data[self.position:self.position+4])[0]
		self.position += 4
		return int

	def getSignedInt (self):
		int = struct.unpack ("i", self.data[self.position:self.position+4])[0]
		self.position += 4
		return int

	def getChar (self):
		char = self.data[self.position]
		self.position += 1
		return char

	def getUnicodeString (self, len = 0):
		if len == 0:
			len = self.size
		string = ''
		pos = self.position
		i = 0
		while pos  < (pos + len):
			try:
				data = self.data[pos:pos+2]
			except IndexError:
				self.position = pos
				return string
				
			if data == b'\x00\x00':
				break
			string += data.decode("utf-16-le")
			pos += 2
			
		self.position += len
		return string
	
	def getString (self, len = 0):
		if len == 0:
			len = self.size
		string = ''
		pos = self.position
		i = 0
		while pos  < (pos + len):
			try:
				data = self.data[pos]
			except IndexError:
				self.position = pos
				return string
				
			if data == '\x00':
				break
			string += data
			pos += 1
			
		self.position += len
		return string
		
class NewPacket:
	def __init__ (self, header, udata = ''):
		self.header = header
		self.data = ''
		self.udata = udata
	
	def addShort (self, number):
		self.data += struct.pack ("H", number)
	
	def addInt (self, number):
		self.data += struct.pack ("I", number)
	
	def addString (self, string, strlen, filler = '\x00'):
		string_length = len(string)
		self.data += string[:strlen]
		if len (string) < strlen:
			for i in range(0, strlen-string_length):
				self.data += filler
	
	def addRaw (self, raw):
		self.data += raw
		
	def addHex (self, hex):
		self.data += binascii.a2b_hex (hex)
		
	def addByte (self, byte):
		self.data += chr (byte)
	
	def getPacket (self):
		packetdata = self.data
		if not self.udata:
			packetdata = '\xf1' + struct.pack ("H", len (packetdata)) + self.header + '\x00' + packetdata + '\xf2'
		else:
			packetdata = '\xf1' + struct.pack ("H", len (packetdata)) + self.header + '\x00' + packetdata + self.udata + '\xf2'
		
		return packetdata
	
	def debugPacket (self):
		packet = self.getPacket ()
		print("*" * 10)
		print("Packet Len: %d" % len(packet))
		print("Header: %s" % binascii.hexlify (self.header))
		print("Size: %d (%X)" % (len(self.data), len (self.data)))
		print("Data:")
		print(binascii.hexlify (packet))
		print("*" * 10)
