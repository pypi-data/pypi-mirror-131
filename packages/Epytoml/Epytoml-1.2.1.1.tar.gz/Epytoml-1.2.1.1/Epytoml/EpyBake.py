"""
EpyBake
An Epytoml module
Created by: Zhean 'Z1aaan' Ganituen

EpyBake is one of the most important modules of Epytoml.
Used for exporting the Epytoml created files to the supported markup languages or pdf.
"""

import os.path as path
import os
import pdfkit
import tkinter as tk
from tkPDFViewer import tkPDFViewer
from Epytoml import Notaker as ntk


def ntkBake(fileName, exportTo=None, directory=None):
    """Exports the file to html and pdf file format.

    Args:
        fileName (str): The file name of the exported file.
        exportTo (int, optional): Exports the file in html only, or html and pdf. Defaults to Both.
        directory (str, optional): Specific file directory you want the exported file to be located. Defaults to None.
    """
    content = ntk.ntk_ContWhole
    fileNameType = fileName + ".html"

    if directory is None or directory == 0:
        fileNameTypePDF = fileName + ".pdf"

        if exportTo is None or exportTo == 0:
            # run default, export to both html and pdf
            with open(fileNameType, "w") as f:
                f.write(content)
            pdfkit.from_file(fileNameType, fileNameTypePDF)
        else:
            if exportTo == 1:
                # export to html only
                with open(fileNameType, "w") as f:
                    f.write(content)
            else:
                # run default, export to both html and pdf
                with open(fileNameType, "w") as f:
                    f.write(content)
                pdfkit.from_file(fileNameType, fileNameTypePDF)

    else:

        # comepleteFileName of .html file
        completeFileName = path.join(directory, fileNameType)

        fileNameTypePDF = fileName + ".pdf"

        # completeFileName of .pdf file
        completeFileNamePDF = path.join(directory, fileNameTypePDF)

        if exportTo is None or exportTo == 0:
            # run default, export to both html and pdf
            with open(completeFileName, "w") as f:
                f.write(content)
            pdfkit.from_file(completeFileName, completeFileNamePDF)
        else:
            if exportTo == 1:
                # export to html only
                with open(completeFileName, "w") as f:
                    f.write(content)
            else:
                # run default, export to both html and pdf
                with open(completeFileName, "w") as f:
                    f.write(content)
                pdfkit.from_file(completeFileName, completeFileNamePDF)


def preBake(filetype):
    """Display the current output of the Epytoml file.

    Args:
        filetype (str): Specify what Epytoml file type is used.
    """

    def makeGUI():
        # title of the preBake window
        global root
        root = tk.Tk()

        root.title("Epytoml - EpyBake - preBake")

        # contents of the GUI
        # render pdf file in the tkinter GUI
        pdfFile = tkPDFViewer.ShowPdf().pdf_view(
            root, pdf_location=bakeFile, bar=False, width=75, height=50
        )
        pdfFile.grid(row=6, column=0, columnspan=10, rowspan=10)

        root.mainloop()

    def makeFile():
        # export the file into html, then pdf, then delete the html file
        # create both html and pdf files

        # write an html file with the content of the notaker file

        filename_html = bakeFile + ".html"
        filename_pdf = bakeFile + ".pdf"

        with open(filename_html, "w") as f:
            f.write(file)

        # convert the created html file into a pdf file
        pdfkit.from_file(filename_html, filename_pdf)

        # delete the created html file
        os.remove(filename_html)

    # store the filename of the notaker file created or the pdf file to be read
    global filename
    bakeFile = ""

    filetype = filetype.upper()
    
    if filetype == "NOTAKER" or "NTK":
        file = ntk.ntk_ContWhole
        bakeFile = "preBake_Notaker"
    

    # run the makeFile function
    makeFile()

    bakeFile = bakeFile + ".pdf"

    # run the makeGUI function
    makeGUI()

    # then once the GUI is closed, delete the created pdf file.
    os.remove(bakeFile)
