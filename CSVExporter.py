import Exporter

class CSVExporter(Exporter.Exporter):

	def export(self, filename = 'export.csv'):
		fh = open(filename, 'w')

		fh.write("'Date';'Article';'Sum';'Count'\n")

		for chckId in self._checkpointData:
			for article in self._checkpointData[chckId]['articles']:
				fh.write(self._checkpointData[chckId]['info'].strftime('%Y-%m-%d')+";'"+article+"';"+str(self._checkpointData[chckId]['articles'][article]['sum'])+";"+str(self._checkpointData[chckId]['articles'][article]['count'])+"\n")
			
		fh.close()
