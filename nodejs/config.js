module.exports = {
	threshold_percentage : 60, // above this numerical, positive repsonse else negative	
	special_characters : ['`','\\','~','!','@','#','$','_','%','^','&','*','(',')','+','=','[','{',']','}',','<',','.','>','?','/','"',';'],
	states : ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming","District of Columbia","Puerto Rico","Guam","American Samoa","U.S. Virgin Islands","Northern Mariana Islands"],
	state_codes : ["AK","AL","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"],	
	states_and_cities : ["Wyoming","Minnesota","California","Georgia","Kansas","Vermont","Indiana","Pennsylvania","Alabama","New York","Florida","Ohio","Texas","Maryland","Louisiana","Missouri","WY","MN","CA","GA","KS","VT","IN","PA","AL","NY","FL","OH","TX","MD","LA"],
	exceptions : {
		"pure_integer" : ["integer"],
		"pure_string" : ["string"]
	},
	never_together : {
		"pure_integer" : ["email"]
	},
	//below are used in testing
	header_row : ["id","first_name","last_name","email","country","ip_address","zip_code"],
	test_row : ["7","Helen","Martin","hmartin6@google.es","China","249.59.72.199","123435"],
	test_row_one : ["1","paul","Matthews","pmatthews0@friendfeed.com","Indo12nesia","235.160.46.2s8","12345"],
	test_row_two : ["2","Tammy","Lane","tlane1@typepad.com","Russia","91.226.216.220","12346"],
	test_row_three : ["3","Barbara","Webb","2345","France","204.48.177.97","123435"],
	test_row_four : ["4","Adam","Miller","amiller3163.com","Reunion","158.15.38.141","123345"]
}