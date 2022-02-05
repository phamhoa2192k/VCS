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


def get_cookie_string(res):
	cookie = ""
	start = re.search("Set-Cookie: wordpress_.*path=/wp-content/plugins; HttpOnly", res).start() + 12
	end = re.search("Set-Cookie: wordpress_.*path=/wp-content/plugins; HttpOnly", res).end() - 36
	cookie += res[start:end] + "; "
	start = re.search("Set-Cookie: wordpress_logged_in.*path=/; HttpOnly", res).start() + 12
	end = re.search("Set-Cookie: wordpress_logged_in.*path=/; HttpOnly", res).end() - 18
	cookie += res[start:end]
	return cookie

def get_file(file_url, cookie, ip, port = 80):
	method = "GET"
	uri = file_url
	header = { "Host" : ip, "Cookie": cookie }
	res = send(create_http_request(method, uri, header, ""),10000, ip)
	if "HTTP/1.1 200 OK" in res :
		body = res[(res.rfind("\r\n\r\n") + 4):]
		print(body)
		print("Do lon file la: ", len(body) , " bytes")
	else:
		"File khong ton tai"
		
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
	get_file(file_url, cookie, ip)
		
if __name__ == "__main__":
	main()
