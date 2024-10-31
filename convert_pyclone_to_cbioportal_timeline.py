import argparse
import os
import pandas as pd


def make_meta_timeline(study_id: str, data_file: str) -> str:
    return f"cancer_study_identifier: {study_id}\ngenetic_alteration_type: CLINICAL\ndatatype: TIMELINE\ndata_filename: {data_file}\n"

def make_dataframe_timeline_from_input(patient_id: str, dict_event: dict, input_data: str) -> pd.DataFrame:
    header = [
        "PATIENT_ID",
        "START_DATE" ,
        "STOP_DATE",
        "EVENT_TYPE",
        "TEST",
        "RESULT",
        ]

    df = pd.read_csv(input_data, sep="\t", header=0)

    data = []
    for index, row in df.iterrows():
        data.append({
            "PATIENT_ID": f"{patient_id}",
            "START_DATE": f"{dict_event[row['sample_id']]['start_date']}",
            "STOP_DATE": f"{dict_event[row['sample_id']]['stop_date']}",
            "EVENT_TYPE": "LAB_TEST",
            "TEST": f"cluster_{row['cluster_id']}",  # Assuming TEST and RESULT are empty as they are not in the print statement
            "RESULT": f"{row['cellular_prevalence']}"
        })

    result_df = pd.DataFrame(data, columns=header)

    # Remove duplicates rows
    result_df = result_df.drop_duplicates()


    return result_df.drop_duplicates()

def make_data_timeline(input_dataframe: pd.DataFrame, path_outfile: str) -> str:
    # Check if file exists
    if os.path.exists(path_outfile):
        previous_data = pd.read_csv(path_outfile, sep="\t", header=0)
        if input_dataframe["PATIENT_ID"].isin(previous_data["PATIENT_ID"]).any():
            previous_data = previous_data[~previous_data["PATIENT_ID"].isin(input_dataframe["PATIENT_ID"])]
            previous_data.to_csv(path_outfile, sep="\t", index=False)
        input_dataframe.to_csv(path_outfile, sep="\t", mode="a", header=False, index=False)
    else:
        input_dataframe.to_csv(path_outfile, sep="\t", index=False)



if __name__  == "__main__":

    # Data from Galaxy
    # path_all_study_directory = "/Users/jeannech/PycharmProjects/galaxy-tool-export-cbioportal/study"
    # input_data = "/Users/jeannech/PycharmProjects/galaxy-tool-export-cbioportal/tests/test_data/pyclone_export.tsv"
    # study_id = "nsclc_tracerx_2017"
    # case_id = "CRUK0009"
    parser = argparse.ArgumentParser(description="Convert PyClone data to cBioPortal timeline format")
    parser.add_argument("--path_all_study_directory", required=True, help="Path to all study directories")
    parser.add_argument("--input_data", required=True, help="Input data file from history")
    parser.add_argument("--study_id", required=True, help="Study ID")
    parser.add_argument("--case_id", required=True, help="Case ID")

    args = parser.parse_args()


    dict_event = {
            "LN1": {
                "start_date": "1",
                "stop_date": "",
            },
            "R1": {
                "start_date": "10",
                "stop_date": "",
            },
            "R2": {
                "start_date": "20",
                "stop_date": "",
            },
            "R3": {
                "start_date": "30",
                "stop_date": "",
            },
            "R4": {
                "start_date": "40",
                "stop_date": "",
            },
            "R5": {
                "start_date": "50",
                "stop_date": "",
            },
            "R6": {
                "start_date": "60",
                "stop_date": "",
            },
            "R7": {
                "start_date": "70",
                "stop_date": "",
            }
    }



    # Make file content
    name_data_file = "data_timeline_pyclone.txt"
    name_meta_file = "meta_timeline_pyclone.txt"

    content_meta_timeline = make_meta_timeline(study_id, name_data_file)
    dataframe_data_timeline = make_dataframe_timeline_from_input(case_id, dict_event, input_data)


    # Make output directory
    path_output_dir = os.path.join(path_all_study_directory, "partial_import", study_id)
    os.makedirs(path_output_dir, exist_ok=True)

    path_outfile_meta = os.path.join(path_output_dir, name_meta_file)
    path_outfile_data = os.path.join(path_output_dir, name_data_file)

    content_data_timeline = make_data_timeline(dataframe_data_timeline, path_outfile_data)


    # Save files
    with open(os.path.join(path_outfile_meta, name_meta_file), "w") as f:
        f.write(content_meta_timeline)













