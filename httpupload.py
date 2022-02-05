import socket, sys, re, os, base64

ENCODING = "utf8"

def send(content, length, ip, port = 80):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port));
	s.sendall(content)
	data = bytearray()
	while True: 
		chunk = s.recv(10000)
		if not chunk: 
			break
		data += chunk
	return data.decode(ENCODING)
	
def create_http_request(method, uri, header, body):
	http_request = method + " /" + uri + " HTTP/1.1\r\n"
	for key in header:
		http_request += key + ": " + str(header[key]) + "\r\n"
	if body != "":
		http_request += "\r\n" + body
	http_request += "\r\n"
	return bytes(http_request, ENCODING)

def create_login_request(username, password, ip, port = 80):
	body = "log=" + username + "&pwd=" + password
	method = "POST"
	uri = "wp-login.php"
	header = { "Host" : ip, "Content-Length" : len(body), "Content-Type" : "application/x-www-form-urlencoded" , "Cookie" :  "wordpress_test_cookie=WP%20Cookie%20check; wp_lang=en_US" }
	return create_http_request(method, uri, header , body)  

def create_media_new_request(cookie, ip, port = 80):
	body = ""
	method = "GET"
	uri = "wp-admin/media-new.php"
	header = { "Host" : ip, "Cookie" : cookie }
	return create_http_request(method, uri, header, body)
	
def get_wpnonce(res):
	start = re.search("name=\"_wpnonce\"", res).end() + 8
	end = start + 10
	return res[start:end]
	
def get_cookie_string(res):
	cookie = ""
	start = re.search("Set-Cookie: wordpress_.*path=/wp-content/plugins; HttpOnly", res).start() + 12
	end = re.search("Set-Cookie: wordpress_.*path=/wp-content/plugins; HttpOnly", res).end() - 36
	cookie += res[start:end] + "; "
	start = re.search("Set-Cookie: wordpress_logged_in.*path=/; HttpOnly", res).start() + 12
	end = re.search("Set-Cookie: wordpress_logged_in.*path=/; HttpOnly", res).end() - 18
	cookie += res[start:end]
	return cookie

def create_upload_request(ip, cookie, nonce, file_url):
	method = "POST"
	uri = "wp-admin/async-upload.php"
	webkit = "WebKitFormBoundaryN9HAMhjnBp3mLawm"
	webkit_body = "------" + webkit
	webkit_header = "----" + webkit
	#file_type = "image/jpeg"
	file_type = "text/plain"
	f = open(file_url , "r")
	file_name = os.path.basename(file_url)
	body = '{webkit}\r\nContent-Disposition: form-data; name="name"\r\n\r\n{file_name}\r\n{webkit}Content-Disposition: form-data; name="post_id"\r\n\r\n0\r\n{webkit}\r\nContent-Disposition: form-data; name="_wpnonce"\r\n\r\n{nonce}\r\n{webkit}\r\nContent-Disposition: form-data; name="type"\r\n\r\n{webkit}\r\nContent-Disposition: form-data; name="tab"\r\n\r\n{webkit}Content-Disposition: form-data; name="short"\r\n\r\n1\r\n{webkit}\r\nContent-Disposition: form-data; name="async-upload"; filename="{file_name}"\r\nContent-Type: {file_type}\r\n\r\n{binary}\r\n\r\n{webkit}--'
	body = body.format(webkit = webkit_body, file_name = file_name, binary = f.read(), nonce = nonce, file_type = file_type)
	header = {"Host": ip, "Content-Length": len(body),"Content-Type": "multipart/form-data; boundary=" + webkit_header, "Cookie": cookie  }
	req = create_http_request(method, uri, header, body)
	return req

def check_upload_res(res):
	if "HTTP/1.1 200 OK" in res:
		print("Upload thanh cong")
		file_id = res[res.rfind("\r\n") + 1:].replace("\n","").replace("\r","")
		return int(file_id)
	else: 
		print("Upload that bai")
		return -1

def get_path_in_server(ip, cookie, file_id):
	method = "POST"
	body = "attachment_id=" + str(file_id) + "&fetch=3"
	uri = "wp-admin/async-upload.php"
	header = { "Host" : ip, "Content-Length" : len(body), "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Cookie": cookie }
	res = send(create_http_request(method, uri, header, body), 10000, ip)
	start = res.find("data-clipboard-text=") + 21
	for i in range(len(res)):
		if i > start and res[i] == '"':
			print(res[start:i])
			break
	
def main():
	ip, username, password, file_url = None, None, None, None
	for i in range(len(sys.argv)):
		if sys.argv[i] == "--url":
			ip = sys.argv[i+1]
		if sys.argv[i] == "--username":
			username = sys.argv[i+1]
		if sys.argv[i] == "--password":
			password = sys.argv[i+1]
		if sys.argv[i] == "--file":
			file_url = sys.argv[i+1]
	log_req = create_login_request(username, password, ip)
	cookie = get_cookie_string(send(log_req, 5000, ip))
	media_new_req = create_media_new_request(cookie, ip)
	nonce = get_wpnonce(send(media_new_req, 30000, ip))
	res = send(create_upload_request(ip, cookie, nonce, file_url), 10000, ip)
	if(check_upload_res(res) > 0):
		get_path_in_server(ip, cookie, check_upload_res(res))
		
if __name__ == "__main__":
	main()
