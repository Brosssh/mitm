import gzip
import io
from mitmproxy import http, ctx
from patches.signature_spoof import *
from patches.spoof_trial import *
from patches.misc import *


def request(flow: http.HTTPFlow) -> None:
    if 'clienttoken' in flow.request.url:
        signature_spoof(flow)

def response(flow: http.HTTPFlow) -> None:

    #if "bootstrap" in flow.request.pretty_url or "user-customization-servi" in flow.request.pretty_url:
    #    spoof_trial(flow)

    if "eager" in flow.request.pretty_url:
        remove_front_ads(flow)