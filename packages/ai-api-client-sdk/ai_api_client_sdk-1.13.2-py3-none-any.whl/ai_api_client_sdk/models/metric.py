from datetime import datetime
from typing import Any, Dict, List

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.metric_label import MetricLabel


class Metric:
    """The Metric object, defines a single metric.

    :param name: Name of the metric
    :type name: str
    :param value: numeric value of the metric
    :type value: float
    :param timestamp: Time when the metric was created
    :type timestamp: datetime
    :param step: any measurement of training progress (number of training iterations, number of epochs, etc.)
    :type step: int
    :param labels: List of the labels of the metric, defaults to None
    :type labels: List[class:`ai_api_client_sdk.models.metric_label.MetricLabel`]
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, name: str, value: float, timestamp: datetime, step: int = None,
                 labels: List[MetricLabel] = None, **kwargs):
        self.name: str = name
        self.value: float = value
        self.timestamp: datetime = timestamp
        self.step: int = step
        self.labels: List[MetricLabel] = labels

    def __eq__(self, other):
        if not isinstance(other, Metric):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    @staticmethod
    def from_dict(metric_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.metric.Metric` object, created from the values in the dict
        provided as parameter

        :param metric_dict: Dict which includes the necessary values to create the object
        :type metric_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.metric.Metric`
        """
        if metric_dict.get('timestamp'):
            metric_dict['timestamp'] = parse_datetime(metric_dict['timestamp'])
        if metric_dict.get('labels'):
            metric_dict['labels'] = [MetricLabel.from_dict(l) for l in metric_dict['labels']]
        return Metric(**metric_dict)

    def to_dict(self):
        """Returns the attributes of the object as a dictionary

        :return: A dict, including all the attributes of the object
        :rtype: Dict[str, str]
        """
        metric = self
        if metric.labels:
            metric.labels = [l.to_dict() for l in self.labels]
        if metric.timestamp:
            metric.timestamp = metric.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

        return metric.__dict__
