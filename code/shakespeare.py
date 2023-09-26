import csv
import os
import re

INPUT_DIR = os.path.join("data", "shakespeare")
STOPWORDS_PATH = os.path.join(INPUT_DIR, "stopwords.txt")
SHAKESPEARE_PATH = os.path.join(INPUT_DIR, "shakespeare.txt")
OUTPUT_DIR = "artifacts"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "shakespeare_report.csv")

NUM_LINES_TO_SKIP = 246
LAST_LINE_STOP = 124437

with open(STOPWORDS_PATH, 'r') as in_file:

    header = in_file.readline()
    text = in_file.read()

clean_stopwords = re.sub('[^A-Za-z\s]', '', text)

def load_stopwords(stopwords):
    """Load the stopwords from the file and return a set of the cleaned stopwords."""

    sw = set()
    for word in stopwords.split('\n'):
        sw.add(word.lower())
    return sw
stopwords_set = load_stopwords(clean_stopwords)

with open(SHAKESPEARE_PATH, 'r') as in_file2:
	text2 = in_file2.readlines()[NUM_LINES_TO_SKIP:LAST_LINE_STOP]
	
dirty_text = ""
should_read = True

for line in text2:
	if line.startswith("<<"):
		should_read = False
	if should_read:
		dirty_text += line
	if line.endswith(">>\n"):
		should_read = True

text_without_punctuation = re.sub('[^A-Za-z\s]', '', dirty_text)
text_without_spaces = re.sub("\s+", " ", text_without_punctuation)
clean_shakespeare = text_without_spaces.lower()

def word_count(str_):
	word_count = {}
	for word in clean_shakespeare.split(" "):
		if word in stopwords_set:
			continue
		if word in word_count:
			word_count[word] += 1
		else:
			word_count[word] = 1
	return word_count

shakespeare_wordcount = word_count(clean_shakespeare)

tuples_wordcounts = shakespeare_wordcount.items()
sorted_wordcounts = sorted(tuples_wordcounts, key = lambda x:x[1], reverse = True)

def write_wordcounts(sorted_counts, path_):

	with open(path_, 'w+') as out_file:
		csv_writer = csv.writer(out_file)

		header = ['word', 'count']
		data = sorted_wordcounts

		csv_writer.writerow(header)
		csv_writer.writerows(data)
		
write_wordcounts(sorted_wordcounts, OUTPUT_PATH)