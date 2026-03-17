import subprocess
import time
import pytest


@pytest.fixture(scope="session")
def server():
    process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
    )

    time.sleep(5)

    yield

    process.terminate()