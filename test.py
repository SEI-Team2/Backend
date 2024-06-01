import requests

# Define the base URL of your Flask application
BASE_URL = 'http://localhost:5000'

# Sample data for the schedules_list endpoint
clubs_data = {
    'clubregularid' : 1,
    'clubid' : 2,
    'spaceid' : 2,
    'dayofweek' : 3,
    'starttime' : '10:00:00', 
    'endtime' : '12:00:00',
}

def test_clubs(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/clubs/clubregular/delete', json=clubs_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

# Sample data for the schedules_list endpoint
normals_black_data = {
    'userid' : 1,
    'reason' : 'shit',
}


def test_normals_black(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/normals/black/delete', json=normals_black_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200


# Sample data for the schedules_list endpoint
normals_restrict_data = {
    'spaceid' : 2,
    'starttime' : '2024-06-01 10:00:00',
    'endtime' : '2024-06-01 11:00:00',
    'desc' : 'descsdsd',
}

def test_normals_restrict(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/normals/restrict', json=normals_restrict_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200



# Sample data for the schedules_list endpoint
profiles_clubmembers_add_data = {
    'studentid' : 12345679,
}

def test_profiles_clubmembers_add(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/profiles/clubmembers/add', json=profiles_clubmembers_add_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

# Sample data for the schedules_list endpoint
profiles_schedules_data = {
    
}

def test_profiles_schedules(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/profiles/schedules', json=profiles_schedules_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200



# Sample data for the schedules_list endpoint
profiles_user_data = {
    
}

def test_profiles_user(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/profiles/user', json=profiles_user_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200




# Sample data for the schedules_list endpoint
rentals_delete_data = {
    'rentalid' : 2
}

def test_rentals_delete(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/rentals/delete', json=rentals_delete_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200



# Sample data for the schedules_list endpoint
rentals_create_data = {
    'spaceid': 2,
    'starttime': '2024-05-31 06:00:00',
    'endtime': '2024-05-31 07:00:00',
    'maxpeople': 5,
    'desc': 'HI',
    'friends': [1,2,3],
}

def test_rentals_create(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/rentals/create', json=rentals_create_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200





# Sample data for the schedules_list endpoint
rentals_cancle_data = {
    'rentalid': 2,
}

def test_rentals_cancle(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/rentals/cancle', json=rentals_cancle_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200



# Sample data for the schedules_list endpoint
rentals_join_data = {
    'rentalid': 2,
}

def test_rentals_join(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/rentals/join', json=rentals_join_data, headers=headers)

    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200


# Sample data for the schedules_list endpoint
rentals_list_data = {
    'spaceid': 1,
    'date': '2024-10-01'
}

def test_rentals_list(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/rentals/list', json=rentals_list_data, headers=headers)


    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200


# Sample data for the schedules_list endpoint
schedules_data = {
    'spaceid': 1,
    'date': '2024-06-01'
}
# Function to test the schedules_list endpoint
def test_schedules_list(jwt_token):
    # Define the headers containing the JWT token

    # Make a POST request to the schedules/list endpoint with the sample data
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Create the headers with the access token
    response = requests.post(f'{BASE_URL}/schedules/list', json=schedules_data, headers=headers)


    # Print the response JSON and status code
    print('Response JSON:', response.json())
    print('Status Code:', response.status_code)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200


# Define test data for user registration
register_data = {
    'sid': '123456789',
    'name': 'John Doe',
    'contact': '1234567890',
    'email': 'john@example.com',
    'password': 'password123',
    'usertype': 'student'
}

# Test user registration API
def test_user_registration():
    response = requests.post(f'{BASE_URL}/users/register', json=register_data)
    print(response.json())
    assert response.status_code == 200  # Check if the response status code is 200 (OK)


# Define test data for user login
login_data = {
    'email': 'email2',
    'password': '1111',
}

# Test user login API
def test_user_login():
    response = requests.post(f'{BASE_URL}/users/login', json=login_data)
    print(response.json())
    assert response.status_code == 200  # Check if the response status code is 200 (OK)
    return response.json().get('jwt_token')

# Run the test functions
if __name__ == '__main__':
    #test_user_registration()
    jwt_token = test_user_login()
    test_clubs(jwt_token)