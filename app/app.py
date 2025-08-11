from flask import Flask, request, render_template, jsonify
import yt_dlp
import os
import json
from threading import Thread
import time
from queue import Queue

app = Flask(__name__)
download_queue = Queue()
QUEUE_FILE = '/queue/queue.json'
DOWNLOAD_DIR = '/downloads'

def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_queue(queue_data):
    os.makedirs(os.path.dirname(QUEUE_FILE), exist_ok=True)
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue_data, f)

def download_worker():
    while True:
        url = download_queue.get()
        if url is None:
            break
            
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            queue_data = load_queue()
            queue_data = [item for item in queue_data if item['url'] != url]
            save_queue(queue_data)
            
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
        
        download_queue.task_done()

download_thread = Thread(target=download_worker, daemon=True)
download_thread.start()

@app.route('/')
def index():
    queue_data = load_queue()
    return render_template('index.html', queue=queue_data)

@app.route('/add', methods=['POST'])
def add_to_queue():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    queue_data = load_queue()
    if not any(item['url'] == url for item in queue_data):
        queue_data.append({
            'url': url,
            'added': time.time()
        })
        save_queue(queue_data)
        download_queue.put(url)
    
    return jsonify({'status': 'success'})

@app.route('/status')
def get_status():
    return jsonify(load_queue())

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
