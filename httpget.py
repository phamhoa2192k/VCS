import socket, sys

ENCODE = "utf8"

def get_title(response):
	response = response.decode(ENCODE)
	if("<title>" not in response):
		return "Khong co tieu de cho trang web."
	else:
		begin = response.find("<title>") + 7
		end = response.find("</title>")
		return response[begin:end]
		
def create_http_request(method, header, body):
	http_request = method + " / HTTP/1.1\r\n"
	for key in header:
		http_request += key + ": " + header[key] + "\r\n"
	http_request += body + "\r\n"
	return bytes(http_request,ENCODE)
	
def send_get_request(ip, port = 80):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port));
	get_request = create_http_request("GET", {"Host": ip} , "")  
	s.sendall(get_request)
	res = s.recv(2048)
	title = get_title(res)
	print("Tieu de la: ", title)

def main():
	if sys.argv[1] != "--url":
		print("Khong co tham so ", sys.argv[1], ". Co phai y ban la --url.")
		return 1
	ip = sys.argv[2]
	send_get_request(ip)
	
if __name__ == "__main__":
	main()
