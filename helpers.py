import os
# Simple, stupid (well.. they used to be stupid.. now they're just bad) helper methods that make the script go vroom


# Returns an executable bash command for running a given Ilastik classifier on a given dataset. adds a "*" at the end of the path to indicate all files in the dataset should be used
#   @ ilastik_path: path to the executable ilastik file. Defined in settings.json
#   @ ilastik_classifier_path: path to the pretrained classifier to use
#   @ input_data: a list of files to run through the classifier
#   @ output_path: the directory to place any output in
#   @ params: a dictionary of optional commands
def build_ilastik_command(ilastik_path, ilastik_classifier_path, input_data, output_path, params=None): 
    command = ilastik_path + " --headless --project=" + ilastik_classifier_path + " "

    for param in params:
        if "--" in param:
            if params[param] != None:
                if param == "--output_filename_format":
                    to_add = output_path + "/" + params[param]
                    command += " " + param + "=" + to_add
                else:
                    command += format_flag(param, params[param])
    
    #! this part is tricky, setting here isn't ideal but is still sometimes necessary...
    if " --output_filename_format" not in command:
        command += " --output_filename_format=" + output_path + "/" + "{nickname}_{result_type}.png"
    
    for data in input_data:
        print(data)
        command += " " + data

    return(command)


# Returns an executable bash command for running a given Cell Profiler project on a given dataset.
#   @ cell_profiler_application_path: path to executable cell profiler OR a singulariy command. Defined in settings file at cell_profiler_application_path
#   @ path_to_pipeline: path to the premade pipeline to use
#   @ input_path: the directory or file that will act as the pipeline input data
#   @ output_path: the directory to place any output in
#   @ params: a dictionary of optional commands
def build_cellprofiler_command(cell_profiler_application_path, path_to_pipeline, input_path, output_path, params=None):
    #command = cell_profiler_application_path + " -c -r -p " + path_to_pipeline + " -o " + output_path + " -i " + input_path + "/../*"
    command = cell_profiler_application_path + " -c -r -p " + path_to_pipeline + " -o " + output_path + " -i " + input_path

    return(command)


#! finish this
def build_fiji_command(fiji_path, path_to_macro, input_path, output_path, params=None):
    command = fiji_path + " --headless --console -macro " + path_to_macro
    command += " '"  + "folder=" + input_path + " parameters=a.properties" + " output=" + output_path + "'"
    return(command)


def getProjects(directory, project_list=None):
    whole_directory = os.listdir(directory)
    just_projects = clean_file_list(whole_directory, "._")
    
    if project_list != None:
        sub_list = []
        for project in project_list:
            if project in just_projects:
                sub_list.append(project)
            else: print("WARNING: Can't find specified file:", project, "in directory:", directory)
        just_projects = sub_list
    
    return(just_projects)


# Method to remove given channels from a file name (for accurate names that reflect what channels are present in segmented images)
# TODO: get rid of to_keep and just make sure to not give values you dont want to remove
#   @file_name: the original name of the file to edit
#   @to_remove: a dictionary of values to remove
#   @to_keep: defaults to none, a string value you want to save from the toREmove values
def remove_unusued_channels(file_name, to_remove, to_keep=None):
    expanded_file_name = file_name.split("_")

    for i in expanded_file_name[:]:
        if (i != to_keep) and (i in to_remove.values()):
            expanded_file_name.remove(i)

    new_file_name = '_'.join(expanded_file_name)
    return(new_file_name)


# Method to get rid of junk files that might be in a directory
#   @dirty_list: the original list of files that may or may not contain unwanted files
#   @to_remove: a string present in the files we want to remove
# TODO: make to_remove a list of strings in case there are many things we want to remove
def clean_file_list(dirty_list, to_remove):
    clean_list = []
    for file in dirty_list:
        if to_remove not in file:
            clean_list.append(file)
    return(clean_list)


# Method to format flags to be added to executable commands, particularly good for adding escape sequences to flags that might have spaces in them
#   @param: the name of the flag that will be added to the command
#   @value: the value of the param flag that will be added to the command
def format_flag(param, value):
    toReturn = " " + param
    if " " in value:
        to_add = value.split(' ')
        to_add = to_add[0] + "\ " + to_add[1]
        toReturn += "=" + to_add
    else:
        toReturn += "=" + value
    return toReturn


# A method to print some spacing and basic context around each pipeline step to make output text more understandable
#   @step: the name of the step about to be perfomed
def pretty_print_step_start(step):
    print("\n\n")
    print("#"*80)
    print("Now performing step: " + step + ":")
    print("\n")

def pretty_print_step_end(step):
    print("\n")
    print("Leaving step: " + step)