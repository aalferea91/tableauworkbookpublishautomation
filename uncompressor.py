import shutil, os
import codecs
from configparser import ConfigParser

#This function gets the Template name from the config file
def getWorkbookName(parser):
	workbookName = parser.get('Template Name', 'Template_Name')
	return workbookName;

#This main function formats the workbook template from .twbx to .zip to then uncompressed and breaks it into a XML file
#and two more folders, one for data and the other for images)
def main():
	parser = ConfigParser(allow_no_value=True)
	with codecs.open('config.ini', 'r', encoding='utf-8') as f:
		parser.read_file(f)
	#parser.read('config.ini')
	workbookName = getWorkbookName(parser)
	temporaryFolder = 'File_2'
	os.chdir('.')
	os.mkdir(temporaryFolder)
	shutil.copy('./' + workbookName + '.twbx', './' + temporaryFolder)
	os.chdir('./' + temporaryFolder)
	prevName = workbookName + '.twbx'
	newName = workbookName + '.zip'
	os.rename(prevName, newName)

	shutil.unpack_archive(workbookName + '.zip', extract_dir='../', format='zip')

main()

