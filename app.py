import os
import time
import PyPDF2
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename
import pdf2image
import os, sys




app = Flask(__name__)
#app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = 'C:/Users/Choi/Desktop/capston/uploads'

@app.route('/') #main 페이지
def inputTest():
    return render_template('index.html')


@app.route('/view', methods=['GET', 'POST']) #/view 페이지
def uploader_file():
    try:
        from PIL import Image
    except ImportError:
        import Image
    import pytesseract
    Image.MAX_IMAGE_PIXELS = None

    #initialize the path to your documents
    PATH = 'C:/Users/Choi/Desktop/capston/uploads/'
    SAVED_PATH = 'C:/Users/Choi/Desktop/capston/ocr_txt/'
    poppler_path= "C:/Users/Choi/Desktop/capston/uploads/poppler-22.04.0/Library/bin"

    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
    #initialize the counter that you will use later in your pdf extraction function
    i = 1


        # This function deletes all ppm and .DS_Store files from the folder
    def delete_ppms():
        for file in os.listdir(PATH):
            if '.ppm' in file or '.DS_Store' in file:
                try:
                    os.remove(PATH + file)
                except FileNotFoundError:
                    pass
                
                
                
    # initialize lists for each document type
    pdf_files = []
    docx_files = []

    # append document names into the lists by their extension type
    for f in os.listdir(PATH):
        full_name = os.path.join(PATH, f) 
        if os.path.isfile(full_name):
            name = os.path.basename(f)
            filename, ext = os.path.splitext(name)
            print(filename)
            if ext == '.pdf' and filename+'.txt' not in os.listdir(SAVED_PATH):
                pdf_files.append(name)
            elif ext == ('.docx'):
                docx_files.append(name)
                
                
    # This function converts pdf to images and then extracts text from images
    def pdf_extract(file_name, i):
        print("extracting from file:", file_name)
        delete_ppms()
        images = pdf2image.convert_from_path(PATH + file_name, poppler_path=poppler_path)
        j = 0
        for file in sorted (os.listdir(PATH)):
            if '.ppm' in file and 'image' not in file:
                os.rename(PATH + file, PATH + 'image' + str(i) + '-' + str(j) + '.ppm')
                j += 1
        j = 0
        f = open(SAVED_PATH +f'{file_name[:-4]}.txt', 'w')
        files = [f for f in os.listdir(PATH) if '.ppm' in f]

        for file in sorted(files, key=lambda x: int(x[x.index('-') + 1: x.index('.')])):
            temp = pytesseract.image_to_string(Image.open(PATH + file))
            f.write(temp)
        f.close()

        # Run for-loop for each document in range of pdf_files list
    for i in range(len(pdf_files)):
        pdf_file = pdf_files[i]
        pdf_extract(pdf_file, i)
    delete_ppms()
    return render_template('view.html')

@app.route('/result', methods=['GET', 'POST']) #결과 확인 페이지
def check_file():
    time.sleep(3)
    return render_template('result.html')

'''
@app.route('/view',methods = ['GET', 'POST']) #pdf read하는 페이지
def view():
    pdffile = open("C:/Users/Choi/Desktop/gugudan/uploads/shibainu.pdf","rb")
    fileReader = PyPDF2.PdfFileReader(pdffile)

    #fileReader.pageMode()

    fileReader.documentInfo
    print(fileReader.numPages)
    pageObj = fileReader.getPage(0)

    text = pageObj.extractText()
    #print("text : ",text,end="")

    minertext = extract_text(pdffile)
    #print(minertext)    
    return render_template('view.html',minertext=minertext)
'''
'''
pdffile = open("C:/Users/Choi/Desktop/gugudan/uploads/shibainu.pdf","rb")
fileReader = PyPDF2.PdfFileReader(pdffile)

#fileReader.pageMode()

fileReader.documentInfo
print(fileReader.numPages)
pageObj = fileReader.getPage(0)

text = pageObj.extractText()
print("text : ",text,end=" ")
'''
if __name__ == '__main__':
    app.debug = True
    app.run()