def assert_status_code(actual_status_code, expected_status_code=200):
    assert actual_status_code == expected_status_code, f"Bad Status code. " \
                                                       f"Expected: {expected_status_code}, " \
                                                       f"Actual: {actual_status_code}."
