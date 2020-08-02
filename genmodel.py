import sys
import re
import os

from markov import MarkovModel


def tokenize (text):
	""" Tokenizes a text sample.
	Args:
		text (str): The text sample
	Returns:
		list of str: A list of tokens
	"""
	replacements = ["\r", "\n", "\t"]
	output = text
	for replacement in replacements:
		output = output.replace(replacement, " ") # Convert whitespace to spaces only.
	return list(filter(lambda s: len(s) > 0, output.split(" "))) # Split along spaces and remove empties.


def analyze (filepaths, line_filters=[], token_filters=[], continuation_char=None):
	""" Returns an analysis of the specified filed necessary to construct a Markov model.
	Args:
		filepaths (list of str): Paths of the files to analyse
		line_filters (list of str): Regexes to match lines to ignore
		token_filters (list of str): Regexes to match tokens to ignore
		continuation_char (str): The token continuation character to use
	Return:
		tuple: A tuple containing the analysis and list of starting tokens.
	"""
	analysis = {} # Dictionary to hold the analysis.
	starts = [] #  List of starting tokens.
	# Loop over filepaths.
	for filepath in filepaths:
		with open(filepath) as file:
			prev_token = None # Buffer previous token.
			for line in file:
				if any([re.match(r, line) for r in line_filters]): # Apply line filters.
					continue
				tokens = tokenize(line) # Tokenize line.
				for token in tokens:
					if any([re.match(r, token) for r in token_filters]): # Apply token filters.
						continue
					if prev_token == None:
						starts.append(token) # Remember first token.
						prev_token = token # Prime previous token if first token.
					elif continuation_char != None and prev_token.endswith(continuation_char): # Token continuation.
						prev_token = prev_token.rstrip(continuation_char) + token
					else:
						if continuation_char != None and not token.endswith(continuation_char):
							if prev_token not in analysis:
								analysis[prev_token] = [] # New list needed.
							analysis[prev_token].append(token)
							if prev_token.endswith((".", "?", "!")) and token[0].isupper(): # Remember sentence start tokens.
								starts.append(token)
						prev_token = token
	return (analysis, starts) # Return analysis and starting token tuple.


def compute_model (analysis, starts):
	""" Computes a Markov model from the given analysis and list of start tokens.
	Args:
		analysis (dict): The analysis to build the model from
		starts (list of str): The list of starting tokens
	Returns:
		MarkovModel: The computer Markov model.
	"""
	model = {}
	for root, successors in analysis.items():
		successor_count = len(successors)
		dist = {s: successors.count(s) / successor_count for s in successors}
		model[root] = dist
	start_count = len(starts)
	return MarkovModel({h: starts.count(h) / start_count for h in starts}, model)


# Allow module to be imported by others.
if __name__ == "__main__":

	# Check args length.
	if len(sys.argv) < 2:
		print("Usage: python3 gen-model.py <file1> <file2> ... <filen>")
		exit()

	# Take in all filepaths from command line and check they exist.
	file_paths = sys.argv[1:]
	if not all([os.path.isfile(f) for f in file_paths]):
		print("Error: Could not read one or more input files.")
		exit(1)

	# TODO: These filters are designed for the Enron email dataset. Change them if needed.

	# Filters on lines.
	line_filters = [
		r"\t.*", # Email headers.
		r"^.*?:",
		r"^_", # Separators.
		r"^=",
		r"^-",
		r"^\+"
	]

	# Filters on individual tokens.
	token_filters = [
		r".*?[><\*\+_\-\"%@\[\]&\(\)#\|=~].*?", # Anything containing awkward symbols.
		r"^[\.\,\?\!:;]+$", # Sentence punctuators by themselves.
		r"^[0-9]+$", # Numbers by themselves.
		r"\b[A-Z]+\b", # Words in all caps.
	]

	# Analyse file, using filters and an "=" line continuation character.
	analysis, starts = analyze(file_paths, line_filters, token_filters, "=")

	# Compute model from analysis.
	model = compute_model(analysis, starts)

	# Output serialized model.
	print(model.serialize())
