protoc:
	cd 9.0.26.632 && protoc --python_out=. proto/spotify.proto 

intercept:
	mitmweb -s 9.0.26.632/main.py 