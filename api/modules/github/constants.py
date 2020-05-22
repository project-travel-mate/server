"""
Uses the Github API V3 doc: https://developer.github.com/v3/repos/
"""
import os

ORGANISATION_NAME = 'project-travel-mate/'
ACTIVE_REPOSITORIES = ['Travel-Mate', 'server', 'project-travel-mate.github.io']

GITHUB_API_KEY = os.environ.get("GITHUB_API_KEY", "")
GITHUB_API_URL = "https://api.github.com/"

GITHUB_API_GET_CONTRIBUTORS_URL = GITHUB_API_URL + "repos/" + ORGANISATION_NAME \
                                  + "{project_name}/contributors?access_token=" + GITHUB_API_KEY

GITHUB_API_GET_ISSUES_URL = GITHUB_API_URL + "repos/" + ORGANISATION_NAME \
                            + "{project_name}/issues?access_token=" + GITHUB_API_KEY
