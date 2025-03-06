@app.route('/input', methods=['POST'])
def input_data():
    data = request.json
    # Process the data...
    return jsonify({"status": "Data received!"})