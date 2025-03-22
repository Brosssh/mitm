import gzip
import json
from mitmproxy import ctx, http
from proto.spotify_pb2 import ClientTokenRequest
import blackboxprotobuf

def spoof_trial(flow: http.HTTPFlow):
        ctx.log.info("bootstrap called")
        ctx.log.info(type(flow.response.content ))

        patches = [("pr:free,tc:0", "pr:premium,tc:0,rt:v2_BR_default_payg-new-family-sub-12m-12m_0_BRL_default"),
           ('"1":"ads","2":{"2":1,"6":1}}', '"1":"ads","2":{"2":0,"6":1}}'),
           ('{"1":"type","2":{"4":"free","6":1}}', '{"1":"type","2":{"4":"premium","6":1}}'),
           ('{"1":"player-license","2":{"4":"mft","6":1}}', '{"1":"player-license","2":{"4":"premium","6":1}}'),
           ('"Spotify Free"', '"Spotify Premium"')]
        
        message, typedef = blackboxprotobuf.protobuf_to_json(flow.response.content)

        message_json = json.loads(message)

        message = json.dumps(message_json, separators=(',', ':'))
        
        for patch in patches:
                found = message.find(patch[0])
                if found == -1:
                        ctx.log.error(f"Patch {patch[0]} not found")
                        continue
                message = message.replace(patch[0], patch[1])
                ctx.log.info(f"Patch {patch[0]} ok")

        edited = blackboxprotobuf.protobuf_from_json(message, typedef)

        flow.response.content = edited