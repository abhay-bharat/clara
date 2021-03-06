import re
import keyword
import time
from New_functions.built_in_functions import Interaction_module
from New_functions.ift_analysis import ift_feedback, incorrect_conditional_exp
from New_functions.operator_analysis import feedback_comp_operator, feedback_arth_operator, feedback_logic_operator
from New_functions.operator_analysis import feedback_incorrect_value
from New_functions.comparing_and_tracing import compare_outputs, incorrect_return, display_location
from New_functions.simp_feed import feed_main 
from Documentation.python_doc_testing import for_loop_func
##Voice based interaction imports
from New_functions.bot_conversation import RecognizeSpeech_during_interaction
from gtts import gTTS
from playsound import playsound
### GIVE THE MOST influential(high cost repair) repair first and then next.
'''
def get_key(index_dict, val):
	l = []
	for key, value in index_dict.items():
		if val == value:
			l.append(key)

	return l

def sort_repair_cost(feedback_list):
	# provide the least cost repair first 
	index_dict = dict()
	sorted_list = []
	for i in range(len(feedback_list)):
		cost = feedback_list[i].split('cost=')[1]
		cost = int(re.findall(r'\d+', cost)[0])
		index_dict[i] = cost

	# Will hold unique cost list
	cost_sorted = list(set(sorted(index_dict.values())))
	# print(cost_sorted)
	for cost in cost_sorted:
		repair_list = get_key(index_dict,cost)
		# print(repair_list)
		for index in repair_list:
			sorted_list.append(feedback_list[index])

	# Sorted list holds the sorted repairs based on cost
	return sorted_list
'''
def check_equal(feedback):
	try:
		if "Add" in feedback or "Delete " in feedback:
			return 0
		sections = feedback.split(" to ")
		sections[0] = sections[0].split("Change ")[1]

		#at index 1 and 3 the required set of strings are present which is to be compared(Change to ==)
		if sections[0] in sections[1]:
			return 1
		return 0
	except Exception as err:
		return 0 #Consider them to be not equal and feedback would be displayed

def compute_cost(feedback_list, programs,rep_prog, inter,args, ins):
	compare_outputs(programs, inter,args, ins)
	### Total cost is already computed in rep_prog[0]
	tot_cost = rep_prog[0]
	#### Consider threshold appropraitely as per the preference 
	if tot_cost > 15:
		print("WARNING : The cost of the repairs generated is more, recommended to analyses and make your program better to have less cost repairs")
		print("As high cost repairs are usually not recommended to consider for debugging")
		print("If you still prefer to look at repairs, press any key, to exit press 0")
		speak = "Please read the warning before continuing"
		speech_obj = gTTS(text = speak, lang = 'en', slow=False)
		speech_obj.save('wit_bot.mp3')
		playsound('wit_bot.mp3', True)
		reply = input()
		if reply == '0':
			print("*** Happy Coding!!! ***\n")
			return 0
	return 1

# Function to analysis the type of feedback 
def feedback_channelizer(clara_feedback, feed_no, programs,rep_prog, inter, inputs, arguements, lang):
	try:
		if inputs != None:
			trace_incorrect_prog = inter.run(programs[-1], None,inputs[0], arguements)
		elif arguements != None:
			trace_incorrect_prog = inter.run(programs[-1], None,  arguements[0], inputs)

		# feed_main is used to clean the feedback
		cleaned_feedback = feed_main(clara_feedback, trace_incorrect_prog)
	except Exception as err:
		### In case of exception just use the clara provided feedback
		print('Exception arose is(cl) :', err)
		cleaned_feedback = clara_feedback
	try:
		if(check_equal(clara_feedback)):   #function to check if feedback generated by clara is with no change suggestions 
			# print("Unnecessary feedback!!!")
			return
		else:
			considered = 0
			### Display the location in program where the bug is
			print("Encountered error number :", feed_no)
			print("----------------------------------------------------------------\n")
			location = display_location(clara_feedback)
			if location != None and ' None' not in location:	
				print("\n----------------------------------------------------------------\n")
				print("** The location in your program where the bug detected is :")
				print(location, "**\n")
				print("--------------------------------------------------------------------------\n")
				speak = "The location in your program where the bug is."
				speak += location 
				speech_obj = gTTS(text = speak, lang = 'en', slow=False)
				speech_obj.save('wit_bot.mp3')
				playsound('wit_bot.mp3', True)

			#When an expression is to be deleted from incorrect program
			if "Add" in clara_feedback or "Delete " in clara_feedback:
				considered = 1
				print("\n--------------------------------------------------------------------------\n")
				print("Clara is suggesting either to remove or add an expression in your code, this would mean that cost of repair is more")
				print("It is recommended that you consider debugging on your own first")
				print("\n--------------------------------------------------------------------------\n")
				speak = "Clara is suggesting either to remove or add an expression in your code."
				speak += "You can look at clara generated repair or prefer to quit, if you wish to debug on own"
				speak += "Please tell your preference now"
				speech_obj = gTTS(text = speak, lang = 'en', slow=False)
				speech_obj.save('wit_bot.mp3')
				playsound('wit_bot.mp3', True)
				talk = 1
				spoke = 0
				# Giving user 3 chances to speak out incase it wasn't recorded properly
				while(talk != 4):
					if(spoke):
						speak = "Please give your preference now."
						speech_obj = gTTS(text = speak, lang = 'en', slow=False)
						speech_obj.save('wit_bot.mp3')
						playsound('wit_bot.mp3', True)

					spoke = 1
					print("\n***Please speak now...\n")
					reply =  RecognizeSpeech_during_interaction('myspeech.wav', 6)
					if reply:
						if (reply[0] == 'Agree' or reply[1] == 'on') and (reply[0] != 'Disagree'):
							print(cleaned_feedback,"\n")
							print("****************************************************\n")
							return 
						else:
							print("*** Happy Coding!!! ***\n")
							return 0
					else:
						print("Sorry, couldn't interpret your response or record your voice")
						if(talk < 3):
							speak = "Sorry...couldn't interpret your response or record your voice, please try again."
						else:
							speak = "Sorry...couldn't interpret your response or record your voice."
					
						speech_obj = gTTS(text = speak, lang = 'en', slow=False)
						speech_obj.save('wit_bot.mp3')
						playsound('wit_bot.mp3', True)
						#Increment to consider the chances taken up
						talk += 1
				return 

			# For python language specific
			if(lang == 'py'):
				#List of the builtin functions in python
				python_builtins = [
        					'input', 'float', 'int', 'bool', 'str', 'list', 'dict',
        					'set', 'tuple', 'round', 'pow', 'sum', 'range', 'xrange', 'len',
        					'reversed', 'enumerate', 'abs', 'max', 'min', 'type', 'zip', 'map',
        					'isinstance']
				keywords = keyword.kwlist

				bltins_error = [] #To store the builtins where the user has gone wrong
				for blt in python_builtins:
					if (blt+"(") in clara_feedback:
						bltins_error.append(blt)

				if ' for loop ' in clara_feedback:
					print("There is an incorrect iterated expression used in for loop\n")
					speak = "There is an incorrect iterated expression used in for loop."
					speech_obj = gTTS(text = speak, lang = 'en', slow=False)
					speech_obj.save('wit_bot.mp3')
					playsound('wit_bot.mp3', True)
					#Ask user preference 
					speak = "Would You like to go through brief explanation of for loop expression .or just continue without reading."
					speak += "Please give your preference now."
					speech_obj = gTTS(text = speak, lang = 'en', slow=False)
					speech_obj.save('wit_bot.mp3')

					print("Would You like to go through brief explanation of for loop, or just continue without reading\n")
					playsound('wit_bot.mp3', True)
					talk = 1
					spoke = 0
					# Giving user 3 chances to speak out incase it wasn't recorded properly
					while(talk != 4):
						if(spoke):
							speak = "Please tell your preference response now."
							speech_obj = gTTS(text = speak, lang = 'en', slow=False)
							speech_obj.save('wit_bot.mp3')
							playsound('wit_bot.mp3', True)

						spoke = 1
						print("\n***Please speak now...\n")
						reply =  RecognizeSpeech_during_interaction('myspeech.wav', 6)
						if reply:
							if (reply[0] == 'Agree' or reply[1] == 'on') and (reply[0] != 'Disagree'):
								speak += "Providing brief explanation."
								print("Go through this brief explanation of for loop.")
								print("\n------------------------------------------------------------------------------------\n")
								for_loop_func()
								print("\n------------------------------------------------------------------------------------\n")
								break
							else:
								break
						else:
							print("Sorry, couldn't interpret your response or record your voice")
							if(talk < 3):
								speak = "Sorry...couldn't interpret your response or record your voice, please try again."
							else:
								speak = "Sorry...couldn't interpret your response or record your voice."

							speech_obj = gTTS(text = speak, lang = 'en', slow=False)
							speech_obj.save('wit_bot.mp3')
							playsound('wit_bot.mp3', True)
							#Increment to consider the chances taken up
							talk += 1

				if bltins_error != []:
					considered = 1
					print("Looks like the incorrect code is due to one of the builtin method or function")
					print("Would you like to know name of builtin?")
					print("yes/no\n")
					reply = input()
					if(reply == 'no' or reply == 'No' or reply == 'NO'):
						print("Nice!!! You don't want to giveup so easily. Happy coding!")
						return 0
					elif(reply == 'yes' or reply == 'Yes' or reply == 'YES'):
						for blt in bltins_error:
							status = Interaction_module(clara_feedback,cleaned_feedback,blt,arguements)
							if status == 0:
								return 0
					return 


				#check for if it is a keyword
				'''
				keyword_error = []
				for key in keyword.kwlist:
					if key in clara_feedback:
						keyword_error.append(key)

				if keyword_error != []:
					print("Looks there are one or more keywords, where you have used it illogically with respect to given problem statement")
					print("This is at line number :",line_num)
					print("Do you ")
				'''
			segments = clara_feedback.split(" to ")
			segments[0] = segments[0].split("Change ")[1]
			segments[1] = segments[1].split(location)[0]

			if 'ite(' in clara_feedback:
				speak = "Interpretation about error is."
				speech_obj = gTTS(text = speak, lang = 'en', slow=False)
				speech_obj.save('wit_bot.mp3')
				playsound('wit_bot.mp3', True)
				print("\n--------------------------------------------------------------------------\n")
				print("Looks like you have implemented if-then-else illogically with respect to the given problem statement.")
				print("It is recommended that you read through the problem statement again, before proceeding to debug")
				print("\n--------------------------------------------------------------------------\n")
				#Wait for 5 seconds till user reads above statement
				time.sleep(5)
				speak = "Would you like to go with the exhaustive feedback phase or. you can prefer to quit, if you wish to debug on own"
				speak += "Please tell your preference now"
				speech_obj = gTTS(text = speak, lang = 'en', slow=False)
				speech_obj.save('wit_bot.mp3')
				playsound('wit_bot.mp3', True)
				talk = 1
				spoke = 0
				# Giving user 3 chances to speak out incase it wasn't recorded properly
				while(talk != 4):
					if(spoke):
						speak = "Please give your response now."
						speech_obj = gTTS(text = speak, lang = 'en', slow=False)
						speech_obj.save('wit_bot.mp3')
						playsound('wit_bot.mp3', True)

					spoke = 1
					print("\n***Please speak now...\n")
					reply =  RecognizeSpeech_during_interaction('myspeech.wav', 6)
					if reply:
						if (reply[0] == 'Agree' or reply[1] == 'on') and (reply[0] != 'Disagree'):
							ift_feedback(cleaned_feedback,cleaned_feedback, inputs, arguements, lang) 
							break
						else:
							print("*** Happy Coding!!! ***\n")
							return 0
					else:
						print("Sorry...couldn't record or interpret your response")
						if(talk < 3):
							speak = "Sorry...couldn't record your voice, please try again."
						else:
							speak = "Sorry...couldn't record your voice."
						speech_obj = gTTS(text = speak, lang = 'en', slow=False)
						speech_obj.save('wit_bot.mp3')
						playsound('wit_bot.mp3', True)
						#Increment to consider the chances taken up
						talk += 1
				return 

			#incorrect conditional statements($cond)
			if '$cond' in clara_feedback:
				status = incorrect_conditional_exp(clara_feedback, arguements, inputs)
				if status == 0:
					return 0

			#check for incorrect return value
			if ('return' in clara_feedback) or ('$ret' in clara_feedback):
				incorrect_return(programs, rep_prog, inter, arguements, inputs)
				if ' if ' in segments[0] or ' if ' in segments[1]:
					print("Since there was 'if' statements involved, press 1 to read about it, else any key to continue")
					ans = input()
					if ans == '1':
						status = ift_feedback(clara_feedback, cleaned_feedback, inputs, arguements, lang)
						if status == 0:
							return 0
				print("Press 1 to continue with possibly any further related repairs, else press 0 to exit")
				reply = input()
				if reply == '0':
					print("*** Happy Coding!!! ***\n")
					return 0

			#incorrect use of operators	
			if not(considered):
				arithmetic_operators_dict = {'+':'Addition', '-':'Subtraction', '*':'Multiplication', 
										'/' : 'Division', '%' : 'Modulus(returns remainder)'}
				comparison_operators_dict = {'==' : 'equal to', '!=' : 'not equal to', '<':'less than',
										'<=':'less than or equal to', '>':'greater than', '>=':'greater than or equal to'}
				logical_operators = [' and ', ' or ', ' && ', ' || ', ' & ', ' | ']

				arithmetic_operators = list(arithmetic_operators_dict.keys())
				comparison_operators = list(comparison_operators_dict.keys())
				for op in arithmetic_operators+comparison_operators+logical_operators:
					if (op in segments[0] and op not in segments[1]) or (op not in segments[0] and op in segments[1]): #This is feasible for single operator error
						if op in arithmetic_operators:
							operator = arithmetic_operators_dict[op]+' ('+op+')'
							return feedback_arth_operator(segments,operator,clara_feedback,cleaned_feedback, inputs, arguements) 
						elif op in comparison_operators:
							operator = comparison_operators_dict[op]+' ('+op+')'
							return feedback_comp_operator(segments,operator,clara_feedback,cleaned_feedback, inputs, arguements)
						elif op in logical_operators:
							return feedback_logic_operator(segments, op,clara_feedback, cleaned_feedback, inputs, arguements) 

				#incorrect use of values
				# using re.findall() 
				# getting numbers from string  
				num1 = re.findall(r'\d+', segments[0]) 
				num2 = re.findall(r'\d+', segments[1]) 
				if num1 != [] and num2 != []: 
					if(num1[0] != num2[0]):
						return feedback_incorrect_value(num1[0], num2[0], clara_feedback,cleaned_feedback, inputs, arguements)
				elif num1 != [] or num2 != []:
					print("There might be an incorrect initialization.")
					speak = "There might be an incorrect initialization."
					speech_obj = gTTS(text = speak, lang = 'en', slow=False)
					speech_obj.save('wit_bot.mp3')
					playsound('wit_bot.mp3', True)
					
					print("It is recommended that you dry run through code and look for right initialization")
					print("Repair to this has been generated, press 1 to see repair or 0 to exit")
					reply2 = input()
					if(reply2 == '1'):
						print(cleaned_feedback, "\n")
						print("***************************************************\n")
					return 0

			print("No further explanation specific to error number :=",feed_no,",could be generated")
			print("Press 1 to just look at repairs directly, else press 0 to exit")
			reply = input()
			if reply == '1':
				speak = "The repair generated for incorrect expression is."
				speech_obj = gTTS(text = speak, lang = 'en', slow=False)
				speech_obj.save('wit_bot.mp3')
				playsound('wit_bot.mp3', True)
				print(cleaned_feedback,"\n")
				print("****************************************************\n")
			else:
				print("*** Happy Coding!!! ***\n")
				return 0
			#FOR most of feedbacks can compare between incorrect and correction expression given in feedback 
	except Exception as err:
		print("Exception arose is :",err)
		print("Detailed explanation couldn't be generated, press 1 to look at repairs directly, else press 0 to exit")
		choice = input()
		if choice == '1':
			print(cleaned_feedback,"\n")
			print("****************************************************\n")
		else:
			print("*** Happy Coding!!! ***\n")
			return 0



