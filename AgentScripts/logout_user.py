"""
Name: logout_user.py
Description: This is intended to log a provided username out of the device.
Author: Travis Crotteau
Date: 20240514
"""

import os
import subprocess
import sys
import traceback
import psutil


def logoff_user(user_list):
    result = {}
    for user in user_list:
        if psutil.WINDOWS:
            sys.stdout.write(f"Looking for {user}'s session ID.\n")

            try:
                env = os.environ
                # Identify the user's active session
                process_output = subprocess.run(
                    "powershell.exe -command \"((quser | Where-Object "f"{{ $_ -match \'{user}\'}}\") -split \' +\')[2]",
                    shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, env=env
                )
                session_id = process_output.stdout.decode().strip()

                if bool(session_id):
                    # Use session ID to run logoff command
                    sys.stdout.write(f"Session ID identified as \"{session_id}\". Logging {user} off.\n")
                    subprocess.run(f"logoff {session_id}")

                    # Check for remaining sessions
                    remaining_sessions = subprocess.run(
                        "powershell.exe -command quser", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    if "Active" in remaining_sessions.stdout.decode():
                        sys.stdout.write(
                            f"There are active sessions remaining.\n {remaining_sessions.stdout.decode().strip()}")
                    else:
                        sys.stdout.write("No other active sessions found.\n")

                else:
                    sys.stdout.write(f"No active sessions found for {user}.\n")

            except Exception:
                sys.stderr.write(f"Failed to log {user} off, error: {traceback.format_exc()}\n")

        if psutil.MACOS:
            try:
                env = os.environ
                # Run command to log user out.
                subprocess.run(
                    f"sudo launchctl bootout user/$(id -u {user})",
                    shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, env=env
                )

            except Exception:
                sys.stderr.write(f"No active session found for {user} or error logging off, {traceback.format_exc()}\n")

    return result






