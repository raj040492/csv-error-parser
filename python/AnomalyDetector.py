#!/usr/bin/env python

import csv
import sys
import re
import requests
from collections import Counter
import compago
app = compago.Application()
globvar = 0
globar = 1
filename = ''
else_count = 0
func_count = 0
local_count = 0
columnsd = ' '
# arr=[]
# zipcode_array =[]
# email_array = []
# decimal_integer_lengths=[]
open('improperData.txt', 'w').close()

class HeaderPrint(object):
	def funky(self,header):
		# print "Header is",header
		r = csv.reader(open(header, "rU"), dialect=csv.excel_tab)
		line1=r.next()
		global filename
		filename = header			
		for element in line1:
			mylist = element.split(',')	
		print mylist		

class ColumnPrint(object):	
	def print_columns(self,filesname,alpha,beta):
		global globvar
		global globar
		global filename
		globvar = alpha
		globar = beta
		filename = filesname			
		with open(filesname,'rU') as data :			
			r = csv.reader(open(filesname, "rU"), dialect=csv.excel_tab)
			line1=r.next()	
			arrt = []
			for element in line1:
				mylist = element.split(',')				
			real_data = csv.DictReader(data)			
			for row in real_data :
				for i in range(int(alpha),int(beta)):					
					arrt.append(row[mylist[i]])								
			print arrt		

@app.command
def columns(filename="something"):
	x = HeaderPrint()
	x.funky(filename)

# @app.command
# def Column(filename = "fileName", begin="something",to="small"):
# 	y = ColumnPrint()
# 	y.print_columns(filename,begin,to)	

class ExecuteProgram(object):
	def fix_file(self,filesname,alpha,beta):
		global globvar
		global globar
		global filename
		globvar = alpha
		globar = beta
		filename = filesname
		count = 0
		counter = 0
		lower_states = []
		upper_states = []
		arr=[]
		zipcode_array =[]
		email_array = []
		decimal_integer_lengths=[]

		two_letter_lowercase_string_not_state_code = string_with_integer_spaces = email = website = string_with_space_no_integer = phone_no_with_alphabets = website_without_www = state_code = pure_uppercase_string = phone_no_two_hyphens = phone_no_with_parantheses = phone_no_without_hyphen_or_alphabets = valid_verified_zipcode_without_hyphen = empty = valid_verified_zipcode_with_two_hyphen = string_with_integer_without_spaces = pure_integer =  valid_verified_zipcode_with_one_hyphen = two_letter_uppercase_string_not_state_code = zipcode_with_two_not_successive_hyphens = string_without_integer_without_spaces = string_with_symbol_instead_of_at = string_first_line_address = integer_seperated_by_hyphen_not_zip_or_phone =  phone_no_one_hyphen = phone_no_with_only_open_parantheses = phone_no_with_only_close_parantheses = uncertain_entries = string_with_dots_not_email_not_website = mostly_zipcode_with_one_hyphen = mostly_zipcode_without_hyphen = mostly_zipcode_with_two_hyphen = mostly_zipcode_four_digits = requests_made = decimal_integer = string_with_integer_hyphen = string_with_special_characters = integer_with_special_characters = email_with_integer = email_without_integer = print_empty_count = string_dots_no_email_or_website = special_characters_print =email_dominant_column= phone_three_parts_two_hyphens= phone_three_parts_one_hyphen_one_parantheses=phone_three_parts_plus_one=phone_11_digits=phone_10_digits=row_count=0
		states = [ "AK","Alaska","AL","Alabama","AR","Arkansas","AS","American Samoa","AZ","Arizona","CA","California","CO","Colorado","CT","Connecticut","DC","District of Columbia","DE","Delaware","FL","Florida","GA","Georgia","GU","Guam","HI","Hawaii","IA","Iowa","ID","Idaho","IL","Illinois","IN","Indiana","KS","Kansas","KY","Kentucky","LA","Louisiana","MA","Massachusetts","MD","Maryland","ME","Maine","MI","Michigan","MN","Minnesota","MO","Missouri","MS","Mississippi","MT","Montana","NC","North Carolina","ND","North Dakota","NE","Nebraska","NH","New Hampshire","NJ","New Jersey","NM","New Mexico","NV","Nevada","NY","New York","OH","Ohio","OK","Oklahoma","OR","Oregon","PA","Pennsylvania","PR","Puerto Rico","RI","Rhode Island","SC","South Carolina","SD","South Dakota","TN","Tennessee","TX","Texas","UT","Utah","VA","Virginia","VI","Virgin Islands","VT","Vermont","WA","Washington","WI","Wisconsin","WV","West Virginia","WY","Wyoming" ]
		state_code_array = ["AK","AL","AR","AS","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","PR","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]
		states_and_cities = ["Wyoming","Minnesota","California","Georgia","Kansas","Vermont","Indiana","Pennsylvania","Alabama","New York","Florida","Ohio","Texas","Maryland","Louisiana","Missouri","WY","MN","CA","GA","KS","VT","IN","PA","AL","NY","FL","OH","TX","MD","LA"]

		for t in range(0,len(states)-1):
			lower_states.append(states[t].lower())
		for t in range(0,len(states)-1):
			upper_states.append(states[t].upper())

		pattern_string = re.compile("[a-zA-Z]")
		pattern_caps = re.compile("[A-Z]")
		pattern_small = re.compile("[a-z]")
		pattern_integer = re.compile("[0-9]")
		pattern_email = re.compile("[\w+|\W+]@[\w+|\W+]")
		pattern_phone = re.compile("-")
		pattern_phone_three_parts_two_hyphens=re.compile("\d{3}-\d{3}-\d{4}")
		pattern_phone_three_parts_one_hyphen_one_parantheses=re.compile("\(\d{3}\) \d{3}-\d{4}")
		pattern_phone_three_parts_plus_one=re.compile("\+1 \d{3} \d{3} \d{4}")
		pattern_phone_11_digits=re.compile("\d{11}")
		pattern_phone_10_digits=re.compile("\d{10}")
		pattern_empty = re.compile("^\s*$")
		pattern_no_entry = re.compile("^(?![\s\S])")
		pattern_website = re.compile("www+|WWW+")
		pattern_dot = re.compile("[.]")
		pattern_word_after_dot = re.compile("[.][a-zA-Z]")
		pattern_http = re.compile("http")
		pattern_space = re.compile("[\w+|\W+]\s[\w+|\W+]")
		pattern_hashtag = re.compile("#")
		pattern_comma = re.compile(",")
		pattern_successive_hyphens = re.compile("--")
		patten_phone_parantheses = re.compile("\(\d+\)|\(\d+|\d+\)|\d+\(\d+\)")
		pattern_slash = re.compile("[\w+|\W+]/[\w+|\W+]")
		pattern_zipcode_one_hyphen = re.compile('^\d{5}-\d{4}$')
		pattern_zipcode_without_hyphen = re.compile('^\d{5}$')
		patter_zipcode_four_digits = re.compile('^\d{4}$')
		pattern_zipcode_two_hyphen = re.compile('^\d{5}--\d{4}$')
		pattern_special_characters = re.compile("[!|$|\\\\|/|%|^|+|=|_|*|}|~|\[|\]|:|?|`|<|>|{]")
		pattern_special_characters_website = re.compile("[\\\\|%|^|\||}|`|<|>|{]")
		pattern_special_characters_phone = re.compile("[!|$|\\\\|/|%|^|=|_|*|}|~|\[|\]|:|?|`|<|>|{]")
		pattern_open_parantheses =  re.compile("[()]")
		pattern_close_parantheses = re.compile("[)]")
		pattern_at_the_rate = re.compile("@")
		pattern_uppercase = re.compile("[A-Z]")
		pattern_lowercase = re.compile("[a-z]")


		def print_uppercase_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :
					for i in range(int(globvar),int(globar)):
						find_uppercase = re.findall(pattern_uppercase,row[mylist[i]])						
						row_no_in_original_file += 1							
						if find_uppercase :
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 : 
									global func_count
									func_count += 1							
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE THERE IS UPPERCASE ENTRY IN COLUMN ") 
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")


		def print_empty_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :
					for i in range(int(globvar),int(globar)):
						find_empty = re.findall(pattern_empty,row[mylist[i]])
						find_no_entry = re.findall(pattern_no_entry,row[mylist[i]])
						row_no_in_original_file += 1							
						if find_empty or find_no_entry :					
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 : 
									global func_count
									func_count += 1							
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE THERE IS NO ENTRY IN COLUMN ") 
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
		
		def print_string_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :
					for i in range(int(globvar),int(globar)):
						find_string = re.findall(pattern_string,row[mylist[i]])
						row_no_in_original_file += 1				
						if find_string :
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 :
									global func_count
									func_count += 1	 							
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE A STRING IS PRESENT IN PLACE OF INTEGER IN COLUMN ") 
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")	

		def print_string_without_hyphen_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :
					for i in range(int(globvar),int(globar)):
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_phone = re.findall(pattern_phone,row[mylist[i]])
						row_no_in_original_file += 1				
						if find_string and not find_phone :
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 :
									global func_count
									func_count += 1	 							
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE A STRING (WITHOUT HYPHEN) IS PRESENT IN COLUMN ") 
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")	

		def print_string_only_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :
					for i in range(int(globvar),int(globar)):
						find_string = re.findall(pattern_string,row[mylist[i]])
						row_no_in_original_file += 1				
						if find_string and len(find_string) == len(row[mylist[i]]) :
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 : 
									global func_count
									func_count += 1								
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE ONLY STRING IS PRESENT IN COLUMN ") 
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_string_with_integer_and_space_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :
					for i in range(int(globvar),int(globar)):
						find_string = re.findall(pattern_string,row[mylist[i]])
						row_no_in_original_file += 1				
						if find_string and find_integer and find_space :
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 : 
									global func_count
									func_count += 1								
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE A STRING WITH INTEGER AND SPACE IS PRESENT IN COLUMN ") 
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_integer_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						row_no_in_original_file += 1								
						if find_integer and len(find_integer)!=len(row[mylist[i]]):
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1										
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE AN INTEGER(BUT NOT ONLY INTEGER) IS PRESENT IN COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_integer_only_entries():
			with open(filename,'rU') as data :		
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])
						row_no_in_original_file += 1								
						if find_integer and not find_string and len(find_integer)==len(row[mylist[i]]) :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1								
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE A PURE INTEGER IS PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_improper_decimal_integers():
			with open(filename,'rU') as data :		
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						row_no_in_original_file += 1

						if find_integer and not find_string and len(find_dot) != counter_decimal_integer.most_common(1)[0][0]:
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1								
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE IMPROPER DECIMAL INTEGER IS PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")												

		def improper_integer_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):
						find_space = re.findall(pattern_space,row[mylist[i]])
						find_empty = re.findall(pattern_empty,row[mylist[i]])
						find_phone = re.findall(pattern_phone,row[mylist[i]])
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_hashtag = re.findall(pattern_hashtag,row[mylist[i]])
						find_pattern_phone_parantheses = re.findall(patten_phone_parantheses,row[mylist[i]])	
						find_slash = re.findall(pattern_slash,row[mylist[i]])	
						row_no_in_original_file += 1													
						if len(find_phone) == 1 and len(find_integer) != 10 and not find_string and not find_hashtag and not find_pattern_phone_parantheses and not find_slash :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 :
									global func_count
									func_count += 1								
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE AN UNCERTAIN INTEGER ENTRY IS PRESENT  IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_email_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)				
				row_no_in_original_file = 0	
				defective_rows = 0	
				for row in real_data :							
					for i in range(int(globvar),int(globar)):				
						find_email = re.findall(pattern_email,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						find_space = re.findall(pattern_space,row[mylist[i]])
						row_no_in_original_file += 1
														
						if find_email and find_dot and not find_space :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 :
									global func_count									
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE AN EMAIL IS PRESENT IN PLACE OF STRING IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")						

		def print_website_entries():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_website = re.findall(pattern_website,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						row_no_in_original_file += 1								
						if find_website and find_dot:
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE A WEBSITE IS PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_special_characters():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_special_characters=re.findall(pattern_special_characters,row[mylist[i]])
						row_no_in_original_file += 1
						if find_special_characters :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE A SPECIAL CHARACTER IS PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_special_characters_phone():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_special_characters_phone=re.findall(pattern_special_characters_phone,row[mylist[i]])
						row_no_in_original_file += 1
						if find_special_characters_phone :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE A SPECIAL CHARACTER (unlikely for telephone no) IS PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")	


		def print_special_characters_website():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_special_characters_website=re.findall(pattern_special_characters_website,row[mylist[i]])
						row_no_in_original_file += 1
						if find_special_characters_website :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE A SPECIAL CHARACTER (unlikely for website) IS PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")															

		def print_hyphen():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_phone=re.findall(pattern_phone,row[mylist[i]])
						row_no_in_original_file += 1
						if find_phone :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE A HYPHEN IS PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
			return func_count								

		def print_space_entries() :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_space = re.findall(pattern_space,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						row_no_in_original_file += 1								
						if (find_string and find_space) or (find_integer and find_space):
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE SPACE IS PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_no_dots() :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						row_no_in_original_file += 1								
						if (find_string and not find_dot) :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE NO DOTS WERE PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
		
		def print_pure_integer_not_zipcode() :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	

				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_phone = re.findall(pattern_phone,row[mylist[i]])
						find_zipcode_without_hyphen= re.findall(pattern_zipcode_without_hyphen,row[mylist[i]])	
						find_zipcode_four_digits=re.findall(patter_zipcode_four_digits,row[mylist[i]])				
						find_dot = re.findall(pattern_dot,row[mylist[i]])

						row_no_in_original_file += 1						
						if find_integer and not find_phone and not find_zipcode_without_hyphen and not find_zipcode_four_digits and not find_string and not find_dot:
							# print "ERERERWE"
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE PURE INTEGER (but not zipcode) IS PRESENT IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")								

		def print_integer_more_than_string() :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])					
						row_no_in_original_file += 1								
						if (len(find_integer) > len(find_string) and not find_website) :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE INTEGERS DOMINATE STRING IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_string_more_than_integer() :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :			
					for i in range(int(globvar),int(globar)):				
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])					
						row_no_in_original_file += 1								
						if (len(find_string) > len(find_integer)) :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE STRING DOMINATE INTEGER IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_not_state_code() :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1										
						if (row[mylist[i]] in states) or (row[mylist[i]] in lower_states) or (row[mylist[i]] in upper_states)or (row[mylist[i]] == " ") or (row[mylist[i]] == "") :
							pass					
						else :
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 :
									# print "Defective",row[mylist[i]] 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE THE ENTRY IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE IS NOT A US STATE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_symbols() :
			print_string_with_symbol_at_but_not_email()
			print_string_with_parantheses()
			print_integer_with_symbol_at_but_not_email()
			print_integer_with_symbol_at_and_dot()
			print_integer_with_parantheses()
			print_string_with_hashtag_without_space()
			print_integer_with_hashtag_without_space()			

		def print_string_with_symbol_at_but_not_email () :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)				
				row_no_in_original_file = 0	
				defective_rows = 0
				for row in real_data :					
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1
						global func_count
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_at_the_rate=re.findall(pattern_at_the_rate,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						
						if find_string and find_at_the_rate and not find_dot :							
							#print "defective_rowspoi:,",defective_rows
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 :
									# print "Defective",row[mylist[i]] 
									# global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE @ IS FOUND (alongside strings) IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE \n")
									fp.write("***************************************************************************************\n")								
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_string_with_hashtag_without_space () :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)				
				row_no_in_original_file = 0	
				defective_rows = 0
				for row in real_data :					
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1
						global func_count
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_hashtag = re.findall(pattern_hashtag,row[mylist[i]])
						find_space = re.findall(pattern_space,row[mylist[i]])						

						if find_string and find_hashtag and not find_space :							
							#print "defective_rowspoi:,",defective_rows
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 :
									# print "Defective",row[mylist[i]] 
									# global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE # IS FOUND (alongside strings) IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE \n")
									fp.write("***************************************************************************************\n")								
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_integer_with_hashtag_without_space () :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)				
				row_no_in_original_file = 0	
				defective_rows = 0
				for row in real_data :					
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1
						global func_count
						find_integer = re.findall(pattern_integer,row[mylist[i]])						
						find_hashtag = re.findall(pattern_hashtag,row[mylist[i]])
						find_space = re.findall(pattern_space,row[mylist[i]])						

						if find_integer and find_hashtag and not find_space :							
							#print "defective_rowspoi:,",defective_rows
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 :
									# print "Defective",row[mylist[i]] 
									# global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE # IS FOUND (alongside integers) IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE \n")
									fp.write("***************************************************************************************\n")								
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
						
		def print_string_with_parantheses ():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)				
				row_no_in_original_file = 0	
				defective_rows = 0
				for row in real_data :					
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1
						global func_count
						find_string = re.findall(pattern_string,row[mylist[i]])						
						find_open_parantheses=re.findall(pattern_open_parantheses,row[mylist[i]])
						find_close_paranthses=re.findall(pattern_close_parantheses,row[mylist[i]])							

						if (find_string and find_open_parantheses) or (find_string and find_close_paranthses):							
							#print "defective_rows:,",defective_rows							
							with open('improperData.txt','a') as fp :								
								defective_rows+=1
								if defective_rows == 1 :									
									# print "Defective",row[mylist[i]] 
									# global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE PARANTHESES IS FOUND (alongside strings) IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE \n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
		
		def print_integer_with_symbol_at_but_not_email ():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)				
				row_no_in_original_file = 0	
				defective_rows = 0
				for row in real_data :					
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1
						global func_count
						find_integer = re.findall(pattern_integer,row[mylist[i]])						
						find_at_the_rate=re.findall(pattern_at_the_rate,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])						

						if find_integer and find_at_the_rate and not find_dot :															
							defective_rows+=1
							with open('improperData.txt','a') as fp :
								
								if defective_rows == 1 :
									# print "Defective",row[mylist[i]] 
									# global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE @ IS FOUND (alongside integers) IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE \n")
									fp.write("***************************************************************************************\n")								
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

						# print "defective_rows:,",defective_rows

		def print_integer_with_symbol_at_and_dot ():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)				
				row_no_in_original_file = 0	
				defective_rows = 0
				for row in real_data :					
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1
						global func_count
						find_integer = re.findall(pattern_integer,row[mylist[i]])			
						find_at_the_rate=re.findall(pattern_at_the_rate,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])				

						if find_integer and find_at_the_rate and find_dot and not find_string :													
							defective_rows+=1
							with open('improperData.txt','a') as fp :						
								if defective_rows == 1 :
									# print "Defective",row[mylist[i]] 
									# global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE @ IS FOUND (alongside decimal integers) IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE \n")
									fp.write("***************************************************************************************\n")								
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")		

		def print_integer_with_parantheses  ():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)				
				row_no_in_original_file = 0	
				defective_rows = 0
				for row in real_data :					
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1
						global func_count
						find_integer = re.findall(pattern_integer,row[mylist[i]])						
						find_open_parantheses=re.findall(pattern_open_parantheses,row[mylist[i]])
						find_close_paranthses=re.findall(pattern_close_parantheses,row[mylist[i]])

						if (find_integer and find_open_parantheses) or (find_integer and find_close_paranthses):							
							defective_rows+=1
							with open('improperData.txt','a') as fp :															
								if defective_rows == 1 :									
									# print "Defective",row[mylist[i]] 
									# global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE PARANTHESES IS FOUND (alongside integers) IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE \n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")							

		def print_decimal_values():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)				
				row_no_in_original_file = 0	
				defective_rows = 0
				for row in real_data :					
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1
						global func_count
						find_integer = re.findall(pattern_integer,row[mylist[i]])												
						find_zipcode_without_hyphen= re.findall(pattern_zipcode_without_hyphen,row[mylist[i]])
						find_zipcode_four_digits=re.findall(patter_zipcode_four_digits,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])

						if find_integer and not find_zipcode_without_hyphen and not find_zipcode_four_digits and not find_string and find_dot:
							defective_rows+=1
							with open('improperData.txt','a') as fp :															
								if defective_rows == 1 :									
									# print "Defective",row[mylist[i]] 
									# global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE DECIMAL INTEGER IS FOUND IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE \n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_state_code() :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1										
						if (row[mylist[i]] in state_code_array) and (row[mylist[i]] not in states_and_cities) :	
							for j in range(i+1,len(row)):
								key = (row[mylist[i]], row[mylist[j]])
								if key[0] == key[1] :	
									with open('improperData.txt','a') as fp :
										defective_rows+=1
										if defective_rows == 1 : 
											global func_count
											func_count += 1	
											fp.write("***************************************************************************************\n")
											fp.write("THIS ROW IS PRINTED BECAUSE THE ENTRY IN THE COLUMN ") 
											fp.write(mylist[a])
											fp.write(" OF THE CSV FILE IS A US STATE\n")
											fp.write("***************************************************************************************\n")
										fp.write(str(row)+ "\n")
										fp.write("Defective row No:")
										fp.write(str(defective_rows) + "\n")
										new_row_no_in_original_file = row_no_in_original_file + 1
										fp.write("Row no in original file is ")
										fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
						else : 
							pass

		def print_state_code_lowercase() :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :					
					for i in range(int(globvar),int(globar)):										
						row_no_in_original_file += 1
						find_lowercase = re.findall(pattern_lowercase,row[mylist[i]])						
						if (row[mylist[i]].upper() in state_code_array) and find_lowercase:
							print "HERE"
							# for j in range(i+1,len(row)):
							# 	key = (row[mylist[i]], row[mylist[j]])
							# 	print "key is",key
							# 	if key[0] == key[1] :	
							with open('improperData.txt','a') as fp :
								defective_rows+=1
								if defective_rows == 1 : 
									global func_count
									func_count += 1	
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE THE ENTRY IN THE COLUMN ") 
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE IS A US STATE ,BUT IN LOWERCASE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
						else : 
							pass							
			
		def print_zip_code() :
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)
				defective_rows = 0
				row_no_in_original_file = 0	
				for row in real_data :
					for i in range(int(globvar),int(globar)):				
						row_no_in_original_file += 1
						find_phone = re.findall(pattern_phone,row[mylist[i]])
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						find_pattern_phone_parantheses = re.findall(patten_phone_parantheses,row[mylist[i]])
						find_successive_hyphens =re.findall(pattern_successive_hyphens,row[mylist[i]])
						find_hashtag = re.findall(pattern_hashtag,row[mylist[i]])
						find_slash = re.findall(pattern_slash,row[mylist[i]])
						find_space = re.findall(pattern_space,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])				

						if len(find_phone) == 1 and len(find_integer) < 10 and not find_string and not find_hashtag and not find_pattern_phone_parantheses and not find_slash and not find_space  :
							
							y = row[mylist[i]].split("-")[0]
							
							for j in range(0,len(zipcodes)-1):						
								if y == zipcodes[j] :
									if(len(y)>3):
										for k in range(0,len(mylist)-1):
											if zipcodes[j+3] == row[mylist[k]]:
												with open('improperData.txt','a') as fp :
													defective_rows+=1
													if defective_rows == 1 :
														global func_count
														func_count += 1	 								
														fp.write("***************************************************************************************\n")
														fp.write("THIS ROW IS PRINTED BECAUSE THE ENTRY IN THE COLUMN ") 
														fp.write(mylist[a])
														fp.write(" OF THE CSV FILE IS POSSIBLY A ZIP CODE WITH A HYPHEN\n")
														fp.write("***************************************************************************************\n")
													fp.write(str(row)+ "\n" + "\n")
													fp.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
													fp.write("Zipcode ")
													fp.write(str(row[mylist[i]]) + " ")
													fp.write("belongs to ")
													fp.write(zipcodes[j+1])
													fp.write(" in the state of ")
													fp.write(zipcodes[j+2] + "\n")
													fp.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
													fp.write("Defective row No:")
													fp.write(str(defective_rows) + "\n")
													new_row_no_in_original_file=row_no_in_original_file + 1
													fp.write("Row no in original file is ")
													fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
								else :
									pass

						elif len(find_integer) == 5 and not find_phone and not find_hashtag and not find_dot and not find_string and not find_space :
							for j in range(0,len(zipcodes)-1):
								if row[mylist[i]] == zipcodes[j] :
									for k in range(0,len(mylist)-1):
										if zipcodes[j+3] == row[mylist[k]]:							
											defective_rows+=1
											with open('improperData.txt','a') as fp :
												if defective_rows == 1 :											
													func_count += 1										
													fp.write("***************************************************************************************\n")			
													fp.write("THIS ROW IS PRINTED BECAUSE THE ENTRY IN THE COLUMN ") 
													fp.write(mylist[a])
													fp.write(" OF THE CSV FILE IS POSSIBLY A ZIP CODE \n")
													fp.write("***************************************************************************************\n")			
												fp.write(str(row)+ "\n" + "\n")
												fp.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
												fp.write("Zipcode ")
												fp.write(str(row[mylist[i]]) + " ")
												fp.write("belongs to ")
												fp.write(zipcodes[j+1])
												fp.write(" in the state of ")
												fp.write(zipcodes[j+2] + "\n")
												fp.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
												fp.write("Defective row No:")
												fp.write(str(defective_rows) + "\n")
												new_row_no_in_original_file = row_no_in_original_file + 1
												fp.write("Row no in original file is ")
												fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
								else :
									pass
						elif len(find_integer) == 4 and not find_phone and not find_hashtag and not find_dot and not find_string and not find_space :
							c = "0" + row[mylist[i]]
							for j in range(0,len(zipcodes)-1):
								if c == zipcodes[j] :
									for k in range(0,len(mylist)-1):
										if zipcodes[j+3] == row[mylist[k]]:											
											defective_rows+=1
											with open('improperData.txt','a') as fp :
												if defective_rows == 1 :											
													func_count += 1										
													fp.write("***************************************************************************************\n")			
													fp.write("THIS ROW IS PRINTED BECAUSE THE ENTRY IN THE COLUMN ") 
													fp.write(mylist[a])
													fp.write(" OF THE CSV FILE IS POSSIBLY A ZIP CODE \n")
													fp.write("***************************************************************************************\n")			
												fp.write(str(row)+ "\n" + "\n")
												fp.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
												fp.write("Zipcode ")
												fp.write(str(row[mylist[i]]) + " ")
												fp.write("belongs to ")
												fp.write(zipcodes[j+1])
												fp.write(" in the state of ")
												fp.write(zipcodes[j+2] + "\n")
												fp.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
												fp.write("Defective row No:")
												fp.write(str(defective_rows) + "\n")
												new_row_no_in_original_file = row_no_in_original_file + 1
												fp.write("Row no in original file is ")
												fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
								else: 
									pass

						else : 
							pass										

		def print_duplicate_email_entries():
			# print "email_array is :",email_array			
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0
				duplicate_emails = [k for k,v in Counter(email_array).items() if v>1]							
				# print "*************************************************************"
				# print "Duplicate emails are:",duplicate_emails
				# print "*************************************************************"
				# for i in range(int(globvar),int(globar)):
				if len(duplicate_emails) > 0 :							
					for row in real_data :
						row_no_in_original_file += 1
						for x in range(0,len(duplicate_emails))	:
							if duplicate_emails[x] in str(row) :						
								with open('improperData.txt','a') as fp :							
									defective_rows += 1
									if defective_rows == 1 :
										global func_count
										func_count += 1								
										fp.write("***************************************************************************************\n")
										fp.write("THIS ROW IS PRINTED BECAUSE THE EMAIL ENTRY IN THE COLUMN ")
										fp.write(mylist[a])
										fp.write(" IS DUPLICATED \n")
										fp.write("***************************************************************************************\n")
									fp.write(str(row)+ "\n")
									fp.write("Defective row No:")
									fp.write(str(defective_rows) + "\n")
									new_row_no_in_original_file = row_no_in_original_file + 1
									fp.write("Row no in original file is ")
									fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_improper_email_entries():
			print_email_with_more_than_one_at()
			print_email_with_space()
			print_email_without_dot()
			print_string_without_email()

		def print_email_with_more_than_one_at():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				global func_count
				for row in real_data :			
					for i in range(int(globvar),int(globar)):	
						find_string = re.findall(pattern_string,row[mylist[i]])			
						find_space = re.findall(pattern_space,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						find_email = re.findall(pattern_email,row[mylist[i]])
						row_no_in_original_file += 1
						# print "find_email length:", len(find_email)
						if len(find_email) >=2 :
							with open('improperData.txt','a') as fp :
								defective_rows += 1
								if defective_rows == 1 :
									
									func_count += 1								
									fp.write("***************************************************************************************\n")
									fp.write("THIS ROW IS PRINTED BECAUSE @ OCCURS TWICE IN THE COLUMN ")
									fp.write(mylist[a])
									fp.write(" OF THE CSV FILE\n")
									fp.write("***************************************************************************************\n")
								fp.write(str(row)+ "\n")
								fp.write("Defective row No:")
								fp.write(str(defective_rows) + "\n")
								new_row_no_in_original_file = row_no_in_original_file + 1
								fp.write("Row no in original file is ")
								fp.write(str(new_row_no_in_original_file)+"\n" + "\n")

		def print_email_with_space():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				global func_count
				for row in real_data :			
					for i in range(int(globvar),int(globar)):	
						find_string = re.findall(pattern_string,row[mylist[i]])			
						find_space = re.findall(pattern_space,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						find_email = re.findall(pattern_email,row[mylist[i]])
						row_no_in_original_file += 1
					if find_string and find_email and find_dot and find_space :
						with open('improperData.txt','a') as fp :
							defective_rows += 1
							if defective_rows == 1 :								
								func_count += 1								
								fp.write("***************************************************************************************\n")
								fp.write("THIS ROW IS PRINTED BECAUSE AN EMPTY SPACE IS PRESENT IN PLACE OF EMAIL IN THE COLUMN ")
								fp.write(mylist[a])
								fp.write(" OF THE CSV FILE\n")
								fp.write("***************************************************************************************\n")
							fp.write(str(row)+ "\n")
							fp.write("Defective row No:")
							fp.write(str(defective_rows) + "\n")
							new_row_no_in_original_file = row_no_in_original_file + 1
							fp.write("Row no in original file is ")
							fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
						
		def print_email_without_dot():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				global func_count
				for row in real_data :			
					for i in range(int(globvar),int(globar)):	
						find_string = re.findall(pattern_string,row[mylist[i]])			
						find_space = re.findall(pattern_space,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						find_email = re.findall(pattern_email,row[mylist[i]])
						row_no_in_original_file += 1
					if find_email and not find_dot :
						with open('improperData.txt','a') as fp :
							defective_rows += 1
							if defective_rows == 1 : 
								
								func_count += 1								
								fp.write("***************************************************************************************\n")
								fp.write("THIS ROW IS PRINTED BECAUSE DOT IS NOT PRESENT IN THE COLUMN ")
								fp.write(mylist[a])
								fp.write(" OF THE CSV FILE\n")
								fp.write("***************************************************************************************\n")
							fp.write(str(row)+ "\n")
							fp.write("Defective row No:")
							fp.write(str(defective_rows) + "\n")
							new_row_no_in_original_file = row_no_in_original_file + 1
							fp.write("Row no in original file is ")
							fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
						
		def print_string_without_email():
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				global func_count
				for row in real_data :			
					for i in range(int(globvar),int(globar)):	
						find_string = re.findall(pattern_string,row[mylist[i]])			
						find_space = re.findall(pattern_space,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						find_email = re.findall(pattern_email,row[mylist[i]])
						row_no_in_original_file += 1
					if find_string and not find_email :
						with open('improperData.txt','a') as fp :
							defective_rows += 1
							if defective_rows == 1 :								
								func_count += 1	 							
								fp.write("***************************************************************************************\n")
								fp.write("THIS ROW IS PRINTED BECAUSE @ IS NOT PRESENT IN THE COLUMN ")
								fp.write(mylist[a])
								fp.write(" OF THE CSV FILE\n")
								fp.write("***************************************************************************************\n")
							fp.write(str(row)+ "\n")
							fp.write("Defective row No:")
							fp.write(str(defective_rows) + "\n")
							new_row_no_in_original_file = row_no_in_original_file + 1
							fp.write("Row no in original file is ")
							fp.write(str(new_row_no_in_original_file)+"\n" + "\n")	

		def print_string_with_dots_not_email_not_website():	
			with open(filename,'rU') as data :
				real_data = csv.DictReader(data)	
				defective_rows = 0
				row_no_in_original_file = 0	
				global func_count
				for row in real_data :			
					for i in range(int(globvar),int(globar)):	
						find_string = re.findall(pattern_string,row[mylist[i]])			
						find_space = re.findall(pattern_space,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						find_email = re.findall(pattern_email,row[mylist[i]])
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						find_empty = re.findall(pattern_empty,row[mylist[i]])
						find_no_entry = re.findall(pattern_no_entry,row[mylist[i]])
						row_no_in_original_file += 1
		 			if (find_string and find_integer and not find_empty and not find_no_entry  and find_dot and not find_email and not find_website) or (find_string and not find_integer and not find_empty and find_dot and not find_email and not find_website and not find_no_entry):
						with open('improperData.txt','a') as fp :
							defective_rows += 1
							if defective_rows == 1 :								
								func_count += 1	 							
								fp.write("***************************************************************************************\n")
								fp.write("THIS ROW IS PRINTED BECAUSE DOT IS PRESENT IN THE COLUMN ")
								fp.write(mylist[a])
								fp.write(" OF THE CSV FILE\n")
								fp.write("***************************************************************************************\n")
							fp.write(str(row)+ "\n")
							fp.write("Defective row No:")
							fp.write(str(defective_rows) + "\n")
							new_row_no_in_original_file = row_no_in_original_file + 1
							fp.write("Row no in original file is ")
							fp.write(str(new_row_no_in_original_file)+"\n" + "\n")															

		#this loop checks for any extra commas which might cause an error prone data
		with open(filename,'rU') as data :
			r = csv.reader(open(filesname, "rU"), dialect=csv.excel_tab)
			line1=r.next()	
			arrt = []
			for element in line1:
				mylist = element.split(',')	
			real_data = csv.DictReader(data)
			defective_rows = 0
			row_no_in_original_file = 0					
			for row in real_data :					
				row_no_in_original_file += 1	
				if (len(row) != len(mylist)) :
					# open('improperData.txt', 'w').close()
					defective_rows += 1
					with open('improperData.txt','a') as fp :
						count+=1
						if count == 1:
							# pass
							fp.write("***************************************************************************************\n")
							fp.write("THESE ROWS ARE PRINTED BECAUSE THEY HAVE IMPERFECT COMMAS\n")
							fp.write("***************************************************************************************\n")
						fp.write(str(row)+ "\n")
						fp.write("Defective row No:")
						fp.write(str(defective_rows) + "\n")
						new_row_no_in_original_file = row_no_in_original_file + 1
						fp.write("Row no in original file is ")
						fp.write(str(new_row_no_in_original_file)+"\n" + "\n")
					
				if (len(row) == len(mylist)) :
					# open('improperData.txt', 'w').close()
					counter+=1									
					for i in range(int(globvar),int(globar)):
						a = i
						b = i+1				
						find_string = re.findall(pattern_string,row[mylist[i]])
						find_integer = re.findall(pattern_integer,row[mylist[i]])
						find_email = re.findall(pattern_email,row[mylist[i]])
						find_phone = re.findall(pattern_phone,row[mylist[i]])
						find_phone_three_parts_two_hyphens = re.findall(pattern_phone_three_parts_two_hyphens,row[mylist[i]])
						find_phone_three_parts_one_hyphen_one_parantheses = re.findall(pattern_phone_three_parts_one_hyphen_one_parantheses,row[mylist[i]])
						find_pattern_phone_three_parts_plus_one=re.findall(pattern_phone_three_parts_plus_one,row[mylist[i]])
						find_pattern_phone_11_digits = re.findall(pattern_phone_11_digits,row[mylist[i]])
						find_pattern_phone_10_digits = re.findall(pattern_phone_10_digits,row[mylist[i]])
						find_empty = re.findall(pattern_empty,row[mylist[i]])
						find_no_entry = re.findall(pattern_no_entry,row[mylist[i]])						
						find_website = re.findall(pattern_website,row[mylist[i]])
						find_dot = re.findall(pattern_dot,row[mylist[i]])
						find_http = re.findall(pattern_http,row[mylist[i]])
						find_space = re.findall(pattern_space,row[mylist[i]])
						find_caps = re.findall(pattern_caps,row[mylist[i]])
						find_word_after_dot = re.findall(pattern_word_after_dot,row[mylist[i]])
						find_hashtag = re.findall(pattern_hashtag,row[mylist[i]])
						find_comma = re.findall(pattern_comma,row[mylist[i]])
						find_successive_hyphens =re.findall(pattern_successive_hyphens,row[mylist[i]])
						find_pattern_phone_parantheses = re.findall(patten_phone_parantheses,row[mylist[i]])
						find_slash = re.findall(pattern_slash,row[mylist[i]])
						find_small = re.findall(pattern_small,row[mylist[i]])
						find_zipcode_one_hyphen=re.findall(pattern_zipcode_one_hyphen,row[mylist[i]])
						find_zipcode_without_hyphen= re.findall(pattern_zipcode_without_hyphen,row[mylist[i]])
						find_zipcode_two_hyphen=re.findall(pattern_zipcode_two_hyphen,row[mylist[i]])
						find_zipcode_four_digits=re.findall(patter_zipcode_four_digits,row[mylist[i]])
						find_special_characters=re.findall(pattern_special_characters,row[mylist[i]])
						find_special_characters_phone=re.findall(pattern_special_characters_phone,row[mylist[i]])
						find_special_characters_website=re.findall(pattern_special_characters_website,row[mylist[i]])
						find_open_parantheses=re.findall(pattern_open_parantheses,row[mylist[i]])
						find_close_paranthses=re.findall(pattern_close_parantheses,row[mylist[i]])
						find_at_the_rate=re.findall(pattern_at_the_rate,row[mylist[i]])
						find_uppercase = re.findall(pattern_uppercase,row[mylist[i]])
						find_lowercase = re.findall(pattern_lowercase,row[mylist[i]])

						if find_string :
							if find_string and find_integer and find_space:						
								print row[mylist[i]],"is string with integer and spaces"
								string_with_integer_spaces+=1
							elif find_string and find_special_characters :
								string_with_special_characters+=1
								print row[mylist[i]],"is string with special characters"
							elif (find_string and find_http and find_slash and find_dot) or (find_string and find_http and find_slash and find_dot and find_integer):
								print row[mylist[i]],"is possible website with http and slash"
								website+=1
							elif find_string and find_dot and find_integer and find_email and not find_empty and not find_no_entry:
								print row[mylist[i]],"is possible email with integer"
								email_with_integer+=1
								email_array.append(row[mylist[i]])
							elif find_string and not find_space and find_integer and not find_email and not find_website and not find_dot and not find_phone:
								print row[mylist[i]],"is string with integer without spaces"
								string_with_integer_without_spaces+=1
							elif find_string and not find_integer and not find_empty and not find_no_entry and not find_email and not find_http and not find_dot and not find_caps and row[mylist[i]] not in lower_states and row[mylist[i]] not in upper_states :
								print row[mylist[i]],"is string without integer and without spaces"
								string_without_integer_without_spaces+=1
							elif find_string and find_email and find_dot and not find_empty and not find_integer and not find_no_entry:
								print row[mylist[i]],"is possible email but without integer"
								email_without_integer+=1
								email_array.append(row[mylist[i]])
							elif find_string and find_email and not find_dot :
								print row[mylist[i]],"is string with @ instead of at"
								string_with_symbol_instead_of_at+=1
							elif (find_string and find_website and find_dot and find_word_after_dot and not find_space) or (find_string and find_word_after_dot and find_http and find_dot and not find_space and len(find_dot) > 1) :
								print row[mylist[i]],"is possible website"
								website+=1
							elif (find_string and find_website and find_dot and find_word_after_dot and not find_space) or (find_string and find_word_after_dot and find_http and find_dot and not find_space and len(find_dot) > 1) :
								print row[mylist[i]],"could be website but contains only one dot instead of two"
								website+=1
							elif find_space and find_string and not find_integer :
								print row[mylist[i]],"is string with spaces but no integer"
								string_with_space_no_integer+=1
							elif find_string and find_phone and find_integer and not find_dot and len(find_integer) >= 6 :						
								print row[mylist[i]],"is possible phone no but with alphabets"
								phone_no_with_alphabets+=1
							elif find_string and find_phone and find_integer and not find_dot and len(find_integer) < 6 :
								print row[mylist[i]],"is Mixture of string integer and hyphen"
								string_with_integer_hyphen += 1

							if find_string and find_dot and not find_website and not find_email and  find_word_after_dot and not find_slash and not find_space and not find_hashtag and not find_comma and (len(find_string) > 5):								
								if len(find_dot) > 1 :
									x = [j for j,val in enumerate(row[mylist[i]]) if val=="."]
									if((x[len(x)-1]-x[0]) >= 3) :								
										print row[mylist[i]],"is possible website but without www (2 dot) and without slashes"
										website_without_www+=1
									else :
										print row[mylist[i]],"is string with more than one dot but not website."
										string_with_dots_not_email_not_website+=1

								elif len(find_dot) <= 1 :
									x = [j for j,val in enumerate(row[mylist[i]]) if val=="."]		
									if(len(row[mylist[i]])-x[0] > 4):
										print row[mylist[i]],"is string with one dot but one website"
										string_with_dots_not_email_not_website+=1
									else :
										print row[mylist[i]],"is possible website but without www (1 dot)."
										website_without_www+=1

								else :
									print row[mylist[i]],"is possible website but without www (1 dot) and without slashes"
									website_without_www+=1 


							elif find_string and find_slash and find_dot and not find_website and find_word_after_dot and not find_space and not find_hashtag and not find_comma and (len(find_string) > 5):						
								x = [j for j,val in enumerate(row[mylist[i]]) if val=="."]
								if((x[len(x)-1]-x[0]) >= 3) :
									print row[mylist[i]],"is possible website but without www and with slashes"
									website_without_www+=1

							else :						
								if len(find_caps) and len((find_string)) == 2 and not find_integer and not find_empty and not find_no_entry  and not find_dot and not find_slash and not find_small:		
									matching = [s for s in states if row[mylist[i]] == s] 		
									if matching  :		
										print row[mylist[i]],"is possible state code"
										state_code+=1
									else :
										print row[mylist[i]],"is two lettered uppercase string not state code"
										two_letter_uppercase_string_not_state_code += 1


								if len(find_small) and len((find_string)) == 2 and not find_integer and not find_empty and not find_dot and not find_no_entry and not find_slash:			
									matching_lower = [s for s in lower_states if row[mylist[i]] == s]
									if matching_lower :		
										print row[mylist[i]],"is possible state code in lowercase"
										state_code+=1
									else :
										print row[mylist[i]],"is two lettered lowercase string not state code"
										two_letter_lowercase_string_not_state_code += 1

								if len(find_caps) == len(find_string) and len(find_string) > 2 and not find_integer and not find_empty and not find_no_entry and not find_dot and not find_slash:			
									matching_upper = [s for s in upper_states if row[mylist[i]] == s]

									if matching_upper :								
										print row[mylist[i]],"is possible state name in capital letters"
										state_code+=1
									else :
										print row[mylist[i]],"is uppercase string"
										two_letter_uppercase_string_not_state_code += 1

								elif (find_string and find_integer and not find_empty and not find_no_entry and find_dot and not find_email) or (find_string and not find_integer and not find_empty and find_dot and not find_email and not find_website):
									print row[mylist[i]],"is string with dot but not email"
									string_with_dots_not_email_not_website += 1
								elif len(find_caps) == 1 and not find_integer and not find_empty and not find_no_entry and not find_dot and not find_slash and len(find_string) > 1:
									print row[mylist[i]],"is string with single caps with no integer or spaces."
									string_without_integer_without_spaces += 1
								elif len(find_caps) == 1 and not find_integer and not find_empty and not find_no_entry and not find_dot and not find_slash and len(find_string) == 1:
									print row[mylist[i]],"is string of unit length with single caps."
									string_without_integer_without_spaces += 1
								elif len(find_string) > 2 and len(find_caps) == len(find_string) and not find_integer and not find_empty and not find_no_entry and not find_dot and not find_slash:
									print row[mylist[i]],"is pure uppercase string with more than 2 characters"
									pure_uppercase_string+=1
								elif find_caps and len(find_caps) != len(find_string) and not find_integer and not find_empty and not find_no_entry and not find_dot and not find_slash and not find_space:
									print row[mylist[i]],"is string with capital letters but not state code nor pure uppercase"
									string_without_integer_without_spaces += 1

						if find_integer :
							if find_phone :
								if(find_zipcode_one_hyphen):
									c = row[mylist[i]].split("-")
									if c[0] in zipcodes :
										print row[mylist[i]], "is Most probably a zipcode with one hyphen"
										# zipcode_array.append(row[mylist[i]])
										mostly_zipcode_with_one_hyphen += 1	
									else :
										print row[mylist[i]], "has one hyphen but is not a zipcode."
										pure_integer += 1

								if(find_zipcode_two_hyphen) :
									c = row[mylist[i]].split("--")
									if c[0] in zipcodes :
										print row[mylist[i]], "is Most probably a zipcode with two hyphen"
										mostly_zipcode_with_two_hyphen += 1

								# if len(find_phone) == 2 and len(find_integer) == 10 and not find_successive_hyphens and len(find_integer) > len(find_string):
								# 		print row[mylist[i]],"is possible phone no because of two hyphens"
								# 		phone_no_two_hyphens+=1	
								if len(find_phone) == 1 and len(find_integer) == 10 and not find_successive_hyphens and len(find_integer) > len(find_string) and find_slash:
										print row[mylist[i]],"is possible phone no but with slash instead of one of the hyphens"
										phone_no_one_hyphen+=1					

								if len(find_phone) == 1 and len(find_integer) != 10 and not find_successive_hyphens and len(find_integer) > len(find_string) and find_slash:
										print row[mylist[i]],"is possible phone no without ten integers but with slash instead of one of the hyphens"
										phone_no_one_hyphen+=1
								if len(find_phone) == 2 and len(find_integer) != 10 and not find_successive_hyphens and not find_string :
									y = row[mylist[i]].split("-")
									if(len(y[0])>3):
										if row[mylist[i]] in zipcodes :
											print row[mylist[i]], "is possible zip codes but with two but not succesive hyphens"
											zipcode_with_two_not_successive_hyphens+=1
									else :
										print row[mylist[i]],"is integers separated by hyphen but not zipcode or phone number"
										integer_seperated_by_hyphen_not_zip_or_phone+=1												
									
								if len(find_phone) == 1 and len(find_integer) == 10 and not find_string and not find_hashtag and find_pattern_phone_parantheses :
									if find_phone_three_parts_one_hyphen_one_parantheses and not find_string :
										print row[mylist[i]],"is phone no with three parts with one hyphen and a parantheseses"
										phone_three_parts_one_hyphen_one_parantheses +=1

									else :
										open_brace = [phone for phone,val in enumerate(row[mylist[i]]) if val=="("]
										close_brace = [phone for phone,val in enumerate(row[mylist[i]]) if val==")"]
										# if open_brace and close_brace :
										# 	print row[mylist[i]],"is phone no with parantheses"					
										# 	phone_no_with_parantheses+=1
										if open_brace and not close_brace :
											print row[mylist[i]],"is phone no with only open parantheses"				
											phone_no_with_only_open_parantheses+=1
										if close_brace and not open_brace :
											print row[mylist[i]],"is phone no with only close parantheses"
											phone_no_with_only_close_parantheses+=1						

								if (len(find_phone) == 1 and len(find_integer) != 10 and not find_string and find_hashtag) or (find_string and find_integer and len(find_space) > 1 and len(find_string) > len(find_integer)):
									print row[mylist[i]],"is possible line1 of address"
									string_first_line_address += 1

								if find_pattern_phone_parantheses and not find_website and not find_string and len(find_integer) == 10 and not find_pattern_phone_10_digits and not find_phone_three_parts_two_hyphens and not find_phone_three_parts_one_hyphen_one_parantheses and not find_pattern_phone_three_parts_plus_one and not find_pattern_phone_11_digits :
									print row[mylist[i]],"is phone no with parantheses"							
									phone_no_with_parantheses+=1

								if find_phone_three_parts_two_hyphens and not find_string :
									print row[mylist[i]], "is phone with two hyphens"
									phone_three_parts_two_hyphens+=1

								# if find_phone_three_parts_one_hyphen_one_parantheses and not find_string :
								# 	print row[mylist[i]], "is phone with one hyphen and one parantheses"
								# 	phone_three_parts_one_hyphen_one_parantheses+=1								

						if find_integer and not find_phone :
							if(find_zipcode_without_hyphen):
								if row[mylist[i]] in zipcodes :
									# for j in range(0,len(zipcodes)-1):
										# a = a.split("-")[0]
										# if row[mylist[i]] == zipcodes[j] :
									print row[mylist[i]], "is most probably a zipcode (without hyphen)" 
											# zipcode_array.append(row[mylist[i]])
									mostly_zipcode_without_hyphen += 1
								else :
									print row[mylist[i]], "is not a Zipcode"
									pure_integer += 1
									zipcode_array.append(row[mylist[i]])
							if(find_zipcode_four_digits):
								c = "0" + row[mylist[i]]
								if c in zipcodes :
									# for j in range(0,len(zipcodes)-1):
										# a = a.split("-")[0]
										# if c == zipcodes[j] :									
									print row[mylist[i]], "is most probably a zipcode (four digits) " 
											# zipcode_array.append(row[mylist[i]])
									mostly_zipcode_four_digits += 1
								else :
									print row[mylist[i]], "is a four digit integer"
									pure_integer += 1

							if not find_zipcode_without_hyphen and not find_zipcode_four_digits and not find_string and find_dot:
								print row[mylist[i]],"is Integer with decimals"
								decimal_integer += 1
								# print "no of dots is",len(find_dot)
								decimal_integer_lengths.append(len(find_dot))
							
							if not find_zipcode_without_hyphen and not find_zipcode_four_digits and not find_string and not find_dot and not find_pattern_phone_10_digits and not find_phone_three_parts_two_hyphens and not find_phone_three_parts_one_hyphen_one_parantheses and not find_pattern_phone_three_parts_plus_one and not find_pattern_phone_11_digits :
								print row[mylist[i]],"is Pure integer"
								pure_integer += 1

							if not find_zipcode_without_hyphen and not find_zipcode_four_digits and not find_string and not find_dot and find_pattern_phone_10_digits and not find_pattern_phone_11_digits:
								print row[mylist[i]],"is 10 digit phone no"
								phone_10_digits += 1

							if find_pattern_phone_three_parts_plus_one and not find_string :
								print row[mylist[i]],"is phone with four parts containing three spaces and +1"
								phone_three_parts_plus_one+=1

							if find_pattern_phone_11_digits and not find_string :
								if row[mylist[i]][0]=="1":
									print row[mylist[i]], "is 11 digit phone no i.e starts with 1 followed by 10 digits"
									phone_11_digits+=1
								else :
									print "11 digit number but not phone no"
									pure_integer+=1

							if find_pattern_phone_10_digits and not find_string :
								phone_10_digits+=1


						if find_integer and find_dot and find_phone and not find_string and row[mylist[i]][0] == "-" :
								print row[mylist[i]],"is Negative integer with decimals"
								decimal_integer += 1
								print "no of dots is",len(find_dot)
								decimal_integer_lengths.append(len(find_dot))

						if find_integer and not find_dot and find_phone and not find_string and row[mylist[i]][0] == "-" :
							print row[mylist[i]],"is Negative integer without decimals"
							pure_integer += 1

						if find_integer and find_special_characters :
							integer_with_special_characters+=1

						if find_empty :
							# print "empty entries are",find_empty
							empty+=1
						# if find_no_entry :
						# 	empty+=1
						#print row[mylist[i]]			
						# #print type(row[mylist[i]])
					# sys.stdout.write(".......................................\n")

			# print "\n!!!!!!!!!\n"
			# print  "\n", count, "rows have imperfect commas"
			if count > 0:
				print "***********************************************************"
				print "Your file has imperfect commas. Please open improperData.txt"
				print "*************************************************************"
			# else:
			# 	print "\nYour file is perfectly comma separated"
			# if string_with_integer_spaces != 0 :
			# 	print "No of string with integer and spaces", string_with_integer_spaces
			# if string_with_integer_without_spaces != 0 :
			# 	print "No of string with integer without spaces", string_with_integer_without_spaces	
			# if string_without_integer_without_spaces != 0 :				
			# 	print "No of string without integer and without spaces / string with single caps with no integer or spaces / string with capital letters but not state code nor pure uppercase", string_without_integer_without_spaces
			# if string_with_dots_not_email_not_website != 0 :
			# 	print "No of string with dot but not email", string_with_dots_not_email_not_website
			# if two_letter_uppercase_string_not_state_code != 0 :
			# 	print "No of two lettered uppercase string not state code", two_letter_uppercase_string_not_state_code
			# if two_letter_lowercase_string_not_state_code != 0 :
			# 	print "No of two lettered lowercase string not state code",two_letter_lowercase_string_not_state_code	
			# if string_with_symbol_instead_of_at != 0 :
			# 	print "No of string with @ instead of at", string_with_symbol_instead_of_at
			# if string_with_integer_hyphen != 0 :
			# 	print "No of string with integer and hyphen", string_with_integer_hyphen
			# if email_without_integer != 0 :
			# 	print "No of possible email without integer",  email_without_integer
			# if email_with_integer != 0 :
			# 	print "No of possible email with integer", email_with_integer
			# if website != 0 :
			# 	print "No of possible website with http and slash/ possible website", website
			# if string_with_space_no_integer != 0 :
			# 	print "No of string with spaces but no integer", string_with_space_no_integer
			# if string_first_line_address != 0 :
			# 	print "No of possible line1 of address" , string_first_line_address
			# if phone_no_with_alphabets != 0 :
			# 	print "No of possible phone no but with alphabets",phone_no_with_alphabets
			# if website_without_www != 0 :
			# 	print "No of possible website but without www and with slashes / possible website but without www (1 dot) and without slashes / possible website but without www (2 dot) and without slashes", website_without_www
			# if state_code != 0 :
			# 	print "No of possible state code", state_code
			# if pure_uppercase_string != 0 :
			# 	print "No of pure uppercase string with more than 2 characters", pure_uppercase_string
			# if phone_no_two_hyphens != 0 :
			# 	print "No of possible phone no because of two hyphens", phone_no_two_hyphens
			# if phone_no_one_hyphen != 0 :
			# 	print "No of possible phone no without ten integers but with slash instead of one of the hyphens / possible phone no but with slash instead of one of the hyphens", phone_no_one_hyphen
			# if phone_no_with_parantheses != 0 :
			# 	print "No of phone no with parantheses", phone_no_with_parantheses
			# if phone_no_without_hyphen_or_alphabets != 0 :
			# 	print "No of possible phone no but without hyphen or alphabets", phone_no_without_hyphen_or_alphabets
			# if phone_no_with_only_open_parantheses != 0 :
			# 	print "No of phone no with only open parantheses",phone_no_with_only_open_parantheses
			# if phone_no_with_only_close_parantheses != 0 :
			# 	print "No of phone no with only close parantheses", phone_no_with_only_close_parantheses
			# # print "No of valid zipcode without hyphen as verified from unitedstateszipcodes.org", valid_verified_zipcode_without_hyphen
			# # print "No of valid zipcode with one hyphen as verified from unitedstateszipcodes.org", valid_verified_zipcode_with_one_hyphen
			# # print "No of valid zipcode with two hyphen as verified from unitedstateszipcodes.org", valid_verified_zipcode_with_two_hyphen
			# if zipcode_with_two_not_successive_hyphens != 0 :
			# 	print "No of possible zip codes but with two but not succesive hyphens", zipcode_with_two_not_successive_hyphens
			# # if empty != 0 :
			# print "No of empty entries", empty
			# if counter != 0 :
			# 	print "Total no of lines", counter
			# if decimal_integer != 0 :
			# 	print "Total no of decimal integers", decimal_integer
			# if pure_integer != 0 :
			# 	print "No of PURE integer", pure_integer
			# if integer_seperated_by_hyphen_not_zip_or_phone != 0 :
			# 	print "No of integers separated by hyphen but not zipcode or phone number", integer_seperated_by_hyphen_not_zip_or_phone
			# if uncertain_entries != 0 :
			# 	print "No of Hard to say if it's a zip code or phone no.", uncertain_entries
			# if mostly_zipcode_with_one_hyphen != 0 :
			# 	print "No of Zipcode with one hyphen found by regular expression", mostly_zipcode_with_one_hyphen	
			# if mostly_zipcode_without_hyphen != 0 :
			# 	print "No of Zipcode without hyphen found by regular expression",mostly_zipcode_without_hyphen
			# if mostly_zipcode_with_two_hyphen != 0 :
			# 	print "No of zipcode with two hyphens found by regular expression", mostly_zipcode_with_two_hyphen
			# if mostly_zipcode_four_digits != 0 :
			# 	print "No of zipcode without hyphen but four digits", mostly_zipcode_four_digits
			# if string_with_special_characters != 0 :
			# 	print "No of string entries with special characters :"	, string_with_special_characters
			# if integer_with_special_characters != 0 :
			# 	print "No of integer entries with special characters :", integer_with_special_characters

			total_zipcode =  valid_verified_zipcode_without_hyphen + valid_verified_zipcode_with_two_hyphen + zipcode_with_two_not_successive_hyphens + valid_verified_zipcode_with_one_hyphen + mostly_zipcode_with_one_hyphen + mostly_zipcode_without_hyphen + mostly_zipcode_with_two_hyphen + mostly_zipcode_four_digits
			total_phone = phone_no_two_hyphens + phone_no_without_hyphen_or_alphabets + phone_no_with_alphabets + phone_no_with_parantheses + phone_no_one_hyphen + phone_no_with_only_open_parantheses + phone_no_with_only_close_parantheses + phone_three_parts_two_hyphens + phone_three_parts_one_hyphen_one_parantheses + phone_three_parts_plus_one + phone_10_digits                                                            
			total_phone_only_integers = phone_no_two_hyphens + phone_no_without_hyphen_or_alphabets + phone_no_with_parantheses + phone_no_one_hyphen + phone_no_with_only_open_parantheses + phone_no_with_only_close_parantheses
			total_string = string_with_space_no_integer + string_with_integer_spaces + pure_uppercase_string + string_with_integer_hyphen + string_without_integer_without_spaces + string_with_symbol_instead_of_at + two_letter_uppercase_string_not_state_code + string_first_line_address + string_with_dots_not_email_not_website + two_letter_lowercase_string_not_state_code + string_with_integer_without_spaces
			total_website = website + website_without_www
			total_pure_string = string_without_integer_without_spaces + string_with_space_no_integer + pure_uppercase_string + two_letter_uppercase_string_not_state_code + email_without_integer+state_code
			total_special_characters = string_with_special_characters + integer_with_special_characters
			total_email = email_with_integer + email_without_integer			

			counter_decimal_integer = Counter(decimal_integer_lengths)
			# print "comman find_dot lenght is ",counter_decimal_integer.most_common(1)[0][0]
			# print "length of decimal_integer_lengths array is", len(decimal_integer_lengths)

			
			# if total_zipcode != 0 :
			# 	print "Total Zipcode",total_zipcode
			# if total_phone != 0 :
			# 	print "Total phone", total_phone
			# if total_phone_only_integers != 0 :
			# 	print "Total phone only integers",total_phone_only_integers
			# if total_string != 0 :
			# 	print "Total string", total_string
			# if total_pure_string != 0 :
			# 	print "Total pure string", total_pure_string
			# if total_website != 0 :
			# 	print "Total Website", total_website
			# if total_special_characters != 0 :
			# 	print "Total special characters", total_special_characters
			# print "Zipcode array with defective entries", zipcode_array
			
			
			print "\nOBSERVATIONS:"
			
			if((email) > (9*(counter - empty))/10):
				print "\tEmail dominates this column. Hence any other type of entries is considered a defective entry."
				print_improper_email_entries()		
				print_integer_only_entries()
				
				print_integer_more_than_string()

			if(empty) < (counter/10) and empty > 0 :
				print "\tMore than 90 percent of this column is filled with entries. Hence any empty entry is considered defective."
				# print_empty_entries()
				print_empty_count+=1

			if(state_code > (6*(counter - empty))/10):
				print "\tThis column is dominated by state codes. Hence integer dataypes are considered defective"		
				print_not_state_code()
				print_state_code_lowercase()

			if(decimal_integer > (5*counter)/10) :
				print "\tDecimal integers dominate this column."
				# print_email_entries()
				print_symbols()
				print_string_entries()
				print_integer_only_entries()
				print_improper_decimal_integers()

			if(total_website > 5*(counter-empty)/10 ):
				print "\tWebsite entries dominate more than half of the column."		
				print_email_entries() 
				print_integer_only_entries()
				print_space_entries()
				print_no_dots()
				# print_integer_more_than_string()
				if special_characters_print == 0 :
					print_special_characters_website()
					special_characters_print+=1
				print_string_only_entries()
				# print_uppercase_entries()
				if(empty) < (counter/10) and empty > 0 :
					if print_empty_count == 0:
						print "\tCertain empty entries are found which are printed"
						# print_empty_entries()
					else :
						pass
				else :
					pass

			if((total_pure_string) > (9*(counter - empty))/10):
				print "\tThis column is dominated by pure string entries. Hence any other datatype is considered defective "
				if(state_code > (6*(counter - empty))/10):
					print_integer_entries()
					print_email_entries()
					print_symbols()			
				if(total_email > counter/2):
					print_integer_only_entries()
					print_space_entries()
					print_no_dots()
					print_symbols()
				else :					
					print_email_entries()
					print_state_code()
					if special_characters_print == 0:					
						print_special_characters()
						special_characters_print+=1
					print_hyphen()
					print_symbols()
					print_integer_entries()
					print_string_with_dots_not_email_not_website()
					string_dots_no_email_or_website+=1

			# if(empty > (9.5*counter)/10):
			# 	print "\tThis column is predominantly empty. Hence any rows where data is present is considered defective."
			# 	print_integer_only_entries()
			# 	print_email_entries()
			# 	print_website_entries()
			# 	print_state_code()

			if(empty > (counter/3) ) :
				if(empty == counter):
					print "\tThis column is completely empty"
				else :
					print "\tMore than One third of this column is empty."
				if(website > (empty/2)) :
					print "\tHigh probability that this column represents website"
					if (email) :
						print "\tsome lines have email in the place of website."

			if((email_without_integer + email_with_integer) > (counter/2)) :
				print "\tVery high probability that this column represents email"
				email_dominant_column+=1
				print_improper_email_entries()
				# print_uppercase_entries()
				# print_duplicate_email_entries()
				if(empty):
					print "\tThere are empty records in this column"

			if (total_zipcode > 0) and (total_zipcode <= (counter/10)):
					# print "\tSome Zipcodes have been wrongly placed in this column"
					# if ((string_with_integer_spaces > (7*(counter-empty))/10)) :
					# 	print "\tSince this column seems to be dominated by one of the lines of address it is hard to distinguish between door no and zipcode. Hence such rows are not flaged here."
					# 	pass
					# else :	
					print_zip_code()

			if(total_phone_only_integers + pure_integer) > (5*counter)/10 :	
				print "\tPure integer occupy a large portion of this column. Hence any string entries are considered defective"
				print_string_without_hyphen_entries()

				if(total_phone) > (4*counter)/10 :
					if special_characters_print == 0:
						print_special_characters_phone()
						special_characters_print+=1
				else :
					if special_characters_print == 0:
						print_special_characters()
						special_characters_print+=1

				print_string_with_symbol_at_but_not_email()
				print_string_with_parantheses()
				print_integer_with_symbol_at_but_not_email()
				print_integer_with_symbol_at_and_dot()
				# print_integer_with_parantheses()
				print_string_with_hashtag_without_space()
				print_integer_with_hashtag_without_space()

				print_decimal_values()

			if(total_phone) > (4*counter)/10 :	
				print "\tPhone numbers occupy a large portion of this column. Hence any string integers are considered defective"
				print_string_entries()
				if special_characters_print == 0:
					print_special_characters_phone()
					special_characters_print+=1

			if(total_zipcode > (counter/2)) :
				print "\tHigh probability that this column represents zipcode"
				print_string_entries()
				print_email_entries()
				if special_characters_print == 0:
					print_special_characters()
					special_characters_print+=1
				print_pure_integer_not_zipcode()

			if(total_special_characters > 0) and (total_special_characters < (10*(counter-empty)/100)):
				print "\tthis column contains special characters"
				if special_characters_print == 0 and email_dominant_column == 0:
					print_special_characters()
					special_characters_print+=1

			# if(total_phone > (counter/2)) :
			# 	print "\tHigh probability that this column represents phone no"

			# if (total_website > (counter/3)):
			# 	print "\tThis column could be website "

			if(total_string > (9*counter)/10 or total_string > (counter - empty)/2 ) and (total_string > empty):
				print "\tThis column is definitely not email,website,zipcode or phone number"		
				global local_count
				local_count += 1
				if ((string_with_integer_spaces > (7*(counter-empty))/10)) :
					print "\tVery high probability that this is a line of address"				
					print_email_entries()					
				if (pure_integer != 0):						
					print_integer_only_entries()
				if(email !=0) :
					print_email_entries()

			if(total_pure_string < (10*(counter-empty)/100)) and total_pure_string !=0 :
				if(total_string > counter-empty/2):
					print "\tString with other datatypes dominate but pure strings are also present"
				if(total_website > 5*(counter-empty)/10 ):
					pass
				else :
					print "\tFew string entries are found. Hence printed"
					print_string_only_entries()

			if string_with_dots_not_email_not_website > 0 :
				if total_website > 5*(counter-empty)/10 :
					print "\tThis column is dominated by website entries"
				elif total_email > 5*(counter-empty)/10 :
					print "\tThis column is dominated by email entries"
				elif ((string_with_integer_spaces > (7*(counter-empty))/10)) :
					print "\tCould be a line of address"
				else :
					print "\tthis column is dominated by string with dots but they are not email or website"
					if string_dots_no_email_or_website == 0 :
						print_string_with_dots_not_email_not_website()

			if (state_code > (9*counter)/10) :
				if(local_count == 0):
					print "\tHigh probability that this column represents state code"
				else :
					pass
			if(email == 0) :
				if(local_count == 0):
					print "\tThis column is definitely not email"
				else :
					pass	
			if(total_website == 0) :
				if(local_count == 0):
					print "\tThis column is definitely not website"
				else :
					pass
			if(total_phone == 0) :
				if(local_count == 0):
					print "\tThis column is definitely not phone"		
				else :
					pass
			if(total_zipcode == 0) :
				if(local_count == 0):
					print "\tThis column is definitely not zipcode"
				else :
					pass					
			if(two_letter_uppercase_string_not_state_code > (counter-empty)/10 ) :
				if(local_count == 0):
					print "\tThis column is definitely not state code"
				else :
					pass
			if(uncertain_entries):
				if(local_count == 0):
					print "\tThis column contains entries which seem anamalous."
				else :
					pass
				improper_integer_entries()

			if(func_count != 0):
				print "****************************"
				print "PLEASE OPEN improperData.txt"
				print "****************************"
			else:
				print "****************************"
				print "This column appears bug free"
				print "****************************"

			# print "decimals array of",columnsd,"is", decimal_integer_lengths
			
testing_execute_program = ExecuteProgram()
# @app.command
# def execute(filename="filename",begin="something",to="small"):
# 	x = ExecuteProgram()
# 	x.fix_file(filename,begin,to)

class executerHeader(object):
	def work_header(self,filesname,columns) :
		global filename				
		filename = filesname
		global else_count 
		global columnsd
		columnsd = columns
		with open(filename,'rU') as data :
			r = csv.reader(open(filesname, "rU"), dialect=csv.excel_tab)
			line1=r.next()	
			arrt = []
			for element in line1:
				mylist = element.split(',')

		for i in range(0,len(mylist)):
			if columns in mylist[i]:				
				start = mylist.index(columns)
				end = mylist.index(columns)+1				
				x = ExecuteProgram()
				x.fix_file(filename,start,end)
				else_count += 1
		if else_count == 1:
			pass
		elif else_count == 0:
			print "header is not available"

testing_execute_header = executerHeader()


class executeSampleHeader(object):
	def sample_header(self,filesname,columns) :
		global filename				
		filename = filesname
		global else_count 
		global columnsd
		columnsd = columns
		table=""
		row_count=0
		with open(filename,'rU') as data :
			r = csv.reader(open(filesname, "rU"), dialect=csv.excel_tab)
			line1=r.next()	
			arrt = []
			for element in line1:
				mylist = element.split(',')

		for i in range(0,len(mylist)):
			if columns in mylist[i]:				
				start = mylist.index(columns)
				with open(filename,'rU') as data :
					for line in data :
						row_count+=1
						if row_count <= 11:
							cells = line.split(",")
							table+=cells[start] + "\n"
					print table
				else_count += 1
		if else_count == 1:
			pass
		elif else_count == 0:
			print "header is not available"



class executeAll(object):
	def whole_file(self,filesname):
		global filename				
		filename = filesname
		with open(filename,'rU') as data :
			r = csv.reader(open(filesname, "rU"), dialect=csv.excel_tab)
			line1=r.next()	
			arrt = []
			for element in line1:
				mylist = element.split(',')

			for i in range(0,len(mylist)):
				start = i
				end = i+1
				x = ExecuteProgram()
				x.fix_file(filename,start,end)

testing_execute_all = executeAll()			

class countRows(object):
	def count_rows(self,filesname):
		global filename
		row_count = 0
		filename=filesname
		with open(filename,'rU') as data :
			real_data = csv.DictReader(data)
			for row in real_data:
				row_count+=1
		if filename[0]==".":			
			b = filename.split("/")
			print "No of rows in",b[len(b)-1],":",row_count
		else :
			print "No of rows in",filename,":",row_count

class printTenRows(object):
	print "\n"
	def ten_rows(self,filesname):
		global filename
		row_count = 0
		filename=filesname
		with open(filename,'rU') as data :
			for line in data:
				row_count+=1
				if row_count < 11:
					print line


@app.command
def sample(filename="filename"):
	x = printTenRows()
	x.ten_rows(filename)

@app.command
def sampleHeader(filename="filename",columns="headerName"):
	x = executeSampleHeader()
	x.sample_header(filename,columns)


@app.command
def count(filename="filename"):
	x = countRows()
	x.count_rows(filename)

@app.command
def executeColumns(filename="filename",columns="headerName"):
	x = executerHeader()
	x.work_header(filename,columns)

@app.command
def execute(filename="filename"):
	x = executeAll()
	x.whole_file(filename)

if __name__ == '__main__': 
	app.run()				