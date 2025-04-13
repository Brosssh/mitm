import json
from mitmproxy import ctx, http
import blackboxprotobuf

patches = [
    ('"1":"nft-disabled","2":{"4":"0","6":1}', '"1":"nft-disabled","2":{"4":"1","6":1}'),
    ('"1":"pick-and-shuffle","2":{"2":1,"6":1}', '"1":"pick-and-shuffle","2":{"2":0,"6":1}'),
    ('"1":"shuffle","2":{"2":1,"6":1}', '"1":"shuffle","2":{"2":0,"6":1}'),
    ('"1":"on-demand","2":{"2":0,"6":1}', '"1":"on-demand","2":{"2":1,"6":1}'),
    ('"1":"player-license","2":{"4":"mft","6":1}', '"1":"player-license","2":{"4":"premium","6":1}'),
    ('"1":"streaming-rules","2":{"4":"shuffle-mode","6":1}', '"1":"streaming-rules","2":{"4":"","6":1}'),
    ('"1":"ads","2":{"2":1,"6":1}', '"1":"ads","2":{"2":0,"6":1}'),
    ('"1":"catalogue","2":{"4":"free",', '"1":"catalogue","2":{"4":"premium",'),
    ('"1":{"1":"android-playlist-creation-createplaylistmenuimpl","2":"create_button_position"},"2":{"1":333216,"2":"exp-planner","3":1224522},"5":{"1":"right"}',
    '"1":{"1":"android-playlist-creation-createplaylistmenuimpl","2":"create_button_position"},"2":{"1":333216,"2":"exp-planner","3":1224522},"5":{"1":"nowhere"}')
]

def spoof_premium(flow: http.HTTPFlow):
        ctx.log.info("bootstrap called")
        ctx.log.info(type(flow.response.content ))

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

        flow.response.content = blackboxprotobuf.protobuf_from_json(message, typedef)