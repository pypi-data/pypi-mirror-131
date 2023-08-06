# cocktail_info

This project is called cocktail_info. The functions are built to get the information of cocktails users want to know. Below are the explanations for what each function can do:

Function get_id(): This function can help users to get the id of the cocktail they input so that they could use for further search.

Function get_cocktail(): This function can help users to get the details of the cocktails they input, such as ID, Name, Category, whether they contain alcohol, the ways to make them, etc.

Function get_one(): This function can help users to get the information of the exact one cocktail they want through the unique id.

Function get_ingredient(): This function can help users to get the names and measures of the ingredients in the cocktail after the users input the name of cocktails. 

Function get_pics(): This function can help users to get the pictures of the cocktails along with the IDs and names they input.

Function decsription(): This function can give users the introduction of cocktails users input.

Function is_in(): This function allows users to check whether the ingredient they input is in the ingredients list.

## Installation

```bash
$ pip install cocktail_info
```

## Usage

```bash
from cocktail_info import cocktail_info
```

### Get the id of the cocktail

```bash
cocktail_info.get_id('gin')
```

### Get the information of the cocktails

```bash
cocktail_info.get_cocktail('gin')
```

### Get the information of the exact cocktail you want to know

```bash
cocktail_info.get_one('gin')
```

### Get the ingredients of the cocktails

```bash
cocktail_info.get_ingredient('gin')
```

### Get the pictures of the cocktails

```bash
cocktail_info.get_pics('gin')
```

### Get the introduction of the cocktail

```bash
cocktail_info.description('gin')
```

### Tell whether one ingredient is in the cocktail

```bash
cocktail_info.is_in('gin')
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`cocktail_info` was created by Kun Yao. It is licensed under the terms of the MIT license.

## Credits

`cocktail_info` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
