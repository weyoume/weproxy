# -*- coding: utf-8 -*-

import ujson

import pytest

parse_error = {
    'id': 1,
    'jsonrpc': '2.0',
    'error': {
        'code': -32700,
        'message':
            'Parse error'
    }
}

invalid_request_error = {
    'id': 1,
    'jsonrpc': '2.0',
    'error': {
        'code': -32600,
        'message':
            'Invalid Request',
        'data': {
            'request': None
        }
    }
}

server_error = {
    'id': 1,
    'jsonrpc': '2.0',
    'error': {
        'code': -32000,
        'message':
            'Server error'
    }
}


@pytest.mark.timeout(10)
@pytest.mark.parametrize('jrpc_request, expected',[
        # single jsonrpc steemd request
    (dict(id=1, method='get_block', params=[1000]),invalid_request_error),
    ])
def test_validate_jsonrpc_request_middleware(app_without_ws, jrpc_request, expected):
    app = app_without_ws
    _, response = app.test_client.post(
        '/', json=jrpc_request, server_kwargs=dict(workers=1))
    assert response.status == 200
    assert response.headers['Content-Type'] == 'application/json'
    json_response = ujson.loads(response.body.decode())
    assert 'error_id' in json_response['error']['data']
    del json_response['error']['data']['error_id']
    assert json_response == expected