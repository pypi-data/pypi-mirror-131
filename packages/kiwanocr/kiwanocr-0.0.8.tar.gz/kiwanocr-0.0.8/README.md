# KiwanOCR

This package takes a single PDF file or a list of PDF files and returns their content as a text file.

[<img alt="Kiwano fruit image" width="250px" src="https://www.eatwellwithgina.com/wp-content/uploads/2014/06/photo-2-1-533x400.jpg" />](https://www.google.com/)

- Requirements
- Methods

## Requirements

### ```pip install``` or ```brew install```
Make sure you have installed these dependencies:
- ```brew install tesseract```
- ```brew install poppler```
- ```pip pdf2images```

### ```import```
Import the following:
- ```from PIL import Image```
- ```import pytesseract``` ## python interface for tesseract
- ```import os``` ## navitage, create directories
- ```import shutil``` ## to delete the image folders with their imgs
- ```from pdf2image import convert_from_path``` ## to turn pdf to image
- ```import glob``` ## to glob files into a list
- ```from pathlib import Path``` ## to specify path to your files
- ```from natsort import natsorted, ns``` ## natural sorting
- ```import re``` ## for regex


## Methods

### Setup

1. ```pip install kiwanocr```.
2. ```from kiwano import ocr```

### OCR a single PDF
```ocr.ocr_file(file_name, output_file_name, language, resolution)```

#### Arguments
- file_name: as a string
- output_file_name: as a string
- language: default is English (use ```tesseract --list-langs``` to retrieve langague codes )
- resolution: default is 300 dpi (use integer value between 100 and 1200)

### OCR a list of PDFs
```ocr.ocr_files(list_name, output_file_name, language, resolution)```
- list_name: The only difference is to enter a list name

## Output

A ```.txt``` file is placed in a ```output``` folder.
