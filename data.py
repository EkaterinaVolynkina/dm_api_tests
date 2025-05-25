import uuid

def generate_user():
    user = f'katya_1_{uuid.uuid4().hex[:6]}'
    email = f'{user}@example.com'
    password = 'Qwerty123!'
    return user, email, password

