



# Pdf2Img
  
Module for performing actions with a PDF file  

*Read this in other languages: [English](Manual_Pdf2Img.md), [Português](Manual_Pdf2Img.pr.md), [Español](Manual_Pdf2Img.es.md)*
  
![banner](imgs/BANNER_PDF2IMG.jpg)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  


## Description of the commands

### Convert to JPG
  
Convert each sheet of a pdf file to jpg format
|Parameters|Description|example|
| --- | --- | --- |
|Input PDF|Location of the folder where the PDF to convert to JPG is located|file.pdf|
|Path and name of the jpg file to save|Location and name of the jpg file to be saved. If the pdf contains more than one sheet, the sheet number will be added to the files|C:/Users/User/Desktop/image.jpg|
|Ancho de imagen|Numeric value that will represent the width of the image in pixels.|1500|
|DPI|DPI or Dots per inch that the image will have. Default is 150 DPI|150|
|Resultado|Variable where True or False will be stored depending on whether the module was able to execute the action|variable|

### Add image to PDF
  
Adds an image to a PDF on the page and coordinates entered.
|Parameters|Description|example|
| --- | --- | --- |
|Input PDF|PDF file to which the image will be added|file.pdf|
|JPG file|jpg file that will be added to the pdf|path/image.jpg|
|Page|Page number of the pdf where the image will be added|3|
|Coordinates|Coordinates of the pdf page where the image will be placed. If coordinates higher than the page size are placed, the image cannot be displayed.|150,340|
|Output PDF|Page number of the pdf where the image will be added|path/new_file.pdf|
|Resultado|Variable where True or False will be stored depending on whether the module was able to execute the action|variable|

### Crop image from PDF
  
Create an image from the assigned coordinates.
|Parameters|Description|example|
| --- | --- | --- |
|Input PDF|PDF file that will be used in the module|file.pdf|
|jpg image|Path and name that the jpg image extracted from the pdf will have|path/image.jpg|
|Page|Page number of the pdf from where the image will be obtained|3|
|Start Coordinates|Coordinates from where the image will be obtained|0,0|
|End Coordinates|Coordinates to where the image will be obtained|1000,1000|
|DPI|DPI or Dots per inch that the image will have. Default is 150 DPI|150|
