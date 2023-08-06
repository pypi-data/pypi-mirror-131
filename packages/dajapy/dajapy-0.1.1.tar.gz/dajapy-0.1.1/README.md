# dajapy
日本語のダジャレを判定するPythonパッケージ

## Installation
```
pip install dajapy
```

## Usage
```
import dajapy

text = "アルミ缶の上にあるみかん"
dajare_flag = dajapy.is_dajare(text)
print(dajare_flag)
```
output
```
True
```