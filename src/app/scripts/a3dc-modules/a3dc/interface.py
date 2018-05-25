# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 23:17:33 2018

@author: Nerberus
"""

import time
import numpy as np
import collections

from . import segmentation
from . import core
from .error import A3dcError as A3dcError
from .imageclass import Image

####################################################Interface to call from C++####################################################
def tagImage(image):

    '''
    Function that runs ITK connected components on input image
    :param image: nd Array
    :param outputImage: nd Array
    '''

    # Start timing
    tstart = time.clock()

    # Creatre LogText and start logging
    logText = '\nRunning connected components on : ' + str(image.metadata['Name'])

    try:

    
        outputArray=segmentation.tag_image(image.array)
      

    except Exception as e:
        raise A3dcError("Error occured while tagging image!",e)

    # Finish timing and add to logText
    tstop = time.clock()
    logText += '\n\tProcessing finished in ' + str((tstop - tstart)) + ' seconds! '

    return Image(outputArray, image.metadata), logText


def threshold(image, method="Otsu", **kwargs):
    '''

    :param image:
    :param imageDictionary:
    :param method:
    :param kwargs:
        lowerThreshold, upperThreshold, mode,blockSize=5, offSet=0

    :return:
        LogText
    '''

    # Start timing
    tstart = time.clock()

    # Threshold methods
    autothresholdList = ['Otsu', 'Huang', 'IsoData', 'Li', 'MaxEntropy', 'KittlerIllingworth', 'Moments', 'Yen',
                         'RenyiEntropy', 'Shanbhag', 'Triangle']
    adaptiveThresholdList = ['Adaptive Mean', 'Adaptive Gaussian']


    # Creatre LogText and start logging
    logText = '\nThresholding: '+image.metadata['Name']
    logText += '\n\tMethod: ' + method

    # Parse kwargs
    if kwargs != {}:
        if method in autothresholdList:
            keyList=['mode']
        elif method in adaptiveThresholdList:
            keyList = ['blockSize', 'offSet']
        elif method == 'Manual':
            keyList =['lowerThreshold', 'upperThreshold']
        else:
            raise KeyError('Thresholding method '+str(method)+' not available or valid!')


        kwargs = {your_key: kwargs[your_key] for your_key in keyList if your_key in kwargs}

    # Run thresholding functions
    try:
        if method in autothresholdList:
            outputArray, thresholdValue = segmentation.threshold_auto(image.array, method, **kwargs)

            logText += '\n\tThreshold values: ' + str(thresholdValue)

        elif method in adaptiveThresholdList:
            logText += '\n\tSettings: ' + str(kwargs)
            outputArray = segmentation.threshold_adaptive(image.array, method, **kwargs)

        elif method == 'Manual':
            logText += '\n\tSettings: ' + str(kwargs)
            outputArray = segmentation.threshold_manual(image.array, **kwargs)

        else:
            raise LookupError("'" + str(method) + "' is Not a valid mode!")

    except Exception as e:
        raise A3dcError("Error occured while thresholding image!",e)

    # Finish timing and add to logText
    tstop = time.clock()
    logText += '\n\tProcessing finished in ' + str((tstop - tstart)) + ' seconds! '

    return Image(outputArray, image.metadata), logText


def analyze(taggedImage, imageList=None, measurementInput=['voxelCount', 'meanIntensity']):
    '''
    Analyzes tagedImage and appends 'dataBase' to its dictionary that contain measured values.
    :param taggedImage: tagged image
    :param taggedDictionary: dictionary with descriptors of tagged image
    :param imageList: image list where intensity is measured within objects of taggedImage
    :param dictionaryList: list of dictionaries that apartain to each element in imageList
    :param outputImage: output image
    :param outputDictionary: dictionary with descriptors of outputImage
    :return:
    '''

    # Start timing
    tstart = time.clock()

    # Creatre LogText and start logging
    logText = '\nAnalyzing: ' + str(taggedImage.metadata['Name'])

    try:
        #Print list of images in Imagelist to log text
        if imageList != None:
            logText += '\n\tMeasuring intensity in: '
            for img in imageList:
                logText += img.metadata['Name']

        #Analyze image
        taggedImage=core.analyze(taggedImage, imageList, measurementInput)

        #Add number of objects to logText
        logText += '\n\tNumber of objects: '+str(len(taggedImage.database['tag']))
        
        

    except Exception as e:
        raise A3dcError("Error occured while analyzing image!",e)

    # Finish timing and add to logText
    tstop = time.clock()
    logText += '\n\tProcessing finished in ' + str((tstop - tstart)) + ' seconds! '
    
    return taggedImage, logText


def apply_filter(image, filterDict=None, removeFiltered=True, overWrite=True):
    '''
    Filters dictionary stored in the 'dataBase' key of the inputDisctionary to be filtered and removes filtered taggs if filterImage=True. Boolean mask is appended to inputDictionary['Database']
    and returned through the output dictionary. If removeFiltered=True tags are removed from the output. If overWrite=True a new Boolean mask is created.

    :param inputDictionary: Dictionary containing informason related to inputImage
    :param inputImage: Tagged image
    :param filterDict: Dictionary contains the keywords to be filtered and the min/maximum value as the following example:

            dictFilter={'volume':{'min':2, 'max':11}}#, 'mean in '+taggedDictList[0]['name']: {'min':2, 'max':3}}

    :param outputDictionary
    :param inputImage
    :param removeFiltered: If True objects that are filtered out are removed
    :return:
    '''
    # Start timing
    tstart = time.clock()

    # Creatre LogText and start logging
    logText = '\nFiltering: ' + str(image.metadata['Name'])
    logText += '\n\tFilter settings: '+str(filterDict).replace('{', ' ').replace('}', ' ')
    logText += '\n\t\tremoveFiltered=' + str(removeFiltered)
    logText += '\n\t\toverwrite=' + str(overWrite)

    try:
        if filterDict==None:
            filterDict={}

        # Filter dictionary
        output_database=core.filter_dataBase(image.database, filterDict, overWrite)

        # Filter image
        if removeFiltered == True:
            output_image = core.filter_image(image.array)
        else:
            output_image=image.array



    except Exception as e:
        raise A3dcError("Error occured while filtering database!",  e)

    # Finish timing and add to logText
    tstop = time.clock()
    logText += '\n\tProcessing finished in ' + str((tstop - tstart)) + ' seconds! '


    return Image(output_image, image.metadata, database=output_database), logText


def colocalization(taggedImageList, sourceImageList=None, overlappingFilter=None,
                   removeFiltered=False, overWrite=True):
    '''

    :param taggedImageList:
    :param taggedDictList:
    :param sourceImageList:
    :param overlappingFilterList:
    :param filterImage:
    :return:
    '''
    # Start timingsourceDictionayList
    tstart = time.clock()

    try:

        # Creatre LogText
        logText = '\nColocalization analysis started using: '
        for img in taggedImageList:
            logText += '\t ' + str(img.metadata['Name'])

        # Add Filter settings
        logText += '\n\tFilter settings: ' + str(overlappingFilter).replace('{', ' ').replace('}', ' ')
        logText += '\n\t\tremoveFiltered=' + str(removeFiltered)
        logText += '\n\t\toverwrite=' + str(overWrite)


        # Determine connectivity data
        overlappingImage = core.colocalization_connectivity(taggedImageList, sourceImageList)
     
        # Filter dataBase and image
        overlappingImage, _ = apply_filter(overlappingImage, overlappingFilter, removeFiltered)
        

        # Analyze colocalization
        overlappingImage, _ = core.colocalization_analysis(taggedImageList, overlappingImage)


        #Print number of objects to logText
        logText += '\n\tNumber of Overlapping Objects: '+str(len(overlappingImage.database['tag']))

    except Exception as e:
        raise A3dcError("Error occured while filtering database!",e)

        # Finish timing and add to logText
    tstop = time.clock()
    logText += '\n\tProcessing finished in ' + str((tstop - tstart)) + ' seconds! '

    return overlappingImage, taggedImageList, logText


def save_data(inputImageList, path, fileName='output', toText=True):
    '''
    :param dictionaryList: Save dictionaries in inputDictionaryList
    :param path: path where file is saved
    :param toText: if True data are saved to text
    :param fileName: fileneme WITHOUT extension
    :return:
    '''
    
    if not isinstance(inputImageList, collections.Iterable):
            inputImageList=[inputImageList]
    
    # Start timing
    tstart = time.clock()
    
    # Creatre LogText and start logging
    logText = '\nSaving database: '
    # Add names of dictionary sources to logText
    for img in inputImageList:
        logText += '\t' + str(img.metadata['Name'])
    #Add settings to logText
    # Add filter settings to logText
    logText += '\n\tPath: '+str(path)
    logText += '\n\tFilename: '+str(fileName)
    if toText==True: logText += '.txt'
    elif toText==False:logText += '.xlsx'
    

    try:

        Image.save_data(inputImageList, path, fileName, toText)

    except Exception as e:
        raise A3dcError("Error occured while filtering database!",e)



    # Finish timing and add to logText
    tstop = time.clock()
    logText += '\n\tProcessing finished in ' + str((tstop - tstart)) + ' seconds! '

    return logText


def save_image(inputImageList, dir_path, suffix):
    
    if not isinstance(inputImageList, collections.Iterable) or isinstance(inputImageList, np.ndarray):
        inputImageList=[inputImageList]
    
    # Start timing
    tstart = time.clock()
    
    # Creatre LogText and start logging
    logText = '\nSaving image: '
    # Add names of dictionary sources to logText
    for img in inputImageList:
        logText += '\t' + str(img.metadata['Name'])
    #Add settings to logText
    # Add filter settings to logText
    logText += '\n\tPath: '+str(dir_path)

    try:
        #Save image using tifffile save
        Image.save_image(inputImageList, dir_path, suffix ) 
        
    except Exception as e:
        raise A3dcError("Error occured while filtering database!",e)



    # Finish timing and add to logText
    tstop = time.clock()
    logText += '\n\tProcessing finished in ' + str((tstop - tstart)) + ' seconds! '

    return logText