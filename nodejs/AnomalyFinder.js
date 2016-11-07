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
	possible_dataType = [],
	all_dataType = [],
	anamolous_datatype = [],
	rowCount = 0,
	details = {
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
	},
	indexNumber = -10; // random number is assigned;

rl.question('Enter the file that you wish to scan > ', function(fileName) {
    rl.question('Enter the column that you wish to scan > ', function(columnName) {
	    read_file(fileName,columnName)
        rl.close();
    });
});


function read_file (fileName,columnName){
	fs.createReadStream(fileName)
		.on('error',function(err){
			// various errors could be thrown; only if error code is "ENOENT", 
			// do we conclude that it's a missing file or directory scenario..
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
		.on('data',function(rows){	// reads csv row wise			
			rowCount +=1;
			if(rowCount == 1) { // the first row of any csv contains heading for each column
				header = rows				
			}
			if(rows.indexOf(columnName)>=0) {
				columnCheck +=1;				
				indexNumber = rows.indexOf(columnName);								
			}
			targetColumnArray.push(rows[indexNumber]);
					
		})
		.on('end',function(){
			if(columnCheck > 0 ) { // if the chosen column exists in the csv
				targetColumnArray.map(function(targetEntry,iterationCount,array){			
					if(targetEntry != columnName) { // we dont want to classify the header line ; i.e the first line of csv file.
						classify(targetEntry);
					}
					if(iterationCount == array.length-1) {
						// console.log("details is ",details)
						analyse(details,array.length-1,columnName)
					}
				})
			}
			else {
				console.log("Column " + columnName + " is not present in " + fileName);
				process.exit(0);
			}
		})
}

function classify(param) {
	// a broad wing is created in the first level in which the following will be invoked
	// if one of the following functions is satisfied by the param, then we go a layer deep 
	// i.e if param satisfies string, we then check for uppercase and pure string scenario
	// in other words it doesnt make much sense to put a param thru string and again thru uppercase when
	// its clear from the first test(string) that it's not a string
	string(param)
	integer(param)
	email(param)
	special_characters(param)
}

function analyse(details,len,columnName) {
	Object.keys(details).map(function(key,iterationCount,array){	
		if(Object.keys(details[key]).length > 0) {
			// all_dataType array contains all possible datatypes in said column, even if they occur just once	
			all_dataType.push(key);
		}
		threshold_percentage = (Object.keys(details[key]).length/len)*100;
		// if a column contains entry is dominated by integers, then in the details object, integer and
		// associated objects will contains many key-value pairs
		// when said object's length exceeds a certain threshold (as mentioned in config.js)
		// we analyse it as belonging to that particular datatype
		if(threshold_percentage >= config.threshold_percentage) {
			possible_dataType.push(key);			
		}
		if(iterationCount == array.length-1) {			
			possible_dataType.map(function(dataType,count,arr){
				//possible_dataType contains datatype that can also be anamolous entries
				// we iteration said array against the never_together object defined in the object
				// never_together object contains datatypes that can never co-exist together				
				if(config.never_together[dataType]) {
					// not all elements in possible_dataType have been defined in never_together object
					// example string and integer have been commented out.
					anamolous_datatype = all_dataType.intersection(config.never_together[dataType]);
				}
				if(anamolous_datatype.length >0) {
					console.log("Column "+columnName+ " is dominated by datatypes : "+possible_dataType)
					anamolous_datatype.map(function(datatype){
						Object.keys(details[datatype]).map(function(key){
							console.log("Entry " + key + " at row number " + details[datatype][key]["rowCount"] + " is out of place; because it contains datatype " + datatype + "" );
						});
					});
					process.exit(0);
				}
				else {
					if(count == arr.length-1) {
						// to avoid consoling multiple times..
						console.log("Column " + columnName + " appears to be clean")	
						process.exit(0);
					}					
				}
			});			
		}
	})
}

function special_characters(param) {
	var re = new RegExp(/\`|\~|\!|\@|\#|\$|\_|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\.|\>|\?|\/|\""|\;|\:/g)
	if(re.test(param)) {
		construct_detail_object("special_characters",param);
	}
}

function uppercase_entries(param) {	
	var re = param.match("[A-Z]");
	if(re != null) {
		construct_detail_object("uppercase_entries",param);
	}
}

function string(param) {
	var re = param.match("[a-zA-Z]"); // looks for integer but even mix of string and somethingElse is accepted	
	if(re != null) {
		pure_string(param)
		uppercase_entries(param)
		construct_detail_object("string",param);		
	}
}

function pure_string(param) {
	var re = new RegExp(/^[a-zA-Z]+$/); // looks for exclusively string
	states(param)
	state_code(param)
	if(re.test(param)) {			
		construct_detail_object("pure_string",param);		
	}
}

function states(param) {
	if(config.states.indexOf(param) >= 0) {
		construct_detail_object("states",param)
	}
}

function state_code(param) {
	if(config.state_codes.indexOf(param) >= 0) {
		construct_detail_object("state_codes",param)
	}
}

function integer(param) {
	var re = new RegExp(/\d/); // looks for integer but even mix of integer and somethingElse is accepted
	if(re.test(param)) {
		pure_integer(param)	
		construct_detail_object("integer",param);
	}
}

function pure_integer(param) {
	var re = new RegExp(/^\d+$/); // looks for exclusively integer
	if(re.test(param)) {
		// zipcode(param)			
		construct_detail_object("pure_integer",param);
	}
}

function zipcode(param) {
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
				construct_detail_object("zip_code",param); //TODO.. OBJECT WONT CONSTRUCT..
			}
		})
	})
}

function email(param) {	
	var re = new RegExp(/\S+@\S+\.\S+/)
	if(re.test(param)) {			
		construct_detail_object("email",param);
	}
}

function construct_detail_object(datatype,param) {
	// this function updates the details Object with all requisite informations.
	// this function has been built flexibly so that it can be invoked from multiple functions
	// console.log("datatype is ",datatype,param)
	details[datatype][param] = {
		"parameter" : param,
		"rowCount" : targetColumnArray.indexOf(param)
	}
}

Array.prototype.diff = function(a) {
    return this.filter(function(i) {return a.indexOf(i) < 0;});
};

Array.prototype.intersection = function(a) {
    return this.filter(function(i) {return a.indexOf(i) >= 0;});
};