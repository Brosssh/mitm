import json
import blackboxprotobuf
from mitmproxy import ctx, http


def remove_front_ads(flow: http.HTTPFlow):
        message, typedef = blackboxprotobuf.protobuf_to_json(flow.response.content)

        message_json = json.loads(message)
        #ctx.log.info(type(message_json))
        #ctx.log.info(message_json["1"]["1"][1])
        del message_json["1"]["1"][1]

        message = json.dumps(message_json)
        
        flow.response.content = blackboxprotobuf.protobuf_from_json(message, typedef)

def change_permission(flow: http.HTTPFlow):
        message, typedef = blackboxprotobuf.protobuf_to_json(flow.response.content)

        message_json = json.loads(message)
        ctx.log.info(type(message_json))
        ctx.log.info(message_json)
        if "1" in message_json:
            message_json["1"] = "default"
        message = json.dumps(message_json)
        
        flow.response.content = blackboxprotobuf.protobuf_from_json(message, typedef)