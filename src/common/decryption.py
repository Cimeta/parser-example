import logging
import os
from subprocess import Popen, PIPE

_log = logging.getLogger(__name__)


def get_encrypted_value(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise ValueError(f'Value for {key} has not been found')
    command = (f"powershell.exe $pwd = ConvertTo-SecureString {value} ; "
               f"$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pwd) ; "
               f"[System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)")
    try:
        stdout = Popen(command, stdout=PIPE, stderr=PIPE)
    except FileNotFoundError:
        return value
    output, err = stdout.communicate()
    if err:
        decoded_err = err.decode("utf-8")
        if "Input string was not in a correct format" in decoded_err:
            return value
        raise ValueError(decoded_err)
    unencrypted_value = output.decode("utf-8").strip()
    return unencrypted_value


def main():
    import argparse
    from common import setup_logger

    parser = argparse.ArgumentParser(
        description="Check decrypt function."
    )

    parser.add_argument(
        "variable",
        help="Environment variable name.",
    )
    args = parser.parse_args()
    setup_logger(level="DEBUG")

    _log.debug(get_encrypted_value(key=args.variable))


if __name__ == "__main__":
    main()
