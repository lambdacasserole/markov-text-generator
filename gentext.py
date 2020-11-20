import sys
import os

from markov_text_generator.markov import MarkovModel


# Check args length.
if len(sys.argv) < 2:
	print("Usage: python3 gen-text.py <modelfile> [n=100]")
	exit()

# Check model path.
path = sys.argv[1]
if not os.path.isfile(path):
	print("Error: Could not read model file.")

# Read in model.
model = MarkovModel.load(path)

# Get number of tokens from command line.
n = 100
if len(sys.argv) > 2:
	try:
		n = int(sys.argv[2])
	except:
		print("Error: Could not parse number of tokens as int.")
		exit(1)

# Output model results.
print(model.generate_text(n))

