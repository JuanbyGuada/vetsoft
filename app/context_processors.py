from django.urls import reverse

links = [
    {"label": "Home", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Mascotas", "href": reverse("pets_repo"), "icon": "bi bi-emoji-heart-eyes"},
    {"label": "Produtos", "href": reverse("products_repo"), "icon": "bi bi-box"},
    {"label": "Veterinarios", "href": reverse("vets_repo"), "icon": "bi bi-person-badge"},
    {"label": "Medicamentos", "href": reverse("medicines_repo"), "icon": "bi bi-droplet-half"},
    {"label": "Proveedores", "href": reverse("providers_repo"), "icon": "bi bi-truck"},
]


def navbar(request):
    def add_active(link):
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}
