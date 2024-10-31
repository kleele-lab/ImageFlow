from tifffile import tifffile
import os
import sys
from helpers import *
import json


def getGlobalMethods():
    allGlobals = globals()
    methods = {}
    for element in allGlobals:
        if hasattr(allGlobals[element], '__call__'):
            methods[element] = allGlobals[element]
    return methods


# Use this to segment out raw (multichannel) data into its respective channels
def separateChannels(input_path, prev_output_path, output_path, params=None): 
    try:
        print("Getting input data...")
        raw_data = os.listdir(input_path)
        print("Attempting to separate channels in: " + input_path)
    except Exception as e:
        print("ERROR while opening input data folder: ", e)

    for file in raw_data:
        try:
            print("Slicing: ", file)

            img = tifffile.imread(input_path + "/" + file)

            if '.h5' in file:
                file = file.replace('.h5', '')

            channel_count = 0
            for channel in settings["input_channels"]:
                file_name = remove_unusued_channels(file, settings["input_channels"], settings["input_channels"][channel])
                img_channel_to_write = img[channel_count]

                if not os.path.exists(output_path + "/" + channel + "_raw"):
                    os.makedirs(output_path + "/" + channel + "_raw")
                    print("Made path: " + output_path + "/" + channel + "_raw")

                tifffile.imwrite((output_path + "/" + channel + "_raw" + "/" + file_name), img_channel_to_write, photometric='minisblack')
                channel_count += 1
            
            print("Sliced: " + file)

        except Exception as e:
            print("ERROR while slicing input data channels: ", e)


# ! subdirectory for each classifier using classifier name to pool output
# Runs ilastik pixel classifier(s)
def runIlastikClassifier(input_path, prev_output_path, output_path, params=None):
    # Establish the list of ilastik classifiers to use
    if ('classifiers' in params.keys() and params['classifiers']): 
        classifier_list = getProjects(settings['ilastik_classifiers_path'], params['classifiers'])
    else: classifier_list = getProjects(settings['ilastik_classifiers_path'])

    # Ilastik classification assumes the previous step will generate the data it takes
    #   Possible bug here if ilastik classification is the first step in the pipeline...
    #allData = os.listdir(prev_output_path)
    #print("All data is: ", allData)

    allData = [os.path.join(root, name)
             for root, dirs, files in os.walk(prev_output_path)
             for name in files
             if name.endswith((".tif"))]
    print("walkData: ", allData)

    for classifier in classifier_list:
        path_to_classifier = settings['ilastik_classifiers_path'] + "/" + classifier
        classifier_name = classifier.split('.')[0]
        new_output_path = output_path + "/" + classifier_name
        
        data_to_classify = []
        classifier_data_group = classifier.split("_")[0]

        for file in allData:
            if settings['input_channels'][classifier_data_group] in file:
                data_to_classify.append(file)
                #data_to_classify.append(prev_output_path + "/" + file)
                
        if data_to_classify != []:
            command = build_ilastik_command(
                settings['ilastik_application_path'],
                path_to_classifier, 
                data_to_classify,
                new_output_path,
                params
            )
            print("Running command: ", command + "\n")
            os.system(command)

        else:
            print("WARNING: No data found for: " + classifier)


# Runs Cell Profiler Pipeline(s)
def runCellProfilerPipeline(input_path, prev_output_path, output_path, params=None): 
    # Establish the list of CP pipelines to use 
    if ('pipelines' in params.keys() and params['pipelines']):
        pipeline_list = getProjects(settings['cell_profiler_pipelines_path'], params['pipelines'])
    else: pipeline_list = getProjects(settings['cell_profiler_pipelines_path'])

    for pipeline in pipeline_list:
        path_to_pipeline = settings['cell_profiler_pipelines_path'] + "/" + pipeline

        command = build_cellprofiler_command(
            settings['cell_profiler_application_path'],
            path_to_pipeline,
            input_path,
            output_path,
            params
        )
        print("Running command: ", command + "\n")
        os.system(command)


# Runs fiji macro(s)
def runFijiMacro(input_path, prev_output_path, output_path, params=None):
    # Establish list of macros to use
    if ('macros' in params.keys() and params['macros']): 
        macro_list = getProjects(settings['fiji_macros_path'], params['macros'])
    else: macro_list = getProjects(settings['fiji_macros_path'])
    print("macro list: ", macro_list)

    for macro in macro_list:
        path_to_macro = settings['fiji_macros_path'] + "/" + macro

        command = build_fiji_command(
            settings['fiji_application_path'],
            path_to_macro,
            input_path,
            output_path,
            params
        )
        print("Running command: ", command + "\n")
        os.system(command)




#####################################################################################################################################
def runPipeline():
    funcs = getGlobalMethods()

    input_path = settings['input_path']
    output_path = settings['output_path']
    prev_output_path = ""
    pipeline = settings['pipeline']


    step_number = 0
    for step in settings['pipeline']:
        pretty_print_step_start(step)

        # output_path = input_path + "/" + step + "_output"
        output_path = settings['output_path'] + "/" + str(step_number) + "_" + step + "_output"

        try:
            if 'skip' in settings['pipeline'][step]['params'].keys():
                if settings['pipeline'][step]['params']['skip']:
                    print("Skipping step: ", step)
                else: globals()[step](input_path, prev_output_path, output_path, settings['pipeline'][step]['params'])
            else: globals()[step](input_path, prev_output_path, output_path, settings['pipeline'][step]['params'])
            
            #input_path += "/" + step + "_output"

        except Exception as e:
            print("Exception: ", e)

        step_number += 1
        prev_output_path = output_path
        pretty_print_step_end(step)


# TODO: make it save the settings file in the root
if __name__ == "__main__":
    settings_file = sys.argv[1]

    try:
        print("Loading settings file...")
        with open(settings_file) as json_file:
            settings = json.load(json_file)
            print("Using settings file: " + settings_file)

            name = os.path.basename(settings_file).split('/')[-1]
            file_path = os.path.join(settings['output_path'], name)

            if not os.path.exists(settings['output_path']):
                os.makedirs(settings['output_path'])

            with open(file_path, 'w') as f:
                print("writing settings file to : " + file_path)
                json.dump(settings, f)

        runPipeline()

    except Exception as e:
        print("ERROR while loading: ", settings_file, e)

    

"""  
 #! tomorrow:
- pres by 4pm
"""