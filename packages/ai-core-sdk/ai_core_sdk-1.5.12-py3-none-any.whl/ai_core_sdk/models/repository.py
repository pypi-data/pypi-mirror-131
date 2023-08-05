from typing import Dict

from ai_core_sdk.models.repository_status import RepositoryStatus


class Repository:
    """The Repository object defines the repository

    :param name: name of the repository
    :type name: str
    :param url: URL of the repository
    :type url: str
    :param status: status of the repository, defaults to None
    :type status: class:`ai_core_sdk.models.repository_status.RepositoryStatus`, optional
    """
    def __init__(self, name: str, url: str, status: RepositoryStatus = None, *args, **kwargs):
        self.name: str = name
        self.url: str = url
        self.status: RepositoryStatus = status

    @staticmethod
    def from_dict(repository_dict: Dict[str, str]):
        """Returns a :class:`ai_core_sdk.models.repository.Repository` object, created
        from the values in the dict provided as parameter

        :param repository_dict: Dict which includes the necessary values to create the object
        :type repository_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.repository.Repository`
        """
        repository_dict['status'] = RepositoryStatus(repository_dict['status'])
        return Repository(**repository_dict)
