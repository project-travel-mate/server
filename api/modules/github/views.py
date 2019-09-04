from datetime import timedelta

import requests
import requests_cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.commonresponses import DOWNSTREAM_ERROR_RESPONSE
from api.modules.github.constants import GITHUB_API_GET_CONTRIBUTORS_URL, GITHUB_API_GET_ISSUES_URL
from api.modules.github.github_response import ContributorResponse, IssueResponse

hour_difference = timedelta(days=1)
requests_cache.install_cache(expire_after=hour_difference)


@api_view(['GET'])
def get_contributors(request, project):
    """
    Return list of people contributed
    :param request:
    :param project:
    :return: 503 if github api fails
    :return: 200 successful
    """
    try:
        api_response = requests.get(
            GITHUB_API_GET_CONTRIBUTORS_URL.format(project_name=project)
        )
        api_response_json = api_response.json()
        # if authentication fails
        if api_response.status_code == 401:
            raise Exception("Authentication fails. Invalid github access token.")
        response = []
        for contributor in api_response_json:
            result = ContributorResponse(
                username=contributor['login'],
                url=contributor['html_url'],
                avatar_url=contributor['avatar_url'],
                contributions=contributor['contributions'],
                repository_name=project,
            )
            result_as_json = result.to_json()
            response.append(result_as_json)
    except Exception:
        return DOWNSTREAM_ERROR_RESPONSE

    return Response(response)


@api_view(['GET'])
def get_issues(request, project):
    """
        Return list of issues
        :param request:
        :param project:
        :return: 503 if github api fails
        :return: 200 successful
        """

    try:
        api_response = requests.get(GITHUB_API_GET_ISSUES_URL.format(project_name=project))
        api_response_json = api_response.json()
        if api_response.status_code == 404:
            error_message = "Repository does not exist"
            return Response(error_message, status=status.HTTP_404_NOT_FOUND)
        if api_response.status_code == 401:
            raise Exception("Authentication fails. Invalid github access token.")
        response = []
        for issue in api_response_json:
            labels_length = len(issue['labels'])
            tags = []
            # Making custom dictionary for tags
            for i in range(0, labels_length):
                # Searching inside "labels" key for tag_name
                for tag, tag_name in issue["labels"][i].items():
                    if tag in ["name"]:
                        label = tag_name
                tags.append(label)
            result = IssueResponse(
                title=issue['title'],
                created_at=issue['created_at'],
                comments=issue['comments'],
                issue_number=issue['number'],
                repository_url=issue['repository_url'],
                labels=tags
            )
            result_as_json = result.to_json()
            response.append(result_as_json)

    except Exception:
        return DOWNSTREAM_ERROR_RESPONSE

    return Response(response)
