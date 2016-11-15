var expect = require('chai').expect,
	assert = require('assert'),
	fs = require('fs'),
	AnomalyFinder = require('../AnomalyFinder.js'),
	details = AnomalyFinder.getDetailsObject(),
	config = require('../config.js'),
	special_characters = config.special_characters,
	states = config.states,
	state_codes = config.state_codes,
	random_state = states[Math.floor(Math.random() * states.length)],
	random_state_code = state_codes[Math.floor(Math.random() * state_codes.length)],
	random_special_character = special_characters[Math.floor(Math.random() * special_characters.length)];


describe('Testing String',function(){
	describe("Testing 1234Random in string scenario ", function() {		
		it("should return index ",function(){
			assert.equal(AnomalyFinder.string(details,"1234Random"),true) // position of the first string
		});
	});

	describe("Testing 1234 in string scenario ", function() {		
		it("should return false ",function(){
			assert.equal(AnomalyFinder.string(details,"1234"),false)
		});
	});

	describe("Testing 1234Random in pure string scenario ", function() {		
		it("should return false ",function(){
			assert.equal(AnomalyFinder.pure_string(details,"1234Random"),false)
		});
	});

	describe("Testing random in pure string scenario ", function() {		
		it("should return true ",function(){
			assert.equal(AnomalyFinder.pure_string(details,"random"),true)
		});
	});

	describe("Testing 1234Random in upper case scenario ", function() {		
		it("should return index ",function(){
			assert.equal(AnomalyFinder.uppercase_entries(details,"1234Random"),true)
		});
	});

	describe("Testing 1234Random in upper case scenario ", function() {		
		it("should return false ",function() {
			assert.equal(AnomalyFinder.uppercase_entries(details,"1234random"),false)		
		});
	});
})

describe('Testing Integer',function(){
	describe("Testing random123 in integer scenario ", function() {		
		it("should pass ",function(){
			assert.equal(AnomalyFinder.integer(details,"random123"),true)
		});
	});

	describe("Testing random in integer scenario ", function() {		
		it("should fail ",function(){
			assert.equal(AnomalyFinder.integer(details,"random"),false)
		});
	});

	describe("Testing 12345 in pure integer scenario ", function() {		
		it("should pass ",function(){
			assert.equal(AnomalyFinder.pure_integer(details,12345),true)
		});
	});

	describe("Testing random in pure integer scenario ", function() {		
		it("should fail ",function(){
			assert.equal(AnomalyFinder.pure_integer(details,"random"),false)
		});
	});
});

describe('Testing Email',function(){
	describe("Testing host@gmail.com in email scenario ", function() {		
		it("should pass ",function(){
			assert.equal(AnomalyFinder.email(details,"host@gmail.com"),true)
		});
	});

	describe("Testing host@gmailcom in email scenario ", function() {			
		it("should fail ",function(){
			assert.equal(AnomalyFinder.email(details,"host@gmailcom"),false)
		});
	});

	describe("Testing hostgmail.com in email scenario ", function() {			
		it("should fail ",function(){
			assert.equal(AnomalyFinder.email(details,"hostgmail.com"),false)
		});
	});

	describe("Testing 123@gmailcom in email scenario ", function() {			
		it("should fail ",function(){
			assert.equal(AnomalyFinder.email(details,"123@gmailcom"),false)
		});
	});
});

describe('Testing states',function(){
	describe('Testing '+random_state+' in state scenario',function(){		
		it("should pass ",function(){
			assert.equal(AnomalyFinder.states(details,random_state),true)
		});
	});

	describe('Testing Albatross in state scenario',function(){
		it("should fail ",function(){
			assert.equal(AnomalyFinder.states(details,"Albatross"),false)
		});
	});
});

describe('Testing state codes',function(){
	describe('Testing '+random_state_code+' in state scenario',function(){
		it("should pass ",function(){
			assert.equal(AnomalyFinder.state_code(details,random_state_code),true)
		});
	});

	describe('Testing AA in state codes scenario',function(){		
		it("should fail ",function(){
			assert.equal(AnomalyFinder.state_code(details,"AA"),false)
		});
	});
});

describe('Testing special_characters codes',function(){
	describe('Testing '+ random_special_character + ' in special_characters scenario',function(){
		it("should pass",function(){
			assert.equal(AnomalyFinder.special_characters(details,random_special_character),true)
		})
	});

	describe('Testing AA in state codes scenario',function(){
		it("should fail ",function(){
			assert.equal(AnomalyFinder.special_characters(details,"AA"),false)
		});
	});
});

// skipping functions getDetailsObject, read_file, //TODO..
describe("Testing Functions",function(){
	describe("Testing Function classify",function(){
		it("should return classified",function(){
			// assert.equal(AnomalyFinder.classify(1234,"id"),"classified")
		})
	});

	describe("Testing Function getDetailsObject", function(){
		it("should return getDetailsObject",function(){
			assert.equal(JSON.stringify(AnomalyFinder.getDetailsObject()),'{"uppercase_entries":{},"string":{},"integer":{},"pure_integer":{},"pure_string":{},"email":{},"state_codes":{},"states":{},"special_characters":{},"zip_code":{}}')
		})
	});
	//start_process can't be tested for now.. DUE to multiple map issue..//TODO

	// describe("Testing Function start_process",function(){
	// 	it("should return bla bla",function(){
	// 		// AnomalyFinder.create_column(config.header_row,"id")
	// 		AnomalyFinder.create_column(config.test_row,"id")
	// 		AnomalyFinder.create_column(config.test_row_one,"id")
	// 		AnomalyFinder.create_column(config.test_row_two,"id")
	// 		AnomalyFinder.create_column(config.test_row_three,"id")
	// 		AnomalyFinder.create_column(config.test_row_four,"id")			
	// 		assert.equal(AnomalyFinder.start_process("id","mock.csv"),"clean_column")
	// 	})		
	// })
	
	describe.skip("Testing construct_detail_object",function(){ // COME BACK HERE TODO..

		// console.log("AnomalyFinder.targetColumnArray is ",AnomalyFinder.targetColumnArray)

		it("should return modified detail object",function(){
			console.log("inside it...")
			AnomalyFinder.create_column(config.header_row,"first_name")
			AnomalyFinder.create_column(config.test_row,"first_name")
			AnomalyFinder.create_column(config.test_row_one,"first_name")
			AnomalyFinder.create_column(config.test_row_two,"first_name")
			AnomalyFinder.create_column(config.test_row_three,"first_name")
			AnomalyFinder.create_column(config.test_row_four,"first_name")
			console.log("targetColumnssssArray is ",AnomalyFinder.targetColumnArray)
			assert.equal(AnomalyFinder.construct_detail_object(AnomalyFinder.getDetailsObject(),"string","paul","first_name"),{ paul: { parameter: 'paul', columnName: 'first_name', rowCount: 3 } })
		})
	})

});

describe("Testing create_column functions",function(){

	it("should return column_doesnt_exist",function(){
		assert.equal(AnomalyFinder.create_column(config.test_row,"id"),"column_doesnt_exist")
	})

	it("should return column_exists",function(){
		assert.equal(AnomalyFinder.create_column(config.header_row,"id"),"column_exists")
	})

});


describe("Testing Functions analyse, manage_exceptions, show_results in a error filled column ",function(){
	var return_from_analyse = AnomalyFinder.analyse(config.test_details_with_error,9,"id"),
		return_from_manage_exceptions = AnomalyFinder.manage_exceptions(return_from_analyse[1],"id"),
		return_from_show_results = AnomalyFinder.show_results("id"),
		return_from_store_performance_details_trigger = AnomalyFinder.store_performance_details_trigger(false,"id"),
		return_from_store_performance_details = AnomalyFinder.store_performance_details(return_from_store_performance_details_trigger[1]);		
	
	it("should return correct possible_anamoly and not_anamoly ",function(){
		assert.equal(return_from_analyse[0].toString(),[ 'string' ].toString())
		assert.equal(return_from_analyse[1].toString(),[ 'integer', 'pure_integer' ].toString())
	})
	
	it("should return correct possible_anamoly and not_anamoly ",function(){
		assert.equal(return_from_manage_exceptions[0].toString(),[ 'string' ].toString())
		assert.equal(return_from_manage_exceptions[1].toString(),[ 'integer', 'pure_integer' ].toString())
	})

	it("should return error_in_column",function(){
		assert.equal(return_from_show_results.toString(),['error_in_column'])
	})

	it("should return single_column_is_scanned",function(){
		assert.equal(return_from_store_performance_details_trigger[0],"single_column_is_scanned")
		assert.equal(return_from_store_performance_details_trigger[1],7)
	})

	it("should return data_stored",function(){
		assert.equal(return_from_store_performance_details,"data_stored")
	})
})

describe("Testing Functions analyse, manage_exceptions, show_results in a clean column ",function(){
	var return_from_analyse = AnomalyFinder.analyse(config.test_details_without_error,9,"email"),
		return_from_manage_exceptions = AnomalyFinder.manage_exceptions(return_from_analyse[1],"email"),
		return_from_show_results = AnomalyFinder.show_results("email"),
		return_from_store_performance_details_trigger = AnomalyFinder.store_performance_details_trigger(false,"email"),
		return_from_store_performance_details = AnomalyFinder.store_performance_details(return_from_store_performance_details_trigger[1]);
	
	it("should return correct possible_anamoly and not_anamoly ",function(){
		assert.equal(return_from_analyse[0].toString(),[])
		assert.equal(return_from_analyse[1].toString(),["string","integer","email","special_characters"].toString())
	})
	
	it("should return correct possible_anamoly and not_anamoly ",function(){
		assert.equal(return_from_manage_exceptions[0].toString(),[])
		assert.equal(return_from_manage_exceptions[1].toString(),["string","integer","email","special_characters"].toString())
	})

	it("should return clean_column",function(){
		assert.equal(return_from_show_results.toString(),['clean_column'])
	})

	it("should return single_column_is_scanned",function(){
		assert.equal(return_from_store_performance_details_trigger[0],"single_column_is_scanned")
		assert.equal(return_from_store_performance_details_trigger[1],7)
	})

	it("should return data_stored",function(){
		assert.equal(return_from_store_performance_details,"data_stored")
	})
})

describe("Testing read_file",function(){ //NOT WORKING COME BACK HERE TODO..
	var return_from_read_file_fail = AnomalyFinder.read_file("test1Cases.csv"),
		return_from_read_file_pass = AnomalyFinder.read_file("testCases.csv");
	it("should return file_doesnt_Exist",function(){
		assert.equal(return_from_read_file_fail,"file_doesnt_Exist")
	})

	it("should return file_exists",function(){
		assert.equal(return_from_read_file_pass,"file_exists")
	})
})

describe("Testing parse_file",function(){ //NOT WORKING COME BACK HERE TODO..
	var return_from_store_variable_for_testing_parse_file_function;
	it("will return nothing, just parse the csv file",function(done){
		this.timeout(10000);
		AnomalyFinder.parse_file("testCases.csv",true);
		done();
	})
	it("should return file_parsed_will_be_tested",function(){
		return_from_store_variable_for_testing_parse_file_function = AnomalyFinder.store_variable_for_testing_parse_file_function();
		// console.log("return_from_store_variable_for_testing_parse_file_function is ",return_from_store_variable_for_testing_parse_file_function)
		assert.equal(return_from_store_variable_for_testing_parse_file_function,"file_parsed_will_be_tested")
	})
})

describe("Testing function fileSizeInMegabytes",function(){
	var fileSizeInMegabytes = (fs.statSync("testCases.csv")["size"])/1000000.0 ;
	it("should return correct file Size",function(){
		assert.equal(AnomalyFinder.fileSizeInMegabytes("testCases.csv"),fileSizeInMegabytes)
	})
})