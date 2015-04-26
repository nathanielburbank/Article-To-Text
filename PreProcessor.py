#!/usr/bin/python

from bs4 import BeautifulSoup 
import re
import codecs


def tokenizer (soup):

	for elem in soup.findAll(['script','style']):
		elem.extract()
	# More clensing Javascript from page # 
	
	token_list = soup.find_all(['div','article','nav'])

	#for token in token_statsist:
	#	for elem in soup.findAll(['div','article','nav']):
	#		elem.extract()

	return token_list	

def classifier (token_list, soup):
	
	i = 0 
	output = [] 

	page_text = soup.get_text()
	page_num_of_sens = (len(re.split(r'[.!?]+', page_text))) + 1 

	#Number of paragraph tags 
	page_num_of_pars = len(soup.find_all('p')) + 1 

	#Number of div elements
	page_num_of_divs = len(token_list)

	
	for token in token_list:

		# Number of sentences 
		plain_text = token.get_text()
		sentence_num = (len(re.split(r'[.!?]+', plain_text)) ) 

		if (sentence_num > 1): #just skip any token that does not have at least two sentences in it.

			#Token ID
			token_stats = [i] 
			sentence_num_adjusted = sentence_num /float(page_num_of_sens)

			# % of sentences 
			token_stats.append(sentence_num_adjusted)
			
			# % of paragraph tags 
			pars = len(token.find_all('p', recursive=False))/float(page_num_of_pars)
			token_stats.append(pars)

			# Becuase you the paragraph tag count in the following two stats, we want a floor 
			pars_a = max(.1,pars)

			#Ratio of sentences to link tags, weighted by paragraph tags 
			links = len(token.find_all('a')) + 1 
			StoLP = (sentence_num / float(links)) * pars_a
			token_stats.append(StoLP)
			
			#Ratio of text to html, weighted by paragraph tags  
			text_density= (len(plain_text)/float(len(token.prettify()))) * pars_a
			token_stats.append(text_density)

			#Weighted score metric, based on a regression analysis of small set of sample data  
			score = -.0079908 + (.0225799 * sentence_num_adjusted) + (1.319708  * pars) + ( -.0017439  *  StoLP) + (.45502 * text_density)
			token_stats.append(score)
			
		

			output.append(token_stats)

		i = i + 1 
	
	return output
			  



