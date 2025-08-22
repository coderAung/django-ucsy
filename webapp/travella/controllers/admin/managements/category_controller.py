from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from travella.domains.forms.category.category_form import CategoryForm
from travella.services.category_service import CategoryService
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from travella.domains.models.tour_models import Category
from django.db.models import Count
from ....dtos import package_dto

base = 'admin/managements/categories/'

def view(name: str) -> str:
    return base + name + '.html'

@login_required
def list(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all().select_related('createdBy').annotate(packages_count = Count(package_dto.Package))
    return render(request, view('list'), {'categories': categories})

@login_required
def new(request: HttpRequest) -> HttpResponse:
    form = CategoryForm()
    return render(request, view('form'), {'form': form})

@login_required
@require_http_methods(["POST"])
def save(request: HttpRequest) -> JsonResponse:
    form = CategoryForm(request.POST)
    if form.is_valid():
        try:
            category_dto = CategoryService.add_category(
                form.cleaned_data['name'], 
                request.user
            )
            return JsonResponse({
                'success': True,
                'redirect_url': '/admins/categories/',
                'category': {
                    'id': category_dto.id,
                    'name': category_dto.name,
                    'created_by': category_dto.created_by,
                    'created_at': category_dto.created_at.strftime("%Y-%m-%d %H:%M")
                }
            })
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
def edit(request: HttpRequest, id: int) -> JsonResponse:
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                category_dto = CategoryService.update_category(
                    id,
                    form.cleaned_data['name'],
                    request.user
                )
                return JsonResponse({
                    'success': True,
                    'category': {
                        'id': category_dto.id,
                        'name': category_dto.name,
                        'created_by': category_dto.created_by,
                        'created_at': category_dto.created_at.strftime("%Y-%m-%d %H:%M")
                    }
                })
            except ValueError as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def delete(request: HttpRequest, id: int) -> HttpResponse:
    try:
        CategoryService.delete_category(id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('categories')
    except ValueError as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        return redirect('categories')