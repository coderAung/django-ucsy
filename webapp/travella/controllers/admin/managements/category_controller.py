from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from travella.domains.forms.category.category_form import CategoryForm
from travella.services.category_service import CategoryService
from django.contrib.auth.decorators import login_required

base = 'admin/managements/categories/'

def view(name: str) -> str:
    return base + name + '.html'

# categories/ GET
def list(request: HttpRequest) -> HttpResponse:
    return render(request, view('list'))

# categories/<id> GET
def detail(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, view('detail'))

# categories/new GET
@login_required
def new(request: HttpRequest) -> HttpResponse:
    form = CategoryForm()
    return render(request, view('form'), {'form': form})

# categories/save POST
@login_required
def save(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            created_by = request.user
            category_dto = CategoryService.add_category(form.cleaned_data['name'], created_by)
            return redirect('/admins/categories/')
    return render(request, view('form'), {'form': form})

# categories/<id>/edit/ GET and POST
@login_required
def edit(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, view('form'))
