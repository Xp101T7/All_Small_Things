#!/usr/bin/env python3

#!/usr/bin/env python3

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import datetime
from typing import Any, Mapping, Optional, Sequence, Tuple

from google.auth.transport import requests

from common import chronicle_auth
from common import datetime_converter
from common import regions

CHRONICLE_API_BASE_URL = "https://backstory.googleapis.com"

def list_errors(
    http_session: requests.AuthorizedSession,
    error_category: str = "",
    error_start_time: Optional[datetime.datetime] = None,
    error_end_time: Optional[datetime.datetime] = None,
    version_id: str = "",
    page_size: int = 0,
    page_token: str = "") -> Tuple[Sequence[Mapping[str, Any]], str]:
    """Lists errors.

    Args:
      http_session: Authorized session for HTTP requests.
      error_category: A string that filters which errors are returned by their
        ErrorCategory (i.e. 'RULES_EXECUTION_ERROR')
        (default = no filter on error category).
      error_start_time: The time to start listing errors from, inclusive
      (default = no min error_start_time).
      error_end_time: The time to end listing errors to, exclusive (default = no
        max error_end_time).
      version_id: Unique ID of the detection rule to retrieve errors for
        ("ru_<UUID>" or "ru_<UUID>@v_<seconds>_<nanoseconds>"). If a version
        suffix isn't specified, we list errors for all versions of that rule.
      page_size: Maximum number of errors to return.
        Must be non-negative, and is capped at a server-side limit of 1000
        (default = server-side default of 100)
      page_token: Page token from a previous ListErrors call used for pagination.
        If not specified, the first page is returned.

    Returns:
      List of errors and a page token for the next page of errors, if there are
      any.

    Raises:
      requests.exceptions.HTTPError: HTTP request resulted in an error
        (response.status_code >= 400).
    """
    url = f"{CHRONICLE_API_BASE_URL}/v2/health/errors"
    params_list = [("category", error_category),
                   ("start_time", datetime_converter.strftime(error_start_time)),
                   ("end_time", datetime_converter.strftime(error_end_time)),
                   ("rule_filter.version_id", version_id),
                   ("page_size", page_size), ("page_token", page_token)]
    params = {k: v for k, v in params_list if v}

    response = http_session.request("GET", url, params=params)

    if response.status_code >= 400:
        print(response.text)
    response.raise_for_status()
    j = response.json()
    return j.get("errors", []), j.get("nextPageToken", "")

def format_error(error):
    """Format a single error for display."""
    return f"""
Error ID: {error.get('errorId', 'N/A')}
Category: {error.get('category', 'N/A')}
Error Time: {error.get('errorTime', 'N/A')}
Error Message: {error.get('text', 'N/A')}
Rule Execution:
  Rule ID: {error.get('ruleExecution', {}).get('ruleId', 'N/A')}
  Version ID: {error.get('ruleExecution', {}).get('versionId', 'N/A')}
  Window Start Time: {error.get('ruleExecution', {}).get('windowStartTime', 'N/A')}
  Window End Time: {error.get('ruleExecution', {}).get('windowEndTime', 'N/A')}
"""

def display_errors(errors):
    """Display formatted errors."""
    if not errors:
        print("No errors found.")
    else:
        for i, error in enumerate(errors, 1):
            print(f"Error {i}:")
            print(format_error(error))
            print("-" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    chronicle_auth.add_argument_credentials_file(parser)
    regions.add_argument_region(parser)
    parser.add_argument(
        "-ec",
        "--error_category",
        type=str,
        required=False,
        help="error category (i.e. 'RULES_EXECUTION_ERROR')")
    parser.add_argument(
        "-est",
        "--error_start_time",
        type=datetime_converter.iso8601_datetime_utc,
        required=False,
        help="error start time in UTC ('yyyy-mm-ddThh:mm:ssZ')")
    parser.add_argument(
        "-eet",
        "--error_end_time",
        type=datetime_converter.iso8601_datetime_utc,
        required=False,
        help="error end time in UTC ('yyyy-mm-ddThh:mm:ssZ')")
    parser.add_argument(
        "-vi",
        "--version_id",
        type=str,
        required=False,
        help="version ID of the detection rule to list errors for ('ru_<UUID>[@v_<seconds>_<nanoseconds>]')"
    )
    parser.add_argument(
        "-s",
        "--page_size",
        type=int,
        required=False,
        help="maximum number of errors to return")
    parser.add_argument(
        "-t",
        "--page_token",
        type=str,
        required=False,
        help="page token from a previous ListErrors call used for pagination")

    args = parser.parse_args()
    CHRONICLE_API_BASE_URL = regions.url(CHRONICLE_API_BASE_URL, args.region)
    session = chronicle_auth.initialize_http_session(args.credentials_file)
    
    errors, next_page_token = list_errors(session, args.error_category,
                                          args.error_start_time,
                                          args.error_end_time, args.version_id,
                                          args.page_size, args.page_token)
    
    display_errors(errors)
    print(f"Next page token: {next_page_token}")