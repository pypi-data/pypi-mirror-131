import logging
import pathlib

import pytest

import tiamatpip
from tests.support.helpers import TiamatPipProject

log = logging.getLogger(__name__)

CODE_ROOT = pathlib.Path(tiamatpip.__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def built_project(request, tmpdir_factory):
    name = f"tiamat-{request.node.parent.name}"
    instance = TiamatPipProject(
        name=name, path=pathlib.Path(tmpdir_factory.mktemp(name, numbered=True))
    )
    with instance:
        yield instance


@pytest.fixture
def project(built_project):
    try:
        log.info("Built Project: %s", built_project)
        yield built_project
    finally:
        built_project.delete_pypath()
