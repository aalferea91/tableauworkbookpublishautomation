# tableauworkbookpublishautomation

### Context:
There is a necessity of developing one dashboard for each country. Each of these dashboards will have the same kind of information but tailored to the data of each specific country. The features of all of the dashboards are the same, therefore it didn´t make sense to manually create a dashboard for each country, because also when a bug is detected or when a new feature needs to be added the developer would have to replicate that change for each of the different dashboards. 

In this case we decided that the solution to be applied would be to create a general dashboard that has a country parameter and depending on the value of that parameter the dashboard would be fit to a specific country. That parameter will be also used in a python script in order to roll any change made to the generic dashboard into all the different dashboards for the countries.

We have not only a dashboard for each country but also a published datasource for each country.
This is the script used to publish those workbooks.

The Project is composed of the following files:

-**Template.twbx**: template of the Tableau datasource. This file is not available in this repository for confidentiality purposes.

-**config.ini**: text file where to input the different configuration parameters of our architecture such as Tableau Server URL, Tableau token credentials for being able to publish it from the command line, etc.

-**Main.py**: reads the configuration file, modifies the file ‘executableBatch.bat’ and executes it in a bash terminal .

-**executableBatch.bat**: bash file that executes ‘uncompressor.py’ and ‘countryWorkbookGenerator.py’, and also uses tabcmd to publish to Tableau Cloud.

-**uncompressor.py**: compress and unzips the Template. This has to be done for the XML code of the file to be updated with the new file name. A simple renaming operation wouldn’t work so this step has to be done.

-**countryWorkbookGenerator.py**: code that will edit the XML code of the Template.tdsx in order to change the country parameter and will create a different tdsx file for each country listed in the configuration file (config.ini). The results for the workbooks will be saved into the folder File_1.

### Requirements:

-Have python installed. We use Python 3.8.2

-Have tabcmd installed. We use tabcmd 2.0.11

### Quick Guide:
To adapt the script for your specific needs you will have to:

-Open the twbx you want to publish and save it as the name of the template given in the config file. If you rename the workbook without opening it and save it as the new name it won´t work because Tableau won’t change the name in the XML file.

-Edit the file config.ini

-Edit the file countryWorkbookGenerator.py: review the code for the functions main() and createCountryWorkbook() to see what of the different steps are needed for your use case. All the transformations needed in the workbook will require to change the underlaying XML code, for example the function countryDatasourceProcessing is tailored to our specific data sources, yours might differ.

-Execute main()
