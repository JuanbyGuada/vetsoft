from django.test import TestCase
from app.models import Client, Medicine


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": "221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

class MedicineClassTest(TestCase):
    def test_can_create_and_get_medicine(self):
        Medicine.save_medicine(
            {
                "name": "MedicineA",
                "description": "DescriptionA",
                "dose": 9,
            }
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "MedicineA")
        self.assertEqual(medicines[0].description, "DescriptionA")
        self.assertEqual(medicines[0].dose, 9)

    def test_valid_dose(self):
        valid_data = {
            "name": "Medicina A",
            "description": "Descripción A",
            "dose": 5
        }
        success, errors = Medicine.save_medicine(valid_data)
        self.assertTrue(success)
        self.assertIsNone(errors)

    def test_dose_too_low(self):
        invalid_data = {
            "name": "Medicina B",
            "description": "Descripción B",
            "dose": 0
        }
        success, errors = Medicine.save_medicine(invalid_data)
        self.assertFalse(success)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "La dosis debe ser un número entre 1 y 10")
    
    def test_dose_too_high(self):
        invalid_data = {
            "name": "Medicina B",
            "description": "Descripción B",
            "dose": 12
        }
        success, errors = Medicine.save_medicine(invalid_data)
        self.assertFalse(success)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "La dosis debe ser un número entre 1 y 10")

    def test_dose_string(self):
        invalid_data = {
            "name": "Medicina B",
            "description": "Descripción B",
            "dose": "a"
        }
        success, errors = Medicine.save_medicine(invalid_data)
        self.assertFalse(success)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "La dosis debe ser un número")

