import argparse
import os

import requests
import pandas as pd
from dotenv import load_dotenv


def parse_events(events_str: str) -> dict:
    parts = events_str.split(",")
    dict_event = {}
    for i in range(0, len(parts) - 1, 3):
        event_id = parts[i]
        start_date = parts[i + 1]
        stop_date = parts[i + 2] if i + 2 < len(parts) else ""

        if not start_date.isdigit():
            raise ValueError(f"Invalid start_date: {start_date}. It must be a string of an integer.")
        if stop_date and not stop_date.isdigit():
            raise ValueError(f"Invalid stop_date: {stop_date}. It must be empty or a string of an integer.")

        dict_event[event_id] = {"start_date": start_date, "stop_date": stop_date}
    return dict_event


def make_meta_timeline(study_id: str, data_file: str) -> str:
    return f"cancer_study_identifier: {study_id}\ngenetic_alteration_type: CLINICAL\ndatatype: TIMELINE\ndata_filename: {data_file}\n"


def make_dataframe_timeline_from_input(patient_id: str, dict_event: dict, input_data: str) -> pd.DataFrame:
    header = [
        "PATIENT_ID",
        "START_DATE",
        "STOP_DATE",
        "EVENT_TYPE",
        "TEST",
        "RESULT",
    ]

    df = pd.read_csv(input_data, sep="\t", header=0)

    data = []
    for index, row in df.iterrows():
        try:
            data.append({
                "PATIENT_ID": f"{patient_id}",
                "START_DATE": f"{dict_event[row['sample_id']]['start_date']}",
                "STOP_DATE": f"{dict_event[row['sample_id']]['stop_date']}",
                "EVENT_TYPE": "LAB_TEST",
                "TEST": f"cluster_{row['cluster_id']}",
                "RESULT": f"{row['cellular_prevalence']}"
            })
        # Exception handling for the case where the sample_id is not found in the dict_event
        except KeyError:
            continue

    result_df = pd.DataFrame(data, columns=header)

    # Remove duplicates rows
    result_df = result_df.drop_duplicates()

    return result_df


def export_timeline_to_cbioportal(df_data_content: pd.DataFrame, meta_content: str, case_id: str, study_id: str, suffix: str="pyclone") -> requests.Response:
    # url = "http://cbioportal-galaxy-connector-container:3001/export-timeline-to-cbioportal"
    url = os.getenv('EXPORT_TIMELINE_ENDPOINT')
    if not url:
        raise ValueError("EXPORT_TIMELINE_ENDPOINT environment variable is not set")

    # Convert dataframe to string
    data_content = df_data_content.to_csv(sep="\t", index=False)

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "dataContent": data_content,
        "caseId": case_id,
        "studyId": study_id,
        "metaContent": meta_content,
        "suffix": suffix
    }

    response_request = requests.post(url, headers=headers, json=payload)

    return response_request


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PyClone data to cBioPortal timeline format")
    parser.add_argument("-i", "--input_data", required=True, help="Input data file from history")
    parser.add_argument("-s", "--study_id", required=True, help="Study ID")
    parser.add_argument("-c", "--case_id", required=True, help="Case ID")
    parser.add_argument("-mo", "--meta_file_output", required=True, help="Output meta file path")
    parser.add_argument("-do", "--data_file_output", required=True, help="Output data file path")
    parser.add_argument("-t", "--timepoints", help="String of timepoints separated by comma")
    parser.add_argument("-e", "--env_dir_path", help="Path to the .env file")

    args = parser.parse_args()
    dict_event = parse_events(args.timepoints)
    load_dotenv(args.env_dir_path)


    # dict_event = {
    #     "LN1": {"start_date": "1", "stop_date": ""},
    #     "R1": {"start_date": "10", "stop_date": ""},
    #     "R2": {"start_date": "20", "stop_date": ""},
    #     "R3": {"start_date": "30", "stop_date": ""},
    #     "R4": {"start_date": "40", "stop_date": ""},
    #     "R5": {"start_date": "50", "stop_date": ""},
    #     "R6": {"start_date": "60", "stop_date": ""},
    #     "R7": {"start_date": "70", "stop_date": ""}
    # }

    # Set file names
    name_data_file = "data_timeline_pyclone.txt"
    name_meta_file = "meta_timeline_pyclone.txt"

    # Make file content
    content_meta_timeline = make_meta_timeline(args.study_id, name_data_file)
    dataframe_data_timeline = make_dataframe_timeline_from_input(args.case_id, dict_event, args.input_data)


    response = export_timeline_to_cbioportal(df_data_content=dataframe_data_timeline, case_id=args.case_id, study_id=args.study_id, meta_content=content_meta_timeline)



    # Write to files
    with open(args.meta_file_output, "w") as f:
        f.write(content_meta_timeline)

    dataframe_data_timeline.to_csv(args.data_file_output, sep="\t", header=True, index=False)
