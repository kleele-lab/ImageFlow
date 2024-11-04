# ImageFlow: automate your segmentation pipeline

## Introduction
The resources of the Kleele lab enable reseachers to develop informationally dense and large scale data sets. While this can be very useful in gaining new insights, it also means that working with this data can present a major hurdle, and optimizing their methods for analyzing these large datasets could serve to benefit the lab's efficiency and reproducability. In this project, we sought to address a small subset of this challenge by developing a custom toolkit that aims to allow members of the lab to combine easily used, well supported, biological image analysis tools into automated analysis pipelines. In this work, we specifically focused on automating quantification of multichannel mitochondrial images, converting images from the microscope into datasets with a push of a button.

## Index
1. [Understanding the basics](#the-basics)
2. [Installation and setup](#installation)
    1. [Local device](#local-installation)
    2. [On Euler](#euler-installation)
3. Building a sample pipeline
    1. Training and including an Ilastik Classifier
    2. Building and integrating a Cell Profiler Pipeline
    3. Setting up your pipeline environment
    4. Configuring the program settings
    5. Executing the pipeline
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

### <a id="local-installation"> Local Setup
When setting up locally you will need to make sure that you install each of the dependencies as you will not have access to Euler's module system. You should also note that, when running the program, you should use the included `local-run.sh` to run things.

#### Setting up Applications
When running locally you can install the applications you will use according to the installation guides for your system. To install [Ilastik](https://www.ilastik.org/) and [Cell Profiler](https://cellprofiler.org/), follow the directions at their respective webpages.

After installing the applications you will use you then must find their executable path, this is the path to the script that actually runs these apps. This value then must be set in the JSON settings file your pipeline will use. Some helpful resources can be found at the pages for [Ilastik headless operation](https://www.ilastik.org/documentation/basics/headless), [Cell Profiler headless operation](https://github.com/CellProfiler/CellProfiler/wiki/Getting-started-using-CellProfiler-from-the-command-line), and [FIJI headless operation](https://imagej.net/learn/headless).


### <a id="euler-installation"> Euler Setup
Setting up on Euler is much more straightforward in terms of dependency management, as all of this is handled in the `euler-run.sh` script included in this repository, which makes use of Euler's module system. However, installing the applications is, unfortunately, still somewhat involved. NOTE: scripts to help with this certainly could and should be made to help reduce confusion.

#### Setting up Applications
The installation and configuration processes for each app we currently support vary, and are described below.

##### Ilastik

##### Cell Profiler

##### FIJI


### <a id="sample-instructions"> Building a sample pipeline
This section will describe the process of setting up a simple Ilastik-Cell Profiler pipeline on multi-channel images. It assumes you already have installed all the project code, downloaded the Ilastik and Cell Profiler apps, and have a trained Ilastik classifier and Cell Profiler pipeline built, and, if you do not, then I suggest following the guides for these present in this project's `guides` folder.

After you have made sure all of the prerequisites above are filled, follow the steps below to get some experience making your own pipeline!

1. Copy the template settings file in the settings-files directory so you have a blank work space to start from. Name it whatever you want, we will refer to it as `example.json` from here on.

2. In `example.json` set the input_path and output_path variables.
Set input_path to the absoute path of the directory holding all of your input data. For now this can only be one folder with images in it, future updates should make this more robust.
Set the output_path to the absolute path of the directory you would like your ouput data to be stored in. This should be a subdirectory of the input folder! For example, if your input directory is `/in`the output directory should be `/in/out`.

3. In `example.json` set the ilastik_application_path and cell_profiler_application_path variables to the path to their respective application executables. The exact specifics of this will vary from person to person depending on how they choose to install these, further details about finding these can be found in the [installation and setup](#installation) section.

4. In `example.json` set the ilastik_classifiers_path and cell_profiler_pipelines_path variables to the paths to the folders that house your project's Ilastik classifier(s) and Cell Profiler pipeline(s). These can be stored anywhere that is accessible to the program, however, as a matter of style and reproducability, you should try to keep track of which project files you are using.

5. In `example.json` set the input_channels variable to describe your input channels. This step is slightly confusing, however, we will try to digest an example to make it easier.<br>
Assume we have a 3 channel image titled: 12345_488SYBR_561-TMRE_640-PKMO.tif. We know from our imaging session metadata that this image photographed GFP with 488SYBR in channel 1, mCherry with 561-TMRE in channel 2, and 640-PKMO Cy5 in channel 3. In this case, we would set the value of input_channels to the dictionary:
```
    {
        "GFP": "488SYBR",
        "mCherry": "561-TMRE",
        "Cy5": "640-PKMO"
    }
```
the key is what we use to identify each channels respective Ilastik classifier.


6. 








