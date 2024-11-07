# ImageFlow: automate your segmentation

## Introduction
The resources of the Kleele lab enable reseachers to develop informationally dense and large scale data sets. While this can be very useful in gaining new insights, it also means that working with this data can present a major hurdle, and optimizing their methods for analyzing these large datasets could serve to benefit the lab's efficiency and reproducability. In this project, we sought to address a small subset of this challenge by developing a custom toolkit that aims to allow members of the lab to combine easily used, well supported, biological image analysis tools into automated analysis pipelines. In this work, we specifically focused on automating quantification of multichannel mitochondrial images, converting images from the microscope into datasets with a push of a button.

## Index
1. [Understanding the basics](#the-basics)
2. [Installation and setup](#installation)
    1. [Local device](#local-installation)
    2. [On Euler](#euler-installation)
3. [Building a sample pipeline](#sample-instructions)
    0. [Prerequisites](#instructions-prerequisites)
    1. [Configuring the Settings File](#instructions-settings)
    2. [Configuring the Run Script](#instructions-runscript)
    3. [Run your pipeline!](#instructions-run)
4. Troubleshooting


## <a id="the-basics"></a> Understanding the basics
This project simply seeks to connect data flows between pre-existing analysis applications, specifically, Ilastik and Cell Profiler as well as some very experimental Fiji macro support. While our script does have some simple processing abilities (such as separating TIFF image channels), the vast majority of the lifting is left to tools made within these applications, whose inputs and outputs may be threaded together with what we have built. As an analogy, one could view our code as a conveyer belt connecting machines in a factory, where the output of each step will be fed into the next until we arrive at the final product.

## <a id="installation"></a> Installation and Setup
Firstly, this project depends on:
- Python 3.9.18
- tifffile 2024.9.20
- JSON python pkg
- Numpy
- os
- sys

To begin both the local and Euler setup processes you should first clone this repository to a directory you will be able to easily find it later. 

### <a id="local-installation"></a> Local Setup
When setting up locally you will need to:
- Clone this repository to your local machine
- Install each of the program's dependencies (you will not have access to Euler's module system)
- Download whatever applications your pipeline will use (for example, Ilastik and Cell Profiler). See the "Local Machine" section of `guides/Application Installation Guide` for instructions
- Ensure you have access to your dataset from whatever directory you execute your program in

### <a id="euler-installation"></a> Euler Setup
When setting up on Euler you will need to:
- Clone this repository to your Euler login node (see Euler instructions for information on how to get set up)
- Download whatever applications your pipeline will use (for example, Ilastik and Cell Profiler). See the "Euler" section of the `guides/Application Installation Guide` for instructions


## <a id="sample-instructions"></a> Building and Running a Sample Pipeline
This section will describe the high-level process of setting up and running a pipeline that segments multi-channel TIF images using Ilastik and Cell Profiler. More detailed descriptions of some of these steps can be found in the `guides` folder.

0. <a id="instructions-prerequisites"></a>Prerequisites, this guide assumes you:
    - Cloned the project code to your local device or the Euler
    - Downloaded Ilastik and Cell Profiler (see guides/Application Installation Guide)
    - Have a trained Ilastik pixel classifier relevant to your dataset (see guides/Training an Ilastik Pixel Classifier)
    - Have a Cell Profiler Pipeline relevant to your dataset (see guides/Building a Cell Profiler Pipeline)
    - Have at least one multi-channel TIF(F) image to run your pipeline on

1. <a id="instructions-settings"></a>Configuring the Settings File
    1. Duplicate template.json in the settings-files directory.<br>
    Name it whatever you want, we will refer to it as `example.json` from here on. Additional details about the settings file can be found at `guides/The Settings File`

    2. In `example.json` set input_path and output_path.<br>
        - Set input_path to the path of the directory holding your input data.
        - Set output_path to the path of the directory you would like your ouput data to be stored in. This should be a subdirectory of the input folder! For example, if your input directory is `/in`the output directory should be `/in/out`.

    3. In `example.json` set ilastik_application_path and cell_profiler_application_path.<br>
    Each should be set to the path of their respective executable, reference each application's respective configuration section in `guides/Application Installation Guide` for furter details.

    4. In `example.json` set ilastik_classifiers_path and cell_profiler_pipelines_path.<br>
    Each should be set to the path of the folders containing your project's Ilastik classifier(s) and Cell Profiler pipeline(s). See the guides `Training an Ilastik Pixel Classifier` and `Building a Cell Profiler Pipeline`, respectively, for more details.

    5. In `example.json` set the input_channels setting to describe your input channels.<br>
    This step is slightly confusing, however, we will digest an example to make it easier.
    Assume we have a 3 channel image titled: 12345_488-SYBR_561-TMRE_640-PKMO.tif. We know from our imaging session that this image photographed GFP using 488-SYBR in channel 1, mCherry using 561-TMRE in channel 2, and Cy5 using 640-PKMO in channel 3. The purpose of the input_channels setting is to tell the program what each channel in the image is, so it can keep track after we slice the image into its distinct channels and progress with the pipeline. The general format this setting expects for each channel is: `"channel_name": "name_in_file_name"`. One important thing to note is that the program will try to use the channel_name piece of this to identify valid Ilastik classifiers and structure your Cell Profiler input, so make sure you keep the channel_name consistent, however, name_in_file_name can change between sessions, just make sure to update your settings.<br>
    In this case, following the structure described above, we would set the value of input_channels to the dictionary:
        ```
            "input_channels": {
                "GFP": "488-SYBR",
                "mCherry": "561-TMRE",
                "Cy5": "640-PKMO"
            }
        ```

    6. In `example.json` set the pipeline setting to the structure of pipeline you want to run.<br>
    In this example, our pipeline will be separating image channels -> Ilastik classification -> Cell Profiler quantification. The current structure of the code does not allow a ton of flexibility, so, unfortunately while this structure is likely not the only configuration it is capable of, it is the only one that has been tested much.<br>
    Each pipeline step follows the repeated structure:
        ```
        "step_name": {
            "params": {
                "skip": true | false (defaults to false)
            }
        }
        ```
        The step_name value is all we need to change for now, although more advanced settings are possible (see the advanced/experimental section of `guides/The Settings File`). For our three step pathway we will copy this structure three times and run the methods `separateChannels` -> `runIlastikClassifier` -> `runCellProfilerPipeline`, each of which correspond to their method name in the system code. If more methods are later added then these too can be called this way.<br>
        Finally, our pipeline setting should be:
        ```
        "pipeline": {
            "separateChannels": {
                "params": {
                    "skip": false
                }
            },
            "runIlastikClassifier": {
                "params": {
                    "skip": false
                }
            },
            "runCellProfilerPipeline": {
                "params": {
                    "skip": false
                }
            }
        }
        ```
    Our settings file is now fully configured!

2. <a id="instructions-runscript"></a>Configuring the Run Script<br>
The script(s) are the`.sh` files included in this repository. These are what actually drive the running of our code, and which one you use will depend on if you use a local device (your desktop or personal computer) or the Euler (we have provided scripts for both). Regardless of which you use, in each you will see a block near the top that looks like:
    ```
    # SET THIS VALUE TO THE PIPELINE YOU WANT TO RUN
    # See settings_files/example.json for a basic pipeline. 
    settings_file=~/code/settings_files/example.json
    ```
    Here, you must set the line beginning with `settings_file` equal to the path to your `example.json` file.

3. <a id="instructions-run"></a>Run your pipeline!<br>
Finally, you are ready to run your pipeline! I highly recommend starting with a small dataset of one or a few images with your first attempt, in case anything is misconfigured. Once you confirm that everything is coming out how you expected you can modify any of these settings to point the pipeline at new datasets and/or tools and start automatically processing your data!<br>
    - To run your program locally go to the directory with your run script and enter the command `./local-run.sh`
    - To run your program on the Euler go to the directory with your run script and enter the command `sbatch euler-run.sh`. PLEASE NOTE if your dataset is in the Kleele 2 server, due to the access rules of the server you should instead go to the directory you defined in the input_path setting and execute the script with `sbatch ABSOLUTE_PATH_TO_RUN_SCRIPT/euler-run.sh`





