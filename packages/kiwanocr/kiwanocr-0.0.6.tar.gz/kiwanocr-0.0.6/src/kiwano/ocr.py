# Import libraries
from PIL import Image
import requests
import pytesseract
import os ## navitage, create directories
import shutil ## to delete the image folders with their imgs
from pdf2image import convert_from_path ## to turn pdf to image
import glob ## to glob files into a list
from pathlib import Path ## to specify path to your files
from natsort import natsorted, ns ## natural sorting
import re ## for regex


### FUNCTION to convert pdf to jpg
def to_jpg(PDF_file, resolution):
    '''
    arguments
    - PDF_file = name of pdf file to OCR
    - resolution = resolution of conversion of pdf to jpeg
    
    '''
    ## store in a folder for conversion
    conversion_path = Path('conversion_img/')
    conversion_path.mkdir(exist_ok=True)

    ## regex for in case folder used
    folder_pattern = re.compile(r".+\/")

    '''
    Part #1 : Converting PDF to images
    '''

    # Store all the pages of the PDF in a variable
    pages = convert_from_path(PDF_file, resolution)
    print(f"Give me a second...converting '{PDF_file}' to a JPEG")

    # Counter to store images of each page of PDF to image
    image_counter = 1
    

    # Iterate through Sall the pages stored above
    for page in pages:
        ## Declaring filename for each page of PDF as JPG
        ## remove the .pdf extention (last 4 characters)
        ## remove the
        if re.search(folder_pattern, PDF_file) != None:
            PDF_file = re.split(folder_pattern, PDF_file)[1]
   
        filename = str(PDF_file[ : -4])+"_page_"+str(image_counter)+".jpg"
        print(f"{filename} has been converted to an image. Will OCR it now...")
        filename = os.path.join(conversion_path,filename)
        print(filename)
        # Save the image of the page in system
        page.save(filename, 'JPEG')

        # Increment the counter to update filename
        image_counter+=1


### FUNCTION TO OCR JPG

def jpg_to_txt(outfile, language = "eng"):

    '''
    Function that Recognizing text from the images using OCR
    Argument(s):
    - outfile = file name (as a string) to store your OCRed text 
    - language = tessaract language code. eng by default
    '''
    ## store in an output folder
    output_path = Path('output/')
    output_path.mkdir(exist_ok=True)
    conversion_path = Path('conversion_img/')

    # # # # Creating a text file to write the output
    outfile = os.path.join(output_path,outfile)
    # # #
    # # # # Open output file and append all info

    with open(outfile, "a") as f:
        ## grab all jpegs
        img_files = sorted(Path(conversion_path).glob('*.jpg'), reverse=False)

        ## path objects turn urls into strings and you can't sort numbers with underscores, etc
        ## the function below uses regex to find the numbers and turn them into integer.
        ## natsort library
        ## https://natsort.readthedocs.io/en/master/howitworks.html
        from natsort import natsorted, ns
        
        ## .as_posix() returns a string representation of the path with forward slashes (/)
        ## more info: https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.as_posix
        ## if you receive a posix error, comment out next line and uncomment the one after
        img_files = [img_file for img_file in img_files] 
#         img_files = [img_file.as_posix() for img_file in img_files] 
#         print(f"img_files: {img_files}")
        img_files = natsorted(img_files, alg=ns.PATH)
#         print(img_files)

        counter = 0
        for img_file in img_files:
            counter+=1
            print(f"Converting image {counter} of {len(img_files)} to text!")
            text = f"\n\n\nFILE_Info: {img_file} \n\n\n \
             {str(pytesseract.image_to_string(Image.open(img_file), lang = language))}"
            
            ## In case a word is hyphenated at the end of a line, we
            ## remove the hyphen by using every '-\n' to ''.
            text = text.replace('-\n', '')
            # print(f"Here's the text: \n {text}")

            f.write(text)

            ## Delete the folder
        shutil.rmtree(conversion_path)
        return img_files
        

## Function that runs the two functions above
 
def ocr_file(PDF_file, outfile, language = "eng", resolution = 300):
    '''
    This function runs to_jpg() and jpg_to_txt()
    Arguments:
    - PDF_file = pdf file name(as strings)
    - outfile = file name (as a string) to store your OCRed text
    - language = tessaract language code. eng by default
    - resolution = resolution of scan as int between 300 and 600
    '''
    to_jpg(PDF_file, resolution)
    checker(outfile)
    jpg_to_txt(outfile)
    
    

## Function to delete outfile if it already exists
## This avoids the problem of appending existing data 

def checker(outfile):
    output_path = Path('output/')
    if os.path.exists(os.path.join(output_path,outfile)):
        os.remove(os.path.join(output_path,outfile))
        print("The file name you provided already existed.\n\
It has been been removed to avoid appending existing data!")
    else:
        print("Can not delete the file as it doesn't exists")

## Function that iterates through a list of files to OCR  
def ocr_files(files_list, name_output_file, language = "eng", resolution = 300):
    '''
    This function iterates through a list that needs OCRing
    It taps all the functions above so we enter ALL the arguments here:
    Arguments:
    - files_list = name of list that must be iterated. You have globbed files into it.
    - outfile = file name (as a string) to store your OCRed text
    - resolution = resolution of scan as int between 300 and 600
    '''
    checker(name_output_file)
    counter = 1
    len(files_list)
    for file in files_list:
        print(f"Grabbing '{file}' (file {counter} of {len(files_list)}) from your list....")
        counter += 1
        file_ocr(file, name_output_file, resolution)
    print(f"A text file called '{name_output_file}' is ready for you....")