import gzip
import io
from mitmproxy import http, ctx
from patches.signature_spoof import *
from patches.premium_spoof import *
from patches.misc import *


def request(flow: http.HTTPFlow) -> None:
    if 'clienttoken' in flow.request.url:
        signature_spoof(flow)

def response(flow: http.HTTPFlow) -> None:

    if "bootstrap" in flow.request.pretty_url or "user-customization-servi" in flow.request.pretty_url:
        spoof_premium(flow)

    if "eager" in flow.request.pretty_url:
        remove_front_ads(flow)
        
    #Does nothing    
    if "playlist-permission" in flow.request.pretty_url and "default-owner" not in flow.request.pretty_url:
        #change_permission(flow)
        pass