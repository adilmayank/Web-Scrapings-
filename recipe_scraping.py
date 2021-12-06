# importing neccessary libraries and modules

from bs4 import BeautifulSoup
import requests
import pandas as pd


# this is the link of a website I've chosen to scrape recipes and their ingredients from
url = 'https://www.indianhealthyrecipes.com/recipes'

# creating a response object after making a get request and converting it to simple text.
r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2}).text

# creating a BeautifulSoup object using the response text
soup = BeautifulSoup(r, 'html.parser')


"""
Since link to all the recipes was found on a single page, we find all instances of tag 'h4' with 'class' attribute
of 'pt-cv-title' which returns a list named recipe_index.
"""
recipe_index = soup.find_all('h4', {'class': 'pt-cv-title'})


# selecting from 3th recipe forwards since first three were themselves link to other recipes in the list.
recipe_index = recipe_index[3:]


# creating a dictionary to hold recipes and their ingredients
recipe_ingredient_dict = {}

# iterating through the list of 'h4' tags

for recipe in recipe_index:
    recipe_link = recipe.find('a')['href'] # find first occurrence of '<a>' tag and selecting 'href' attribute.
    recipe_link_request = requests.get(recipe_link).text # response object from link for the recipe.
    recipe_soup = BeautifulSoup(recipe_link_request, 'html.parser') # creating a BeautifulSoup object.
    recipe_name = recipe_soup.title.text # saving the recipe name from page title.

    # adding recipe_name as key in recipe_ingredient_dict's keys if not already present (which usually isn't the case.)
    if recipe_name not in recipe_ingredient_dict.keys():
        recipe_ingredient_dict[recipe_name] = [] # creating an empty list as a value for corresponding key.
    print(recipe_name) # just to see in realtime how many recipes-ingredients have been successfully added.

    # We use try block to keep any error in check.
    # There may be a link to a recipe which doesn't contain any ingredients or may not follow the logic of this block,
    # in which case the following block will raise an error and stop the execution.
    # So, if such a case occurs, the execution will move towards except block where the we delete the key (recipe_name)
    # for current iteration, since it will have no corresponding value, and continue the iteration.

    try:

        # fetching the recipe_id is important before finding its ingredients.

        recipe_id = recipe_soup.find_all('header', {'class': 'entry-header'})[0].find_all('a')[1]['data-recipe']
        box = recipe_soup.find_all('div', {'class': f'wprm-recipe-ingredients-container wprm-recipe-{recipe_id}-\
                                   ingredients-container wprm-block-text-normal wprm-ingredient-style-regular'})

        # this is where the ingredients are, 'box' object contains ingredients listed in different sub divisions.
        for i in box[0].find_all('div', {'class': 'wprm-recipe-ingredient-group'}):

            # since each subdivision has a list of ingredients, we need to interate through the list to fetch
            # each ingredient individually. This is why this inner loop is for.

            for j in i.find_all('li', {'class': 'wprm-recipe-ingredient'}):
                ingredient = j.find_all('input', {'class': 'wprm-checkbox'})[0]['aria-label']
                recipe_ingredient_dict[recipe_name].append(ingredient)
    except:
        del recipe_ingredient_dict[recipe_name]
        pass

# saving the recipe_ingredient_dict as an excel file.

#result = pd.DataFrame({key:pd.Series(value) for key, value in recipe_ingredient_dict.items()}).to_excel('Recipe.xlsx')


