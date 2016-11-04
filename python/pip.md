If you are uncomfortable with git and familiar with pip install our pip package and starting 
playing right away.

On your terminal<br>
<code>sudo pip install CSV-anomaly-detector==1.2.17</code><br>
(Right now 1.2.17 is the stable version. When upgraded, changes will be reflected here).<br>

Go to any directory that contains that has a .csv file (say sample.csv) and start using the tool. 

Following commands are available in the tool :<br>
<b>columns</b> --> prints the headers of the csv file.<br>
<b>count</b> --> gives the total number of rows in the csv file.<br>
<b>executeColumns</b> --> scan the particular (mentioned) column to find out bugs.<br>
<b>execute</b> --> scan the whole file (i.e all columns) to spot bugs.<br>
<b>sample</b> --> prints the first 10 rows of the csv file.<br>
<b>sampleHeader</b>--> prints the first 10 rows, but only that of the (mentioned) header.<br>

Sample command prompt execution for each of the above commands<br>
<code>AnomalyDetector columns --filename=mock.csv </code><br>
<code>AnomalyDetector count --filename=mock.csv</code><br>
<code>AnomalyDetector executeColumns --filename=mock.csv --columns=email</code><br>
<code>AnomalyDetector execute --filename=mock.csv </code><br>
<code>AnomalyDetector sample --filename=mock.csv </code><br>
<code>AnomalyDetector sampleHeader --column=email --filename=mock.csv</code><br>