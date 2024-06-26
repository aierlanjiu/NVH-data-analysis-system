<picture>
  <img alt="a" src="https://github.com/aierlanjiu/NVH-data-analysis-system/blob/main/NVH%20Data%20Analysis%20Tool.png">
</picture>
<p align="center">
    <br> English | <a href="README-CN.md">中文</a>
</p>


<p align="center">
  <a href="LICENSE" target="_blank">
    <img alt="MIT License" src="LICENSE" />
  </a>

  <!-- TypeScript Badge -->
  <img alt="TypeScript" src="https://img.shields.io/badge/-TypeScript-blue?style=flat-square&logo=typescript&logoColor=white" />

  <!-- Python Badge -->
  <img alt="Python" src="https://img.shields.io/badge/-Python-blue?style=flat-square&logo=python&logoColor=white" />

  <!-- Tkinter Badge -->
  <img alt="Tkinter" src="https://img.shields.io/badge/-Tkinter-blue?style=flat-square&logo=python&logoColor=white" />

  <!-- Qt Badge -->
  <img alt="Qt" src="https://img.shields.io/badge/-Qt-blue?style=flat-square&logo=qt&logoColor=white" />

  <!-- Windows Badge -->
  <a href="https://github.com/yetone/openai-translator/releases" target="_blank">
    <img alt="Windows" src="https://img.shields.io/badge/-Windows-blue?style=flat-square&logo=windows&logoColor=white" />
  </a>
</p>


[![Conventional Installation Method](https://img.shields.io/static/v1?label=&message=Conventional%20Installation%20Method&color=gray)]

<a href="root/aniconda3.md">Install</a>


## Project Introduction
This project aims to develop an interactive software for the Windows operating system, specifically designed for the automotive industry to handle efficiency data, NVH semi-anechoic chamber data, EOL production line data, and whole vehicle noise data analysis. The software is written in Python and utilizes the Tkinter or Qt framework to build an intuitive and feature-rich graphical user interface (GUI). Moreover, the software integrates a database system to support data import, storage, and retrieval.
<picture>
  <img alt="b" src="Graphical User Interface.png">
</picture>

<picture>
  <img alt="e" src="Python-based Development.png">
</picture>

## Functional Modules

### 1. Efficiency Data Processing Module
- Data Import: Provides interfaces for importing data files in various formats.
- Data Analysis: Includes data cleaning, organization, statistical calculations, and visualization features.
- Result Output: Supports exporting to formats such as Excel, PDF, and displays key metrics in real-time.
<picture>
  <img alt="c" src="Efficiency Data Handling.png">
</picture>

### 2. NVH Semi-Anechoic Chamber Data Processing Module
- Data/Condition/Measurement Point/Prototype/Analysis Order/Target Import: Fully supports the input of various parameters.
- Advanced Data Analysis: Conducts frequency domain, time domain analysis, and in-depth study of NVH characteristics.
- Report Compilation and Output: Features an embedded report editor, generates professional reports automatically, and supports preview, printing, and export.

### 3. EOL Production Line Data Processing Module
- Data and Parameters Import: Compatible with specific data structures of the EOL production line and has flexible configuration capabilities.
- Fitting and Data Analysis: Extends model fitting functions to conduct in-depth analysis of data collected on the production line.
- Report Generation and Output: Also equipped with a report preparation tool and customizes report content according to EOL characteristics.

### 4. Whole Vehicle Noise Data Analysis Module
- Data Import: Supports the import of audio files and other noise-related data.
- Audio Playback: Integrates an audio player for convenient playback of original audio data.
- Audio Colormap Output: Converts audio signals into visual images, such as sound pressure level spectrums.
<picture>
  <img alt="d" src="Rotating Parts NVH Analysis.png">
</picture>

```plaintext

 ├── main.py  # Main program entry, responsible for overall process control and GUI initialization
 ├── config.py  # Configuration program
 ├── __init__.py # Initialization
 ├── gui/
 │   ├── __init__.py
 ├── data_management/
 │   ├── __init__.py
 │   ├── data_init.py  # Create data copies
 │   ├── data_loader.py  # Data loading module, reads and parses various data files
 ├── data_processing/
 │   ├── __init__.py
 │   ├── efficiency_data.py  # Efficiency data analysis module
 │   ├── semiacoustic.py  # NVH semi-anechoic chamber data analysis module
 │   ├── eol_data.py  # EOL production line data analysis module
 │   └── fitting_curve.py  # EOL production line data target fitting
 ├── visualization/
 │   ├── __init__.py
 │   ├── eol_plot.py  # Data visualization module
 │   └── noise_plot.py  # Data visualization module
 └── reports/
     ├── __init__.py
     └── report_generation.py  # Report generation module, automatically generates and exports reports
```

# Overview of main.py Example Content

Set up the running environment according to the aniconda3 tutorial, enter `python main.py` to run the program. If aniconda3 prompts that it cannot import PIL, please run `main.py` in VSCODE.

### 🌟 Star History
[![Star History Chart](https://api.star-history.com/svg?repos=aierlanjiu/NVH-data-analysis-system&type=Date)](https://star-history.com/#aierlanjiu/NVH-data-analysis-system&Date)

