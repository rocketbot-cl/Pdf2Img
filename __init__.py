# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"

    pip install <package> -t .

"""

from time import sleep
from subprocess import Popen, PIPE
import os, sys

base_path = tmp_global_obj["basepath"]
cur_path = os.path.join(base_path, 'modules', 'Pdf2Img', 'libs')
if cur_path not in sys.path:
    sys.path.append(cur_path)
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter


# Functions
def pdf2Img(pdf, conf, img=None, dim=None, format_="-jpeg"):
    global Popen, PIPE

    print("**", pdf)
    env = os.environ.copy()
    base_path = tmp_global_obj["basepath"]

    if img:
        img = img.split(".jpg")[0]
    else:
        img = pdf.split(".pdf")[0]

    print(img)

    scale = ""

    executable = base_path + "modules" + os.sep + "Pdf2Img" + os.sep + "bin" + os.sep + "pdftoppm.exe"
    popper = [executable, format_, pdf, img]
    
    if conf:
        for i in conf:
            popper.append(i)


    if dim:
        scale += "-sz -W {x} -H {y}".format(x=dim[0], y=dim[1])
        #popper = popper + scale.split(" ")
    
    # popper = [executable, conf + " " + format_ + " " + '"' + pdf + '"' + " " + '"' + str(img) + '.jpg"'

    con = Popen(popper, env=env, shell=True, stdout=PIPE, stderr=PIPE)
    print(popper)
    
    a = con.communicate()
    return a


def makeTmpDir(name):
    try:
        os.mkdir("tmp")
        os.mkdir("tmp" + os.sep + name)
    except:
        try:
            os.mkdir("tmp" + os.sep + name)
        except:
            pass

    return os.sep.join(["tmp", name])


"""
    Obtengo el modulo que fueron invocados
"""

module = GetParams("module")

if module == "toJpg":
    pdf = GetParams("pdf").replace("/", os.sep)
    jpg = GetParams("jpg").replace("/", os.sep)
    width = GetParams("width")
    ppx = GetParams("dpi")
    var_ = GetParams("result")

    r = True
    try:
        # conf = ""
        conf = []
        if ppx:
            # conf = conf + " -r " + ppx
            conf.append("-r")
            conf.append(ppx)
        if width:
            # conf = conf + " -scale-to " + width
            conf.append("-scale-to")
            conf.append(width)
        
        # conf = "-scale-to-x"

        a = pdf2Img(pdf, conf, img=jpg)
        a = a[1].decode()
        response = False
        if a != "No display font for 'ArialUnicode'":
            response = True
        SetVar(var_, response)
    except Exception as e:
        raise Exception(e)

if module == "addImage":
    pdf_path = GetParams("pdf").replace("/", os.sep)
    jpg = GetParams("jpg").replace("/", os.sep)
    page = GetParams("page")
    coord = GetParams("coordinates")
    pdf_new = GetParams("pdf_new")
    result = GetParams("result")

    try:
        page = int(page) - 1
        if ";" in coord:
            coord = coord.split(";")
            for i in range(len(coord)):
                coord[i] = eval(coord[i])
        else:
            coord = eval(coord)

        print("coord", coord)
    except NameError:
        PrintException()
        raise e
    try:
        tmp_path = makeTmpDir("pdf2img") + os.sep + "tmp_pdf.pdf"
        pdf = PdfFileReader(pdf_path)
        dim = (pdf.getPage(0).mediaBox.getWidth(), pdf.getPage(0).mediaBox.getHeight())
        tmp = pdf.getPage(page)
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(tmp)
        with open(tmp_path, 'wb') as out:
            pdf_writer.write(out)
        sleep(2)
        a = pdf2Img(tmp_path, conf="", dim=dim)

        pdf_im = Image.open(tmp_path.split(".pdf")[0] + "-1.jpg")
        im = Image.open(jpg)
        # pdf_im = pdf_im.resize(dim, resample=Image.ANTIALIAS)

        if type(coord) is list:
            for c in coord:
                pdf_im.paste(im, c)
        else:
            pdf_im.paste(im, coord)
        pdf_im.save(tmp_path)
        pdf_im.save(tmp_path.split(".pdf")[0] + ".jpg", 'JPEG', quality=100)

        pdf_writer = PdfFileWriter()
        number_page = pdf.getNumPages()
        pdf_img = PdfFileReader(tmp_path).getPage(0)

        for i in range(number_page):

            if i == page:
                pdf_writer.addPage(pdf_img)
                scale = float(dim[0] / pdf_writer.getPage(i).mediaBox.getWidth())
                pdf_writer.getPage(i).scale(scale, scale)
            else:
                pdf_writer.addPage(pdf.getPage(i))

            print((pdf_writer.getPage(i).mediaBox.getWidth(), pdf_writer.getPage(i).mediaBox.getHeight()))

        with open(pdf_new, 'wb') as fh:
            pdf_writer.write(fh)

        SetVar(result, True)

    except Exception as e:
        PrintException()
        raise Exception(e)

if module == "cropImage":
    pdf_path = GetParams("pdf")
    image_path = GetParams("jpg")
    coord = GetParams("coordinates")
    size = GetParams("size")
    page = GetParams("page")
    dpi = GetParams("dpi")

    tmp_path = makeTmpDir("pdf2img") + os.sep + "tmp.pdf"

    try:
        coord = eval(coord)
        size = eval(size)

        pdf = PdfFileReader(pdf_path)
        if pdf.isEncrypted:
            pdf.decrypt('')
        tmp = pdf.getPage(int(page) - 1)
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(tmp)
        with open(tmp_path, 'wb') as out:
            pdf_writer.write(out)
            
        
            
        if dpi:
            conf = ["-r", dpi]
        else:
            conf = ["-r", "150"]
        
        
        a = pdf2Img(tmp_path, conf, dim="", format_="-png")

        img = tmp_path.replace(".pdf", "-1.png")
        pdf_im = Image.open(img)
        pdf_im.crop(coord + size).save(image_path)

    except Exception as e:
        PrintException()
        raise e
