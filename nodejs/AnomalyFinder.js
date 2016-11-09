// use maps.googleapis.com to find validity of a zipcode// TODO...
// for ex. http://maps.googleapis.com/maps/api/geocode/json?address=99571 gives details of Alaska ..
// Improvise from the json

var fs = require('fs'),
	parse = require('csv-parse'),
	config = require("./config.js"),
	http = require("http"),
	threshold_percentage = 0,
	columnCheck = 0, // to check if the chosen column actually exists in the csv file..
	Regex = require("regex"),
	header = '',
	targetColumnArray = [],
	possible_anamoly = [],
	previous_column = '',
	current_column = '',
	all_dataType = [],
	anamolous_datatype = [],
	rowCount = 0,
	details = getDetailsObject(),
	indexNumber,
	fileName  = process.argv[2],
	columnName  = process.argv[3];

if(fileName && columnName) {
	read_file(fileName,columnName);
}
else {
	if(fileName && columnName == undefined) {
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

function list_header(fileName) {
	fs.createReadStream(fileName)
		.on('error',function(err){
			// various errors could be thrown; only if error code is "ENOENT", 
			// do we conclude that, it's a missing file or directory scenario..
			if (err["code"] == "ENOENT") {
				console.log("File "+ fileName + " doesnt exist")
				console.log("Ensure if the file is in the same directory")
				console.log("Look for typo errors")
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
			rowCount +=1;
			if(rowCount == 1) { // the first row of any csv contains heading for each column
				header = rows;
				console.log(header + "\n")
			}
		})
		.on('end',function(rows){
			rl.question('Enter the column that you wish to scan > ', function(columnName) {
			    read_file(fileName,columnName)
		        rl.close();
		    });
		})
}

function read_file (fileName,columnName){
	fs.createReadStream(fileName)
		.on('error',function(err){
			// various errors could be thrown; only if error code is "ENOENT", 
			// do we conclude that, it's a missing file or directory scenario..
			if (err["code"] == "ENOENT") {
				console.log("File "+ fileName + " doesnt exist")
				console.log("Ensure if the file is in the same directory")
				console.log("Look for typo errors")
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

			create_column(rows,columnName);
		})
		.on('end',function(){			
			start_process(columnName,fileName)
		})
}

function create_column(rows,columnName) {	
	rowCount +=1;
	if(rowCount == 1) { // the first row of any csv contains heading for each column
		header = rows;
		if (columnName == "ALL") {
			// array inside array for each columns 
			// for single column scan, a simple array would do, no need to create child arrays
			// such new array initialization must happen only once  N only when ALL columns are to scanned
			// else will break our logic
			for(var i=0;i<rows.length;i++) {
				targetColumnArray[i] = new Array();
			}
		}
	}
	if(rows.indexOf(columnName)>=0) {
		columnCheck +=1;				
		indexNumber = rows.indexOf(columnName);								
	}
	else if (columnName == "ALL") {
		columnCheck +=1;
		for(var i=0;i<rows.length;i++) {
			targetColumnArray[i].push(rows[i])
		}
	}
	if(columnName != "ALL") {		
		targetColumnArray.push(rows[indexNumber]);
	}
}

function analyse_column(targetEntry,columnName) {
	targetEntry.map(function(actualEntry,innerArrayIterationCount,innerArray){
		if(innerArrayIterationCount == 0) {
			columnName = targetEntry[0]
		}
		if(innerArrayIterationCount != 0) { // we dont want to classify the header line ; i.e the first line of csv file.
			classify(actualEntry,columnName,targetEntry);			
		}
		if(innerArrayIterationCount == innerArray.length-1) {
			analyse(details,innerArray.length-1,columnName)
		}
	})
}

function start_process(columnName,fileName) {
	if(columnCheck > 0 ) { // if the chosen column exists in the csv	
		targetColumnArray.map(function(targetEntry,iterationCount,array){
			if(targetEntry.constructor === Array) {
				analyse_column(targetEntry,columnName)
			}
			else {
				if(targetEntry != columnName) { // we dont want to classify the header line ; i.e the first line of csv file.
					classify(targetEntry,columnName);
				}
				if(iterationCount == array.length-1) {
					analyse(details,array.length-1,columnName)
				}
			}
		})
	}
	else {
		console.log("Column " + columnName + " is not present in " + fileName);
		process.exit(0);
	}
}

function classify(param,columnName,arrayFullScan) {
	// a broad wing is created in the first level in which the following will be invoked
	// if one of the following functions is satisfied by the param, then we go a layer deep 
	// i.e if param satisfies string, we then check for uppercase and pure string scenario
	// in other words it doesnt make much sense to put a param thru string and again thru uppercase when
	// its clear from the first test(string) that it's not a string

	if(columnName != current_column) {
		// while scanning the whole file, the flows goes from one column to another
		// thus when a switch happens from one column to another, we must reset the details object
		// else the object will contain data from previous column..
		// reset happens in getDetailsObject();
		current_column = columnName
		details = getDetailsObject();
	}

	string(details,param,columnName,arrayFullScan)
	integer(details,param,columnName,arrayFullScan)
	email(details,param,columnName,arrayFullScan)
	special_characters(details,param,columnName,arrayFullScan)
}

function analyse(details,len,columnName) {
	all_dataType = [];
	possible_anamoly = [];	
	Object.keys(details).map(function(key,iterationCount,array){
		threshold_percentage = (Object.keys(details[key]).length/len)*100;
		// after scanning each column, we have an object (details) that comprises of multiple datatypes
 		// each datatype has a percentange of occurence (can vary from 0-100%)
		// if this percentage is lesser than the threshold_percentage (decided in config.js)
		// then we decide that particular datatype and associated entries to be anamolous.
		if(threshold_percentage < config.threshold_percentage && threshold_percentage >0 && possible_anamoly.indexOf(key) == -1) {
			possible_anamoly.push(key);			
		}
		if(iterationCount == array.length-1) {
			if(possible_anamoly.length >0) {
				possible_anamoly.map(function(datatype,anamolyIterationCount,possibleAnamolyArray){
					Object.keys(details[datatype]).map(function(key){
						console.log("Entry " + key + " at row number " + details[datatype][key]["rowCount"] + " in column "+ columnName +" is out of place; because it contains datatype " + datatype + "" );
					});					
					if(header.indexOf(columnName) == header.length-1) {
						process.exit(0)
					}
				});
			}
			else {
				console.log("Column " + columnName + " appears to be clean");
			}					
		}
	})
}

function special_characters(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/\`|\~|\!|\@|\#|\$|\_|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\.|\>|\?|\/|\""|\;|\:/g)	
	if(re.test(param)) {
		construct_detail_object(details,"special_characters",param,columnName,arrayFullScan);
		return true
	}
	else {
		return false
	}
}

function uppercase_entries(details,param,columnName,arrayFullScan) {	
	var re = param.match("[A-Z]");
	//return re
	if(re != null) {
		construct_detail_object(details,"uppercase_entries",param,columnName,arrayFullScan);
		return re
	}
}

function string(details,param,columnName,arrayFullScan) {
	var re = param.match("[a-zA-Z]"); // looks for integer but even mix of string and somethingElse is accepted	
	//return re
	if(re != null) {
		pure_string(details,param,columnName,arrayFullScan)
		uppercase_entries(details,param,columnName,arrayFullScan)
		construct_detail_object(details,"string",param,columnName,arrayFullScan);	
		return re	
	}
}

function pure_string(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/^[a-zA-Z]+$/); // looks for exclusively string
	//return re.test(param)
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
		// return true
		construct_detail_object(details,"states",param,columnName,arrayFullScan)
		return true
	}
	else {
		return false
	}
}

function state_code(details,param,columnName,arrayFullScan) {
	if(config.state_codes.indexOf(param) >= 0) {
		// return true
		construct_detail_object(details,"state_codes",param,columnName,arrayFullScan)
		return true
	}
	else {
		return false
	}
}

function integer(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/\d/); // looks for integer but even mix of integer and somethingElse is accepted
	//return re.test(param)
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
	//return re.test(param)
	if(re.test(param)) {
		// zipcode(param)			
		construct_detail_object(details,"pure_integer",param,columnName,arrayFullScan);
		return re.test(param)
	}
	else {
		return false
	}
}

function zipcode(details,param,columnName,arrayFullScan) {
	// zipcodes follow various practises; i.e five digits , four digits, five digits and four digits separated by single 
	//	hyphen five digits and four digits separated by two hyphen
	// but here we restrict ourselves to just five digits scenario since it is widely used practise
	var body = [];
	http.get("http://maps.googleapis.com/maps/api/geocode/json?address="+param +"",function(res){
		res.on('data',function(data){
			body.push(data);
		});
		res.on('end',function(){
			var data = JSON.parse(body.toString())
			if(data["status"] == "OK") {
				construct_detail_object(details,"zip_code",param,columnName,arrayFullScan); //TODO.. OBJECT WONT CONSTRUCT..
			}
		})
	})
}

function email(details,param,columnName,arrayFullScan) {	
	var re = new RegExp(/\S+@\S+\.\S+/)
	//return re.test(param)
	if(re.test(param)) {			
		construct_detail_object(details,"email",param,columnName,arrayFullScan);
		return re.test(param)
	}
	else {
		return false
	}
}

function construct_detail_object(details,datatype,param,columnName,arrayFullScan) {
	// return "rajjj"
	// this function updates the details Object with all requisite informations.
	// this function has been built flexibly so that it can be invoked from multiple functions
	rowCount = arrayFullScan == undefined ? targetColumnArray.indexOf(param) : arrayFullScan.indexOf(param)
	//when single column is scanned targetColumnArray will comprise of single array where we use indexOf to find our param
	//when whole file is scanned targetColumnArray comprises of multiple array ;now we pick each child array(arrayFullScan)
	// and find the indexOf param in it.
	details[datatype][param] = {
		"parameter" : param,
		"columnName" : columnName,
		"rowCount" : rowCount
	}
	// return details
}

Array.prototype.diff = function(a) {
    return this.filter(function(i) {return a.indexOf(i) < 0;});
};

Array.prototype.intersection = function(a) {
    return this.filter(function(i) {return a.indexOf(i) >= 0;});
};

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
	special_characters : special_characters
}