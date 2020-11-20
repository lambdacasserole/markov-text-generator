import random
import json


class MarkovModel():
	""" Represents a Markov model that can be used for text generation
	"""

	# Starting tokens for text generation.
	heads = None

	# The model structure.
	model = None

	def __init__(self, heads, model):
		""" Initialises a new instance of a Markov model.
		Args:
			heads (dict): A dictionary of starting points against their probabilities
			model (dict): The model structure (tokens against probabilities)
		"""
		self.heads = heads
		self.model = model

	def head (self):
		""" Gets a random starting token.
		Returns:
			str: A random starting token
		"""
		rand = random.random()
		choice = None
		for token, prob in self.heads.items(): # Choose token (random, weighted).
			choice = token
			rand -= prob
			if rand <= 0:
				break
		return choice

	def generate (self, n):
		""" Generates a stream of tokens using the model.
		Args:
			n (int): The number of tokens to generate
		Return:
			list of str: A list of generated tokens
		"""
		tokens = [self.head()] # Random head.
		for _ in range(n):
			if tokens[-1] not in self.model: # Dead end, restart.
				tokens.append(self.head())
			dist = self.model[tokens[-1]] # Get distribution for previous token.
			rand = random.random()
			for token, prob in dist.items(): # Choose successor token (random, weighted).
				rand -= prob
				if rand <= 0:
					tokens.append(token)
					break
		return tokens

	def generate_text (self, n):
		""" Generates text using the model.
		Args:
			n (int): The number of tokens to generate for the string
		Return:
			str: A string consisting of generated tokens
		"""
		return " ".join(self.generate(n))

	def serialize (self):
		""" Serializes this model to a JSON string.
		Returns:
			str: The model encoded as a JSON string
		"""
		return json.dumps({
			"heads": self.heads,
			"model": self.model
		})

	def persist (self, path):
		""" Persists this model to a file.
		Args:
			path (str): The output path
		"""
		with open(path, "w") as file:
			file.write(self.serialize())

	@staticmethod
	def load (path):
		""" Loads a model from a file.
		Args:
			path (str): The input path
		"""
		with open(path) as file:
			text = file.read()
			obj = json.loads(text)
			return MarkovModel(obj["heads"], obj["model"])
