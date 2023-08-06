"""
RedBrick SDK is a Python package for the RedBrick AI platform.

Visit https://docs.redbrickai.com/python-sdk/sdk-overview for an
overview of how to use the SDK and to view code examples.

To use the RedBrick SDK you need to create an API key. Please
see this documentation for accomplishing that.
https://docs.redbrickai.com/python-sdk/sdk-overview#generate-an-api-key
"""

import asyncio

import nest_asyncio  # type: ignore

from redbrick.common.context import RBContext
from redbrick.common.enums import LabelType, StorageMethod
from redbrick.project import RBProject
from redbrick.organization import RBOrganization

from redbrick.utils.logging import print_info, print_warning
from redbrick.repo import (
    ExportRepo,
    LabelingRepo,
    LearningRepo,
    Learning2Repo,
    UploadRepo,
    ProjectRepo,
)
from .version_check import __version__


# if there is a running event loop, apply nest_asyncio
try:
    asyncio.get_running_loop()
    nest_asyncio.apply()
    print_info(
        "Applying nest-asyncio to a running event loop, this likely means you're in a jupyter"
        + " notebook and you can safely ignore this."
    )
except RuntimeError:
    pass


DEFAULT_URL = "https://api.redbrickai.com"


def _populate_context(context: RBContext) -> RBContext:
    context.export = ExportRepo(context.client)
    context.labeling = LabelingRepo(context.client)
    context.learning = LearningRepo(context.client)
    context.learning2 = Learning2Repo(context.client)
    context.upload = UploadRepo(context.client)
    context.project = ProjectRepo(context.client)
    return context


ORG_API_HAS_CHANGED = (
    "this api has changed recently, try running help(redbrick.get_org)"
    + " or visiting https://redbrick-sdk.readthedocs.io/en/stable/#redbrick.get_org"
)


PROJECT_API_HAS_CHANGED = (
    "this api has changed recently, try running help(redbrick.get_project)"
    + " or visiting https://redbrick-sdk.readthedocs.io/en/stable/#redbrick.get_project"
)

print_warning(
    "For 0.7 onwards, we've made url an optional argument,"
    + " you'll need to update your code to use the following:"
    + "\n \t\t get_org(org_id=org_id, api_key=api_key) and"
    + "\n \t\t get_project(org_id=org_id, project_id=project_id, api_key=api_key),"
    + "\n https://redbrick-sdk.readthedocs.io/en/stable/#redbrick.get_org"
)


def get_org(org_id: str, api_key: str, url: str = DEFAULT_URL) -> RBOrganization:
    """
    Get an existing redbrick organization object.

    Organization object allows you to interact with your organization
    and perform high level actions like creating a project.

    Parameters
    ---------------
    org_id: str
        Your organizations unique id https://app.redbrickai.com/<org_id>/.

    api_key: str
        Your secret api_key, can be created from the RedBrick AI platform.

    url: str = DEFAULT_URL
        Should default to https://api.redbrickai.com
    """
    if len(org_id) != 36:
        raise ValueError("Your first argument looks incorrect, " + ORG_API_HAS_CHANGED)
    if "." in api_key:
        raise ValueError(
            "Your second argument looks like a url, " + ORG_API_HAS_CHANGED
        )

    context = _populate_context(RBContext(api_key, url))

    return RBOrganization(context, org_id)


def get_project(
    org_id: str, project_id: str, api_key: str, url: str = DEFAULT_URL
) -> RBProject:
    """
    Get an existing RedBrick project object.

    Project objects allow you to interact with your RedBrick Ai projects,
    and perform actions like importing data, exporting data etc.

    Parameters
    ---------------
    org_id: str
        Your organizations unique id https://app.redbrickai.com/<org_id>/

    project_id: str
        Your projects unique id https://app.redbrickai.com/<org_id>/<project_id>/

    api_key: str
        Your secret api_key, can be created from the RedBrick AI platform.

    url: str = DEFAULT_URL
        Should default to https://api.redbrickai.com
    """
    if len(org_id) != 36:
        raise ValueError(
            "Your first argument looks incorrect, " + PROJECT_API_HAS_CHANGED
        )
    if "http" in project_id:
        raise ValueError(
            "Your second argument looks like a url, " + PROJECT_API_HAS_CHANGED
        )

    context = _populate_context(RBContext(api_key, url))
    return RBProject(context, org_id, project_id)
