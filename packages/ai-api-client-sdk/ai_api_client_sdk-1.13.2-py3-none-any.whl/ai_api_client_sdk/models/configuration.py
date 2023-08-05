from datetime import datetime
from typing import Any, Dict, List

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.input_artifact_binding import InputArtifactBinding
from ai_api_client_sdk.models.parameter_binding import ParameterBinding


class Configuration:
    """The Configuration object defines a configuration

    :param id: ID of the configuration
    :type id: str
    :param name: Name of the configuration
    :type name: str
    :param scenario_id: ID of the scenario which the configuration belongs to
    :type scenario_id: str
    :param executable_id: ID of the executable, which is configured
    :type executable_id: str
    :param created_at: Time when the configuration was created
    :type created_at: datetime
    :param parameter_bindings: List of the input parameters defined as key-value pairs, defaults to None
    :type parameter_bindings: List[class:`ai_api_client_sdk.models.parameter_binding.ParameterBinding`], optional
    :param input_artifact_bindings: List of the input artifacts which are to be used by the executable, defaults to None
    :type input_artifact_bindings: List[class:`ai_api_client_sdk.models.input_artifact_binding.InputArtifactBinding`],
        optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, name: str, scenario_id: str, executable_id: str, created_at: datetime,
                 parameter_bindings: List[ParameterBinding] = None,
                 input_artifact_bindings: List[InputArtifactBinding] = None, **kwargs):
        self.id: str = id
        self.name: str = name
        self.scenario_id: str = scenario_id
        self.executable_id: str = executable_id
        self.parameter_bindings: List[ParameterBinding] = parameter_bindings
        self.input_artifact_bindings: List[InputArtifactBinding] = input_artifact_bindings
        self.created_at: datetime = created_at

    @staticmethod
    def from_dict(configuration_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.configuration.Configuration` object, created from the values in the
        dict provided as parameter

        :param configuration_dict: Dict which includes the necessary values to create the object
        :type configuration_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.configuration.Configuration`
        """
        configuration_dict['created_at'] = parse_datetime(configuration_dict['created_at'])
        if configuration_dict.get('parameter_bindings'):
            configuration_dict['parameter_bindings'] = \
                [ParameterBinding.from_dict(pb) for pb in configuration_dict['parameter_bindings']]
        if configuration_dict.get('input_artifact_bindings'):
            configuration_dict['input_artifact_bindings'] = \
                [InputArtifactBinding.from_dict(iab) for iab in configuration_dict['input_artifact_bindings']]
        return Configuration(**configuration_dict)
