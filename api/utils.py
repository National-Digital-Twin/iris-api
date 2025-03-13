pass_through_headers = [
    "x-amzn-oidc-data",
    "x-amzn-oidc-accesstoken",
    "x-amzn-oidc-identity",
    "Authorization",
    "x-auth-request-access-token",
]


def get_headers(headers):
    forward_headers = {}
    for header in pass_through_headers:
        hv = headers.get(header)
        if hv is not None:
            forward_headers[header] = hv
    return forward_headers
