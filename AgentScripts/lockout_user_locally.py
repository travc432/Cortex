"""
Name: lockout_user_locally.py
Description: This script is intended to lock out a provided username locally.
Author: Travis Crotteau
Date: 20240514
"""

import os
import subprocess
import sys
import traceback
import psutil


def lockout_user_locally(user_list):
    result = {}
    for user in user_list:
        if psutil.WINDOWS:
            try:
                env = os.environ
                sys.stdout.write(f"Attempting lock out {user}.\n")
                subprocess.run(f"net user {user} / active: no", shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=env)
            except Exception:
                sys.stderr.write(f"Failed to lock out {user}, error: {traceback.format_exc()}\n")

        if psutil.MACOS:
            try:
                # Attempt to disable the user
                env = os.environ
                sys.stdout.write(f"Attempting to disable {user}.\n")
                user_disablement = subprocess.run(f"pwpolicy -u {user} disableuser", shell=True, stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE, env=env)
                disablement_check = subprocess.run(f"pwpolicy -u {user} getaccountpolicies", shell=True,
                                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
                if "not found" in user_disablement.stderr.decode():
                    raise ValueError(f"{user} was not found.\n")
                if "account is disabled" in disablement_check.stderr.decode():
                    sys.stdout.write(f"{user} disabled successfully.")
            except Exception:
                sys.stderr.write(f"Failed to lock out {user}, error: {traceback.format_exc()}\n")

    return result
