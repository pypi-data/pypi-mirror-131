# dta (Dict to Attributes)

dta is very small dict (or json) to attributes converter.  
It is only have 1 files and applied to every python versions.  
No need dependencies required so your repository size won't go to hell.

## Features

- Ability to convert lame dict object to class attributes!
- Ability to convert those attributes back to dict!

## Installation

Use pip to install [package](https://pypi.org/project/dta)
```bash
pip install dta
```

Or Use github repository and build it
```bash
pip install git+https://github.com/dumb-stuff/dta
```

## Usage

Import dta.
```py
import dta
```
For converting to attributes do
```py
import dta 
SomeCoolConvertedDictToAttributes = dta.Dict2Attr({"stuff":["balls","watch anime girls","OwO"]})
SomeCoolConvertedDictToAttributes.stuff[1]
```
For converting attributes back to dict for saving purpose do
```py
import dta
dta.Attr2Dict(SomeCoolConvertedDictToAttributes)
```
