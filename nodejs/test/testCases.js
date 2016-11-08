var expect = require('chai').expect,
	assert = require('assert'),
	AnomalyFinder = require('../AnomalyFinder.js'),
	states = require('../config.js').states,
	state_codes = require('../config.js').state_codes,
	special_characters = require('../config.js').special_characters,
	random_state = states[Math.floor(Math.random() * states.length)],
	random_state_code = state_codes[Math.floor(Math.random() * state_codes.length)],
	random_special_character = special_characters[Math.floor(Math.random() * special_characters.length)],
	details = AnomalyFinder.getDetailsObject();

describe('Testing String',function(){
	describe("Testing 1234Random in string scenario ", function() {
		string_check_pass = AnomalyFinder.string(details,"1234Random");
		it("should return index ",function(){
			assert.equal(string_check_pass['index'],4) // position of the first string
		});
	});

	describe("Testing 1234 in string scenario ", function() {
		string_check_fail = AnomalyFinder.string(details,"1234");
		it("should return null ",function(){
			assert.equal(string_check_fail,null)
		});
	});

	describe("Testing 1234Random in pure string scenario ", function() {
		pure_string_check_fail = AnomalyFinder.pure_string(details,"1234Random");
		it("should return false ",function(){
			assert.equal(pure_string_check_fail,false)
		});
	});

	describe("Testing random in pure string scenario ", function() {
		pure_string_check_pass = AnomalyFinder.pure_string(details,"random");
		it("should return true ",function(){
			assert.equal(pure_string_check_pass,true)
		});
	});

	describe("Testing 1234Random in upper case scenario ", function() {
		uppercase_check_pass = AnomalyFinder.uppercase_entries(details,"1234Random");
		it("should return index ",function(){
			assert.equal(uppercase_check_pass['index'],4)
		});
	});

	describe("Testing 1234Random in upper case scenario ", function() {
		uppercase_check_fail = AnomalyFinder.uppercase_entries(details,"1234random");
		it("should return null ",function() {
			assert.equal(uppercase_check_fail,null)		
		});
	});
})

describe('Testing Integer',function(){
	describe("Testing random123 in integer scenario ", function() {
		integer_check_pass = AnomalyFinder.integer(details,"random123");
		it("should pass ",function(){
			assert.equal(integer_check_pass,true)
		});
	});

	describe("Testing random in integer scenario ", function() {
		integer_check_fail = AnomalyFinder.integer(details,"random");
		it("should fail ",function(){
			assert.equal(integer_check_fail,false)
		});
	});

	describe("Testing 12345 in pure integer scenario ", function() {
		pure_integer_check_pass = AnomalyFinder.pure_integer(details,12345);
		it("should pass ",function(){
			assert.equal(pure_integer_check_pass,true)
		});
	});

	describe("Testing random in pure integer scenario ", function() {
		pure_integer_check_fail = AnomalyFinder.pure_integer(details,"random");
		it("should fail ",function(){
			assert.equal(pure_integer_check_fail,false)
		});
	});
});

describe('Testing Email',function(){
	describe("Testing host@gmail.com in email scenario ", function() {
		email_check_pass = AnomalyFinder.email(details,"host@gmail.com");		
		it("should pass ",function(){
			assert.equal(email_check_pass,true)
		});
	});

	describe("Testing host@gmailcom in email scenario ", function() {
		email_check_fail = AnomalyFinder.email(details,"host@gmailcom");		
		it("should fail ",function(){
			assert.equal(email_check_fail,false)
		});
	});

	describe("Testing hostgmail.com in email scenario ", function() {
		email_check_fails = AnomalyFinder.email(details,"hostgmail.com");		
		it("should fail ",function(){
			assert.equal(email_check_fails,false)
		});
	});

	describe("Testing 123@gmailcom in email scenario ", function() {
		email_check_failed = AnomalyFinder.email(details,"123@gmailcom");		
		it("should fail ",function(){
			assert.equal(email_check_failed,false)
		});
	});
});

describe('Testing states',function(){
	describe('Testing '+random_state+' in state scenario',function(){
		state_check_pass = AnomalyFinder.states(details,random_state)
		it("should pass ",function(){
			assert.equal(state_check_pass,true)
		});
	});

	describe('Testing Albatross in state scenario',function(){
		state_check_fail = AnomalyFinder.states(details,"Albatross")
		it("should fail ",function(){
			assert.equal(state_check_fail,false)
		});
	});
});

describe('Testing state codes',function(){
	describe('Testing '+random_state_code+' in state scenario',function(){
		state_codes_check_pass = AnomalyFinder.state_code(details,random_state_code)
		it("should pass ",function(){
			assert.equal(state_codes_check_pass,true)
		});
	});

	describe('Testing AA in state codes scenario',function(){
		state_codes_check_fail = AnomalyFinder.state_code(details,"AA")
		it("should fail ",function(){
			assert.equal(state_codes_check_fail,false)
		});
	});
});

describe('Testing special_characters codes',function(){
	describe('Testing '+ random_special_character + ' in special_characters scenario',function(){
		special_characters_check_pass = AnomalyFinder.special_characters(details,random_special_character)
		it("should pass",function(){
			assert.equal(special_characters_check_pass,true)
		})
	});

	describe('Testing AA in state codes scenario',function(){
		special_characters_check_fail = AnomalyFinder.special_characters(details,"AA")
		it("should fail ",function(){
			assert.equal(special_characters_check_fail,false)
		});
	});
});