from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO
import yt_dlp
import os
import json
from threading import Thread
import time
from queue import Queue

app = Flask(__name__)
socketio = SocketIO(app)
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

def progress_hooks(d):
    if d['status'] == 'downloading':
        socketio.emit('status', {
            'url': d['info_dict']['original_url'],
            'progress': d['_percent_str'],
            'speed': d['_speed_str'],
            'eta': d['_eta_str'],
        })

def download_worker():
    while True:
        item = download_queue.get()
        if item is None:
            break
        
        url = item['url']
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hooks],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            queue_data = load_queue()
            queue_data = [q_item for q_item in queue_data if q_item['url'] != url]
            save_queue(queue_data)
            socketio.emit('download_complete', {'url': url})
            
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
            socketio.emit('download_error', {'url': url, 'error': str(e)})
        
        download_queue.task_done()

download_thread = Thread(target=download_worker, daemon=True)
download_thread.start()

@app.route('/')
def index():
    queue_data = load_queue()
    return render_template('index.html', queue=queue_data)

def get_video_info(url):
    ydl_opts = {'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', 'N/A'),
            'thumbnail': info.get('thumbnail', 'N/A'),
        }

@app.route('/add', methods=['POST'])
def add_to_queue():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    queue_data = load_queue()
    if not any(item['url'] == url for item in queue_data):
        try:
            info = get_video_info(url)
            queue_item = {
                'url': url,
                'added': time.time(),
                'title': info['title'],
                'thumbnail': info['thumbnail']
            }
            queue_data.append(queue_item)
            save_queue(queue_data)
            download_queue.put(queue_item)
        except Exception as e:
            return jsonify({'error': f'Could not get video info: {str(e)}'}), 500
    
    return jsonify({'status': 'success'})

@app.route('/status')
def get_status():
    return jsonify(load_queue())

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    socketio.run(app, host='0.0.0.0', port=5000)
