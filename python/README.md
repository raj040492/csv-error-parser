<h1>CSV-anomaly-detector </h1>
A tool to detect anomalies in CSV files (especially large files)

<h2> Description </h2>

This tool is handy if you are working with a large csv file wherein scanning each
line for anomalies is a daunting task. Even if the file is received from a reliable
source it is always safe to verify the veracity of the file before proceeding further.

Each column has a title, all of which will be mentioned in the very first line of any 
csv file which we shall refer as "HEADER" throughout this page.

The tool takes a header-wise scanning approach.After scanning each Header, the dominant
datatype is identified and any another datatype is assumed ("we are not concluding 
because the final decision rests with the user") to be defective. 

<h2> Command line execution </h2>

Following commands are available in the tool :

<b>columns</b> --> prints the headers of the csv file.<br>
<b>count</b> --> gives the total number of rows in the csv file.<br>
<b>executeColumns</b> --> scan the particular (mentioned) column to find out bugs.<br>
<b>execute</b> --> scan the whole file (i.e all columns) to spot bugs.<br>
<b>sample</b> --> prints the first 10 rows of the csv file.<br>
<b>sampleHeader</b>--> prints the first 10 rows, but only that of the (mentioned) header.<br>


Sample command prompt execution for each of the above commands

<code>python AnomalyDetector.py columns --filename=mock.csv </code><br>
<code>python AnomalyDetector.py count --filename=mock.csv</code><br>
<code>python AnomalyDetector.py executeColumns --filename=mock.csv --columns=email</code><br>
<code>python AnomalyDetector.py execute --filename=mock.csv </code><br>
<code>python AnomalyDetector.py sample --filename=mock.csv </code><br>
<code>python AnomalyDetector.py sampleHeader --column=email --filename=mock.csv</code><br>



Upon completion of the scanning process (either execute/executeColumns), you will see either 
of these two responses:
<li>This Column appears bug free.</li>
<li>PLEASE OPEN improperData.txt**</li>

To view the commands available:<br>
<code> python AnomalyDetector.py --help </code>

Please "avoid" spacing in the following areas:<br>
<code>--filename = mock.csv </code>(will throw error)<br>
<code>--filename= mock.csv</code>(will throw error)<br>
<code>--filename =mock.csv</code>(will throw error)<br>
<code>--filename=mock.csv</code>(will give result)<br>

All entries are case sensitive<br>
** improperData.txt contains all errors. It will be created automatically when .py
file is executed.<br>

<h5> Please ensure that the source file (AnomalyDetector.py) and the .csv file are in the 
same directory. </h5>

<h3> Note: </h3>
<li>If you are using compound words (more than a word ex. first name), please make sure 
it is enclosed inside quotes.</li>
<code>python AnomalyDetector.py executeColumns --filename=mock.csv --columns=first name</code>
(WON'T WORK)<br>
<code>python AnomalyDetector.py executeColumns --filename=mock.csv --columns="first name"</code>
(WORKS LIKE A CHARM)<br>
<li>Relative addressing from the terminal also works:</li> 
<code>python AnomalyDetector.py execute --filename="./Verticals/sample.csv"</code>
