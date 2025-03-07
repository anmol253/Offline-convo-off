import requests
import json
import time
import threading
import http.server
import socketserver

# ========== SERVER CONFIGURATION ==========
HOST = "0.0.0.0"  # ✅ Host Address
PORT = 10000  # ✅ Port Number

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"-- SERVER RUNNING>>RAJ H3R3")

def execute_server():
    with socketserver.TCPServer((HOST, PORT), MyHandler) as httpd:
        print(f"\n🚀 Server Running at http://{HOST}:{PORT} 🚀\n")  # ✅ Host & Port Printed
        httpd.serve_forever()

# ========== LOAD FILE DATA ==========
def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] '{filename}' फाइल नहीं मिली!")
        return []

# ========== AUTO COMMENT FUNCTION ==========
def auto_comment():
    tokens_list = load_file('tokennum.txt')  
    posts_list = load_file('convo.txt')  
    comments_list = load_file('hatersname.txt')  
    time_list = load_file('time.txt')  

    if not tokens_list or not posts_list or not comments_list or not time_list:
        print("[ERROR] Tokens, Posts, Comments या Time फाइल खाली है!")
        return

    comment_index = 0
    time_interval = int(time_list[0])  

    while True:
        for token in tokens_list:
            if comment_index >= len(comments_list):
                comment_index = 0  

            comment_text = comments_list[comment_index]

            for post_id in posts_list:
                url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
                headers = {"Authorization": f"Bearer {token}"}
                payload = {"message": comment_text}

                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    print(f"[SUCCESS] पोस्ट {post_id} पर कमेंट किया: {comment_text}")
                else:
                    print(f"[FAILED] पोस्ट {post_id} पर कमेंट नहीं हो सका, स्टेटस कोड: {response.status_code}")

                time.sleep(time_interval)  

            comment_index += 1

# ========== RUN SCRIPT ==========
def main():
    print(f"🔹 Server Starting at {HOST}:{PORT}...")  # ✅ Host & Port Printed Before Server Starts
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()
    auto_comment()

if __name__ == "__main__":
    main()
