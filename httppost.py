import socket, sys

ENCODING = "utf8"

def create_http_request(method, uri, header, body):
	http_request = method + " /" + uri + " HTTP/1.1\r\n"
	for key in header:
		http_request += key + ": " + str(header[key]) + "\r\n"
	
	if body != "":
		http_request += "\r\n" + body
	http_request += "\r\n"
	return bytes(http_request, ENCODING)

def check_response(res):
	res = res.decode(ENCODING)
	if "Location: http://localhost/wp-admin" in res:
		print("Dang nhap thanh cong")
	else:
		print("Dang nhap that bai")

def send_post_request(ip, username, password, port = 80):
	body = "log=" + username + "&pwd=" + password
	method = "POST"
	uri = "wp-login.php"
	header = { "Host" : ip, "Content-Length" : len(body), "Content-Type" : "application/x-www-form-urlencoded" , "Cookie" :  "wordpress_test_cookie=WP%20Cookie%20check; wp_lang=en_US" }
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port));
	
	get_request = create_http_request(method, uri, header , body)  
	s.sendall(get_request)
	
	res = s.recv(4096)
	check_response(res)
	
def main():
	ip, username, password = None, None, None
	for i in range(len(sys.argv)):
		if sys.argv[i] == "--url":
			ip = sys.argv[i+1]
		if sys.argv[i] == "--username":
			username = sys.argv[i+1]
		if sys.argv[i] == "--password":
			password = sys.argv[i+1]
	send_post_request(ip, username, password)
	
if __name__ == "__main__":
	main()
