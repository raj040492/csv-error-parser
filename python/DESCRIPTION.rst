CSV-anamoly-detector :
	A tool to detect anamolies in CSV files (especially large files)

Description of the tool :

	This tool is handy if you are working with a large csv file wherein scanning each
	line for anamolies is a daunting task. Even if the file is received from a reliable
	source it is always safe to verify the veracity of the file before proceeding further.

	Each column has a title, all of which will be mentioned in the very first line of any 
	csv file which we shall refer as "HEADER" throughout this page.

	The tool takes a header-wise scanning approach.After scanning each Header, the dominant
	datatype is identified and any another datatype is assumed ("we are not concluding 
	because the final decision rests with the user") to be defective. 

	Datatypes described in the tool are so exhaustive that even what plain eye may miss 
	will be detected by the tool.
	Ex.R0HAN is different from ROHAN (notice zero instead of 'o' in the first case.)


Command line execution:

	Let us assume that we have a file named mock.csv & our source code is in automation.py
	
	To view the headers of the file:	
		python automation.py columns --filename=mock.csv

	We will be shown the following result:
		['id', 'first_name', 'last_name', 'email', 'country', 'ip_address']
	where each element of the above array is a header
	
	To find out the anamolies in each header (say email) :
		python automation.py executeColumns --filename=mock.csv --columns=email

	Upon completion of the scanning process, you will see either of these two responses:
	1) This Column appears bug free.
	2) PLEASE OPEN improperData.txt (this file contains all the error prone entries)

	To know the commands available:
		python automation.py --help

	Please "avoid" spacing in the following areas:
		--filename = mock.csv (will throw error)
		--filename= mock.csv (will throw error)
		--filename =mock.csv(will throw error)
		--filename=mock.csv (will give result)

		The above set of rules also apply for --columns
