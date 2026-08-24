import allure
from faker import Faker

from conftest import attach_json

fake = Faker

pytestmark = [
    allure.parent_suite("EaseBankAPI"),
    allure.suite("Students / Employee"),
    allure.sub_suite("Employee CRUD")
]

def employee_payload():
    return {
        "email": fake.email(),
        "full_name": fake.full_name(),
        "password": fake.password()
    }

def test_student_manage_employee(api_client, base_url):
    created_employee_id = None
    create_payload = employee_payload()

    with allure.step("Create employee POST /students/employee"):
        attach_json("create-employee-request", create_payload)
        response = api_client.post(
            f'{base_url}/students/employees',
            json = create_payload
        )
        attach_json("create-employee-request" , response.json())

        assert response.status_code == 200

        created_employee = response.json()
        created_employee_id = created_employee['id']

        assert created_employee['email'] == create_payload['email']
        assert created_employee['name'] == create_payload['name']

    with allure.step(f"Check employee GET /students/employee/employee_id"):
        response = api_client.get(
            f'{base_url}/students/employees/{created_employee_id}')
        attach_json("get-employee-request" , response.json())

        assert response.status_code == 200
        assert response.json()['id'] == created_employee_id

    with allure.step(f"Update employee PATCH /students/employee/employee_id"):
        update_payload = {
            "email": fake.email() ,
            "full_name": fake.full_name() ,
        }
        attach_json("update-employee-request" , update_payload)
        response = api_client.patch(
            f'{base_url}/students/employees/{created_employee_id}',
            json=update_payload
        )
        attach_json("update-employee-response" , response.json())

        assert response.status_code == 200
        assert response.json()['full_name'] == update_payload['full_name']
        assert response.json()['email'] == update_payload['email']

    with allure.step(f"Delete created employee DELETE /students/employee/employee_id"):
        response = api_client.delete(
            f'{base_url}/students/employees/{created_employee_id}')
        attach_json("delete-employee-response" , response.json())

        assert response.status_code == 200
