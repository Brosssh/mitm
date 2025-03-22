import gzip
import json
from mitmproxy import ctx, http
from proto.spotify_pb2 import ClientTokenRequest
import blackboxprotobuf



def spoof_trial(flow: http.HTTPFlow):
        ctx.log.info("bootstrap called")
        ctx.log.info(type(flow.response.content ))

        patches = [('{"1":"showcase-android"', '{"1":"on-demand-trial","2":{"4":"active","6":1}},{"1":"showcase-android"'),
                    ('"1":"ads","2":{"2":1,"6":1}}', '"1":"ads","2":{"2":0,"6":1}}'),
                    ('"1":"on-demand","2":{"2":0,"6":1}}', '"1":"on-demand","2":{"2":1,"6":1}}'),
                    ('"1":"on-demand-trial-in-progress","2":{"2":0,"6":1}}', '"1":"on-demand-trial-in-progress","2":{"2":1,"6":1}}'),
                    ("pr:free,tc:0", "pr:free,tc:0,rt:v2_IT_trial-consecutive-activity-started_trial-14d-14d_0_EUR_default"),
                    ('{"1":"streaming-rules","2":{"4":"shuffle-mode","6":1}}', '{"1":"streaming-rules","2":{"4":"shuffle-mode","6":1}}'),
                    ('{"1":"player-license","2":{"4":"mft","6":1}}', '{"1":"player-license","2":{"4":"premium","6":1}}'),
                    ('"Spotify Free"', '"Spotify Premium"')
                    ]
        
        message, typedef = blackboxprotobuf.protobuf_to_json(flow.response.content)

        with open("dump_bootstrap_alt", "r") as f:
            message = f.read()
        
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