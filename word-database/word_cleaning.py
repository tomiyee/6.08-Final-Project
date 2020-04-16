from rake_nltk import Rake
import nltk
import pandas as pd
import re
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_colwidth', 500)
pd.set_option('display.width', 1000)

def meaning_filter(x):
    first_def = x.split(";")[0]
    first_def = re.sub(r'.* pertaining to', 'pertaining to', first_def)
    return first_def


r = Rake(max_length = 2)

dict_file = "raw_full_dictionary.txt"
df = pd.read_csv(dict_file, sep = "=", names = ["word", "meaning"])
##print(df[:10])

print()

filtered = df.copy()
filtered['meaning'] = filtered['meaning'].apply(meaning_filter)

##print(filtered[filtered.meaning.str.contains(' or ')][:100])

shorter = filtered[len(filtered['meaning'].str.split()) < 5]
print(shorter)

##print(filtered[filtered.meaning.str.contains('pertaining')])
##with open(dict_file, 'r', encoding="utf8") as f:
##    for line in f:
##        separated = line.split("=")
##        word, meaning = separated[0], separated[1][:-1]
##        meaning = meaning.replace("-", " - ")
##        meaning = meaning.split(";")[0]
##        print(word)
##        print(meaning)
##        break
    
##        meaning_words = len(meaning.split())
##        
##        if len(word) > 8 and meaning_words <= 4:
##            r.extract_keywords_from_text(meaning)
##            
##            try:
##                
##                best = r.get_ranked_phrases()[0]
##                print("{} = {}".format(word, meaning))
##                print("{} = {}".format(word, meaning.replace(best, "____", 1)))
##                print()
##            except:
##                pass
##            print(r.get_ranked_phrases())
##            break
##        for c in "xyz":
##            if c in word and meaning_words <= 3:
##                print(word, meaning)
##        break
