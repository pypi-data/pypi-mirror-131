from django.test import TestCase, Client


class CRUDUserProxy(TestCase):
    def test_user_proxy_crud(self):
        client = Client()

        client.post("/api/v1/auth_proxy", {"user_id": "67e601a4-becc-4a04-89d7-f174982a01f6"}, content_type="application/json")
        response = client.get("/api/v1/auth_proxy/?pk=67e601a4-becc-4a04-89d7-f174982a01f6")

        print(response.body)
