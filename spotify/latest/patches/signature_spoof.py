from mitmproxy import ctx, http
from proto.spotify_pb2 import ClientTokenRequest

def signature_spoof(flow: http.HTTPFlow):
        ctx.log.info("clienttoken called")
        outer_message = ClientTokenRequest()
        outer_message.ParseFromString(flow.request.content)
        ctx.log.info("Signature: "+ outer_message.field2.field3.field1.field1.field9)
        outer_message.field2.field3.field1.field1.field9 = outer_message.field2.field3.field1.field1.field9.replace('5d08264b44e0e53fbccc70b4f016474cc6c5ab5c', 'd6a6dced4a85f24204bf9505ccc1fce114cadb32')
        ctx.log.info(f"Modified Signature: {outer_message.field2.field3.field1.field1.field9}")
        modified_content = outer_message.SerializeToString()

        flow.request.content = modified_content