import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--skip-ai-tests", action="store_true", default=False, help="skip tests that call AI APIs"
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "ai: marks tests as calling AI APIs")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-ai-tests"):
        skip_ai = pytest.mark.skip(reason="--skip-ai-tests option was provided")
        for item in items:
            if "ai" in item.keywords:
                item.add_marker(skip_ai)