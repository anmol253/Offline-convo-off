import requests
import json
import time
import threading
import http.server
import socketserver

# HTTP Server Class (for testing server running status)
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"-- SERVER RUNNING >> AUTO COMMENT BOT")

# Function to start HTTP Server
def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

# Function to read Tokens from file
def read_tokens():
    with open('tokens.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to read Comments from file
def read_comments():
    with open('comments.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to read Facebook Post URLs from file
def read_posts():
    with open('posts.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to Auto Comment on Facebook Posts
def auto_comment():
    tokens = read_tokens()
    comments = read_comments()
    posts = read_posts()

    if not tokens or not comments or not posts:
        print("[ERROR] Missing tokens, comments, or post URLs.")
        return

    while True:
        for post in posts:
            for token in tokens:
                comment = random.choice(comments)  # Pick a random comment
                url = f"https://graph.facebook.com/v17.0/{post}/comments"
                payload = {"message": comment, "access_token": token}

                response = requests.post(url, data=payload)
                result = response.json()

                if "id" in result:
                    print(f"[SUCCESS] Comment posted: {comment} on {post}")
                else:
                    print(f"[ERROR] Failed to post comment on {post}. Reason: {result}")

                time.sleep(30)  # Time interval between comments

# Function to start the main process
def main():
    # Start HTTP Server in a separate thread
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    # Start Facebook Auto Commenting
    auto_comment()

if __name__ == "__main__":
    main()
