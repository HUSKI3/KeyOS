from zipfile import ZipFile
import os

def pack(sources,name=None):
	# create a ZipFile object
	pack = ZipFile(['{0}.keypack' if name else "custom_skin"].format(name), 'w')
	# Add multiple files to the zip
	for source in sources:
		pack.write('sample_file.csv')
	# close the Zip File
	pack.close()
	path = os.path.abspath(os.getcwd())
	print("Generated a new theme at:",path)
	return 0