protoc:
	protoc --python_out=. proto/spotify.proto 

intercept:
	mitmproxy -s main.py 

intercept-web:
	mitmweb -s main.py 

bb:
	mitmproxy -s bbpb.py 

bb-web:
	mitmweb -s bbpb.py 

test:
	python patches/unlock_trial/test.py