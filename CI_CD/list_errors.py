#!/usr/bin/env python3

# ... (keep the existing imports and function definitions) ...

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