import gzip
import io
from mitmproxy import http, ctx
from patches.signature_spoof import *
from patches.premium_spoof import *
from patches.misc import *


def request(flow: http.HTTPFlow) -> None:
    if 'clienttoken' in flow.request.url:
        signature_spoof(flow)

    if "artistview/v1/artist" in flow.request.pretty_url:
        flow.request.url = flow.request.url + "&trackRows=true"
        
    if "user-customization-servi" in flow.request.pretty_url:
        del flow.request.headers["if-none-match"]

def response(flow: http.HTTPFlow) -> None:
    if "user-customization-servi" in flow.request.pretty_url:
        spoof_premium(flow)