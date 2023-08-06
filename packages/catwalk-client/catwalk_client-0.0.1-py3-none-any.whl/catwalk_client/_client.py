import json
import logging
import os
import requests
from ._case_builder import CaseBuilder
from catwalk_common import CommonCaseFormat

logger = logging.getLogger("catwalk_client")


class CatwalkClient:

    submitter_name: str
    submitter_version: str
    catwalk_url: str

    def __init__(self, submitter_name: str, submitter_version: str, catwalk_url: str = None):
        self.submitter_name = submitter_name
        self.submitter_version = submitter_version
        self.catwalk_url = catwalk_url or os.environ.get("CATWALK_URL")

    def new_case(self) -> CaseBuilder:
        return CaseBuilder(client=self)

    def send(self, case: dict):
        case = CommonCaseFormat(
            submitter={"name": self.submitter_name, "version": self.submitter_version},
            **case
        )

        response = requests.post(self.catwalk_url.rstrip('/') + "/api/cases/collect", data=case.json())

        if response.ok:
            data = json.loads(response.text)
            logger.info(f"Collected catwalk case: {data['id']}")
