import gzip
import io
from mitmproxy import http, ctx
from patches.signature_spoof import *
from patches.spoof_trial import *


def request(flow: http.HTTPFlow) -> None:
    if 'clienttoken' in flow.request.url:
        signature_spoof(flow)

def response(flow: http.HTTPFlow) -> None:

    if "bootstrap" in flow.request.pretty_url:
        spoof_trial(flow)