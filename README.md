# ImageFlow: automate your segmentation

## Introduction
The resources of the Kleele lab enable reseachers to develop informationally dense and large scale data sets. While this can be very useful in gaining new insights, it also means that working with this data can present a major hurdle, and optimizing their methods for analyzing these large datasets could serve to benefit the lab's efficiency and reproducability. In this project, we sought to address a small subset of this challenge by developing a custom toolkit that aims to allow members of the lab to combine easily used, well supported, biological image analysis tools into automated analysis pipelines. In this work, we specifically focused on automating quantification of multichannel mitochondrial images, converting images from the microscope into datasets with a push of a button.

This project tries to channel data between pre-existing analysis applications, specifically, Ilastik and Cell Profiler as well as some very experimental Fiji support. While our script does have some simple processing abilities (such as separating TIFF image channels), the vast majority of the lifting is left to tools made within other applications. As an analogy, one could view our code as a conveyer belt connecting machines in a factory, where the output of each step will be fed into the next until we arrive at the final product.

## Index
1. [Installation and setup](#installation)
    1. [Local Setup](#local-installation)
    2. [Euler Setup](#euler-installation)
2. [Configure a Sample Pipeline](#sample-instructions)
    1. [Prerequisites](#instructions-prerequisites)
    2. [Configuring the Settings File](#instructions-settings)
    3. [Configuring the Run Script](#instructions-runscript)
    4. [Run your pipeline!](#instructions-run)
3. [Known Shortcomings](#toimprove)


## <a id="installation"></a> Installation and Setup
Firstly, this project depends on:
- Python 3.9.18
- tifffile 2024.9.20

To begin both the local and Euler setup processes you should first clone this repository to a directory you will be able to easily find it later. 

### <a id="local-installation"></a> Local Setup
When setting up locally you will need to:
- Clone this repository to your local machine
- Install each of the program's dependencies
- Download the applications your pipeline will use (for example, Ilastik and Cell Profiler).
- Ensure you have access to your dataset from whatever directory you will execute your program in

### <a id="euler-installation"></a> Euler Setup
When setting up on Euler you will need to:
- Clone this repository to your Euler login node (see Euler instructions for information on how to get set up)
- Download whatever applications your pipeline will use (for example, Ilastik and Cell Profiler). See *Euler Application Install Guide* for instructions


## <a id="sample-instructions"></a> Configure a Sample Pipeline
This section describes the process of setting up and running a pipeline to segment multi-channel TIFF images using Ilastik and Cell Profiler. More detailed descriptions of some of these steps can be found in the `guides` folder.

1. <a id="instructions-prerequisites"></a>Prerequisites, this guide assumes you:
    - Cloned the project code to your local device or the Euler
    - Downloaded Ilastik and Cell Profiler (see *Euler Application Install Guide* for reference if using Euler)
    - Have a trained Ilastik pixel classifier (see *Ilastik - Building a Pixel Classifier* for reference)
    - Have a Cell Profiler pipeline (see *Building a Cell Profiler Pipeline* for reference)
    - Have at least one multi-channel TIF(F) image to run your pipeline on

2. <a id="instructions-settings"></a>Configuring the Settings File
    1. Duplicate template.json in the settings-files directory.<br>
    Name it whatever you want, we will refer to it as `example.json` from here on. Additional details about the settings file can be found in *The Settings File* in the guides folder.
    2. In `example.json` set input_path and output_path.
        ```json 
        "input_path": "path/to/input/image/folder",
        "output_path": "path/to/input/image/folder/output",
        ```
    3. In `example.json` set ilastik_application_path and ilastik_classifiers_path.
        ```json
        "ilastik_application_path": "path/to/Ilastik/run_ilastik.sh",
        "ilastik_classifiers_path": "path/to/ilastik/classifiers",
        ```
    4. In `example.json` set cell_profiler_application_path and cell_profiler_pipelines_path.
        ```json
        "cell_profiler_application_path": "path/to/Cell_Profiler/cp", (different on Euler)
        "cell_profiler_pipelines_path": "path/to/cell_profiler/pipelines",
        ```
    5. In `example.json` set the input_channels setting to describe your image's channels. This step is a bit confusing, *The Settings File* guide describes this step in detail.
        ```json
        "input_channels": {"mCherry": "561TMRE", "Cy5": "640PKMO"},
        ```
    6. In `example.json` set the pipeline setting to the structure of pipeline you want to run.<br>
    Each pipeline step follows the repeated structure:
        ```json
        "step_name": {
            "params": {
                "skip": true | false (defaults to false)
            }
        }
        ```
        The step_name value is all we need to change for now, although more advanced settings are possible. For our three step pathway we will copy this basic structure three times and run the methods `separateChannels` -> `runIlastikClassifier` -> `runCellProfilerPipeline`, each of which correspond to their method name in the system code. The current structure of the code does not allow a ton of flexibility, so, unfortunately while this structure is likely not the only configuration it is capable of, it is the only one that has been tested much.<br>

        Finally, our pipeline setting should be:
        ```json
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
        Our settings file is now fully configured, and should look something like this:
        ```json 
        {
            "input_path": "path/to/input/image/folder",
            "output_path": "path/to/input/image/folder/output",

            "ilastik_application_path": "path/to/Ilastik/run_ilastik.sh",
            "ilastik_classifiers_path": "path/to/ilastik/classifiers",

            "cell_profiler_application_path": "path/to/Cell_Profiler/cp",
            "cell_profiler_pipelines_path": "path/to/cell_profiler/pipelines",

            "input_channels": {"mCherry": "561TMRE", "Cy5": "640PKMO"},

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
        }
        ```
    7. (Optional) Validate your settings with a JSON validation like [JSON Lint](https://jsonlint.com/).
    These JSON validators will parse through your JSON and make sure everything is formatted correctly, and are very useful when trying to find bugs!

3. <a id="instructions-runscript"></a>Configuring the Run Script<br>
The script(s) are the `.sh` files included in this repository. These are what actually drive our code, and which one you use depends on if you use a local device (your desktop or personal computer) or the Euler (we have provided scripts for both). Regardless of which you use, in each you will see a block near the top that looks like:
    ```bash
    # SET THIS VALUE TO THE PIPELINE YOU WANT TO RUN
    # See settings_files/example.json for a basic pipeline. 
    settings_file=~/code/settings_files/example.json
    ```
    Here, you must set the line beginning with `settings_file` equal to the path to your `example.json` file.

4. <a id="instructions-run"></a>Run your pipeline!<br>
Finally, you are ready to run your pipeline! I recommend starting with a small dataset of one or a few images with your first attempt to ensure things run properly. Once you confirm that everything is coming out how you expected you can point the pipeline at new datasets and start automatically processing your data!<br>
    - To run your program locally go to the directory with your run script and enter the command:
        ```
        ./local-run.sh
        ```
    - To run your program on the Euler go to the directory with your run script and enter the command 
        ```
        sbatch euler-run.sh
        ``` 
        <strong>PLEASE NOTE</strong> if your dataset is in the Kleele 2 server, due to the access rules of the server you should instead go to the directory you defined in the input_path setting and execute the script with:
        ```
        sbatch ABSOLUTE_PATH_TO_RUN_SCRIPT/euler-run.sh
        ```


## <a id="toimprove"></a> Known Shortcomings

While we were able to get a pipeline working to quantify neuronal mitochondria, there is absolutely still more work that needs to be done to make this tool more versatile to be acceptable for everyday use in the lab. This section lists some known shortcomings with the tool in the hope that it may be improved in the future.
- <strong>The output folder needs to be a subfolder of the input folder</strong>. This should be changed so people can put their output wherever they want, however, the system can't handle this yet when steps in a pipeline depend on previous step(s)
The way different pipeline steps handle input folders is hardcoded differently and should be improved. For example, some steps take the output of the previous step as input (runIlastikClassifier), while others take just the root input (runCellProfilerPipeline). If a pipeline were to be Ilastik -> CP with an output folder not a subfolder of the input folder, Cell Profiler would have no access to the Ilastik output.
- <strong>The channel naming scheme in the settings is confusing</strong>. Somehow the user needs to tell the system the channels of their multichannel images so it can use this to identify them uniquely if separated. The current method, while functional, seems confusing and very prone to user error.
- <strong>The flag options for headless running are implemented in Ilastik but not CP or Fiji</strong>. Because we got Ilastik working much sooner, the flag system is much more developed. This could be extended to work with CP/Fiji, however, we didn't have time to test this so it has not been done