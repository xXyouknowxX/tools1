from mitmproxy import http
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

def request(flow: http.HTTPFlow) -> None:
    # If content needs to be decoded (like gzipped), decode it
    if flow.request.content:
        flow.request.decode()
        
    url = flow.request.url
    parsed_url = urlparse(url)
    params = parse_qsl(parsed_url.query)

    print("\nOriginal Params:")
    for k, v in params:
        print(f"{k}: {v}")

    # Request for user input to modify parameters
    for i, (key, value) in enumerate(params):
        new_value = input(f"Modify value for {key} (Current: {value}): ")
        if new_value:
            params[i] = (key, new_value)

    # Update the request with modified parameters
    new_query = urlencode(params)
    modified_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment)
    )
    flow.request.url = modified_url

    # If we've decoded the content earlier, encode it back
    if flow.request.content:
        flow.request.encode()

def response(flow: http.HTTPFlow) -> None:
    # If content needs to be decoded (like gzipped), decode it
    if flow.response.content:
        flow.response.decode()
    
    original_content = flow.response.content
    print("\nOriginal Response:")
    print(original_content.decode('utf-8', 'replace'))

    new_content = input("\nModify response content (Leave blank to keep original): ")
    if new_content:
        flow.response.content = new_content.encode('utf-8')

    # If we've decoded the content earlier, encode it back
    if flow.response.content:
        flow.response.encode()

addons = [
    # This will add our request and response functions to mitmproxy's event loop
    __name__
]
