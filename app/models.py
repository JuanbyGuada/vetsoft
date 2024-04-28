from django.db import models
from datetime import datetime



def validate_client(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address
        self.save()

        

    
#  Provider Class

def validate_provider(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")


    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


    @classmethod
    def save_provider(cls, provider_data):
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
        )

        return True, None

    def update_provider(self, provider_data):
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email

        self.save() 
        
#  Product Class

def validate_product(data):
    errors = {}

    name = data.get("name", "")
    type = data.get("type", "")
    price = data.get("price", "")


    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if type == "":
        errors["type"] = "Por favor ingrese un tipo"

    if not price:
        errors["price"] = "Por favor ingrese un precio"
    else:
        try:
            float(price)
        except ValueError:
            errors["price"] = "El precio debe ser un número"

    return errors


class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='products')

    @classmethod
    def save_product(cls, product_data):
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        provider_id = product_data.get("provider")
        provider = Provider.objects.get(pk=provider_id) 

        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
            provider=provider,
        )

        return True, None

    def update_product(self, product_data):
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price

        if 'provider' in product_data:
            provider_id = product_data.get("provider")
            self.provider = Provider.objects.get(pk=provider_id)
        self.save() 

#client-product (sale)

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['client', 'product'] 

#  Pet Class

def validate_pet(data):
    errors = {}

    name = data.get("name", "")
    breed = data.get("breed", "")
    birthday = data.get("birthday", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if breed == "":
        errors["breed"] = "Por favor ingrese una raza"

    if birthday == "":
        errors["birthday"] = "Por favor ingrese fecha de nacimiento"
    else:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
            today = datetime.now().date()
            if birthday_date > today:
                errors["birthday"] = "La fecha de nacimiento no puede ser mayor a la fecha de hoy"

    return errors

class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    birthday= models.DateField()
    vets = models.ManyToManyField("Vet")

    def __str__(self):
        return self.name
    
    @classmethod
    def save_pet(cls, pet_data):
        errors = validate_pet(pet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
        )
        return True, None
    
    def update_pet(self, pet_data):
        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday

        self.save()

#  Vet Class

def validate_vet(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors

class Vet(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    @classmethod
    def save_vet(cls, vet_data):
        errors = validate_client(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            email=vet_data.get("email"),
            phone=vet_data.get("phone"),
        )
        return True, None

    def update_vet(self, vet_data):
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone
    
        self.save()


#  Medicine Class

def validate_medicine(data):
    errors = {}

    name = data.get("name", "")
    description = data.get("description", "")
    dose = data.get("dose", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if description == "":
        errors["description"] = "Por favor ingrese una descripción"

    if dose == "":
        errors["dose"] = "Por favor ingrese una dosis"

    return errors

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    dose = models.IntegerField()

    def __str__(self):
        return self.name
    
    @classmethod
    def save_medicine(cls, medicine_data):
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        )
        return True, None
    
    def update_medicine(self, medicine_data):
        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose

        self.save() 

#Pet-Med


class PetMedicine(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medications')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='used_on_pets')
    administration_date = models.DateField()

    def __str__(self):
        return f"{self.medicine.name} administrado a {self.pet.name} el {self.administration_date}"
    
    @staticmethod
    def validate_petmed(data):
        errors = {}
        administration_date = data.get("administration_date", "")

        if not administration_date:
            errors["administration_date"] = "Por favor ingrese fecha de administración"
        else:
            try:
                parsed_date = datetime.strptime(administration_date, "%Y-%m-%d").date()
                if parsed_date > datetime.now().date():
                    errors["administration_date"] = "La fecha de administración no puede ser mayor a la fecha de hoy"
            except ValueError:
                errors["administration_date"] = "Formato de fecha inválido"
        return errors

    @classmethod
    def save_petmed(cls, pet_med_data):
        errors = cls.validate_petmed(pet_med_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        pet = Pet.objects.get(id=pet_med_data['pet_id'])
        medicine = Medicine.objects.get(id=pet_med_data['medicine_id'])

        PetMedicine.objects.create(
            pet=pet,
            medicine=medicine,
            administration_date=pet_med_data.get("administration_date"),
        )
        return True, None
    
    def update_petmed(self, pet_med_data):
        self.administration_date = pet_med_data.get("administration_date", "")
        if 'medicine' in pet_med_data:
            medicine_id = pet_med_data.get("medicine")
            self.medicine = Medicine.objects.get(pk=medicine_id)
        self.save()
