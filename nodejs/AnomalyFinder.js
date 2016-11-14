// TODO unistall pubnub-rickshaw-memory if not needed
// TODO look into pure_string and whether its needed

var fs = require('fs'),
	parse = require('csv-parse'),
	config = require("./config.js"),
	// pnrickmem = require('pubnub-rickshaw-memory'),
	threshold_percentage = 0,
	header = '',
	targetColumnArray = [],
	fileSize,
	possible_anamoly = [],
	current_column = '',
	allColumnScan = false, // this variable is used to decide when to trigger storing of performance details
	rowCountArray = [],
	rowCount = 0,
	total_rows = 0,
	details = getDetailsObject(),
	indexNumber,
	start = Date.now(),
	end,
	timeTaken,
	fileName  = process.argv[2],
	columnName  = process.argv[3];

if(fileName && columnName) {
	read_file(fileName,columnName);
}
else {
	if(fileName && columnName == undefined) {
		allColumnScan = true;
		read_file(fileName,"ALL");
	}
	else if(fileName == undefined && columnName == undefined) {
		console.log("Please enter the filename that you wish to scan \n ex: node <filename> <columnName> \n <columnName> is optional")
		process.exit(0);
	}
}
function getDetailsObject(){
	return {		
		"uppercase_entries" : {},
		"string" : {},
		"integer" : {},
		"pure_integer" : {},
		"pure_string" : {},
		"email" : {},
		"state_codes" : {},
		"states" : {},
		"special_characters" : {},
		"zip_code" : {}
	}	
}
function fileSizeInMegabytes(filename) {
	var stats = fs.statSync(filename),
		fileSizeInBytes = stats["size"],
 		fileSizeInMegabytes = fileSizeInBytes / 1000000.0 ; //Convert the file size to megabytes 
	return fileSizeInMegabytes
}
function read_file (fileName,columnName){
	fileSize = fileSizeInMegabytes(fileName);
	fs.createReadStream(fileName)
		.on('error',function(err){
			if (err["code"] == "ENOENT") { // various errors could be thrown; only if error code is "ENOENT", do we conclude that, it's a missing file or directory scenario..
				console.log("File "+ fileName + " doesnt exist \nEnsure if the file is in the same directory \nLook for typo errors")	
				process.exit(0);
			}
			else {
				console.log(err)
			}			
		})
		.pipe(parse({
				delimiter : ','
			}))		
		.on('data',function(rows){	// reads csv, row wise
			total_rows +=1;
			create_column(rows,columnName);
		})
		.on('end',function(){
			start_process(columnName,fileName)
		})
}
function create_column(rows,columnName) {
	// given header name this function creates an array that contains all entries under that header
	// ex: if columnName is "id" all entries in csv file under id (1,2,3,4,....100) will be pushed inside an array
	// said array will scanned and tested subsequently..
	// if incorrect columnName is fed, the process terminates...	
	rowCount +=1;
	if(rowCount == 1) { // the first row of any csv contains heading for each column
		header = rows;
		if (columnName == "ALL") {
			// array inside array for each columns 
			// for single column scan, a simple array would do, no need to create child arrays
			// such new array initialization must happen only once  N only when ALL columns are to scanned			
			var len = rows.length // to improve execution speed;
			for(var i=0;i<len;i++) {
				targetColumnArray[i] = new Array();
			}
		}
	}
	if(rows.indexOf(columnName)>=0) {			
		indexNumber = rows.indexOf(columnName);								
	}
	if (columnName == "ALL") {
		var len = rows.length // to improve execution speed;
		for(var i=0;i<len;i++) {
			targetColumnArray[i].push(rows[i])
		}
	}
	if(columnName != "ALL") {
		if(indexNumber == undefined){ // indexNumber remains undefined only if the columnName chosen doesnt exist in 
			return "column_doesnt_exist" // the first line of the csv file.
			process.exit(0)
		}		
		else {			
			if(targetColumnArray.indexOf(rows[indexNumber]) == -1) {
				targetColumnArray.push(rows[indexNumber]);	
			}			
			return "column exists"
		}		
	}
}
function analyse_column(targetEntry,columnName) {	
	var cleaned_column_length = targetEntry.length; // to improve execution speed;
	targetEntry.map(function(actualEntry,innerArrayIterationCount,innerArray){
		if(innerArrayIterationCount == 0) {
			columnName = targetEntry[0]
		}
		if(innerArrayIterationCount != 0) { // we dont want to classify the header line ; i.e the first line of csv file.
			classify(actualEntry,columnName,targetEntry);			
		}
		if(innerArrayIterationCount == cleaned_column_length-1) {
			analyse(details,cleaned_column_length-1,columnName,targetEntry)
		}
	})
}
function start_process(columnName,fileName) {
	var targetColumnArray_length = targetColumnArray.length
	targetColumnArray.map(function(targetEntry,iterationCount,array){
		if(targetEntry.constructor === Array) { // when ALL columns are scanned this condition will satisfy because			
			analyse_column(remove_duplicate(targetEntry),columnName) // in this case, targetColumnArray is an array of 
		} // arrays, else it's an array of entries...
		else {
			if(targetEntry != columnName) { // we dont want to classify the header line ; i.e the first line of csv file.
				classify(targetEntry,columnName);
			}
			if(iterationCount == targetColumnArray_length-1) {
				analyse(details,targetColumnArray_length-1,columnName)
			}
		}
	})	
}
function classify(param,columnName,arrayFullScan) {
	// a broad wing is created in the first level in which the following will be invoked
	// if one of the following functions is satisfied by the param, then we go a layer deep i.e if param satisfies string, 
	// we then check for uppercase and pure string scenario in other words it doesnt make much sense to put a param thru 
	// string and again thru uppercase when its clear from the first test(string) that it's not a string
	if(columnName != current_column) {
		// while scanning the whole file, the flows goes from one column to another; thus when a switch happens from one 
		// column to another, we must reset the details object else the object will contain data from previous column.. 
		// reset happens in getDetailsObject();
		current_column = columnName
		rowCountArray = []; //after each column switch
		details = getDetailsObject();
	}
	string(details,param,columnName,arrayFullScan)
	integer(details,param,columnName,arrayFullScan)
	email(details,param,columnName,arrayFullScan)
	special_characters(details,param,columnName,arrayFullScan)
	return "classified"
}
function analyse(details,len,columnName) {
	not_anamoly = [];
	possible_anamoly = [];
	var details_key_length = Object.keys(details).length;
	Object.keys(details).map(function(key,iterationCount,array){
		threshold_percentage = (Object.keys(details[key]).length/len)*100;
		// after scanning each column, we have an object (details) that comprises of multiple datatypes; each datatype has a 
		// percentange of occurence (can vary from 0-100%) ;if this percentage is lesser than the threshold_percentage 
		//(decided in config.js) then we decide that particular datatype and associated entries to be anamolous.
		if(threshold_percentage < config.threshold_percentage && threshold_percentage >0 && possible_anamoly.indexOf(key) == -1) {
			possible_anamoly.push(key);
		}
		else if(threshold_percentage > config.threshold_percentage && not_anamoly.indexOf(key) == -1) {
			not_anamoly.push(key);
		}
		if(iterationCount == details_key_length-1) {
			manage_exceptions(not_anamoly,columnName);			
		}
	})
}
function manage_exceptions(not_anamoly,columnName) {
	possible_anamoly.map(function(anamolous_datatype){
		if(config.never_together[anamolous_datatype] != undefined && common_array_entries(not_anamoly,config.never_together[anamolous_datatype]) == false) {
			not_anamoly.map(function(non_anamolous_datatype){
				if(config.exceptions[anamolous_datatype] && config.exceptions[anamolous_datatype].indexOf(non_anamolous_datatype)>=0) {
					var index = possible_anamoly.indexOf(anamolous_datatype)
					possible_anamoly.splice(index,1);
				}
			});
		}
		else if(config.never_together[anamolous_datatype] == undefined) {
			not_anamoly.map(function(non_anamolous_datatype){
				if(config.exceptions[anamolous_datatype] && config.exceptions[anamolous_datatype].indexOf(non_anamolous_datatype)>=0) {
					var index = possible_anamoly.indexOf(anamolous_datatype)
					possible_anamoly.splice(index,1);
				}
			});
		}
		not_anamoly.map(function(non_anamolous_datatype){	
			if(config.exceptions[anamolous_datatype] && config.exceptions[anamolous_datatype].indexOf(non_anamolous_datatype)>=0) {
				var index = possible_anamoly.indexOf(anamolous_datatype)
				possible_anamoly.splice(index,1);
			}
		});
	});
	show_results(columnName)	
}
function show_results(columnName){
	if(possible_anamoly.length >0) {
		var possible_anamoly_length = possible_anamoly.length;
		possible_anamoly.map(function(datatype,anamolyIterationCount,possibleAnamolyArray){
			Object.keys(details[datatype]).map(function(key){
				console.log("\x1b[31m","Entry " + key + " at row number " + details[datatype][key]["rowCount"] + " in column "+ columnName +" is out of place; because it contains datatype " + datatype + "" ,"\x1b[0m");
			});	
			if(anamolyIterationCount == possible_anamoly_length-1){
				store_performance_details_trigger(timeTaken,allColumnScan,columnName);
			}
		});
		
	}
	else {
		console.log("\x1b[32m","Column " + columnName + " appears to be clean","\x1b[0m");
		store_performance_details_trigger(timeTaken,allColumnScan,columnName);
		return "clean_column"
	}
}
function store_performance_details_trigger(timeTaken,allColumnScan,columnName){
	end = Date.now();
	timeTaken = (end-start)/1000;
	if(allColumnScan == true && header.indexOf(columnName) == header.length-1) { // When all Columns are Scanned the 		
		store_performance_details(timeTaken,header.length,targetColumnArray) //performance function should be invoked only 
	} // after the last column is scanned; thus the if loop;
	else if(allColumnScan == false){ // when single column is scanned no of columns scanned should be registered as "1"
		store_performance_details(timeTaken,1,targetColumnArray)
	}
}
function store_performance_details(timeTaken,columnsScanned) {
	var heapUsed = process.memoryUsage()["heapUsed"],
		performanceDetails = "Time Taken : "+timeTaken+" secs \nFileSize : "+ fileSize+" MB \nMemory Heap Used : "+ heapUsed + "\nColumns Scanned : "+columnsScanned+ "\nRows Scanned : "+total_rows+ "\nTime: "+Date(Date.now())+"\n\n";
	fs.appendFileSync('performance.txt', performanceDetails, 'utf8')
}
function special_characters(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/\`|\~|\!|\@|\#|\$|\_|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:/g)	
	if(re.test(param)) {
		construct_detail_object(details,"special_characters",param,columnName,arrayFullScan);
		return true
	}
	else {
		return false
	}
}
function uppercase_entries(details,param,columnName,arrayFullScan) {	
	var re = new RegExp("[A-Z]");
	if(re.test(param)) {
		construct_detail_object(details,"uppercase_entries",param,columnName,arrayFullScan);
		return true
	}
	else {
		return false
	}
}
function string(details,param,columnName,arrayFullScan) {
	var re = new RegExp("[a-zA-Z]"); // looks for integer but even mix of string and somethingElse is accepted	
	if(re.test(param)) {
		// pure_string(details,param,columnName,arrayFullScan)
		uppercase_entries(details,param,columnName,arrayFullScan)
		construct_detail_object(details,"string",param,columnName,arrayFullScan);	
		return true
	}
	else {
		return false
	}
}
function pure_string(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/^[a-zA-Z]+$/); // looks for exclusively string
	states(details,param,columnName,arrayFullScan)
	state_code(details,param,columnName,arrayFullScan)
	if(re.test(param)) {
		construct_detail_object(details,"pure_string",param,columnName,arrayFullScan);		
		return true
	}
	else {
		return false
	}
}
function states(details,param,columnName,arrayFullScan) {
	if(config.states.indexOf(param) >= 0) {
		construct_detail_object(details,"states",param,columnName,arrayFullScan)
		return true
	}
	else {
		return false
	}
}
function state_code(details,param,columnName,arrayFullScan) {
	if(config.state_codes.indexOf(param) >= 0) {
		construct_detail_object(details,"state_codes",param,columnName,arrayFullScan)
		return true
	}
	else {
		return false
	}
}
function integer(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/\d/); // looks for integer but even mix of integer and somethingElse is accepted
	if(re.test(param)) {
		pure_integer(details,param,columnName,arrayFullScan)	
		construct_detail_object(details,"integer",param,columnName,arrayFullScan);
		return re.test(param)
	}
	else {
		return false
	}
}
function pure_integer(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/^\d+$/); // looks for exclusively integer
	if(re.test(param)) {		
		construct_detail_object(details,"pure_integer",param,columnName,arrayFullScan);
		return re.test(param)
	}
	else {
		return false
	}
}
function email(details,param,columnName,arrayFullScan) {	
	var re = new RegExp(/\S+@\S+\.\S+/)
	if(re.test(param)) {			
		construct_detail_object(details,"email",param,columnName,arrayFullScan);
		return re.test(param)
	}
	else {
		return false
	}
}
function construct_detail_object(details,datatype,param,columnName,arrayFullScan) {
	// this function updates the details Object with all requisite informations.
	// this function has been built flexibly so that it can be invoked from multiple functions	with varying parameters
	rowCount = arrayFullScan == undefined ? targetColumnArray.indexOf(param) : arrayFullScan.indexOf(param)
	rowCountArray.push(rowCount)
	//when single column is scanned "targetColumnArray" will comprise of single array where we use indexOf to find our param
	//when whole file is scanned targetColumnArray comprises of multiple array ;now we pick each child array(arrayFullScan)
	// and find the indexOf param in it.
	details[datatype][param] = {
		"parameter" : param,
		"columnName" : columnName,
		"rowCount" : rowCount+1 
	}
	return details[datatype]
}
function remove_duplicate(array){
	return array.filter(function(item, pos) {
	    return array.indexOf(item) == pos;
	})
}
function common_array_entries(array, arr) {
    return arr.some(function (v) {
        return array.indexOf(v) >= 0;
    });
}

module.exports = {
	getDetailsObject : getDetailsObject,
	string : string,
	pure_string : pure_string,
	uppercase_entries : uppercase_entries,
	integer  : integer,
	pure_integer : pure_integer,
	email : email,
	states : states,
	state_code : state_code,
	special_characters : special_characters,
	classify : classify,
	create_column : create_column,
	read_file : read_file,
	start_process : start_process,
	targetColumnArray : targetColumnArray,
	construct_detail_object : construct_detail_object,
	show_results : show_results
}