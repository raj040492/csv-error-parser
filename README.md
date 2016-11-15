# csv-error-parser
Scans your csv file and looks for errors

To test your csv file 
	1.clone the repo 
	2.cd nodejs 
		(i)Please copy your .csv file to this folder
		(ii) Your csv file and AnomalyFinder.js must always be in the same directory.
	3. To test your file
		(i) Open terminal
		(ii) Navigate to the respective directory
		(iii) To scan whole File:
			Run node AnomalyFinder.js <filename>
		(iv) To scan a specific column in the .csv file
			Run node AnomalyFinder.js <fileName> <columnName>
