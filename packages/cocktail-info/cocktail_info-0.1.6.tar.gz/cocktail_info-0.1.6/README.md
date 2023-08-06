# cocktail_info

Get the information of cocktails.

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
