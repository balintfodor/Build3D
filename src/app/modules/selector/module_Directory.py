import a3dc_module_interface as a3
from modules.a3dc_modules.a3dc.utils import error
import os

def module_main(ctx):

    if os.path.isdir(a3.inputs['Directory'].path):
        a3.outputs['Directory']=a3.inputs['Directory']
    else:
        error("Error occured while executing "+str(ctx.name())+" ! Invalid Directory!!")

config = [
    a3.Parameter('Directory', a3.types.url).setBoolHint('folder', True),
    a3.Output('Directory',  a3.types.url)]

a3.def_process_module(config, module_main)
