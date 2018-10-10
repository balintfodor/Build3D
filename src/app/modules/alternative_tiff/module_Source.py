import a3dc_module_interface as a3
from modules.a3dc_modules.a3dc.utils import SEPARATOR, error, print_line_by_line
from modules.a3dc_modules.a3dc.imageclass import VividImage
from modules.a3dc_modules.a3dc.multidimimage import to_multidimimage

import time


def module_main(ctx):

    try:
        filename = a3.inputs['FileName'].path

        #Inizialization
        tstart = time.clock()
        print(SEPARATOR)
        print('Loading the following image: ', filename)
        
        #Load and reshape image
        img=VividImage.load(filename)
        
        #Print important image parameters
        print_line_by_line(str(img))
        
        #Create Output 1
        ch_1=img.get_dimension(a3.inputs['Channel A'], 'C')
        ch_1.metadata['Path']=filename
        a3.outputs['Channel A'] = ch_1

        #Create Output 2
        ch_2=img.get_dimension(a3.inputs['Channel B'], 'C')
        ch_2.metadata['Path']=filename
        a3.outputs['Channel B'] = ch_2
     
        #Finalization
        tstop = time.clock()
        print('Processing finished in ' + str((tstop - tstart)) + ' seconds! ')
        print('Image loaded successfully!')
        print(SEPARATOR)

    except Exception as e:
        raise error("Error occured while executing '"+str(ctx.type())+"' module '"+str(ctx.name())+"' !",exception=e)


    
config = [a3.Input('FileName', a3.types.url),
          a3.Parameter('Channel A', a3.types.int8)
                .setIntHint('default', 0),
                #.setIntHint('max', 8)
                #.setIntHint('min', 0)
                #.setIntHint('unusedValue', 1),  
          a3.Parameter('Channel B', a3.types.int8)
                .setIntHint('default', 1),
                #.setIntHint('max', 8)
                #.setIntHint('min', 0)
                #.setIntHint('unusedValue', 1),
          a3.Output('Channel A', a3.types.GeneralPyType),
          a3.Output('Channel B', a3.types.GeneralPyType)]
    

a3.def_process_module(config, module_main)