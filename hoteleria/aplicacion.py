import flet as ft
import requests

API_BASE_URL = "http://127.0.0.1:8000"
session = requests.Session()
auth_token = None  # Para almacenar el token de autenticación
csrf_token = None

def main(page: ft.Page):
    page.title = "App de Usuarios"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username_input = ft.TextField(label="Username", width=300)
    password_input = ft.TextField(label="Password", width=300, password=True)
    login_message = ft.Text(value="", color=ft.colors.RED)
    user_role = ft.Text(value="")

    register_username = ft.TextField(label="Nuevo Username", width=300)
    register_email = ft.TextField(label="Email", width=300)
    register_password = ft.TextField(label="Password", width=300, password=True)
    register_message = ft.Text(value="", color=ft.colors.RED)


    def get_token():
        global csrf_token
        response = session.get(f"{API_BASE_URL}/api/csrf-token/")
        print("entre", response.status_code)
        if response.status_code == 200:
            csrf_token = response.json().get('csrfToken')
            print(csrf_token)


    # Función para realizar el Login
    def login(e):
        global auth_token
        try:
            response = session.post(
                f"{API_BASE_URL}/api/login/",
                json={"username": username_input.value, "password": password_input.value}
            )

            if response.status_code == 200:
                auth_token = response.json().get('token')  # Suponiendo que usas JWT
                user_data = session.get(f"{API_BASE_URL}/api/users/me/")#, headers={"Authorization": f"Bearer {auth_token}"})
                print(user_data)
                if user_data.status_code == 200:
                    user = user_data.json()
                    user_role.value = "admin" if user['is_staff'] else "usuario"
                    page.update()
                login_message.value = "Inicio de sesión exitoso"
            else:
                login_message.value = "Error al iniciar sesión"
            page.update()

        except Exception as err:
            login_message.value = f"Error de conexión: {err}"
            page.update()

    # Función para registrar usuarios
    def register(e):
        print(user_role.value)
        if user_role.value != "admin":
            register_message.value = "No tienes permiso para registrar usuarios."
            page.update()
            return

        try:
            get_token()
            response = session.post(
                f"{API_BASE_URL}/register/",
                json={
                    "username": register_username.value,
                    "email": register_email.value,
                    "password": register_password.value
                },
                headers={"X-CSRFToken": csrf_token}
            )

            if response.status_code == 201:
                register_message.value = "Usuario registrado exitosamente."
            else:
                register_message.value = response.json().get('detail', 'Error al registrar usuario.')
            page.update()
        except Exception as err:
            register_message.value = f"Error de conexión: {err}"
            page.update()

    page.add(
        ft.Column(
            [
                ft.Text("Iniciar Sesión", size=20),
                username_input,
                password_input,
                ft.ElevatedButton("Login", on_click=login),
                login_message,
                user_role,

                ft.Text("Registrar Nuevo Usuario", size=20),
                register_username,
                register_email,
                register_password,
                ft.ElevatedButton("Registrar", on_click=register),
                register_message
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(target=main)