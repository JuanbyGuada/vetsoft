from django.test import TestCase
from app.models import Client, Medicine, Product, Provider


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "54221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

<<<<<<< HEAD
        client.update_client({
            "name": client.name,
            "phone": "54221555233",
            "address": client.address,
            "email": client.email,
            })
=======
        client.update_client(
            {"name": "Juan Sebastian Veron",
            "phone": "221555233",
            "address": "13 y 44",
            "email": "brujita75@hotmail.com"}
        )
>>>>>>> develop

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555232")


    def test_cant_create_with_invalid_phone(self):
        success, errors= Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 0)
        self.assertFalse(success)
        self.assertIn("phone", errors)
        self.assertEqual(errors["phone"], "El teléfono debe empezar con 54")


    def test_cant_update_client_with_invalid_phone(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        success, errors= client.update_client({
            "name": client.name,
            "phone": "221555233",
            "address": client.address,
            "email": client.email,
            })
        
        self.assertFalse(success)
        self.assertIn("phone", errors)
        self.assertEqual(errors["phone"], "El teléfono debe empezar con 54")

<<<<<<< HEAD

=======
        client.update_client(
                    {"name": "Juan Sebastian Veron",
                    "phone": "",
                    "address": "13 y 44",
                    "email": "brujita75@hotmail.com"}
        )
        client_updated = Client.objects.get(pk=1)
>>>>>>> develop


    def test_nombre_invalido(self):
        success, errors = Client.save_client(
            {
                "name": "brujita75",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        self.assertFalse(success)
        self.assertIn("name", errors)
        self.assertEqual(errors["name"], "El nombre solo puede contener letras y espacios")
        client = Client.objects.all()
        self.assertEqual(len(client), 0)

class ProductModelTest(TestCase):
    def setUp(self):
        # Crear un proveedor para los productos de prueba
        self.provider = Provider.objects.create(name="ProveedorEjemplo", email="correo@utn.com")
        proveedores = Provider.objects.all()
        self.assertEqual(len(proveedores), 1)

    def test_can_create_and_get_product(self):
        success, errors = Product.save_product(
            {
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": 100,
                "provider": self.provider.id,
            }
        )
        self.assertTrue(success)
        products = Product.objects.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Collar de Perro")
        self.assertEqual(products[0].price, 100)
        self.assertEqual(products[0].type, "Ropa")
        self.assertEqual(products[0].provider, self.provider)

    def test_precio_positivo(self):
        success, errors = Product.save_product(
            {
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": 100,
                "provider": self.provider.id,
            }
        )
        self.assertIsNone(errors)
        self.assertTrue(success)
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

    def test_precio_negativo(self):
        success, errors = Product.save_product(
            {
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": -100,
                "provider": self.provider.id,
            }
        )
        self.assertFalse(success)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un numero positivo")
        products = Product.objects.all()
        self.assertEqual(len(products), 0)

    def test_precio_nulo(self):
        success, errors = Product.save_product(
            {
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": 0,
                "provider": self.provider.id,
            }
        )
        self.assertFalse(success)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio")
        products = Product.objects.all()
        self.assertEqual(len(products), 0)

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