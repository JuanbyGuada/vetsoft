from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Client, Product, Pet, Vet, Medicine, Provider, Sale


def home(request):
    return render(request, "home.html")


def clients_repository(request):
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})


def clients_form(request, id=None):
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            client.update_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST}
        )

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client})


def clients_delete(request):
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))


#provider


def providers_repository(request):
    providers = Provider.objects.all()
    return render(request, "providers/repository.html", {"providers": providers})


def providers_form(request, id=None):
    if request.method == "POST":
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("providers_repo"))

        return render(
            request, "providers/form.html", {"errors": errors, "provider": request.POST}
        )

    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "providers/form.html", {"provider": provider})

def provider_products(request, provider_id):
    provider = Provider.objects.get(pk=provider_id)
    products = provider.products.all()
    return render(request, 'provider_products.html', {'provider': provider, 'products': products})


def providers_delete(request):
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()

    return redirect(reverse("providers_repo"))



#product


def product_list(request):
    # Utiliza select_related para obtener los detalles del proveedor junto con cada producto
    products = Product.objects.select_related('provider').all()
    return render(request, 'product_list.html', {'products': products})

def products_repository(request):
    products = Product.objects.all()
    return render(request, "products/repository.html", {"products": products})



def products_form(request, id=None):

    providers = Provider.objects.all()  


    if request.method == "POST":
        product_id = request.POST.get("id", "")

        errors = {}
        saved = True

        if product_id == "":
            saved, errors = Product.save_product(request.POST)
        else:
            product = get_object_or_404(Product, pk=product_id)
            product.update_product(request.POST)

        if saved:
            return redirect(reverse("products_repo"))

        return render(
            request, "products/form.html", {"errors": errors, "product": request.POST, "providers": providers }
        )
    
    else:
        product = None
        if id is not None:
            product = get_object_or_404(Product, pk=id)
            return render(request, "products/form.html", {"product": product, "providers": providers})
        
        return render(request, "products/form.html", {"providers": providers})

    
        

    return render(request, "products/form.html", {"product": product})


def products_delete(request):
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()

    return redirect(reverse("products_repo"))

#sale

def client_purchases(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    purchases = Sale.objects.filter(client=client)
    return render(request, 'clients/products/client_purchases.html', {'client': client, 'purchases': purchases})


def add_purchase(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        # Verifica si ya existe una entrada para este cliente y producto
        existing_sale = Sale.objects.filter(client=client, product=product).exists()
        
        if not existing_sale:
            # Si no existe, crea la nueva entrada
            Sale.objects.create(client=client, product=product)
        
        # Redirige al usuario a la página de compras del cliente
        return redirect('client_purchases', client_id=client.id)
    else:
        products = Product.objects.all()
        return render(request, 'clients/products/addproduct.html', {'products': products, 'client': client})
    
#pet

def pets_repository(request):
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})

def pets_form(request, id=None):
    if request.method == "POST":
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            pet.update_pet(request.POST)

        if saved:
            return redirect(reverse("pets_repo"))

        return render(
            request, "pets/form.html", {"errors": errors, "pet": request.POST}
        )

    pet = None
    if id is not None:
        pet = get_object_or_404(Pet, pk=id)

    return render(request, "pets/form.html", {"pet": pet})


def pets_delete(request):
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()

    return redirect(reverse("pets_repo"))

def mascota_detalle(request, mascota_id):
    mascota = get_object_or_404(Pet, pk=mascota_id)
    veterinarios = mascota.vets.all()
    return render(request, 'pet-vet/mascota_detalle.html', {'mascota': mascota, 'veterinarios': veterinarios})

def asociar_veterinario(request, mascota_id):
    if request.method == 'POST':
        veterinario_id = request.POST.get('veterinario_id')
        mascota = get_object_or_404(Pet, pk=mascota_id)
        veterinario = get_object_or_404(Vet, pk=veterinario_id)
        mascota.vets.add(veterinario)
        return redirect('mascota_detalle', mascota_id=mascota_id)
    else:
        veterinarios = Vet.objects.all()
        return render(request, 'pet-vet/asociar_veterinario.html', {'veterinarios': veterinarios, 'mascota_id': mascota_id})
    
def desasociar_veterinario(request, mascota_id, veterinario_id):
    mascota = get_object_or_404(Pet, pk=mascota_id)
    veterinario = get_object_or_404(Vet, pk=veterinario_id)
    mascota.vets.remove(veterinario)
    return redirect('mascota_detalle', mascota_id=mascota_id)

# vet

def vets_repository(request):
    vets = Vet.objects.all()
    return render(request, "vets/repository.html", {"vets": vets})

def vets_form(request, id=None):
    if request.method == "POST":
        vet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if vet_id == "":
            saved, errors = Vet.save_vet(request.POST)
        else:
            vet = get_object_or_404(Vet, pk=vet_id)
            vet.update_vet(request.POST)

        if saved:
            return redirect(reverse("vets_repo"))

        return render(
            request, "vets/form.html", {"errors": errors, "vet": request.POST}
        )

    vet = None
    if id is not None:
        vet = get_object_or_404(Vet, pk=id)

    return render(request, "vets/form.html", {"vet": vet})

def vets_delete(request):
    vet_id = request.POST.get("vet_id")
    vet = get_object_or_404(Vet, pk=int(vet_id))
    vet.delete()

    return redirect(reverse("vets_repo"))

#medicine
def medicines_repository(request):
    medicines = Medicine.objects.all()
    return render(request, "medicines/repository.html", {"medicines": medicines})

def medicines_form(request, id=None):
    if request.method == "POST":
        medicine_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if medicine_id == "":
            saved, errors = Medicine.save_medicine(request.POST)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            medicine.update_medicine(request.POST)

        if saved:
            return redirect(reverse("medicines_repo"))

        return render(
            request, "medicines/form.html", {"errors": errors, "medicine": request.POST}
        )

    medicine = None
    if id is not None:
        medicine = get_object_or_404(Medicine, pk=id)

    return render(request, "medicines/form.html", {"medicine": medicine})

def medicines_delete(request):
    medicine_id = request.POST.get("medicine_id")
    medicine = get_object_or_404(Medicine, pk=int(medicine_id))
    medicine.delete()

    return redirect(reverse("medicines_repo"))



