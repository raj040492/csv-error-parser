var expect = require('chai').expect,
	assert = require('assert'),
	AnomalyFinder = require('../AnomalyFinder.js'),
	config = require('../config.js'),
	special_characters = config.special_characters,
	states = config.states,
	state_codes = config.state_codes,
	random_state = states[Math.floor(Math.random() * states.length)],
	random_state_code = state_codes[Math.floor(Math.random() * state_codes.length)],
	random_special_character = special_characters[Math.floor(Math.random() * special_characters.length)],
	details = AnomalyFinder.getDetailsObject();	

describe.skip('Testing String',function(){
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

describe.skip('Testing Integer',function(){
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

describe.skip('Testing Email',function(){
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

describe.skip('Testing states',function(){
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

describe.skip('Testing state codes',function(){
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

describe.skip('Testing special_characters codes',function(){
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
describe.skip("Testing Functions",function(){
	describe("Testing Function classify",function(){
		it("should return classified",function(){
			// assert.equal(AnomalyFinder.classify(1234,"id"),"classified")
		})
	});

	


	// describe("Testing Function read_file", function(){
	// 	it("should return error",function(){
	// 		console.log("AnomalyFinder.read_file('mock.csv','asdas') is ",AnomalyFinder.read_file("asda",'asas'))
	// 		assert.equal(AnomalyFinder.read_file("asda","adas"),"asdasdasdasdasads")
	// 	})
	// });

	describe("Testing Function getDetailsObject", function(){
		it("should return getDetailsObject",function(){
			assert.equal(JSON.stringify(AnomalyFinder.getDetailsObject()),'{"uppercase_entries":{},"string":{},"integer":{},"pure_integer":{},"pure_string":{},"email":{},"state_codes":{},"states":{},"special_characters":{},"zip_code":{}}')
		})
	});
	//start_process and analyse can't be tested for now.. DUE to multiple map issue..

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
	
	describe("Testing construct_detail_object",function(){
		before(function(done){
			console.log("AnomalyFinder.targetColumnArray is ",AnomalyFinder.targetColumnArray)
			// AnomalyFinder.targetColumnArray = [];
			console.log("inside before...")
			console.log("AnomalyFinder.targetColumnArray after reset is ",AnomalyFinder.targetColumnArray)
			done();
		});
		
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


describe.skip("Testing create_column functions",function(){

	describe("Testing Function create_column failure",function(){
		it("should return column_doesnt_exist",function(){
			assert.equal(AnomalyFinder.create_column(config.test_row,"id"),"column_doesnt_exist")
		})
	});

	describe("Testing Function create_column",function(){
		AnomalyFinder.create_column(config.header_row,"id")
		it("should return something",function(){
			assert.equal(AnomalyFinder.create_column(config.header_row,"id"),"column exists")
		})
	});

	// afterEach(function(){
	// 	AnomalyFinder.targetColumnArray = [];
	// 	console.log("inside after...")
	// 	console.log("targetColumnssssArray____ is ",AnomalyFinder.targetColumnArray)
	// })
});

describe("Testing show results function",function(){
	it("should return asdasdasa",function(){
		assert.equal(AnomalyFinder.show_results(['pure_integer'],['integer']),[])
	})
})