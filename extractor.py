import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
import pytesseract
import textract
import os
import pdfplumber
root = Tk()

# layout and background.
background_image = tkinter.PhotoImage(file='background.png')
background_label = tkinter.Label(root, image=background_image)
background_label.place(relwidth=1,relheight=1)

# functions for the buttons in the software

def readfromimage():
    path = PathTextBox.get( '1.0', 'end-1c' )
    if path:
        im = Image.open(path)
        text = pytesseract.image_to_string( im, lang='eng' )
        ResultTextBox.delete( '1.0', END )
        ResultTextBox.insert( END, text )
        def write():
            # write output to txt file
            file = open( 'output.txt', 'w' )
            file.write( ResultTextBox.get( '1.0', 'end-1c' ) )
            file.close()
        write()
    else:
        ResultTextBox.delete( '1.0', END )
        ResultTextBox.insert( END, "FILE CANNOT BE READ" )
def OpenFile():
    name = askopenfilename( initialdir="/",
                            filetypes=(("PNG File", "*.png"), ("BMP File", "*.bmp"), ("JPEG File", "*.jpeg"),('PDF File',"*.pdf"),('DOCX File','*.docx')),
                            title="Choose a file."
                            )
    PathTextBox.delete( "1.0", END )
    PathTextBox.insert( END, name )
def docx_reader():
    docpath = PathTextBox.get( '1.0', 'end-1c' )
    text = textract.process(docpath)
    ResultTextBox.delete( '1.0', END )
    ResultTextBox.insert( END, text )
    def write():
        # write output to txt file
        file = open( 'output.txt', 'w' )
        file.write( ResultTextBox.get( '1.0', 'end-1c' ) )
        file.close()
    write()
def get_pdf_name():
    pathe = PathTextBox.get( '1.0', 'end-1c' )
    with pdfplumber.open(pathe) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
    os.system(f'ocrmypdf {pathe} output.pdf')
    with pdfplumber.open('output.pdf') as pdf:
        page = pdf.pages[0]
        text = page.extract_text(x_tolerance=2)
    ResultTextBox.delete('1.0', END)
    ResultTextBox.insert(END, text)
    def write():
        file = open( 'output.txt', 'w' )
        file.write( ResultTextBox.get( '1.0', 'end-1c' ) )
        file.close()
    write()


Title = root.title( "Southampton" )
path = StringVar()


# Labels in software.
HeadLabel = Label(root, text="    Text Extractor " )
HeadLabel.grid(row=1, column=2,sticky=(W))
InputLabel = Label( root, text="File Path:" )
InputLabel.grid( row=2, column=1, sticky=(W) )
PathLabel = Label( root, text="Path:" )
PathLabel.grid( row=3, column=1, sticky=(W) )
DataLabel = Label( root, text="Text:" )
DataLabel.grid( row=6, column=1, sticky=(W) )

# Buttons in the software.
BrowseButton = Button( root, text="Find File Path", command=OpenFile )
BrowseButton.grid( row=2, column=2 )

BrowseButton2 = Button( root, text="Extract Text From Pdf ", command=get_pdf_name)
BrowseButton2.grid( row=3, column=2 )


ReadButton = Button( root, text="Extract Text From Image", command=readfromimage)
ReadButton.grid( row=5, column=2 )
ReadButton2 = Button( root, text="Extract Text From docx", command=docx_reader)
ReadButton2.grid( row=6, column=2 )

# output textbox
PathTextBox = Text( root, height=2 )
PathTextBox.grid( row=4, column=1, columnspan=2 )
ResultTextBox = Text( root, height=6 )
ResultTextBox.grid( row=7, column=1, columnspan=2 )



root.mainloop()