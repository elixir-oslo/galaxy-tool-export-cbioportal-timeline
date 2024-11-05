# galaxy-tool-export-cbioportal-timeline

## Overview
`galaxy-tool-export-cbioportal-timeline` is a Python-based tool designed to convert PyClone data to cBioPortal timeline format. This tool can be used as a standalone script or integrated into the Galaxy platform.

## Features
- Converts PyClone data to cBioPortal timeline format.
- Generates meta and data files for cBioPortal.
- Supports exporting data to cBioPortal via an API endpoint.

## Requirements
- Python 3.x
- `pandas`
- `requests`
- `python-dotenv`

## Installation
Install the required Python packages using `pip`:
```sh
pip install -r requirements.txt
```

## Usage
### Standalone Script
To run the script standalone, use the following command:
```sh
python export_cbioportal_timeline.py --env_dir_path <path_to_env_file> --input_data <input_data_file> --study_id <study_id> --case_id <case_id> --meta_file_output <meta_file_output> --data_file_output <data_file_output> --timepoints <timepoints>
```
- `--env_dir_path`: Path to the `.env` file containing environment variables.
- `--input_data`: Input data file from history.
- `--study_id`: Study ID.
- `--case_id`: Case ID.
- `--meta_file_output`: Output meta file path.
- `--data_file_output`: Output data file path.
- `--timepoints`: String of timepoints separated by commas.

### Galaxy Tool
This tool can also be used within the Galaxy platform. The corresponding XML configuration is provided in the `export_cbioportal_timeline.xml` file.

#### XML Configuration
The XML configuration file `export_cbioportal_timeline.xml` defines the tool for Galaxy:
- **Tool ID**: `export_cbioportal_timeline`
- **Name**: `Load PyClone-VI output to cBioPortal Timeline`
- **Version**: `1.0.3`
- **Description**: Converts PyClone data to cBioPortal timeline format.

#### Inputs
- `input_data`: Input data file from history (tabular format).
- `study_id`: Study ID (default: `nsclc_tracerx_2017`).
- `case_id`: Case ID (default: `CRUK0009`).
- `timepoints`: Annotate timepoints of experiments.

#### Outputs
- `meta_file`: Meta Timeline file.
- `data_file`: Data Timeline file.

## Example
```sh
python export_cbioportal_timeline.py --env_dir_path .env --input_data input_data.tsv --study_id nsclc_tracerx_2017 --case_id CRUK0009 --meta_file_output meta_timeline.txt --data_file_output data_timeline.txt --timepoints "LN1,1,,R1,10,,R2,20,,R3,30,,R4,40,,R5,50,,R6,60,,R7,70,"
```
