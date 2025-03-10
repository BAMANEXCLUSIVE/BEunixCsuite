@app.route('/output', methods=['GET'])
def output_data():
    # Fetch processed data...
    return jsonify({"result": "Processed Data"})