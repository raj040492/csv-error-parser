module.exports = {
	threshold_percentage : 70, // above this numerical, positive repsonse else negative
	never_together : { // these objects can never co-exist together..
		"pure_integer" : ["string","pure_string","email","uppercase_entries","special_characters"],
		"pure_string" : ["integer","pure_integer","email","special_characters"],		
		// "string" : ["pure_integer"], //these two lines are commented out because it's too tricky handle these cases
		// "integer" : ["pure_string","email"], //i.e just integer or just string can be found almost everywhere . thus tricky
		"email" : ["pure_integer","pure_string"]
	},
	states : ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming","District of Columbia","Puerto Rico","Guam","American Samoa","U.S. Virgin Islands","Northern Mariana Islands"],
	state_codes : ["AK","AL","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"],	
	states_and_cities : ["Wyoming","Minnesota","California","Georgia","Kansas","Vermont","Indiana","Pennsylvania","Alabama","New York","Florida","Ohio","Texas","Maryland","Louisiana","Missouri","WY","MN","CA","GA","KS","VT","IN","PA","AL","NY","FL","OH","TX","MD","LA"]
}