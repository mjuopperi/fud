
API_HOST = 'api.testserver'

def signup_data(username='test-user', email='test@example.com', password='password'):
    return {
        'username': username,
        'email': email,
        'password': password
    }