import pytest


@pytest.mark.requests
class TestRequestsSuite(object):

    @pytest.mark.tba_requests
    @pytest.mark.tcid4
    def test_create_tba_request(self, app):
        source_name = app.config['tba_request']['source_name']
        endpoint = app.config['tba_request']['endpoint']
        request_type = app.config['tba_request']['subject']
        request_id = app.requests_actions.create_request(source_name, endpoint, role="user")
        app.requests_actions.verify_new_request(request_id, request_type)

    @pytest.mark.tbu_requests
    @pytest.mark.tcid5
    def test_create_tbu_request(self, app):
        source_name = app.config['tbu_request']['source_name']
        endpoint = app.config['tbu_request']['endpoint']
        request_type = app.config['tbu_request']['subject']
        request_id = app.requests_actions.create_request(source_name, endpoint, role="admin")
        app.requests_actions.verify_new_request(request_id, request_type)

    @pytest.mark.owt_requests
    @pytest.mark.tcid6
    def test_create_owt_request(self, app):
        source_name = app.config['owt_request']['source_name']
        endpoint = app.config['owt_request']['endpoint']
        request_type = app.config['owt_request']['subject']
        request_id = app.requests_actions.create_request(source_name, endpoint, role="admin")
        app.requests_actions.verify_new_request(request_id, request_type)

    @pytest.mark.ca_requests
    @pytest.mark.tcid7
    def test_create_ca_request(self, app):
        source_name = app.config['ca_request']['source_name']
        endpoint = app.config['ca_request']['endpoint']
        request_type = app.config['ca_request']['subject']
        request_id = app.requests_actions.create_request(source_name, endpoint, role="admin")
        app.requests_actions.verify_new_request(request_id, request_type)

    @pytest.mark.tba_requests
    @pytest.mark.tcid8
    def test_update_request_rate(self, app):
        source_name = app.config['tba_request']['source_name']
        endpoint = app.config['tba_request']['endpoint']
        request_id = app.requests_actions.create_request(source_name, endpoint, role="user")
        source_name = app.config['update_rate']['source_name']
        endpoint = app.config['update_rate']['endpoint']
        request_id = app.requests_actions.update_conversion_rate(source_name, endpoint, request_id)
        rate = app.config['update_rate']['rate']
        app.requests_actions.verify_request_rate_update(request_id, rate)

    @pytest.mark.tba_requests
    @pytest.mark.tcid9
    def test_execute_tba_request(self, app):
        source_name = app.config['tba_request']['source_name']
        endpoint = app.config['tba_request']['endpoint']
        request_id = app.requests_actions.create_request(source_name, endpoint, role="user")
        app.requests_actions.execute_request(request_id)
        app.requests_actions.verify_request_status(request_id, status="executed")

    @pytest.mark.tba_requests
    @pytest.mark.tcid10
    def test_cancel_tba_request(self, app):
        source_name = app.config['tba_request']['source_name']
        endpoint = app.config['tba_request']['endpoint']
        request_id = app.requests_actions.create_request(source_name, endpoint, role="user")
        app.requests_actions.cancel_request(request_id)
        app.requests_actions.verify_request_status(request_id, status="cancelled")
