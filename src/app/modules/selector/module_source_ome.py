import a3dc_module_interface as a3
from modules.a3dc_modules.external.PythImage import Image
from modules.a3dc_modules.a3dc.utils import SEPARATOR
import time

def module_main(_):

    filename = a3.inputs['FileName'].path
    
    #Inizialization
    tstart = time.clock()
    print(SEPARATOR)
    print('Loading the following image: ', filename)
    
    #Load and reshape image
    img = Image.load(filename, file_type='ome')
    img.reorder('XYZCT')

    #Create Output
    a3.outputs['Array'] = img.image
    a3.outputs['MetaData']=img.metadata
    
    #Finalization
    tstop = time.clock()
    print('Processing finished in ' + str((tstop - tstart)) + ' seconds! ')
    print('Image loaded successfully!')
    print(SEPARATOR)


config = [a3.Input('FileName', a3.types.url),
    a3.Output('Array', a3.types.GeneralPyType),
    a3.Output('MetaData', a3.types.GeneralPyType)]
    

a3.def_process_module(config, module_main)
