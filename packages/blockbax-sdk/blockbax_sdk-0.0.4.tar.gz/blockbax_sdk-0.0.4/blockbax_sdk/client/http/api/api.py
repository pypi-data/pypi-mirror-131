from typing import List, Optional

from . import api_utils
from blockbax_sdk import errors

import requests
from urllib3.util import retry
import json
import math

import logging
logger = logging.getLogger(__name__)

class Api:
    access_token: str
    project_id: str
    base_url: str
    api_url: str = "https://api.blockbax.com"
    api_version: str = "v1"
    property_types_endpoint: str = "propertyTypes"
    subject_types_endpoint: str = "subjectTypes"
    subjects_endpoint: str = "subjects"
    metrics_endpoint: str = "metrics"
    measurements_endpoint: str = "measurements"
    default_page_size: int = 200
    retry_total: int = 2
    backoff_factor: int = 2 # backoff factor 2 in seconds (depending on retry_total): 1, 2, 4, 8, 16, 32, 64, 128, 256, 512
    retry_status_forcelist: List[int] = [429, 500, 502, 503, 504]
    
    def __init__(
        self, 
        access_token: str, 
        project_id: str,
        http_adapter: Optional[requests.adapters.BaseAdapter] = None,
        retry_strategy: Optional[retry.Retry] = None,
    ):
        self.session = requests.Session()
        
        if not retry_strategy:
            retry_strategy =  retry.Retry(
                total=self.retry_total,
                backoff_factor=self.backoff_factor,
                status_forcelist=self.retry_status_forcelist,
                )
        if not http_adapter:
            http_adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
        
        self.session.mount("http://", http_adapter)
        self.session.mount("https://", http_adapter)

        self.access_token = access_token
        self.project_id = project_id
        self.base_url = f"{self.api_url}/{self.api_version}/projects/{project_id}"
        self.session.headers.update(
            {
                "Authorization": "ApiKey " + self.access_token,
                "Content-Type": "application/json",
            }
        )
        # response handlers
        self.session.hooks["response"] = [
            lambda response, *args, **kwargs: api_utils.http_error_handler(response),
            lambda response, *args, **kwargs: api_utils.response_status_handler(response),
            ]   
    
    # http requests
    
    def get(self, endpoint: str = "",params = {}) -> Optional[dict]:
        """get a single instance from the API using ID"""
        r = self.session.get(url=f"{self.base_url}/{endpoint}".strip(),params=params)
        return api_utils.parse_response(r)
        
    def search(self, endpoint:str = "", params: dict = None) -> List[dict]:
        """search multiple instances from the API using automatic paging, returns a list of results"""
        # check params, if no size or page was given use default
        if not params:
            params = {}
        params['size'] = self.default_page_size
        
        current_page_index = 0
        last_page_number = None
        results = []
        done = False
        # while the previous page is not equal to the last page index get the current page index
        while(not done):
            params['page'] = current_page_index
            r = self.session.get(url=f"{self.base_url}/{endpoint}".strip(), params=params)
            response = api_utils.parse_response(r)
            results.extend(response.get('result') if response.get('result') is not None else [])
            if response.get("count") is None:
                return results # return because we do not know when to stop
            
            if last_page_number is None:
                last_page_number = math.ceil(response['count']  / params['size']) # page index starts from 0
            current_page_index += 1
            
            if current_page_index >= last_page_number:
                done = True
        return results
            
    def post(self, endpoint, data):
        r = self.session.post(
            url=f"{self.base_url}/{endpoint}".strip(), 
            data=json.dumps(data, cls=api_utils.JSONEncoderWithDecimal)
            )
        if not r.text:
            return None
        return json.loads(r.text)

    def put(self, endpoint, data):
        r = self.session.put(
            url=f"{self.base_url}/{endpoint}".strip(), 
            data=json.dumps(data, cls=api_utils.JSONEncoderWithDecimal)
            )
        if not r.text:
            return None
        return json.loads(r.text)

    def delete(self, endpoint):
        self.session.delete(url=f"{self.base_url}/{endpoint}".strip())
    
    # project

    def get_project(self):
        return self.get()

    # property types
    
    def get_property_type(self, property_type_id: str):
        return self.get(endpoint=f"{self.property_types_endpoint}/{property_type_id}")

    def get_property_types(self, name: Optional[str] = None, external_id: Optional[str] = None):
        params = {"name" : name, "externalId": external_id}
        return self.search(self.property_types_endpoint, params=params)

    def create_property_type(
        self, 
        name: str, 
        data_type: str, 
        predefined_values: bool = False, 
        values: List[dict] = []
    ):

        body = {
            "name": name,
            "dataType": data_type,
            "predefinedValues": predefined_values,
            "values": values,
        }
        response = self.post(
            endpoint=self.property_types_endpoint, 
            data=body
            )
        return response

    def update_property_type(
        self,
        property_type_id: str,
        name: str,
        data_type: str,
        predefined_values=False,
        values=[],
    ):

        body = {
            "name": name,
            "dataType": data_type,
            "predefinedValues": predefined_values,
            "values": values,
        }
        response = self.put(
            endpoint=f"{self.property_types_endpoint}/{property_type_id}",
            data=body
        )
        return response
    def delete_property_type(self, property_type_id: str):
        self.delete(endpoint=f"{self.property_types_endpoint}/{property_type_id}")
    
    # subject types
    
    def get_subject_type(self, subject_type_id: str):
        return self.get(endpoint=f"{self.subject_types_endpoint}/{subject_type_id}")
    
    def get_subject_types(self, name: Optional[str] = None, property_type_ids: Optional[list] = None):
        params = {"name" : name, "propertyTypes": property_type_ids}
        return self.search(endpoint=f"{self.subject_types_endpoint}",params=params)
    
    def create_subject_type(
        self,
        name: str,
        parent_id: str = None,
        primary_location: dict = {},
        property_types: list = []
    ):
        body = {
            "name": name,
            "parentSubjectTypeId":parent_id,
            "primaryLocation": primary_location,
            "propertyTypes": property_types,
        }
        response = self.post(endpoint=self.subject_types_endpoint, data=body)
        return response

    def update_subject_type(
        self,
        subject_type_id: str,
        name: str,
        parent_id: str = None,
        primary_location: dict = {},
        property_types: list = []
    ):
        body = {
            "name": name,
            "parentSubjectTypeId":parent_id,
            "primaryLocation": primary_location,
            "propertyTypes": property_types
        }
        response = self.put(
            endpoint=f"{self.subject_types_endpoint}/{subject_type_id}", 
            data=body
        )
        return response

    def delete_subject_type(self, subject_type_id: str):
        self.delete(endpoint=f"{self.subject_types_endpoint}/{subject_type_id}")

    # subjects

    def get_subject(
        self, 
        subject_id: str
    ) -> dict:
        return self.get(endpoint=f"{self.subjects_endpoint}/{subject_id}")
    
    def get_subjects(
        self, 
        name: Optional[str] = None,
        subject_ids: List[str] = None,
        subject_type_ids: Optional[list] = None,
        subject_external_id: Optional[str] = None, 
        property_value_ids: Optional[str] = None
    ) -> list:
        params = {"name" : name, "subjectIds" : subject_ids , "subjectTypeIds" : subject_type_ids, "externalId" : subject_external_id, "propertyValueIds" : property_value_ids}
        return self.search(endpoint=self.subjects_endpoint, params=params)

    def create_subject(
            self,
            name: str,
            subject_type_id: str,
            external_id: str,
            ingestion_ids: list,
            parent_id: str = None,
            properties: list = None,
    ):
        body = {
            "name": name,
            "subjectTypeId": subject_type_id,
            "parentSubjectId":parent_id,
            "externalId": external_id,
            "ingestionIds": ingestion_ids,
            "properties": properties
        }
        response = self.post(
            endpoint=self.subjects_endpoint, 
            data=body
            )
        return response

    def update_subject(
            self,
            subject_id: str,
            name: str,
            subject_type_id: str,
            external_id: str,
            ingestion_ids: list,
            parent_id: str = None,
            properties: list = None,
    ):
        body = {
            "name": name,
            "subjectTypeId": subject_type_id,
            "parentSubjectId":parent_id,
            "externalId": external_id,
            "ingestionIds": ingestion_ids,
            "properties": properties
        }
        
        response = self.put(
            endpoint=f"{self.subjects_endpoint}/{subject_id}", 
            data=body
            )
        
        return response

    def delete_subject(self, subject_id: str):
        self.delete(endpoint=f"{self.subjects_endpoint}/{subject_id}")
        
    # metrics

    def get_metric(
        self, 
        metric_id: str
    ) -> dict:
        return self.get(endpoint=f"{self.metrics_endpoint}/{metric_id}")

    def get_metrics(
        self, 
        name: Optional[str] = None, 
        subject_type_ids: Optional[List[str]] = None, 
        metric_external_id: Optional[str] = None
    ) -> List[dict]:
        params = {"name": name, "subjectTypeIds": subject_type_ids,"externalId": metric_external_id}
        return self.search(endpoint=self.metrics_endpoint, params=params)

    def create_metric(
        self,
        name: str,
        data_type: str,
        external_id: str,
        type_: str,
        discrete: bool,
        subject_type_id: str,
        unit:str = None,
        precision: str = None,
        visible:str = None
    ):
        body = {
            "name": name,
            "externalId": external_id,
            "subjectTypeId": subject_type_id,
            "dataType": data_type,
            "unit": unit,
            "precision": precision,
            "visible": visible,
            "type": type_,
            "discrete": discrete,
        }
        response = self.post(
            endpoint=self.metrics_endpoint, 
            data=body
            )
        return response

    def update_metric(
        self,
        metric_id: str,
        name: str,
        data_type: str,
        external_id: str,
        type_: str,
        discrete: bool,
        subject_type_id: str,
        unit:str = None,
        precision: str = None,
        visible:str = None
    ):
        body = {
            "name": name,
            "externalId": external_id,
            "subjectTypeId": subject_type_id,
            "dataType": data_type,
            "unit": unit,
            "precision": precision,
            "visible": visible,
            "type": type_,
            "discrete": discrete,
        }
        response = self.put(
            endpoint=f"{self.metrics_endpoint}/{metric_id}", 
            data=body
            )
        return response

    def delete_metric(self, metric_id: str):
        self.delete(endpoint=f"{self.metrics_endpoint}/{metric_id}")

    # measurements

    def get_measurements(
        self, 
        subject_ids: Optional[str] = None, 
        metric_ids: Optional[str] = None, 
        from_date: Optional[str] = None, 
        to_date: Optional[str] = None,
        size: Optional[int] = None,
        order: Optional[str] = "asc",
    ) -> List[dict]:
        params = {
            "subjectIds": subject_ids,
            "metricIds": metric_ids,
            "fromDate": from_date,
            "toDate": to_date,
            "size":size,
            "order":order
        }
        return self.get(endpoint=self.measurements_endpoint,params=params)

    def send_measurements(self, series: List[dict], auto_create_subjects: bool = False):
        body = {
            "autoCreateSubjects": auto_create_subjects,
            "series":series
        }
        response = self.post(
            endpoint=self.measurements_endpoint, 
            data=body
            )
        return response