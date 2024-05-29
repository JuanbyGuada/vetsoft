from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client, Medicine, Product, Provider


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)

class ProductTest(TestCase):
    def setUp(self): # Crear un proveedor para los productos de prueba
        self.provider = Provider.objects.create(name="ProveedorEjemplo", email="correo@utn.com")

    def test_repo_use_repo_template(self): # Test para verificar que se use el template correcto para el repositorio de productos
        response = self.client.get(reverse("products_repo"))
        self.assertTemplateUsed(response, "products/repository.html")
    
    def test_repo_display_all_products(self): # Test para verificar que se muestren todos los productos
        response = self.client.get(reverse("products_repo"))
        self.assertTemplateUsed(response, "products/repository.html")

    def test_form_use_form_template(self): # Test para verificar que se use el template correcto para el formulario
        response = self.client.get(reverse("products_form"))
        self.assertTemplateUsed(response, "products/form.html")

    def test_can_create_product(self): # Test para verificar que se pueda crear un producto
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": 100,
                "provider": self.provider.id,
            },
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        self.assertEqual(products[0].name, "Collar de Perro")
        self.assertEqual(products[0].type, "Ropa")
        self.assertEqual(products[0].price, 100)
        self.assertEqual(products[0].provider, self.provider)

        self.assertRedirects(response, reverse("products_repo"))

    def test_validation_errors_create_product(self):
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "",
                "type": "",
                "price": "",
            },
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un tipo")
        self.assertContains(response, "Por favor ingrese un precio")

        
    def test_should_response_with_404_status_if_product_doesnt_exists(self): # Test para verificar que se muestre un error 404 si el producto no existe
        response = self.client.get(reverse("products_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)
    
    def test_validacion_precio_negativo(self): # Test para verificar que se muestre un error si el precio es negativo al crear un producto
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": -100,
                "provider": self.provider.id,
            },
        )

        self.assertContains(response, "Por favor ingrese un numero positivo")

    def test_validacion_precio_nulo(self): # Test para verificar que se muestre un error si el precio es nulo al crear un producto
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": 0,
                "provider": self.provider.id,
            },
        )

        self.assertContains(response, "Por favor ingrese un precio")
    
    def test_edit_product_with_valid_data(self): # Test para verificar que se pueda editar un producto con datos válidos
        product = Product.objects.create(
            name="Collar de Perro",
            type="Ropa",
            price=100,
            provider=self.provider,
        )

        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "name": "Collar de Gato",
                "type": product.type,
                "price": 90,
                "provider": product.provider.id,
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedProduct = Product.objects.get(pk=product.id)
        self.assertEqual(editedProduct.name, "Collar de Gato")
        self.assertEqual(editedProduct.type, product.type)
        self.assertEqual(editedProduct.price, 90)
        self.assertEqual(editedProduct.provider, product.provider)

    def test_validacion_precio_negativo_edit_product(self): # Test para verificar que se muestre un error si el precio es negativo al editar un producto
        product = Product.objects.create(
            name="Collar de Perro",
            type="Ropa",
            price=100,
            provider=self.provider,
        )

        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "name": "Collar de Gato",
                "type": product.type,
                "price": -90,
                "provider": product.provider.id,
            },
        )

        self.assertContains(response, "Por favor ingrese un numero positivo")

    def test_validacion_precio_nulo_edit_product(self): # Test para verificar que se muestre un error si el precio es nulo al editar un producto
        product = Product.objects.create(
            name="Collar de Perro",
            type="Ropa",
            price=100,
            provider=self.provider,
        )

        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "name": "Collar de Gato",
                "type": product.type,
                "price": 0,
                "provider": product.provider.id,
            },
        )
        
class MedicinesTest(TestCase):

    def test_can_create_medicine(self):
        response = self.client.post (
            reverse("medicines_form"),
            data={
                "name": "MedicineA",
                "description": "MedicineA",
                "dose": "10",
            },
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "MedicineA")
        self.assertEqual(medicines[0].description, "MedicineA")
        self.assertEqual(medicines[0].dose, 10)

        self.assertRedirects(response, reverse("medicines_repo"))

    def test_validation_errors_create_medicine(self):
        response = self.client.post(
            reverse("medicines_form"),
            data={},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese una descripción")
        self.assertContains(response, "Por favor ingrese una dosis")

    def test_edit_medicine_with_valid_data(self):
        medicine = Medicine.objects.create(
            name="Medi_A",
            description="Desc_A",
            dose=10,
        )

        response = self.client.post(
            reverse("medicines_form"),
            data={
                "id": medicine.id,
                "name": "Medi_B",
                "description": medicine.description,
                "dose": 2,
            },
        )

        self.assertEqual(response.status_code, 302)


        editedMedicine = Medicine.objects.get(pk=medicine.id)
        self.assertEqual(editedMedicine.name, "Medi_B")
        self.assertEqual(editedMedicine.description, medicine.description)
        self.assertEqual(editedMedicine.dose, 2)


    def test_edit_medicine_with_invalid_dose(self):
        medicine = Medicine.objects.create(name="Medicina B", description="Descripción B", dose=5)

        response = self.client.post(reverse("medicines_form"),
                        {
                        "id": medicine.id,
                        "name": medicine.name,
                        "description": medicine.description,
                        "dose": -10
                        })

        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "La dosis debe ser un número entre 1 y 10") #no cambia el medicamento, le vuelve a pedir los datos de vuelta
