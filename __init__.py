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
"""
    Obtengo el modulo que fueron invocados
"""
module = GetParams("module")

if module == "toJpg":
    print("Entro")
    pdf = GetParams("pdf").replace("/",os.sep)
    jpg = GetParams("jpg").replace("/",os.sep)
    width = GetParams("width")
    ppx = GetParams("dpi")
    var_ = GetParams("result")
    pdf = '"' + pdf + '"'

    print('PATH',pdf)
    r = True
    try:
        env = os.environ.copy()
        base_path  = tmp_global_obj["basepath"]
        conf = ""
        if ppx:
            conf = conf + " -r " + ppx
        if width:
            conf = conf + " -scale-to " + width
        
        popper = base_path + "modules" + os.sep + "Pdf2Img" + os.sep + "bin" + os.sep + "pdftoppm.exe" + conf+" -jpeg " + pdf + " " + str(jpg).split(".jpg")[0]        
        print(popper)
        con = Popen(popper, env=env, shell=True, stdout=PIPE, stderr=PIPE)
        a = con.communicate()
        SetVar( var_,  str(a))
    except Exception as e:
        raise Exception(e)
