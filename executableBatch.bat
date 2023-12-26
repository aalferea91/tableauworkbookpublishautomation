@echo off
REM This command is used to execute the python file.
python uncompressor.py 
REM This command is used to execute the python file.
python countryWorkbookGenerator.py 
REM This command is used to switch from one directory to another.
cd .\File_1 
REM This command allow the generation of new empty subfolders, sharing same names with all .twb files. 
forfiles /m *.twb /c "cmd /c md @FNAME
REM This command allow the reallocation of each workbook (in twb format) within the folder that share its same name.  
forfiles /m *.twb /c "cmd /c xcopy ..\File_1\@FNAME.twb ..\File_1\@FNAME 
REM This command allow the adding of the "Data" folder within each subfolder. 
forfiles /m *.twb /c "cmd /c xcopy /s /i /y "..\Data" "..\File_1\@FNAME\Data" 
REM This command allow the adding of the "Image" folder within each subfolder. 
forfiles /m *.twb /c "cmd /c xcopy /s /i /y "..\Image" "..\File_1\@FNAME\Image" 
REM This command allow the adding of the "TwbxExternalCache" folder within each subfolder.
forfiles /m *.twb /c "cmd /c xcopy /s /i /y "..\TwbxExternalCache" "..\File_1\@FNAME\TwbxExternalCache"
REM This command is used to zip those folders containing Workbook, Data, Image and TwbxExternalCache folders. 
forfiles /m *.twb /c "cmd /c 7z a -tzip ..\File_1\@FNAME.zip ..\File_1\@FNAME\* 
REM This command is used to switch from a .zip format to a .twbx format.
forfiles /m *.zip /c "cmd /c move @FNAME.zip @FNAME.twbx
REM This command allow the cleansing of extra folders that won´t be used anymore. 
forfiles /m *.twb /c "cmd /c RD /S /Q ..\File_1\@FNAME
REM This command allow the cleansing of extra .twb files that won´t be used anymore. 
forfiles /m *.twb /c "cmd /c Del @FILE
REM This command is used to switch from one directory to another. 
cd ..\ 
REM This command is used to delete Data folder, not needed anymore.
rd /s /q Data 
REM This command is used to delete File_2 folder (temporary folder), not needed anymore.
rd /s /q File_2 
REM This command is used to delete Image folder, not needed anymore.
rd /s /q Image 
REM This command is used to delete TwbxExternalCache folder, not needed anymore.
rd /s /q TwbxExternalCache 
REM This command is used to delete Template file in its .twb format, once it has served its purpose
del /q CME_Template_20181112.twb 
REM This command is used to proceed with the log in once all workbooks are created and ready to be uploaded to the server
REM tabcmd login -s https://tableau.tst.gydatalake.cloud -u typeusername -p typepassword
REM This command is used to switch from one directory to another. 
cd .\File_1 


