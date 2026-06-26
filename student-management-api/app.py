import os
from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = "https://mzdxcfnamtgxbqkrxehp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im16ZHhjZm5hbXRneGJxa3J4ZWhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0NTIzMjcsImV4cCI6MjA5ODAyODMyN30.VoEzEvWwcKpbdrrQLLmji-NgxzuF3dWNs2ontzBgKZ4"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return jsonify({
        'message'        : 'Student Management API is Running!',
        'version'        : '1.0.0',
        'total_endpoints': 5,
        'endpoints'      : {
            '1. CREATE' : 'POST   /students',
            '2. GET ALL': 'GET    /students',
            '3. GET ONE': 'GET    /students/<id>',
            '4. UPDATE' : 'PUT    /students/<id>',
            '5. DELETE' : 'DELETE /students/<id>'
        }
    }), 200

@app.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.json
        required_fields = ['name', 'email', 'course', 'cgpa']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'Missing field: {field}'}), 400
        response = supabase.table('students').insert({
            'name'  : data['name'],
            'email' : data['email'],
            'course': data['course'],
            'cgpa'  : data['cgpa']
        }).execute()
        return jsonify({'status': 'success', 'message': 'Student created!', 'data': response.data}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/students', methods=['GET'])
def get_all_students():
    try:
        response = supabase.table('students').select('*').execute()
        return jsonify({'status': 'success', 'count': len(response.data), 'data': response.data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    try:
        response = supabase.table('students').select('*').eq('id', id).execute()
        if not response.data:
            return jsonify({'status': 'error', 'message': f'Student {id} not found!'}), 404
        return jsonify({'status': 'success', 'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/students/<id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.json
        required_fields = ['name', 'email', 'course', 'cgpa']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'Missing field: {field}'}), 400
        response = supabase.table('students').update({
            'name'  : data['name'],
            'email' : data['email'],
            'course': data['course'],
            'cgpa'  : data['cgpa']
        }).eq('id', id).execute()
        return jsonify({'status': 'success', 'message': 'Student updated!', 'data': response.data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    try:
        check = supabase.table('students').select('*').eq('id', id).execute()
        if not check.data:
            return jsonify({'status': 'error', 'message': f'Student {id} not found!'}), 404
        supabase.table('students').delete().eq('id', id).execute()
        return jsonify({'status': 'success', 'message': f'Student {id} deleted!'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)