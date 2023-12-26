import sys, datetime, xml.etree.cElementTree as ET, codecs
from configparser import ConfigParser


#This function gets the Template name from the config file.
def getWorkbookName(parser):
	workbookName = parser.get('Template Name', 'Template_Name')
	return workbookName;


#This function reads the chosen prefix, to identify and name all workbooks.  This is taken
# from the config file.
def getProjectPrefix(parser):
	projectPrefix = parser.get('Project_prefix', 'Project_prefix')
	return projectPrefix;


#This function returns the XML tree, which is the structure of the Workbook´s Template.
def getTree(xmlName):
	tree = ET.ElementTree(file=xmlName)
	return tree;


#This function returns the root from the tree.
def getRoot(tree):
	root = tree.getroot()
	return root;


#This function returns data sources from the tree.
def getDatasources(root):
	datasources = root.find("datasources")
	return datasources;


#This function returns dashboards from the tree.
def getDashboards(root):
	dashboards = root.find("dashboards")
	return dashboards;


#This function returns actions from the tree.
def getActions(root):
	actions = root.find("actions")
	return actions;



#This function returns shared-views from the tree.
def getSharedViews(root):
	sharedViews = root.find("shared-views")
	return sharedViews;


#This function collects the parameter´s section comprised within data sources.
def getParameterList(root):
	datasources = getDatasources(root)
	for datasource in datasources:
		if datasource.get("name") == "Parameters":
			return datasource;

#This function returns the list of countries we are creating. This is read from the
# config file.
def getListOfCountries(parser):
	listOfCountries = parser.options('Python List Of Countries')
	for i in range(len(listOfCountries)):
		listOfCountries[i] = listOfCountries[i].upper()
	return listOfCountries;

#This function returns the nuts1-nuts2-nuts3 naming for each country. This is read from the
# config file.
def getConfigurationList(parser):
    configurationList = parser.options('Geoconfiguration')
    for i in range(len(configurationList)):
        configurationList[i] = configurationList[i].lower()
    return configurationList

#This function returns a general dictionary that will contain all the parameters set for each country in terms of
#Season mix, brand Tier as well as the project where each workbook will be located. This general dictionary will comprise as much
#sub dictionaries as countries were listed.
def getGeneralDictionary(countries ,configurationList, parser):
    generalDictionary = {}
    for country in countries:
        parameterListByCountry = parser[country]
        parameterList = {}
        for j in parameterListByCountry:
            parameterName = j
            if parameterName in configurationList:
                parameterValue = parameterListByCountry[j]
                parameterList[parameterName] = parameterValue
            generalDictionary[country] = parameterList
    return generalDictionary


#This function delimits names for both embedded data sources and published data sources that will be used to feed each
# country´s workbook.
def datasourcesProcessing(datasources, country):
	for i in datasources:
		if i.get("caption") == "Geomarketing":
			datasourceAlias = "Geomarketing_" + country
			repositorylocation = i[0]
			repositorylocation.set("id", datasourceAlias)
			connection = i[1]
			connection.set("dbname", datasourceAlias)
			connection.set("server-ds-friendly-name", datasourceAlias)
		elif i.get("caption") == "Geomarketing_Panel":
			datasourceAlias = "Geomarketing_Panel_" + country
			repositorylocation = i[0]
			repositorylocation.set("id", datasourceAlias)
			connection = i[1]
			connection.set("dbname", datasourceAlias)
			connection.set("server-ds-friendly-name", datasourceAlias)
		elif i.get("caption") == "Geomarketing_POS":
			datasourceAlias = "Geomarketing_POS_" + country
			repositorylocation = i[0]
			repositorylocation.set("id", datasourceAlias)
			connection = i[1]
			connection.set("dbname", datasourceAlias)
			connection.set("server-ds-friendly-name", datasourceAlias)
		if i.get("caption") == "Geomarketing_countryview":
			datasourceAlias = "Geomarketing_countryview_" + country
			repositorylocation = i[0]
			repositorylocation.set("id", datasourceAlias)
			connection = i[1]
			connection.set("dbname", datasourceAlias)
			connection.set("server-ds-friendly-name", datasourceAlias)
	return;

#This function aims to set specified parameters for each country´s workbook. These parameters are read from the config
#file.
def setParameter(country , parameters, generalDictionary,configurationList):
	for i in range(len(parameters)):
		parameter = parameters[i]
		if str(parameter.get("caption")).lower() == "countrycode":
			parameter.set("value", '"' + country + '"')
			parameter[0].set("formula", '"' + country + '"')
		if str(parameter.get("caption")).lower() == "map level":
			for i in range(4):
				for dictionaryKey in generalDictionary:
					if dictionaryKey == country:
						mini_dictionary = generalDictionary[dictionaryKey]
						parameter.set("alias", mini_dictionary[configurationList[2]])
						parameter[1][i].set("value", mini_dictionary[configurationList[i]])
						if i==2:
							parameter[2][3].set("alias", mini_dictionary[configurationList[i]])
						if i==3:
							parameter[2][2].set("alias", mini_dictionary[configurationList[i]])
						else:
							parameter[2][i].set("alias", mini_dictionary[configurationList[i]])
			if country in ("BG","CY","DK","EE","GB","HR","IE","IS","LV","MK","NL","NO","PT","SE","SI"):
				child1 = parameter[1][0]
				parameter[1].remove(child1)
				child2 = parameter[2][0]
				parameter[2].remove(child2)
				child11 = parameter[1][2]
				parameter[1].remove(child11)
				child22 = parameter[2][1]
				parameter[2].remove(child22)

			if country in ("ME"):
				child11 = parameter[1][2]
				parameter[1].remove(child11)
				child22 = parameter[2][1]
				parameter[2].remove(child22)
				child1 = parameter[1][0]
				parameter[1].remove(child1)
				child2 = parameter[2][0]
				parameter[2].remove(child2)
				parameter.set("value", "4")
			if country in ("AL","AT","BA","BE","CH","CZ","DE","FI","FR","HU","IT","LT","LU","RS","SK"):
				child1 = parameter[1][3]
				parameter[1].remove(child1)
				child2 = parameter[2][2]
				parameter[2].remove(child2)
			for dictionaryKey in generalDictionary:
				if dictionaryKey == country:
					mini_dictionary = generalDictionary[dictionaryKey]
					parameter.set("alias", mini_dictionary[configurationList[1]])
				#x = 3
				#j = len(parameter[1])
				#while x < j:

				#	j = j - 1
				#x1 = 3
				#k = len(parameter[2])
				#while x1 < k:
				#	child = parameter[2][x1]
				#	parameter[2].remove(child)
				#	k = k - 1



	return;


#This function sets which Snowflake Server will be used to feed workbooks.
def snowflakeServerSelector(datasource, parser):
    databaseserver = parser.get('Snowflake Server Selection','Snowflake_Server_Lowercase')
    i = datasource
    if i[0].tag == 'connection' and 'federated' in i[0].get('class'):
        j = i[0]
        if j[0].tag == 'named-connections':
            h = j[0]
            if h[0].tag == 'named-connection':
                e = h[0]
                if e[0].tag == 'connection' and 'goodyear-emea_analytics.snowflakecomputing.com' in str(e[0].get('server')):
                    p = e[0]
                    p.set('server',databaseserver)


#This function sets the location of those datasources used in live mode
def serverDataSourcesLive(datasources, parser):
	livedatasourceslocation = parser.get('Live Data Sources url','Live_Data_Sources_Url')
	for i in datasources:
		if 'sqlproxy' in str(i.get('name')) and 'https' in str(i[1].get('channel'))\
				and 'sqlproxy' in str(i[1].get('class')):
			q = i[1]
			q.set('server',livedatasourceslocation)
	return


#This function creates workbooks for each country listed within the config file.
def createWorkbook(country, tree, projectPrefix):
	outFileName = 'File_1/' + projectPrefix + '_' + country + '.twb'
	outFile = open(outFileName, 'wb')
	tree.write(outFile)
	print("Created " + outFileName)
	return;


#This function gathers all functions displayed up to this point, following a proper execution order, for it to be
#called by the Main function.
def createCountryWorkbook(countries, now, parser, projectPrefix,  workbook, configurationList):
	for country in countries:

		tree = getTree(workbook)
		root = getRoot(tree)
		datasources = getDatasources(root)
		parameters = getParameterList(root)
		snowflakeServerSelector(datasources, parser)
		serverDataSourcesLive(datasources, parser)
		generalDictionary = getGeneralDictionary(countries, configurationList, parser)
		datasourcesProcessing(datasources, country)
		setParameter(country, parameters, generalDictionary, configurationList)
		sharedViews = getSharedViews(root)
		actions = getActions(root)
		dashboards = getDashboards(root)
		createWorkbook(country, tree, projectPrefix)
		#print(generalDictionary)


#This main function calls and executes all the above function, creating as much workbooks as countries are listed with
# their corresponding parameters and specifications.
def main():
	parser = ConfigParser(allow_no_value=True)
	with codecs.open('config.ini', 'r', encoding='utf-8') as f:
		parser.read_file(f)
	ET.register_namespace('user', "http://www.tableausoftware.com/xml/user")
	countries = getListOfCountries(parser)
	workbookName = getWorkbookName(parser)
	projectPrefix = getProjectPrefix(parser)
	configurationList = getConfigurationList(parser)
	workbook = workbookName + ".twb"
	now = datetime.datetime.now()

	createCountryWorkbook(countries, now, parser, projectPrefix,  workbook, configurationList)


main()
