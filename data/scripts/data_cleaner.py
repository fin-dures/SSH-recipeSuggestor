import nltk
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import csv

INGREDIENTS = "/home/finlay-dures/Documents/ingredients.csv" # change to path of ingredients file

def lemmatizer(word):
    return WordNetLemmatizer().lemmatize(word)


def main():
    
    ingredients_count = {}

    with open(INGREDIENTS) as f:

        for line in f:
            ingredients_line = (line.split(","))[2:]
            ingredients_line = [ingredient for ingredient in ingredients_line if len(ingredient)>2 and ingredient!=", "]
            ingredient_tokens = [ingredient.split(" ") for ingredient in ingredients_line]
            ingredient_tokens_flattened = [token.strip() for sublist in ingredient_tokens for token in sublist]
            ingredient_tokens_flattened = [token for token in ingredient_tokens_flattened if token.isalnum()]
            
            for ingredient in ingredient_tokens_flattened:
                ingredients_count[ingredient] = ingredients_count.get(ingredient, 0)+1

    ingredients_set = set(key for key in ingredients_count if ingredients_count[key]>=3)

    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

    word_tags = pos_tag(list(ingredients_set))
    ingredients_set_final = set()

    for word, tag in word_tags:

        if tag == "NN":
            ingredients_set_final.add(word)
        
        elif tag == "NNS":
            ingredients_set_final.add(lemmatizer(word))

    SAVEFILE = "ingredients_list_cleaned.csv"
    with open(SAVEFILE, mode="w", newline='') as f:
        writer = csv.writer(f)
        
        for ingredient in ingredients_set_final:
            print(ingredient)
            writer.writerow([ingredient])



if __name__=="__main__":
    main()