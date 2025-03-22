import json
import os
import blackboxprotobuf

with open('patches/unlock_trial/mitm_bootstrap', 'rb') as file:
    mitm_bootstrap = file.read()

patches = [("pr:free,tc:0", "pr:free,tc:0,rt:v2_IT_trial-consecutive-activity-started_trial-14d-14d_0_EUR_default"),
           ('"1":"ads","2":{"2":1,"6":1}}', '"1":"ads","2":{"2":0,"6":1}}'),
           ('{"1":"type","2":{"4":"free","6":1}}', '{"1":"type","2":{"4":"premium","6":1}}'),
           ('{"1":"player-license","2":{"4":"mft","6":1}}', '{"1":"player-license","2":{"4":"premium","6":1}}')]

message, typedef = blackboxprotobuf.protobuf_to_json(mitm_bootstrap)

message_json = json.loads(message)

message = json.dumps(message_json, separators=(',', ':'))

with open('data.json', 'w') as f:
    f.write(message)
    
message = message.replace("pr:free,tc:0", "pr:premium,tc:0")

print(message_json)

edited = blackboxprotobuf.protobuf_from_json(message, typedef)
# Print the decoded message for analysis (you may need to analyze the structure)
#print("Decoded Protobuf Message:", edited)