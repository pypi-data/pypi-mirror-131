# Simple localization package for Python

## Setup:
1. Create a localization folder wherever you want in your project.
2. Add localization files inside. This package use `.json` files.

    ### Example:

    ### (localization/en_EN.json)
    ```json
    {
        "GREETINGS": "Hello !",
        "GOODBYE": "Goodbye !"
    }
    ```
    ### (localization/fr_FR.json)
    ```json
    {
        "GREETINGS": "Bonjour !",
        "GOODBYE": "Au revoir !"
    }
    ```

## Usage

```python
from simple_localization import LocalizationManager

localization = LocalizationManager('../localization', 'en_EN')
```
It's as simple as that !

```python
>>> localization['GREETINGS']
Hello !
```

You can change the language of an already existing LocalizationManager object using `change_language`:

```python
>>> localization['GREETINGS']
Hello !
>>> localization.change_language("fr_FR")
>>> localization['GREETINGS']
Bonjour !
```

## Links
- [Documentation](https://myselfleo.com/simple-localization/docs/)