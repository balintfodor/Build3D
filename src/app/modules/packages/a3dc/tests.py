import unittest
import segmentation
import numpy as np
import time
import cProfile
import pstats 
import io
import sys

class SegmentationTest(unittest.TestCase):
        
    def setUp(self):
        self.__start = time.time()
        print('Running: {}'.format(self.id()))
        #print('{} ({}s)'.format(self.id(), round(elapsed, 2))) 
        
    def tearDown(self):
        elapsed = time.time() - self.__start
        print('Finished: {} ({}s)\n'.format(self.id(), round(elapsed, 4)))    
    
    def test_tag_image(self):
        
        input_array = np.array([[0,0,0,0,0,0,0,0,0,0],
                                [0,200,200,200,0,0,0,0,0,0], 
                                [0,200,255,200,0,0,0,0,0,0],
                                [0,200,200,200,0,0,0,0,0,0],
                                [0,0,0,0,0,0,50,50,50,0],
                                [150,150,150,150,150,0,50,100,50,0],
                                [150,50,100,50,150,0,50,50,50,0],
                                [150,100,150,100,150,0,0,0,0,0],
                                [150,50,100,50,150,0,0,255,0,255],
                                [150,150,150,150,150,0,0,0,0,0]],dtype=np.uint16)
    
    
        input_array_2 = np.array([[[0,0,0,0,0,0,0,0,0,0],
                            [0,200,200,200,0,0,0,0,0,0], 
                            [0,200,255,200,0,0,0,0,0,0],
                            [0,200,200,200,0,0,0,0,0,0],
                            [0,0,0,0,0,0,50,50,50,0],
                            [150,150,150,150,150,0,50,100,50,0],
                            [150,50,100,50,150,0,50,50,50,0],
                            [150,100,150,100,150,0,0,0,0,0],
                            [150,50,100,50,150,0,0,255,0,255],
                            [150,150,150,150,150,0,0,0,0,0]],[[0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0], 
                            [0,0,255,0,0,0,0,0,0,0],
                            [0,0,200,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,50,50,50,0],
                            [0,0,0,0,150,0,50,100,50,0],
                            [0,50,100,50,0,0,50,50,50,0],
                            [0,100,150,100,0,0,0,0,0,0],
                            [0,50,100,50,0,0,0,255,0,255],
                            [0,0,0,0,150,0,0,0,0,0]]],dtype=np.uint16)

        
        case_1={'input':input_array, 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                          [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                          [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                          [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                          [0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
                                                          [3, 3, 3, 3, 3, 0, 2, 2, 2, 0],
                                                          [3, 3, 3, 3, 3, 0, 2, 2, 2, 0],
                                                          [3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
                                                          [3, 3, 3, 3, 3, 0, 0, 4, 0, 5],
                                                          [3, 3, 3, 3, 3, 0, 0, 0, 0, 0]],dtype=np.uint32)} 
        
        
        case_2={'input':input_array_2, 'result':np.array([[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                      [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                      [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                      [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                      [0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
                                                                      [3, 3, 3, 3, 3, 0, 2, 2, 2, 0],
                                                                      [3, 3, 3, 3, 3, 0, 2, 2, 2, 0],
                                                                      [3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
                                                                      [3, 3, 3, 3, 3, 0, 0, 4, 0, 5],
                                                                      [3, 3, 3, 3, 3, 0, 0, 0, 0, 0]],

                                                                     [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                      [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                                                                      [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                                                                      [0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
                                                                      [0, 0, 0, 0, 3, 0, 2, 2, 2, 0],
                                                                      [0, 3, 3, 3, 0, 0, 2, 2, 2, 0],
                                                                      [0, 3, 3, 3, 0, 0, 0, 0, 0, 0],
                                                                      [0, 3, 3, 3, 0, 0, 0, 4, 0, 5],
                                                                      [0, 0, 0, 0, 3, 0, 0, 0, 0, 0]]],dtype=np.uint32)} 
        case_list=[case_1,case_2]
        
        
        for idx, cs in enumerate(case_list):
            
            output_array=segmentation.tag_image(cs['input'])
            result_array=cs['result']
            

            case_text="Case "+str(idx)
            
            #Test if data types are equal
            with self.subTest():
                self.assertEqual(output_array.dtype,  result_array.dtype, msg=case_text) 
            
            #Test if array values are equal
            #If data type is float use assert_almost_equal or assert_allclose
            with self.subTest():
                np.testing.assert_array_equal(output_array,result_array, verbose=True,err_msg=case_text)        
        

        
    def test_threshold_manual(self):
        
        input_array = np.array([[0,0,0,0,0,0,0,0,0,0],
                                [0,200,200,200,0,0,0,0,0,0], 
                                [0,200,255,200,0,0,0,0,0,0],
                                [0,200,200,200,0,0,0,0,0,0],
                                [0,0,0,0,0,0,50,50,50,0],
                                [150,150,150,150,150,0,50,100,50,0],
                                [150,50,100,50,150,0,50,50,50,0],
                                [150,100,150,100,150,0,0,0,0,0],
                                [150,50,100,50,150,0,0,255,0,255],
                                [150,150,150,150,150,0,0,0,0,0]],dtype=np.uint16)
    
    
        input_array_2 = np.array([[[0,0,0,0,0,0,0,0,0,0],
                            [0,200,200,200,0,0,0,0,0,0], 
                            [0,200,255,200,0,0,0,0,0,0],
                            [0,200,200,200,0,0,0,0,0,0],
                            [0,0,0,0,0,0,50,50,50,0],
                            [150,150,150,150,150,0,50,100,50,0],
                            [150,50,100,50,150,0,50,50,50,0],
                            [150,100,150,100,150,0,0,0,0,0],
                            [150,50,100,50,150,0,0,255,0,255],
                            [150,150,150,150,150,0,0,0,0,0]],[[0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0], 
                            [0,0,255,0,0,0,0,0,0,0],
                            [0,0,200,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,50,50,50,0],
                            [0,0,0,0,150,0,50,100,50,0],
                            [0,50,100,50,0,0,50,50,50,0],
                            [0,100,150,100,0,0,0,0,0,0],
                            [0,50,100,50,0,0,0,255,0,255],
                            [0,0,0,0,150,0,0,0,0,0]]],dtype=np.uint16)
        
        
        
        case_1={'upper':1, 'lower':0, 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                        [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                        [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                        [1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
                                                        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8)} 
        
        
        case_2={'upper':50, 'lower':0, 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                         [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                         [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                         [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                         [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                                                         [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                         [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                                                         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8)} 
        
        case_3={'upper':150, 'lower':0, 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                         [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                         [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                         [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],dtype=np.uint8)} 
        
        case_4={'upper':150, 'lower':100, 'result':np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                            [0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                                                            [0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
                                                            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                                                            [0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
                                                            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]],dtype=np.uint8)} 

    
    
        
        case_list=[case_1,case_2,case_3,case_4]
        
        
        for idx, cs in enumerate(case_list):
            
            output_array=segmentation.threshold_manual(input_array, upper=cs['upper'], lower=cs['lower'])
            result_array=cs['result']
            

            case_text="Case "+str(idx)+" with upper="+str(cs['upper'])+" lower="+str(cs['lower'])
            
            #Test if data types are equal
            with self.subTest():
                self.assertEqual(output_array.dtype,  result_array.dtype, msg=case_text) 
            
            #Test if array values are equal
            #If data type is float use assert_almost_equal or assert_allclose
            with self.subTest():
                np.testing.assert_array_equal(output_array,result_array, verbose=True,err_msg=case_text)
        

    def test_threshold_auto(self):
        
        input_array = np.array([[0,0,0,0,0,0,0,0,0,0],
                                [0,200,200,200,0,0,0,0,0,0], 
                                [0,200,255,200,0,0,0,0,0,0],
                                [0,200,200,200,0,0,0,0,0,0],
                                [0,0,0,0,0,0,50,50,50,0],
                                [150,150,150,150,150,0,50,100,50,0],
                                [150,50,100,50,150,0,50,50,50,0],
                                [150,100,150,100,150,0,0,0,0,0],
                                [150,50,100,50,150,0,0,255,0,255],
                                [150,150,150,150,150,0,0,0,0,0]],dtype=np.uint16)
            
        input_array_2 = np.array([[[0,0], [5,82]],
                                  [[0,200], [15,45]], 
                                  [[0,200], [45,70]]], dtype=np.uint16)
        
        
        
        case_1={'method':'Otsu', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                          [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                          [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                          [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                          [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                                                                          [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                          [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                          [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                                                                          [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'result_threshold':50, 'input':input_array}
        
        case_2={'method':'MaxEntropy', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                   [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                                                                   [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                   [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                   [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                                                                   [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8),'result_threshold':50, 'input':input_array} 
    
        case_3={'method':'Li', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                   [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                                                                   [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                   [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                   [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                                                                   [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8),'result_threshold':54, 'input':input_array} 
            
    
        case_4={'method':'RenyiEntropy', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                   [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                                                                   [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                   [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                   [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                                                                   [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'result_threshold':65, 'input':input_array}
        
        case_5={'method':'KittlerIllingworth', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                       [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                                                                       [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                       [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                                                                       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'result_threshold':61, 'input':input_array} 
    
        case_6={'method':'Yen', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                       [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                                                                       [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                       [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                                                                       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8),'result_threshold':50, 'input':input_array} 
    
    
    
    
        case_7={'method':'Moments', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                       [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                                                       [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                       [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8),'result_threshold':100.0,'input':input_array}            
        
        case_8={'method':'Shanbhag', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                       [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                                                       [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                       [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'result_threshold':100,'input':input_array} 
        
        case_9={'method':'IsoData', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                              [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                              [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                              [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                              [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                              [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                                                              [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                              [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                              [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'result_threshold':100, 'input':input_array}     
    
        
        case_10={'method':'Huang', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                           [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                           [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                           [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                           [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                           [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                           [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                           [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                           [1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
                                                                           [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'result_threshold':0,'input':input_array} 
        
        case_11={'method':'Triangle', 'mode':'Slice', 'result_array':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                              [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                              [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                              [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                              [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                              [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                              [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                              [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                              [1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
                                                                              [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8),  'result_threshold':2, 'input':input_array} 
    

        case_12={'method':'Otsu', 'mode':'Slice', 'result_array':np.array([[[0, 0],[0, 0]],
                                                                         [[0, 1],[1, 0]],
                                                                         [[0, 1],[1, 0]]],dtype=np.float64),  'result_threshold':[14.0, 82.0], 'input':input_array_2} 

        case_13={'method':'Otsu', 'mode':'Stack', 'result_array':np.array([[[0, 0],[0, 0]],
                                                                         [[0, 1],[0, 0]],
                                                                         [[0, 1],[0, 0]]],dtype=np.uint8),  'result_threshold':82, 'input':input_array_2} 

    

        case_14={'method':'MaxEntropy', 'mode':'Slice', 'result_array':np.array([[[0, 0],[0, 1]],
                                                                                [[0, 1],[1, 0]],
                                                                                [[0, 1],[1, 1]]],dtype=np.float64),  'result_threshold':[5.0, 69.0], 'input':input_array_2} 

        case_15={'method':'MaxEntropy', 'mode':'Stack', 'result_array':np.array([[[0, 0],[0, 1]],
                                                                         [[0, 1],[0, 1]],
                                                                         [[0, 1],[1, 1]]],dtype=np.uint8),  'result_threshold':44, 'input':input_array_2} 

    
        
        case_16={'method':'Li', 'mode':'Slice', 'result_array':np.array([[[0, 0],[0, 0]],
                                                                        [[0, 1],[1, 0]],
                                                                        [[0, 1],[1, 0]]],dtype=np.float64),  'result_threshold':[9.0, 106.0], 'input':input_array_2} 

        case_17={'method':'Li', 'mode':'Stack', 'result_array':np.array([[[0, 0],[0, 1]],
                                                                         [[0, 1],[0, 0]],
                                                                         [[0, 1],[0, 1]]],dtype=np.uint8),  'result_threshold':54, 'input':input_array_2} 
    
    
    
    
        case_18={'method':'RenyiEntropy', 'mode':'Slice', 'result_array':np.array([[[0., 0.],[0., 1.]],
                                                                        [[0., 1.],[1., 0.]],
                                                                        [[0., 1.],[1., 1.]]],dtype=np.float64),  'result_threshold':[5.0, 58.0], 'input':input_array_2} 

        case_19={'method':'RenyiEntropy', 'mode':'Stack', 'result_array':np.array([[[0, 0],[0, 1]],
                                                                         [[0, 1],[0, 1]],
                                                                         [[0, 1],[1, 1]]],dtype=np.uint8),  'result_threshold':44, 'input':input_array_2} 
    
    
    
    
        case_20={'method':'KittlerIllingworth', 'mode':'Slice', 'result_array':np.array([[[False, False],[True, True]],
                                                                        [[False, True],[True, True]],
                                                                        [[False, True],[True, True]]],dtype=np.bool),  'result_threshold':[0, 0], 'input':input_array_2} 

        case_21={'method':'KittlerIllingworth', 'mode':'Stack', 'result_array':np.array([[[0, 0],[0, 1]],
                                                                         [[0, 1],[0, 0]],
                                                                         [[0, 1],[0, 1]]],dtype=np.uint8),  'result_threshold':49, 'input':input_array_2}
    
        
    
        case_22={'method':'Yen', 'mode':'Slice', 'result_array':np.array([[[0., 0.],[0., 1.]],
                                                                        [[0., 1.],[1., 0.]],
                                                                        [[0., 1.],[1., 1.]]],dtype=np.float64),  'result_threshold':[5.0, 69.0], 'input':input_array_2} 

        case_23={'method':'Yen', 'mode':'Stack', 'result_array':np.array([[[0, 0],[0, 1]],
                                                                         [[0, 1],[0, 1]],
                                                                         [[0, 1],[1, 1]]],dtype=np.uint8),  'result_threshold':44, 'input':input_array_2} 


        case_24={'method':'Moments', 'mode':'Slice', 'result_array':np.array([[[0., 0.],[0., 1.]],
                                                                        [[0., 1.],[0., 0.]],
                                                                        [[0., 1.],[1., 0.]]],dtype=np.float64),  'result_threshold':[15.0, 81.0], 'input':input_array_2} 

        case_25={'method':'Moments', 'mode':'Stack', 'result_array':np.array([[[0, 0],[0, 1]],
                                                                         [[0, 1],[0, 0]],
                                                                         [[0, 1],[0, 0]]],dtype=np.uint8),  'result_threshold':81.0, 'input':input_array_2} 

        case_26={'method':'Shanbhag', 'mode':'Slice', 'result_array':np.array([[[0., 0.],[0., 1.]],
                                                                        [[0., 1.],[1., 1.]],
                                                                        [[0., 1.],[1., 1.]]],dtype=np.float64),  'result_threshold':[5.0, 44.0], 'input':input_array_2} 

        case_27={'method':'Shanbhag', 'mode':'Stack', 'result_array':np.array([[[0, 0],[0, 1]],
                                                                         [[0, 1],[0, 1]],
                                                                         [[0, 1],[1, 1]]],dtype=np.uint8),  'result_threshold':44.0, 'input':input_array_2} 

        
        case_28={'method':'IsoData', 'mode':'Slice', 'result_array':np.array([[[0., 0.],[1., 1.]],
                                                                        [[0., 1.],[1., 1.]],
                                                                        [[0., 1.],[1., 1.]]],dtype=np.float64),  'result_threshold':[1.0, 1.0], 'input':input_array_2} 

        case_29={'method':'IsoData', 'mode':'Stack', 'result_array':np.array([[[0, 0],[1, 1]],
                                                                         [[0, 1],[1, 1]],
                                                                         [[0, 1],[1, 1]]],dtype=np.uint8),  'result_threshold':1.0, 'input':input_array_2} 

        
        case_30={'method':'Triangle', 'mode':'Slice', 'result_array':np.array([[[0., 0.],[1., 0.]],
                                                                        [[0., 1.],[1., 0.]],
                                                                        [[0., 1.],[1., 0.]]],dtype=np.float64),  'result_threshold':[0.0, 199.0], 'input':input_array_2} 

        case_31={'method':'Triangle', 'mode':'Stack', 'result_array':np.array([[[0, 0],[1, 1]],
                                                                         [[0, 1],[1, 1]],
                                                                         [[0, 1],[1, 1]]],dtype=np.uint8),  'result_threshold':1.0, 'input':input_array_2} 

        case_32={'method':'Huang', 'mode':'Slice', 'result_array':np.array([[[0., 0.],[0., 0.]],
                                                                        [[0., 1.],[1., 0.]],
                                                                        [[0., 1.],[1., 0.]]],dtype=np.float64),  'result_threshold':[14.0, 82.0], 'input':input_array_2} 

        case_33={'method':'Huang', 'mode':'Stack', 'result_array':np.array([[[0, 0],[0, 0]],
                                                                         [[0, 1],[0, 0]],
                                                                         [[0, 1],[0, 0]]],dtype=np.uint8),  'result_threshold':82.0, 'input':input_array_2} 


        case_list=[case_1,case_2, case_3, case_4, case_5, case_6,case_7,case_8,case_9, case_10, case_11, case_12, case_13,case_14,case_15, case_16, case_17, case_18, case_19,case_20,case_21, case_22, case_23, case_24, case_25,case_26,case_27, case_28, case_29, case_30, case_31, case_32, case_33]#[case_1,case_2, case_3, case_4, case_5, case_7]#]
        
        
        for idx, cs in enumerate(case_list):
            
            case_text="Case "+str(idx+1)+" with method="+str(cs['method'])+" mode="+str(cs['mode'])
            
            output=segmentation.threshold_auto(cs['input'], method=cs['method'], mode=cs['mode'])
            
            #Test if data types are equal
            with self.subTest():
                self.assertEqual(output[0].dtype,  cs['result_array'].dtype, msg=case_text) 
            
            #Test if array values are equal
            #If data type is float use assert_almost_equal or assert_allclose
            

            with self.subTest():
                np.testing.assert_array_equal(output[0], cs['result_array'], verbose=True, err_msg=case_text)
            #Test if thresholds are equal
            with self.subTest():
                self.assertEqual(output[1], cs['result_threshold'], msg='Threshold values do not match '+case_text)                


    def test_threshold_adaptive(self):
        
        input_array = np.array([[0,0,0,0,0,0,0,0,0,0],
                                [0,200,200,200,0,0,0,0,0,0], 
                                [0,200,255,200,0,0,0,0,0,0],
                                [0,200,200,200,0,0,0,0,0,0],
                                [0,0,0,0,0,0,50,50,50,0],
                                [150,150,150,150,150,0,50,100,50,0],
                                [150,50,100,50,150,0,50,50,50,0],
                                [150,100,150,100,150,0,0,0,0,0],
                                [150,50,100,50,150,0,0,255,0,255],
                                [150,150,150,150,150,0,0,0,0,0]],dtype=np.uint16)
        
        
        
        case_1={'blocksize':2, 'offset':0, 'method':'Mean', 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                               [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                               [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                               [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                               [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                               [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                               [1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
                                                                               [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                               [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                               [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'input':input_array} 
        
        case_2={'blocksize':5, 'offset':0, 'method':'Mean', 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                               [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                               [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                               [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                               [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                               [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                               [1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
                                                                               [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                               [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                               [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'input':input_array}        
        


        case_3={'blocksize':10, 'offset':0, 'method':'Mean', 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                                [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                                [1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
                                                                                [1, 0, 1, 0, 1, 0, 0, 1, 1, 0],
                                                                                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                                [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                                                                                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'input':input_array}

        case_4={'blocksize':2, 'offset':0, 'method':'Gaussian', 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                   [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                                   [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                                   [1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
                                                                                   [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                                   [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                                   [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'input':input_array}         
        
        
        case_5={'blocksize':5, 'offset':0, 'method':'Gaussian', 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                                    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                                    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                                    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
                                                                                    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                                    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                                    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'input':input_array}  
        
        case_6={'blocksize':10, 'offset':0, 'method':'Gaussian', 'result':np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                                     [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                     [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                     [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                                     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                                     [1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
                                                                                     [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                                     [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                                     [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'input':input_array}  
    
        case_7={'blocksize':5, 'offset':2, 'method':'Mean', 'result':np.array([[0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                                                                               [0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                                                                               [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                               [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                               [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                               [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                               [1, 0, 1, 0, 1, 0, 0, 1, 1, 0],
                                                                               [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                                                                               [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                               [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'input':input_array} 
    
        case_8={'blocksize':5, 'offset':2, 'method':'Gaussian', 'result':np.array([[0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                                                                                   [0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                                                                                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                                                                   [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                                                                   [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                                                                                   [1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
                                                                                   [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                                                                   [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                                                                                   [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]],dtype=np.uint8), 'input':input_array}  
        
    
    
        case_list=[case_1,case_2, case_3, case_4, case_5, case_6, case_7, case_8]#,,case_3,case_4]
        
  
        for idx, cs in enumerate(case_list):
            
            output_array=segmentation.threshold_adaptive(cs['input'], method=cs['method'], blocksize=cs['blocksize'], offset=cs['offset'])
            result_array=cs['result']
            

            case_text="Case "+str(idx)+" with method="+str(cs['method'])+" blocksize="+str(cs['blocksize'])+" offset="+str(cs['offset'])
            
            #Test if data types are equal
            with self.subTest():
                self.assertEqual(output_array.dtype,  result_array.dtype, msg=case_text) 
            
            #Test if array values are equal
            #If data type is float use assert_almost_equal or assert_allclose
            with self.subTest():
                np.testing.assert_array_equal(output_array,result_array, verbose=True,err_msg=case_text)
        
        
    
    

if __name__ == '__main__':

    input_array = np.array([[[0,0,0,0,0,0,0,0,0,0],
                            [0,200,200,200,0,0,0,0,0,0], 
                            [0,200,255,200,0,0,0,0,0,0],
                            [0,200,200,200,0,0,0,0,0,0],
                            [0,0,0,0,0,0,50,50,50,0],
                            [150,150,150,150,150,0,50,100,50,0],
                            [150,50,100,50,150,0,50,50,50,0],
                            [150,100,150,100,150,0,0,0,0,0],
                            [150,50,100,50,150,0,0,255,0,255],
                            [150,150,150,150,150,0,0,0,0,0]],[[0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0], 
                            [0,0,255,0,0,0,0,0,0,0],
                            [0,0,200,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,50,50,50,0],
                            [0,0,0,0,150,0,50,100,50,0],
                            [0,50,100,50,0,0,50,50,50,0],
                            [0,100,150,100,0,0,0,0,0,0],
                            [0,50,100,50,0,0,0,255,0,255],
                            [0,0,0,0,150,0,0,0,0,0]]],dtype=np.uint16)
    
    
    input_array_2 = np.array([[[0,0], [5,82]],
                                  [[0,200], [15,45]], 
                                  [[0,200], [45,70]]], dtype=np.uint16)
    
    methods=['Mean', 'Gaussian']
    
    print(list([segmentation.tag_image(input_array)]))
    
     
    print('\nRunning Tests:')
    print('-------------\n')
    
    #Redirest stderr to dummy stream
    #Some SimpleITK functions output warnings to stderr
    sys.stderr = io.StringIO()


    #Run cProfiles without saving to files
    #Using cProfile.run('fun()') convention prints full report
    pr=cProfile.Profile()#
    pr.enable()
    
    
    test_suite = unittest.TestLoader().loadTestsFromTestCase(SegmentationTest)


    unittest.TestResult()
    test_stream=io.StringIO()
    test_result=unittest.TextTestRunner(stream=test_stream, verbosity=4).run(test_suite)
    
    pr.disable()

    #Create stream and generate profile stats report form profile
    s=io.StringIO()
    ps = pstats.Stats(pr, stream=s)
    
    #Format and sort stats report
    #Sort by cumulative time and only show results for functions containing 'tests'
    ps.strip_dirs().sort_stats('cumulative').print_stats('test')
    
    #Print results
    print('\nTest Results:')
    print('-------------\n')
    print(test_stream.getvalue())
    #Print formatted stats report
    print('\nProfile Report:')
    print('---------------\n')
    print(s.getvalue())



    
    
    