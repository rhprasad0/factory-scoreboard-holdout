"""Starts the API under test the way the frozen local-run contract says it starts.

Set APP_DIR to the app/ directory of the checkout being graded.
"""

import os
import signal
import socket
import subprocess
import time
from pathlib import Path

import httpx
import pytest

PORT = 9000
# A cold Rust build happens on the first request, and that request blocks until it ends.
STARTUP_SECONDS = 600
STOP_SECONDS = 10


def _wait_until_serving(client: httpx.Client, server: subprocess.Popen) -> None:
    deadline = time.monotonic() + STARTUP_SECONDS
    while time.monotonic() < deadline:
        if server.poll() is not None:
            pytest.fail(f"cargo lambda watch exited early with code {server.returncode}")
        try:
            # Any answer below 500 means it is up. Whether it is right is the oracle's job.
            if client.get("/health").status_code < 500:
                return
        except httpx.TransportError:
            pass
        time.sleep(2)
    pytest.fail(f"API did not start within {STARTUP_SECONDS} seconds")


def _stop(server: subprocess.Popen) -> None:
    os.killpg(server.pid, signal.SIGTERM)
    try:
        server.wait(STOP_SECONDS)
    except subprocess.TimeoutExpired:
        os.killpg(server.pid, signal.SIGKILL)
        server.wait()


@pytest.fixture(scope="session")
def api():
    app_dir = Path(os.environ["APP_DIR"]).resolve()
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", PORT)) == 0:
            pytest.fail(f"port {PORT} is in use, and a stale server would grade the wrong code")

    # Its own process group, because cargo lambda watch spawns the function as a child.
    server = subprocess.Popen(["cargo", "lambda", "watch"], cwd=app_dir, start_new_session=True)
    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{PORT}", timeout=STARTUP_SECONDS) as client:
            _wait_until_serving(client, server)
            yield client
    finally:
        _stop(server)
