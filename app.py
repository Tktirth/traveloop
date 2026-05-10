from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

trips = []
next_id = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/api/trips', methods=['GET','POST'])
def api_trips():
    global next_id
    if request.method == 'POST':
        data = request.get_json() or {}
        trip = {
            'id': next_id,
            'name': data.get('name','Untitled'),
            'start': data.get('start'),
            'end': data.get('end')
        }
        next_id += 1
        trips.append(trip)
        return jsonify(trip), 201
    else:
        return jsonify(trips)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
