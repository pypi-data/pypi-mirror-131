import requests
import json
import pandas as pd
import numpy as np
import re
from IPython.display import Image, HTML
import warnings
warnings.filterwarnings('ignore')

def get_id(text):
    '''
    Introduction:
    -------------
    This function can help users to get the id of the cocktail they input so that they could use for further search.

    Inputs:
    -------------
    'text': str. The name of cocktail the users input.

    Outputs:
    -------------
    One dataframe containing the ID, Name of the cocktails the users want to find.

    Example:
    -------------
    >>>from cocktail_info import cocktail_info
    >>>a = cocktail_info.get_id('gin')
    >>>a
        ID   Drink
    0 11410 Gin Fizz
    1 11417 Gin Sour
    2 11936 Pink Gin
    3 11408 Gin Daisy
    4 11415 Gin Sling
    5 11416 Gin Smash
    6 11420 Gin Toddy
    7 11407 Gin Cooler
    8 11418 Gin Squirt
    9 17230 Gin Rickey
    10 11419 Gin Swizzle
    11 178342 Gin and Soda
    12 11403 Gin And Tonic
    13 12057 Royal Gin Fizz
    14 178314 Gin Basil Smash
    15 12224 Sloe Gin Cocktail
    16 12718 Pineapple Gingerale Smoothie
    '''
    try:
        params_text = {'s' : text}
        r = requests.get('http://www.thecocktaildb.com/api/json/v1/1/search.php?', params = params_text)
        r.raise_for_status()

    except:
        print("Please input the right cocktail's name!")

    else:
        dump = json.dumps(r.json(), indent = 2)
        cock_get_id = json.loads(dump)
        cock_id = pd.DataFrame(cock_get_id['drinks'])
        cock_id_new = cock_id[['idDrink', 'strDrink']]
        cock_id_new.rename(columns = {'idDrink':'ID', 'strDrink':'Name'}, inplace = True)

        return cock_id_new

def get_cocktail(name):
    '''
    Introduction:
    -------------
    This function can help users to get the details of the cocktails they input, such as ID, Name, Category, whether they contain alcohol, the ways to make them, etc.

    Inputs:
    -------------
    'name': str. The name of cocktail the users input.

    Outputs:
    -------------
    One dataframe containing the ID, Name, Category, Alcoholic, Glass, Instructions and the pictures of them.

    Example:
    -------------
    >>>from cocktail_info import cocktail_info
    >>>b = cocktail_info.get_cocktail('gin')
    >>>b
        ID Name Category Alcoholic Glass Instructions Picture
    0 11410 Gin Fizz Ordinary Drink Alcoholic Highball glass Shake all ingredients with ice cubes, except soda water. Pour into glass. Top with soda water. 
    1 11417 Gin Sour Ordinary Drink Alcoholic Whiskey sour glass In a shaker half-filled with ice cubes, combine the gin, lemon juice, and sugar. Shake well. Strain into a sour glass and garnish with the orange slice and the cherry. 
    2 11936 Pink Gin Ordinary Drink Alcoholic White wine glass Pour the bitters into a wine glass. Swirl the glass to coat the inside with the bitters, shake out the excess. Pour the gin into the glass. Do not add ice. 
    3 11408 Gin Daisy Ordinary Drink Alcoholic Old-fashioned glass In a shaker half-filled with ice cubes, combine the gin, lemon juice, sugar, and grenadine. Shake well. Pour into an old-fashioned glass and garnish with the cherry and the orange slice. 
    4 11415 Gin Sling Ordinary Drink Alcoholic Old-fashioned glass Dissolve powdered sugar in mixture of water and juice of lemon. Add gin. Pour into an old-fashioned glass over ice cubes and stir. Add the twist of orange peel and serve. 
    5 11416 Gin Smash Ordinary Drink Alcoholic Old-fashioned glass Muddle sugar with carbonated water and mint sprigs in an old-fashioned glass. Add gin and 1 ice cube. Stir, add the orange slice and the cherry, and serve. 
    6 11420 Gin Toddy Ordinary Drink Alcoholic Old-fashioned glass Mix powdered sugar and water in an old-fashioned glass. Add gin and one ice cube. Stir, add the twist of lemon peel, and serve. 
    (The 'Picture' could show the pictures of cocktail, but the example could not show this kind of files.)
    ......

    '''
    try:
        params_cocktail = {'s' : name}
        r = requests.get('http://www.thecocktaildb.com/api/json/v1/1/search.php?', params = params_cocktail)
        r.raise_for_status()

    except:
        print("Please input the right cocktail's name!")

    else:
        dump = json.dumps(r.json(), indent = 2)
        cock_name = json.loads(dump)
        original = pd.DataFrame(cock_name['drinks'])
        cock_info = original[['idDrink', 'strDrink', 'strCategory', 'strAlcoholic', 'strGlass', 'strInstructions', 'strDrinkThumb']]
        cock_info.rename(columns = {'idDrink':'ID', 'strDrink':'Name', 'strCategory':'Category', 'strAlcoholic':'Alcoholic', 'strGlass':'Glass','strInstructions':'Instructions', 'strDrinkThumb':'Picture'}, inplace = True)
        cock_info['Instructions'] = cock_info.Instructions.apply(lambda x: x.replace('\r\n', ' '))

        def path_to_image_html(path):
            '''
             This function essentially convert the image url to 
             '<img src="'+ path + '"/>' format. And one can put any
             formatting adjustments to control the height, aspect ratio, size etc.
             within as in the below example. 
            '''

            return '<img src="'+ path + '" style=max-height:124px;"/>'

        html = HTML(cock_info.to_html(escape=False ,formatters=dict(Picture=path_to_image_html)))
        return html

def get_one(number):
    '''
    Introduction:
    -------------
    This function can help users to get the information of the exact one cocktail they want through the unique id.

    Inputs:
    -------------
    'number': int. The unique id of cocktail the users input.

    Outputs:
    -------------
    One dataframe containing the ID, Name, Category, Alcoholic, Glass, Instructions and Picture.

    Example:
    -------------
    >>>from cocktail_info import cocktail_info
    >>>c = cocktail_info.get_one('178342')
    >>>c
         ID Name Category Alcoholic Glass Instructions Picture
    0 178342 Gin and Soda Cocktail Alcoholic Highball glass Pour the Gin and Soda water into a highball glass almost filled with ice cubes. Stir well. Garnish with the lime wedge. 
    (The 'Picture' could show the pictures of cocktail, but the example could not show this kind of files.)

    '''
    try:
        params_id = {'i' : number}
        r = requests.get('http://www.thecocktaildb.com/api/json/v1/1/lookup.php?', params = params_id)
        r.raise_for_status()

    except:
        print("The id you input is wrong, please input the right cocktails IDs!")

    else:
        dump = json.dumps(r.json(), indent = 2)
        cock_get_one = json.loads(dump)
        cock_one = pd.DataFrame(cock_get_one['drinks'])
        cock_one_old = cock_one[['idDrink', 'strDrink', 'strCategory', 'strAlcoholic', 'strGlass', 'strInstructions', 'strDrinkThumb']]
        cock_one_old.rename(columns = {'idDrink':'ID', 'strDrink':'Name', 'strCategory':'Category', 'strAlcoholic':'Alcoholic', 'strGlass':'Glass', 'strInstructions':'Instructions', 'strDrinkThumb':'Picture'}, inplace=True)
        cock_one_old['Instructions']= cock_one_old.Instructions.apply(lambda x: x.replace('\r\n', ' '))

        def path_to_image_html(path):
            '''
             This function essentially convert the image url to 
             '<img src="'+ path + '"/>' format. And one can put any
             formatting adjustments to control the height, aspect ratio, size etc.
             within as in the below example. 
            '''

            return '<img src="'+ path + '" style=max-height:124px;"/>'

        html = HTML(cock_one_old.to_html(escape=False ,formatters=dict(Picture=path_to_image_html)))

        return html

def get_ingredient(cock_name):
    '''
    Introduction:
    -------------
    This function can help users to get the names and measures of the ingredients in the cocktail after the users input the name of cocktails. 

    Inputs:
    -------------
    'cock_name': str. The name of cocktail the users input.

    Outputs:
    -------------
    One dataframe containing the ID, Name, Ingredients and their mesaures.

    Example:
    -------------
    >>>from cocktail_info import cocktail_info
    >>>d = cocktail_info.get_ingredient('vodka')
    >>>d
        idDrink strDrink strIngredient1 strIngredient2 strIngredient3 strIngredient4 strIngredient5 strIngredient6 strMeasure1 strMeasure2 strMeasure3 strMeasure4 strMeasure5
    0 13196 Long vodka Vodka Lime Angostura bitters Tonic water Ice 5 cl 1/2 4 dashes 1 dl Schweppes 4
    1 16967 Vodka Fizz Vodka Half-and-half Limeade Ice Nutmeg 2 oz 2 oz 2 oz 
    2 12800 Coffee-Vodka Water Sugar Coffee Vanilla Vodka Caramel coloring 2 cups 2 cups white 1/2 cup instant 1/2 1 1/2 cup
    3 14167 Vodka Martini Vodka Dry Vermouth Olive 1 1/2 oz 3/4 oz 1 
    4 15403 Vodka Russian Vodka Schweppes Russchian 2 oz 
    5 12460 Vodka And Tonic Vodka Tonic water 2 oz 

    '''

    try:
        params_cocktail_name = {'s' : cock_name}
        r = requests.get('http://www.thecocktaildb.com/api/json/v1/1/search.php?', params = params_cocktail_name)
        r.raise_for_status()

    except:
        print("Please input the right cocktail's name!")

    else:
        dump = json.dumps(r.json(), indent = 2)
        cock_components = json.loads(dump)
        original_components = pd.DataFrame(cock_components['drinks'])
        components = original_components.iloc[ : , 17 : 46].dropna(axis = 1,how = 'all') 
        id_name = original_components.iloc[: , 0 : 2]
        all_ingredient = pd.concat([id_name, components], axis = 1)
        all_ingredient.fillna(' ',inplace=True)

        return all_ingredient

def get_pics(pics):
    '''
    Introduction:
    -------------
    This function can help users to get the pictures of the cocktails along with the IDs and names they input.

    Inputs:
    -------------
    'pics': str. The name of cocktail the users input.

    Outputs:
    -------------
    One dataframe containing the IDs, names and the pictures of the cocktails.

    Example:
    -------------
    >>>from cocktail_info import cocktail_info
    >>>e = cocktail_info.get_pics('whisky')
    >>>e
        ID Drink_Name Picture
    0 16262   H.D. 
    (The 'Picture' could show the pictures of cocktail, but the example could not show this kind of files.)

    '''      
    try:
        params_pics = {'i' : pics}
        r = requests.get('http://www.thecocktaildb.com/api/json/v1/1/filter.php?', params = params_pics)
        r.raise_for_status()

    except:
        print("Please input the right name of the cocktail!")  

    else:
        dump = json.dumps(r.json(), indent = 2)
        parsed = json.loads(dump)
        pics_old = pd.DataFrame(parsed['drinks'])
        pics_new = pics_old[['idDrink', 'strDrink', 'strDrinkThumb']]
        pics_new.rename(columns = {'idDrink':'ID','strDrink':'Drink_Name', 'strDrinkThumb':'Picture'}, inplace=True)

        def path_to_image_html(path):

            '''
             This function essentially convert the image url to 
             '<img src="'+ path + '"/>' format. And one can put any
             formatting adjustments to control the height, aspect ratio, size etc.
             within as in the below example. 
            '''
            return '<img src="'+ path + '" style=max-height:124px;"/>'

        html = HTML(pics_new.to_html(escape=False ,formatters=dict(Picture=path_to_image_html)))
        return html

def description(history):
    '''
    Introduction:
    -------------
    This function can give users the introduction of cocktails users input.

    Inputs:
    -------------
    'history': str. The name of cocktail the users input.

    Outputs:
    -------------
    One paragraph introduction about the cocktail the users input.

    Example:
    -------------
    >>>from cocktail_info import cocktail_info
    >>>f = cocktail_info.description('gin')
    >>>f
    'The name of the wine you type in is or similar to: Gin. Gin is a distilled alcoholic drink that derives its predominant flavour from juniper berries (Juniperus communis). Gin is one of the broadest categories of spirits, all of various origins, styles, and flavour profiles, that revolve around juniper as a common ingredient. From its earliest origins in the Middle Ages, the drink has evolved from a herbal medicine to an object of commerce in the spirits industry. Gin emerged in England after the introduction of the jenever, a Dutch liquor which originally had been a medicine. Although this development had been taking place since early 17th century, gin became widespread after the William of Orange-led 1688 Glorious Revolution and subsequent import restrictions on French brandy. Gin today is produced in subtly different ways, from a wide range of herbal ingredients, giving rise to a number of distinct styles and brands. After juniper, gin tends to be flavoured with botanical/herbal, spice, floral or fruit-flavours or often a combination. It is most commonly consumed mixed with tonic water. Gin is also often used as a base spirit to produce flavoured gin-based liqueurs such as, for example, Sloe gin, traditionally by the addition of fruit, flavourings and sugar.'
    
    '''

    try:
        params = {'i': history}
        r = requests.get('http://www.thecocktaildb.com/api/json/v1/1/search.php?', params = params)
        r.raise_for_status()

    except:
        print("Please input the right alcohol name!")  

    else:
        description1 = json.dumps(r.json(), indent = 2)
        parsed = json.loads(description1)
        alcohol_name = parsed['ingredients'][0]['strIngredient']
        introduction = parsed['ingredients'][0]['strDescription'].replace('\r\n\r\n', ' ')
        all_info = "The name of the wine you type in is or similar to: " + alcohol_name + "." + " " + introduction

        return all_info

def is_in(ingredient):
    '''
    Introduction:
    -------------
    This function allows users to check whether the ingredient they input is in the ingredients list.

    Inputs:
    -------------
    'ingredient': str. The name of ingredient the users input.

    Outputs:
    -------------
    One sentence to tell the users whether the ingredient they input is a component of the cocktail.

    Example:
    -------------
    >>>from cocktail_info import cocktail_info
    >>>g = cocktail_info.is_in('gin')
    >>>g
    'The ingredient is in the list.'
    '''
    try:
        ingre = ingredient.capitalize()
        r = requests.get('http://www.thecocktaildb.com/api/json/v1/1/list.php?i=list')
        r.raise_for_status()
    except:
        print("The ingredient you input is not valid, try another ingredient!")

    else:
        dump = json.dumps(r.json(), indent = 2)
        ingredients = json.loads(dump)
        all_ingredients = pd.DataFrame(ingredients['drinks'])
        all_ingredient = [a for a in all_ingredients.strIngredient1]
        if (ingre in all_ingredient) or (ingredient in all_ingredient):
            return "The ingredient is in the list."
        else:
            return "The ingredient is not in the list, please try another ingredient"

