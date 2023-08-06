from snitch_ai.internal.guid import GUID
from snitch_ai.internal.api_client import ApiClient
from snitch_ai.internal.analysis_status import AnalysisState, AnalysisStatus
from snitch_ai.internal.logger import Logger

class DriftAnalysis:

    def __init__(self, project_id: GUID, drift_id: GUID):
        self.project_id = project_id
        self.drift_id = drift_id


    def get_status(self) -> AnalysisStatus:
        """
        Gets the status of this Drift analysis.
        :return: The status of the analysis.
        """
        client = ApiClient()
        resp = client.get(f"project/{self.project_id}/drift/{self.drift_id}/status")
        if resp.status_code != 200:
            raise Exception(f"Error while waiting on analysis: {resp} {resp.text}")

        json = resp.json()

        return AnalysisStatus(AnalysisState(json["state"]), json["error"])


    def get_json(self):
        """
        Gets the JSON results for this Drift analysis.
        :return: The JSON results.
        """
        Logger.information("Fetching JSON results...")

        client = ApiClient()
        resp = client.get(f"project/{self.project_id}/drift/{self.drift_id}/json")
        if resp.status_code != 200:
            raise Exception(f"Error while getting drift analysis JSON: {resp.text}")
        
        Logger.information("Fetched JSON results!")

        return resp.json()


    def save_pdf(self, path):
        """
        Saves the PDF report of this Drift analysis to the specified path.
        :param path: The path to save the PDF report to.
        """
        Logger.information("Saving PDF report...")

        client = ApiClient()
        resp = client.get(f"project/{self.project_id}/drift/{self.drift_id}/pdf")
        if resp.status_code != 200:
            raise Exception(f"Error while getting drift analysis PDF: {resp.text}")

        with open(path, "wb") as f:
            f.write(resp.content)
        
        Logger.information("Saved PDF report!")



    def __str__(self):
        return f"Drift Analysis {self.drift_id}"