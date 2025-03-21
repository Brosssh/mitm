import gzip
import io
from mitmproxy import http, ctx
from patches.signature_spoof import *

def request(flow: http.HTTPFlow) -> None:
    if 'clienttoken' in flow.request.url:
        signature_spoof(flow)

def response(flow: http.HTTPFlow) -> None:
    if "start-trial" in flow.request.pretty_url:

        try:
            buf = io.BytesIO(flow.response.content)
            with gzip.GzipFile(fileobj=buf, mode="rb") as f:
                decoded_content = f.read()

            decoded_content = decoded_content.decode("utf-8").replace("NOT_STARTED", "STARTED").encode("utf-8")
            
            modified_buf = io.BytesIO()
            with gzip.GzipFile(fileobj=modified_buf, mode="wb") as f:
                f.write(decoded_content)

            flow.response.content = modified_buf.getvalue()


            del flow.response.headers["Content-Length"]
            
            print(f"Modified and re-encoded response.")
        except Exception as e:
            print(f"Error decoding or modifying gzip content: {e}")
        print(f"Modified Response Status: {flow.response.status_code}")

