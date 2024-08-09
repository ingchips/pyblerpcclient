# RPC Client for Python

Python version >= 3.10, no additional requirements.

## Install

To install in editable mode:

```shell
python -m pip install -e .
```

## Run Examples

1. A simple Python REPL:

    ```shell
    python examples/shell.py
    ```

1. Central Role:

    ```shell
    python examples/thermo_client.py
    ```

1. PTS Automation:

    [PTS](https://www.bluetooth.com/develop-with-bluetooth/qualify/qualification-test-tools/profile-tuning-suite/)
    & 32-bit Python is required to run this demo.

    Use `pip` to install additional packages: `codecs`, `lxml`.

    ```shell
    python examples/pts_gap.py
    ```

1. PTS Automation with custom Implicit Send DLL:

    Download and activate custom [Implicit Send DLL](https://github.com/ingchips/pts_implicit_send_over_tcp) in the workspace.
    Start server:

    ```shell
    python examples/implicitsend_test.py
    ```

    Run the supported cases in PTS.