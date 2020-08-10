from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import sys
import os
import random



# Leave HOSTNAME blank for localhost or not serving to WAN
HOSTNAME = ""

# Server port to host at; should be 8000+
SERVERPORT = 8000

# Page to use at the root URL "127.0.0.1:8000/"
#    Give the relative path to the index file from the location of this script
#    "index.html" assumes that the index page is located in the same directory as this script
INDEX_PAGE = "index.html"

# Full directory to your image directory including drive letter for Windows
#    Windows example:  "C:\Users\user_name\Pictures"
#    Linux example:    "/home/user_name/Pictures"
DIR = "/full/directory/to/images"

# List where the images will be collected to
catalog = []




class HTTPHandler(BaseHTTPRequestHandler):
		
	def do_GET(self):
		
		# Site root
		if self.path == "/":
			html_content = parseHTML(INDEX_PAGE)
			
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			
			self.wfile.write(html_content.encode("utf-8"))
		
		# AJAX image refresh	
		if self.path == "/get_image.html":
			image = random.choice(catalog)
			self.wfile.write(image.encode("utf-8"))
		
		# Image request
		if self.path.lower().endswith(".jpg") or self.path.lower().endswith(".png"):
			self.send_response(200)
			self.send_header("Content-type", "text/png")
			self.end_headers()
			
			f = open(DIR + "/" + self.path, "rb")
			self.wfile.write(f.read())
			f.close()



### Replaces instance of "{{ image }}" in html with the name of a random image from the collection
###    <img src="{{ image }}">
def parseHTML(page_to_parse):
	f = open(page_to_parse, "r")
	html_content = f.read()
	f.close()
	
	image_len = len("{{ image }}")
	end = len(html_content) - image_len
	index = 0
	while index < end:
		if html_content[index:(index + image_len)] == "{{ image }}":
			prefix = html_content[0:index]
			suffix = html_content[(index + image_len):]
			
			rand_img = random.choice(catalog)
			
			return prefix + rand_img + suffix
				
		index += 1
	
	return html_content



### Populates the list of images with PNG or JPG images
def catalogImages():
	catalog = []
	
	with os.scandir(DIR) as objects:
		for element in objects:
			if element.name[-4:].lower() == ".jpg" or element.name[-4:].lower() == ".png":
				catalog.append(element.name)
	
	return catalog



### Python main function to run when script is called ###
if __name__ == "__main__":
	catalog = catalogImages()
	
	web_server = HTTPServer((HOSTNAME, SERVERPORT), HTTPHandler)
	print("Server started http://%s:%s" % (HOSTNAME, SERVERPORT))

	try:
		web_server.serve_forever()
	except KeyboardInterrupt:
		pass
	
	web_server.server_close()
	print("Server stopped.")

