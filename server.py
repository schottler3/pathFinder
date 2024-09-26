from flask import Flask, send_file, render_template, abort
import os

app = Flask(__name__)

max_id = 10000

@app.route("/image/<int:id>", methods=['GET'])
def getImage(id):
    if not isinstance(id,int) or id < 0 or id > max_id:
        abort(404, description="Image not found")

    log = open("traffic.log", "a")
    ip = request.remote_addr

    log.write(f"{ip} requested for image {id}\n")
    log.close()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, 'images', f'{id}.jpg')
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpg')
    else:
        abort(404, description="Image not found")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1471)