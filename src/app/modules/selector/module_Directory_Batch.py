import a3dc_module_interface as a3
from a3dc_module_interface import def_process_module
from glob import glob
import os
from modules.a3dc_modules.a3dc.utils import SEPARATOR

def module_main(ctx):
    
    print(SEPARATOR)
    print('Retrieving file!')
    
    #Absolute path
    path = os.path.abspath(a3.inputs['path'].path)
    
    #Get file extension and directory
    if os.path.isfile(path):
        base_dir = os.path.dirname(path)
    else:
        base_dir = path    
    
    ext = os.path.splitext(a3.inputs['path'].path)[1]

    print('Input directory:', base_dir)


    # Gett all the files with matching extensions
    file_list = [os.path.abspath(x) for x in glob(base_dir + '/*' + ext)]

    if os.path.isfile(path):
        file_list.remove(path)
        file_list.insert(0, path)

    if len(file_list) == 0:
        raise Warning('path {} is empty'.format(base_dir))

    index = ctx.run_id()
    if index < len(file_list) - 1:
        ctx.set_require_next_run(True)
    else:
        ctx.set_require_next_run(False)

    url = a3.Url()
    url.path = file_list[index]
    
    #Print current filename and index
    _, curr_filename = os.path.split(url.path)
    print('Currently processing:', curr_filename)
    #print('Current index:', index)
    
    #Set output
    a3.outputs['file'] = url

    print(SEPARATOR)

config = [
    a3.Parameter('path', a3.types.url),
    a3.Output('file', a3.types.url)]

def_process_module(config, module_main)
