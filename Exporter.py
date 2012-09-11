class Exporter(object):

	_checkpointData = {}

	def __init__(self, chkData):
		self._checkpointData = chkData
		
	def export(self):
		raise Exception("this method must be overwritten")
