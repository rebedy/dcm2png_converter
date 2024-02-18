# Simple Dicom2PNG Converter

This is a simple python script to convert dicom files to png files based on dataframe to only convert matching dicom files. It uses the SimpleITK library to read and convert the dicom files and the Pillow library to save the png files.

<br>

## Installation

To install the required libraries, run the following command:

```bash
pip install -r requirements.txt
```

<br>

## Usage

To convert dicom files to png files, run the following command:

```bash
python dcm2png.py
```

<br>

## Configuration

To configure the script, open the `dcm2png.py` file and modify the following variables:

- `dcm_path`: The directory containing the dicom files.
- `output_path`: The directory to save the png files. If the directory does not exist, it will be created.
