from datetime import datetime
from typing import Any, Dict

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.enactment import Enactment
from ai_api_client_sdk.models.status import Status
from ai_api_client_sdk.models.target_status import TargetStatus


class Deployment(Enactment):
    """The Deployment object defines a deployment
    :param id: ID of the deployment
    :type id: str
    :param deployment_url: URL of the running deployment
    :type url: str
    :param configuration_id: ID of the configuration which configured the deployment
    :type configuration_id: str
    :param configuration_name: Name of the configuration which configured the deployment
    :type configuration_name: str
    :param scenario_id: ID of the scenario which the deployment belongs to
    :type scenario_id: str
    :param status: Status of the deployment
    :type status: class:`ai_api_client_sdk.models.status.Status`
    :param target_status: Target status of the deployment
    :type target_status: class:`ai_api_client_sdk.models.target_status.TargetStatus`
    :param created_at: Time when the deployment was created
    :type created_at: datetime
    :param modified_at: Time when the deployment was last modified
    :type modified_at: datetime
    :param status_details: A dict, which gives detailed information about the status of the deployment, defaults to None
    :type status_details: Dict[str, Any], optional
    :param submission_time: Time when the deployment was submitted
    :type submission_time: datetime, optional
    :param start_time: Time when the deployment status changed to RUNNING
    :type start_time: datetime, optional
    :param completion_time: Time when the deployment status changed to DEAD/STOPPED
    :type completion_time: datetime, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, deployment_url: str, configuration_id: str, configuration_name: str, scenario_id: str,
                 status: Status, target_status: TargetStatus, created_at: datetime, modified_at: datetime,
                 status_details: Dict[str, Any] = None, submission_time: datetime = None, start_time: datetime = None, 
                 completion_time: datetime = None, **kwargs):
        super().__init__(id=id, configuration_id=configuration_id, configuration_name=configuration_name,
                         scenario_id=scenario_id, status=status, target_status=target_status, created_at=created_at,
                         modified_at=modified_at, status_details=status_details, submission_time=submission_time, 
                         start_time=start_time, completion_time=completion_time, **kwargs)
        self.deployment_url: str = deployment_url

    @staticmethod
    def from_dict(deployment_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.deployment.Deployment` object, created from the values in the dict
        provided as parameter

        :param deployment_dict: Dict which includes the necessary values to create the object
        :type deployment_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.deployment.Deployment`
        """
        deployment_dict['status'] = Status(deployment_dict['status'])
        deployment_dict['target_status'] = TargetStatus(deployment_dict['target_status'])
        deployment_dict['created_at'] = parse_datetime(deployment_dict['created_at'])
        deployment_dict['modified_at'] = parse_datetime(deployment_dict['modified_at'])
        if deployment_dict.get('submission_time'):
            deployment_dict['submission_time'] = parse_datetime(deployment_dict['submission_time'])
        if deployment_dict.get('start_time'):
            deployment_dict['start_time'] = parse_datetime(deployment_dict['start_time'])
        if deployment_dict.get('completion_time'):
            deployment_dict['completion_time'] = parse_datetime(deployment_dict['completion_time'])
        return Deployment(**deployment_dict)
