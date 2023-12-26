import subprocess
from configparser import ConfigParser
import datetime
import codecs
import shutil,os
import time

#This function gets the Tableau Server url from the config file.
def getUrl(parser):
	tableauServerUrl = parser.get('Tableau Server url', 'Tableau_Server_Url')
	return tableauServerUrl;

def getSite(parser):
	tableauSite = parser.get('Tableau Site', 'Tableau_Site')
	return tableauSite;

#This function gets the name of the main python script from the config file.
def getScriptName(parser):
	scriptName = parser.get('Script Name', 'Script_Name')
	return scriptName;

#This function gets the Template name from the config file.
def getTemplateName(parser):
	templateName = parser.get('Template Name', 'Template_Name')
	return templateName;

#This function gets the Tableau Token Name that will be used to publish in the server. This is taken from the
# config file
def getTableauTokenName(parser):
	tableauTokenName = parser.get('Tableau Token Name', 'Tableau_token_name')
	return tableauTokenName;

#This function gets the Token value corresponing to the token name, which is used to publish in the server. This is taken
# from the config file
def getTableauTokenValue(parser):
	tableauTokenValue = parser.get('Tableau Token Value', 'Tableau_token_value')
	return tableauTokenValue;

#This function gets the name of the project within will be published correspponding workbooks.
def getTableauServerProject(parser):
	tableauServerProject = parser.get('Tableau Server Project', 'Tableau_server_project')
	return tableauServerProject;

#This function gets the Tableau server site specified in the config file, wheteher is needed one different
# from 'Default'
def getTableauServerSite(parser):
	tableauServerSite = parser.get('Tableau Server Site', 'Tableau_server_site')
	return tableauServerSite;

#This function helps to confirm if the user wants to publish generated dashboard on separated folders or not.
def getSeparateFoldersConfirmation(parser):
	separateFolderConfirmation = parser.get('Separate_folders_confirmation', 'Confirm_if_separate_folders_is_required')
	return separateFolderConfirmation;

#This function gets the prefix that is chosen to identify and name the workbooks. This is taken
# from the config file
def getProjectPrefix(parser):
	projectPrefix = parser.get('Project_prefix', 'Project_prefix')
	return projectPrefix;


#This function gets the name of the data base used to feed the tableau server. This is taken from the config file
def getDataBaseUserName(parser):
	tableauDbUsername = parser.get('Tableau Database Username', 'Tableau_Db_Username')
	return tableauDbUsername;

#This function gets the password of the data base previously specified .
def getDataBasePassword(parser):
	tableauDbPassword = parser.get('Tableau Database Password', 'Tableau_Db_password')
	return tableauDbPassword;

#This function gets all country codes listed within the config file.
def getListOfCountries(parser):
	listOfCountries = parser.options('Python List Of Countries')
	return listOfCountries;

#This function allos us to confirm whether the user wants to publish workbooks adding the suffix 20181005 or not
def getProjectSuffixConfirmation(parser):
	projectSuffixConfirmation = parser.get('Project Suffix Confirmation 20181005','Project_Suffix_Confirmation_20181005')
	return projectSuffixConfirmation;

#This main function calls, executes and cordinates functions as them are requiered whenever they are needed.
# It can be broken down into three sections: A first block which is in charge of calling all the above function in
# a specific order; following by a second section meant to read code-lines from the batch file, which
# contains commands for generating and publishing workbooks, and finally a third block for creating a temporary
# batch file which has been customized depending on the given parameters in the config file. This temporary file,
# will be executed and afterwards it will be deleted in order to have a clean folder.
def main ():

	# First Block: Calling functions

	batchFileName = 'executableBatch'
	temporaryFolder = 'File_3'
	parser = ConfigParser(allow_no_value=True)
	with codecs.open('config.ini', 'r', encoding='utf-8') as f:
		parser.read_file(f)
	#parser.read('config.ini')
	tableauServerUrl = getUrl(parser)
	tableauSite = getSite(parser)
	scriptName = getScriptName(parser)
	templateName = getTemplateName(parser)
	tableauTokenName = getTableauTokenName(parser)
	tableauTokenValue = getTableauTokenValue(parser)
	tableauServerProject = getTableauServerProject(parser)
	tableauServerSite = getTableauServerSite(parser)
	separateFolderConfirmation = getSeparateFoldersConfirmation(parser)
	projectPrefix = getProjectPrefix(parser)
	projectSuffixConfirmation = getProjectSuffixConfirmation(parser)
	tableauDbUsername = getDataBaseUserName(parser)
#% is a special character so in order to make it literal we have to duplicate it in the following line with the replace function
	tableauDbPassword = getDataBasePassword(parser).replace('%','%%')
	listOfCountries = getListOfCountries(parser)
	now = datetime.datetime.now()
	folder = str(now.year) + str(now.month) + str(now.day)


	for i in range(len(listOfCountries)):
		listOfCountries[i] = listOfCountries[i].upper()

	# Second Block: Reading the batch file and customizing as it is specified in the config file

	f = open(batchFileName + '.bat', 'r')

	lines = f.readlines()

	lines[4] = 'python ' + scriptName + '.py\n'
	lines[36] = 'del /q ' + templateName + '.twb\n'
	lines[38] = 'tabcmd login -s ' + tableauServerUrl + ' -t ' + tableauSite + ' --token-name ' + tableauTokenName + ' --token-value ' + tableauTokenValue + '\n'
	lines[40] = 'cd .\File_1' + '\n'

	subfolder = 'Geomarketing'
	# for country in listOfCountries:
	# 	lines.append(
	# 		'tabcmd publish ' + projectPrefix + '_' + country + '.twbx' + ' -s ' + tableauServerUrl + ' -u ' +
	# 		tableauUserId + ' -p ' + tableauUserPassword + ' -r ' + tableauServerProject + '\" '
	# 										'--tabbed -o --db-username \"' + tableauDbUsername + '\" --db-password \"' +
	# 		tableauDbPassword + '\" --save-db-password\n')
	# 	lines.append(
	# 		'tabcmd refreshextracts --workbook  ' + ' -r ' + projectPrefix + '_' + country + ' -s ' +
	# 		tableauServerUrl + ' -u ' + tableauUserId + ' -p ' + tableauUserPassword + '\n' )
	for country in listOfCountries:
		lines.append(
			'tabcmd publish ' + projectPrefix + '_' + country + '.twbx' + ' -s ' + tableauServerUrl + ' -t ' + tableauSite
			+ ' --token-name ' + tableauTokenName + ' --token-value ' + tableauTokenValue + ' -r ' + country + ' --parent-project-path '
			+ tableauServerProject + ' -o --tabbed --db-username \"' +
			tableauDbUsername + '\" --db-password \"' + tableauDbPassword + '\" --save-db-password\n')
		print((
			'tabcmd publish ' + projectPrefix + '_' + country + '.twbx' + ' -s ' + tableauServerUrl + ' -t ' + tableauSite
			+ ' --token-name ' + tableauTokenName + ' --token-value ' + tableauTokenValue + ' -r ' + country + ' --parent-project-path '
			+ tableauServerProject + ' -o --tabbed --db-username \"' +
			tableauDbUsername + '\" --db-password \"' + tableauDbPassword + '\" --save-db-password\n'))
		lines.append(
			'tabcmd refreshextracts --parent-project-path ' + tableauServerProject +' --project '
			+ country + ' --workbook  ' + projectPrefix + '_' + country + ' -s ' +
			tableauServerUrl+ ' -t ' + tableauSite + ' --token-name ' + tableauTokenName + ' --token-value ' + tableauTokenValue + '\n' )
	f.close()

	# Third Block: Creating a temporary batch for code-execution and then deleting for cleaning the folder

	os.mkdir(temporaryFolder)
	shutil.copy(batchFileName + '.bat', './' + temporaryFolder)

	os.chdir('./' + temporaryFolder)

	prevName = batchFileName + '.bat'
	newName = batchFileName + '_Temporary.bat'
	os.rename(prevName, newName)

	shutil.copy(newName, '../')

	os.chdir('../')
	shutil.rmtree('./' + temporaryFolder)

	f = open(newName, 'w')
	f.writelines(lines)
	f.close()

	f = open(newName, 'a')
	f.write('tabcmd logout\n')
	f.close()

	subprocess.call(newName, shell=True)

	os.remove(newName)

main()
