"""
Example safe plugin.

Lifecycle:
- --setup     : safe, no sandbox required
- --run       : requires MERCURY_SAFE=1
- --cleanup   : safe, no sandbox required

This design matches Mercury CI expectations.
"""

import os
import sys
import socket
import argparse


def demo_local_connect(host="127.0.0.1", port=9001):
    """Attempt a local-only connection as a safe demo."""
    try:
        s = socket.create_connection((host, port), timeout=1)
        with s:
            s.sendall(b"hello from example_simulator\n")
            resp = s.recv(1024)
            print("[example_simulator] received:", resp.decode(errors="ignore").strip())
    except Exception as e:
        print("[example_simulator] local connect failed (expected):", e)


def setup():
    print("[example_simulator] setup (no-op)")
    return 0


def run():
    if os.environ.get("MERCURY_SAFE") != "1":
        print(
            "[example_simulator] must be run via Mercury sandbox "
            "(set MERCURY_SAFE=1)"
        )
        return 1

    print("[example_simulator] running safe example plugin")

    try:
        from mercury.simulated_device import SimulatedDevice
        d = SimulatedDevice()
        print(d.device_info())
    except Exception:
        print("[example_simulator] no simulated device available")

    demo_local_connect()
    return 0


def cleanup():
    print("[example_simulator] cleanup (no-op)")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Example Simulator (educational, safe plugin)"
    )
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--cleanup", action="store_true")

    args = parser.parse_args()

    if args.setup:
        return setup()
    if args.cleanup:
        return cleanup()
    if args.run:
        return run()

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
