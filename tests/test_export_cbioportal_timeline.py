import unittest
import pandas as pd
from io import StringIO
from export_cbioportal_timeline import parse_events, make_meta_timeline, make_dataframe_timeline_from_input, export_timeline_to_cbioportal

class TestExportCbioportalTimeline(unittest.TestCase):

    def test_parse_events(self):
        events_str = "LN1,1,,R1,10,,R2,20,,R3,30,,R4,40,,R5,50,,R6,60,,R7,70,"
        expected_output = {
            "LN1": {"start_date": "1", "stop_date": ""},
            "R1": {"start_date": "10", "stop_date": ""},
            "R2": {"start_date": "20", "stop_date": ""},
            "R3": {"start_date": "30", "stop_date": ""},
            "R4": {"start_date": "40", "stop_date": ""},
            "R5": {"start_date": "50", "stop_date": ""},
            "R6": {"start_date": "60", "stop_date": ""},
            "R7": {"start_date": "70", "stop_date": ""}
        }
        self.assertEqual(parse_events(events_str), expected_output)

    def test_make_meta_timeline(self):
        study_id = "test_study"
        data_file = "data_timeline.txt"
        expected_output = "cancer_study_identifier: test_study\ngenetic_alteration_type: CLINICAL\ndatatype: TIMELINE\ndata_filename: data_timeline.txt\n"
        self.assertEqual(make_meta_timeline(study_id, data_file), expected_output)

    def test_make_dataframe_timeline_from_input(self):
        patient_id = "CRUK0009"
        dict_event = {
            "LN1": {"start_date": "1", "stop_date": ""},
            "R1": {"start_date": "10", "stop_date": ""}
        }
        input_data = StringIO("sample_id\tcluster_id\tcellular_prevalence\nLN1\t1\t0.5\nR1\t2\t0.6\n")
        expected_output = pd.DataFrame({
            "PATIENT_ID": ["CRUK0009", "CRUK0009"],
            "START_DATE": ["1", "10"],
            "STOP_DATE": ["", ""],
            "EVENT_TYPE": ["LAB_TEST", "LAB_TEST"],
            "TEST": ["cluster_1", "cluster_2"],
            "RESULT": ["0.5", "0.6"]
        })
        result_df = make_dataframe_timeline_from_input(patient_id, dict_event, input_data)
        pd.testing.assert_frame_equal(result_df, expected_output)

    def test_export_timeline_to_cbioportal(self):
        # Mocking the requests.post method
        import requests
        from unittest.mock import patch

        # Set environment variables CBIOPORTAL_URL
        import os
        os.environ["CBIOPORTAL_URL"] = "http://localhost:8080/cbioportal/"


        df_data_content = pd.DataFrame({
            "PATIENT_ID": ["CRUK0009"],
            "START_DATE": ["1"],
            "STOP_DATE": [""],
            "EVENT_TYPE": ["LAB_TEST"],
            "TEST": ["cluster_1"],
            "RESULT": ["0.5"]
        })
        meta_content = "cancer_study_identifier: test_study\ngenetic_alteration_type: CLINICAL\ndatatype: TIMELINE\ndata_filename: data_timeline.txt\n"
        case_id = "CRUK0009"
        study_id = "test_study"

        with patch('requests.post') as mocked_post:
            mocked_post.return_value.status_code = 200
            mocked_post.return_value.json.return_value = {"message": "Data successfully exported to cBioPortal."}

            response = export_timeline_to_cbioportal(df_data_content, meta_content, case_id, study_id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Data successfully exported to cBioPortal."})

if __name__ == '__main__':
    unittest.main()