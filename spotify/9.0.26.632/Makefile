protoc:
	protoc --python_out=. proto/spotify.proto 

intercept:
	mitmproxy -s main.py -s bbpb.py 

intercept-web:
	mitmweb -s main.py -s bbpb.py 