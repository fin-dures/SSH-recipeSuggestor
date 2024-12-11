import csv



def main():

    PATH = "/home/finlay-dures/RecipeNLG/dataset/full_dataset.csv" # change to path of recipeNLG dataset
    ingredient_set = get_ingredients_set()
    ingredients_index = dict.fromkeys(ingredient_set)
    

    
    with open(PATH) as f:

        reader = csv.reader(f)
        index = -1

        for line in reader:
            
            line_reader = csv.reader(line,dialect=csv.excel_tab)

            try:
                seperated = [line for line in line_reader]
            except csv.Error:
                print("newline error")
                index+=1
                continue

            try:
                ner = seperated[6]

            except IndexError:
                print("Out of range")
                index+=1
                continue
            
            
            try:
                csvIndex = int(seperated[0][0])    
            except IndexError:
                csvIndex = -1
                print("out of range")

            try:
                assert(csvIndex==index)
            except AssertionError:
                print("list out of sync")

            print(seperated[1])
            print(index)
            input()

            ingredients = []
            for ingredient in ner:
                text = process_ingredient_text(ingredient)
                for word in text.split(" "):
                    ingredients.append(word)
            
            matched_ingredients = set(ingredient for ingredient in ingredients if ingredient in ingredient_set)

            for ingredient in matched_ingredients:
                ingredients_list = ingredients_index.get(ingredient, [])
                if ingredients_list==None:
                    ingredients_list = []

                ingredients_list.append(index)
                ingredients_index[ingredient]= ingredients_list

            index+=1        

    save(ingredients_index)

def indexString(indexes):
    string = ""
    for index in indexes:
        string+=str(index)
        string+=","

    return string[:-1]

def save(ingredients_index):

    SAVEFILE = "ingredients_index.csv"
    with open(SAVEFILE, mode="w", newline='') as f:
        writer = csv.writer(f)
        for ingredient in ingredients_index:
            if ingredients_index[ingredient]==None or ingredients_index[ingredient]==[]:
                continue

            row = [ingredient] + [indexString(ingredients_index[ingredient])]
            writer.writerow(row)


def get_ingredients_set():

    PATH  = "data/datasets/ingredients_list_cleaned.csv"
    ingredients = set()

    with open(PATH) as f:
        
        for line in f:
            word = line
            word = word.replace("\n", "")
            ingredients.add(word)
    

    return ingredients

def process_ingredient_text(ingredient):
    
    newWord = ""
    for letter in ingredient:
        if letter.isalnum() or letter==" ":
            newWord+=letter

    return newWord.strip()


if __name__=="__main__":
    main()