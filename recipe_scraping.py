from bs4 import BeautifulSoup
import requests
import pandas as pd


url = 'https://www.indianhealthyrecipes.com/recipes'

r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2}).text

soup = BeautifulSoup(r, 'html.parser')

recipe_index = soup.find_all('h4', {'class': 'pt-cv-title'})
recipe_index = recipe_index[3:]

recipe_ingredient_dict = {}

for recipe in recipe_index:
    recipe_link = recipe.find('a')['href']
    recipe_link_request = requests.get(recipe_link).text
    recipe_soup = BeautifulSoup(recipe_link_request, 'html.parser')
    recipe_name = recipe_soup.title.text

    if recipe_name not in recipe_ingredient_dict.keys():
        recipe_ingredient_dict[recipe_name] = []
    print(recipe_name)
    try:
        recipe_id = recipe_soup.find_all('header', {'class': 'entry-header'})[0].find_all('a')[1]['data-recipe']
        box = recipe_soup.find_all('div', {'class': f'wprm-recipe-ingredients-container wprm-recipe-{recipe_id}-ingredients-container wprm-block-text-normal wprm-ingredient-style-regular'})



        for i in box[0].find_all('div', {'class': 'wprm-recipe-ingredient-group'}):
            for j in i.find_all('li', {'class': 'wprm-recipe-ingredient'}):
                ingredient = j.find_all('input', {'class': 'wprm-checkbox'})[0]['aria-label']
                recipe_ingredient_dict[recipe_name].append(ingredient)
    except:
        del recipe_ingredient_dict[recipe_name]
        pass


#result = pd.DataFrame({key:pd.Series(value) for key, value in recipe_ingredient_dict.items()}).to_excel('Recipe.xlsx')


