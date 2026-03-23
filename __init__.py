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
import os
import sys

base_path = tmp_global_obj["basepath"]
cur_path = os.path.join(base_path, 'modules', 'Pdf2Img', 'libs')
if cur_path not in sys.path:
    sys.path.append(cur_path)

from PIL import Image
from PyPDF2 import PdfReader, PdfWriter


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
    except Exception as e:
        PrintException()
        raise Exception(e)

    try:
        tmp_path = makeTmpDir("pdf2img") + os.sep + "tmp_pdf.pdf"

        with open(pdf_path, "rb") as f:
            pdf = PdfReader(f)
            first_page = pdf.pages[0]
            dim = (
                float(first_page.mediabox.width),
                float(first_page.mediabox.height)
            )

            tmp = pdf.pages[page]
            pdf_writer = PdfWriter()
            pdf_writer.add_page(tmp)

            with open(tmp_path, 'wb') as out:
                pdf_writer.write(out)

        sleep(2)
        pdf2Img(tmp_path, conf="", dim=dim)

        pdf_im = Image.open(tmp_path.split(".pdf")[0] + "-1.jpg")
        im = Image.open(jpg)
        # pdf_im = pdf_im.resize(dim, resample=Image.ANTIALIAS)

        if isinstance(coord, list):
            for c in coord:
                pdf_im.paste(im, c)
        else:
            pdf_im.paste(im, coord)

        pdf_im.save(tmp_path)
        pdf_im.save(tmp_path.split(".pdf")[0] + ".jpg", 'JPEG', quality=100)

        pdf_writer = PdfWriter()

        with open(pdf_path, "rb") as f_original:
            pdf_original = PdfReader(f_original)
            number_page = len(pdf_original.pages)

            with open(tmp_path, "rb") as f_img:
                pdf_img_reader = PdfReader(f_img)
                pdf_img = pdf_img_reader.pages[0]

                for i in range(number_page):
                    if i == page:
                        pdf_writer.add_page(pdf_img)
                    else:
                        pdf_writer.add_page(pdf_original.pages[i])

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

        with open(pdf_path, "rb") as f:
            pdf = PdfReader(f)

            if pdf.is_encrypted:
                try:
                    pdf.decrypt('')
                except:
                    pass

            tmp = pdf.pages[int(page) - 1]
            pdf_writer = PdfWriter()
            pdf_writer.add_page(tmp)

            with open(tmp_path, 'wb') as out:
                pdf_writer.write(out)

        if dpi:
            conf = ["-r", dpi]
        else:
            conf = ["-r", "150"]

        ext = os.path.splitext(image_path)[1].lower()

        if ext == ".png":
            pdf2Img(tmp_path, conf, dim="", format_="-png")
            img = tmp_path.replace(".pdf", "-1.png")

        elif ext in [".jpg", ".jpeg"]:
            pdf2Img(tmp_path, conf, dim="", format_="-jpeg")
            img = tmp_path.replace(".pdf", "-1.jpg")

        else:
            raise Exception("Formato de salida no soportado. Usa .png, .jpg o .jpeg")

        pdf_im = Image.open(img)
        cropped = pdf_im.crop(coord + size)

        if ext == ".png":
            cropped.save(image_path, format="PNG")
        else:
            cropped = cropped.convert("RGB")
            cropped.save(image_path, format="JPEG", quality=100)

    except Exception as e:
        PrintException()
        raise e

