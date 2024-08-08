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