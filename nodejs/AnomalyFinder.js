// use maps.googleapis.com to find validity of a zipcode// TODO...
// for ex. http://maps.googleapis.com/maps/api/geocode/json?address=99571 gives details of Alaska ..
// Improvise from the json

var fs = require('fs'),
	parse = require('csv-parse'),
	config = require("./config.js"),
	readline = require('readline'),
	rl = readline.createInterface(process.stdin, process.stdout),
	http = require("http"),
	threshold_percentage = 0,
	columnCheck = 0, // to check if the chosen column actually exists in the csv file..
	Regex = require("regex"),
	targetColumnArray = [],
	possible_anamoly = [],
	previous_column = '',
	current_column = '',
	all_dataType = [],
	anamolous_datatype = [],
	rowCount = 0,
	details = getDetailsObject(),
	indexNumber ;

rl.question('Enter the file that you wish to scan > ', function(fileName) {
	rl.question('Kindly Choose One : \n 1.Scan Whole File \n 2.Scan Single Column \n', function(choice) {
		if(choice == 1) {
			read_file(fileName,"ALL")
		}
		else if (choice == 2) {
			list_header(fileName);					
		}
		else {
			console.log("Kindly pick either 1 or 2")
			process.exit(0);
		}
	});
    
});

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
		// if a column contains entry is dominated by integers, then in the details object, integer and
		// associated objects will contains many key-value pairs
		// when said object's length exceeds a certain threshold (as mentioned in config.js)
		// we analyse it as belonging to that particular datatype
		if(threshold_percentage < config.threshold_percentage && possible_anamoly.indexOf(key) == -1) {
			possible_anamoly.push(key);			
		}
		if(iterationCount == array.length-1) {
			// after scanning each column, we have an object (details) that comprises of multiple datatypes
			// each datatype has a percentange of occurence (can vary from 0-100%)
			// if this percentage is lesser than the threshold_percentage (decided in config.js)
			// then we decide that particular datatype and associated entries to be anamolous.
			if(possible_anamoly.length >0) {
				possible_anamoly.map(function(datatype){
					Object.keys(details[datatype]).map(function(key){
						console.log("Entry " + key + " at row number " + details[datatype][key]["rowCount"] + " in column "+ columnName +" is out of place; because it contains datatype " + datatype + "" );
					});
				});					
			}
			else {
				if(count == arr.length-1) {
					// to avoid consoling multiple times..
					console.log("Column " + columnName + " appears to be clean");
				}					
			}					
		}
	})
}

function special_characters(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/\`|\~|\!|\@|\#|\$|\_|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\.|\>|\?|\/|\""|\;|\:/g)
	if(re.test(param)) {
		construct_detail_object(details,"special_characters",param,columnName,arrayFullScan);
	}
}

function uppercase_entries(details,param,columnName,arrayFullScan) {	
	var re = param.match("[A-Z]");
	if(re != null) {
		construct_detail_object(details,"uppercase_entries",param,columnName,arrayFullScan);
	}
}

function string(details,param,columnName,arrayFullScan) {
	var re = param.match("[a-zA-Z]"); // looks for integer but even mix of string and somethingElse is accepted	
	if(re != null) {
		pure_string(details,param,columnName,arrayFullScan)
		uppercase_entries(details,param,columnName,arrayFullScan)
		construct_detail_object(details,"string",param,columnName,arrayFullScan);		
	}
}

function pure_string(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/^[a-zA-Z]+$/); // looks for exclusively string
	states(details,param,columnName,arrayFullScan)
	state_code(details,param,columnName,arrayFullScan)
	if(re.test(param)) {			
		construct_detail_object(details,"pure_string",param,columnName,arrayFullScan);		
	}
}

function states(details,param,columnName,arrayFullScan) {
	if(config.states.indexOf(param) >= 0) {
		construct_detail_object(details,"states",param,columnName,arrayFullScan)
	}
}

function state_code(details,param,columnName,arrayFullScan) {
	if(config.state_codes.indexOf(param) >= 0) {
		construct_detail_object(details,"state_codes",param,columnName,arrayFullScan)
	}
}

function integer(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/\d/); // looks for integer but even mix of integer and somethingElse is accepted
	if(re.test(param)) {
		pure_integer(details,param,columnName,arrayFullScan)	
		construct_detail_object(details,"integer",param,columnName,arrayFullScan);
	}
}

function pure_integer(details,param,columnName,arrayFullScan) {
	var re = new RegExp(/^\d+$/); // looks for exclusively integer
	if(re.test(param)) {
		// zipcode(param)			
		construct_detail_object(details,"pure_integer",param,columnName,arrayFullScan);
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
	if(re.test(param)) {			
		construct_detail_object(details,"email",param,columnName,arrayFullScan);
	}
}

function construct_detail_object(details,datatype,param,columnName,arrayFullScan) {
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
}

Array.prototype.diff = function(a) {
    return this.filter(function(i) {return a.indexOf(i) < 0;});
};

Array.prototype.intersection = function(a) {
    return this.filter(function(i) {return a.indexOf(i) >= 0;});
};