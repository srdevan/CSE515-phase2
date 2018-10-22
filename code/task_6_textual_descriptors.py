import numpy
from operator import itemgetter
from util import Util
from data_extractor import DataExtractor
from datetime import datetime
import pandas as pd
import constants

class Task6:
	
	def runner(self):
		k = input('Enter the k value: ')
		k = int(k)

		util = Util()
		data_extractor = DataExtractor()

		location_id_to_title_map = data_extractor.location_mapping()
		location_title_to_id_map = data_extractor.location_title_to_id_mapping()
	
		location_list = list(location_title_to_id_map.values()) # List of location ids
		LOCATION_COUNT = len(location_list) # constant

		global_term_dictionary_current_index = 0 # To store the count of unique terms and indexing a given term in the global dictionary
		global_term_dictionary = dict() # To store the global list of terms as keys and their indices as values
		global_term_index_dictionary = dict() # To store the global list of terms referenced via the indices as the keys and terms as the values
		location_dictionary = dict() # To store the terms of a particular location and their corresponding attributes
		similarity_matrix = numpy.zeros((LOCATION_COUNT, LOCATION_COUNT)) # To capture location-location similarity

		with open(constants.TEXTUAL_DESCRIPTORS_DIR_PATH + 'devset_textTermsPerPOI.txt', encoding='utf-8') as f:
			lines = [line.rstrip('\n') for line in f] # split into lines
			for line in lines:
				words = line.split() # split all words in the line

				temp_list_for_title = []

				# extract location title
				while '\"' not in words[0]:
					temp_list_for_title.append(words.pop(0))
				location_title = ('_').join(temp_list_for_title)
				location_id = location_title_to_id_map[location_title]

				# Build the term vocabulary and also the dictionary for terms corresponding to the locations and their scores
				for index, word in enumerate(words):
					index_mod4 = index%4
					
					if index_mod4 == 0: # the term
						current_word = word.strip('\"')
						if not global_term_dictionary.get(current_word):
							global_term_dictionary[current_word] = global_term_dictionary_current_index
							global_term_index_dictionary[global_term_dictionary_current_index] = current_word
							global_term_dictionary_current_index+= 1
						if not location_dictionary.get(location_id):
							location_dictionary[location_id] = {}
						if not location_dictionary.get(location_id).get(current_word):
							location_dictionary[location_id][current_word] = { 'TF': 0, 'DF': 0, 'TFIDF': 0}
					elif index_mod4 == 1: # TF
						location_dictionary[location_id][current_word]['TF'] = int(word)
					elif index_mod4 == 2: # DF
						location_dictionary[location_id][current_word]['DF'] = int(word)
					elif index_mod4 == 3: # TFIDF
						location_dictionary[location_id][current_word]['TFIDF'] = float(word)
				
		the_model = 'TFIDF'
		# Go over every location as a potential query location
		for query_location_id in location_list:
			query_model_vector = [0] * global_term_dictionary_current_index
			
			# Construct the query model vector (<the_model> values of each term in the query location)
			for current_term_id_key, current_term_id_value in location_dictionary[query_location_id].items():
				if current_term_id_key == the_model:
					continue
				current_term_index = global_term_dictionary[current_term_id_key]
				query_model_vector[current_term_index] = location_dictionary[query_location_id][current_term_id_key][the_model] 

			# Go over every location as a potential target location
			for target_location_id, target_location_id_data in location_dictionary.items():
				# If query location is the same as target location, similarity = 1
				if target_location_id == query_location_id:
					similarity_matrix[query_location_id - 1][target_location_id - 1] = 1
					continue
				else:
					if not location_dictionary.get(target_location_id).get(the_model):
						location_dictionary[target_location_id][the_model] = [0] * global_term_dictionary_current_index
	
					# Build the target model vector comprising of the_model scores of the target location
					for current_term_key, current_term_value in location_dictionary[target_location_id].items():
						if current_term_key == the_model:
							continue
						current_term_index = global_term_dictionary[current_term_key]
						location_dictionary[target_location_id][the_model][current_term_index] = location_dictionary[target_location_id][current_term_key][the_model]
					
					# Compute the Cosine Similarity between the query model vector and target model vector
					cosine_similarity_value = util.cosine_similarity(query_model_vector, location_dictionary[target_location_id][the_model])
					similarity_matrix[query_location_id - 1][target_location_id - 1] = cosine_similarity_value

		# Store the similarity matrix data in a CSV if needed

		# df = pd.DataFrame(similarity_matrix)
		# loc_list = []
		# for i in range(1,31):
		# 	loc_list.append(location_id_to_title_map[str(i)])

		# df.to_csv('./similarity_matrix_td_tfidf_global.csv', encoding='utf-8', header=None, index=False)
		# df.to_csv('./similarity_matrix_td_tfidf_global_descriptive.csv', encoding='utf-8', header=loc_list, index=loc_list)

		# Apply SVD on the data
		U, S, Vt = numpy.linalg.svd(similarity_matrix)

		# {
		#  <location_id>: [{'Location Name': <>, 'Weight': <>}, {'Location Name': <>, 'Weight': <>}, ...],
		#  <location_id>: [{'Location Name': <>, 'Weight': <>}, {'Location Name': <>, 'Weight': <>}, ...],
		#  ...
		# }
		semantic_data_dict = {}
		for arr_index, arr in enumerate(Vt[:k, :]):
			if not semantic_data_dict.get(arr_index+1):
				semantic_data_dict[arr_index+1] = []

			for index, element in enumerate(arr):
				semantic_data_dict[arr_index+1].append({ 'Location Name': location_id_to_title_map[str(index+1)], 'Weight': element })

			# Sort the list based on the weight attribute
			sorted_list = sorted(semantic_data_dict[arr_index+1], key=itemgetter('Weight'), reverse=True)
			semantic_data_dict[arr_index+1].clear()
			semantic_data_dict[arr_index+1] = sorted_list

			# Print the latent semantic as location name-weight pairs sorted in decreasing order of weights
			print('Latent Semantic: ', arr_index+1)
			for idx, data in enumerate(sorted_list):
				print('\tLocation Name: ', semantic_data_dict[arr_index+1][idx]['Location Name'], '| Weight: ', semantic_data_dict[arr_index+1][idx]['Weight'])