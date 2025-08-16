
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from travella.forms import CategoryForm
from travella.services.category_service import CategoryService

@login_required
@require_POST
def save(request):
    form = CategoryForm(request.POST)

    if not form.is_valid():
        return JsonResponse({'success': False, 'error': 'Invalid form data.'})

    try:
        category_dto = CategoryService.add_category(form.cleaned_data['name'], request.user)
        print(f"[DEBUG] New category saved: ID={category_dto.id}, Name={category_dto.name}, CreatedBy={category_dto.created_by}")

        return JsonResponse({
            'success': True,
            'category': {
                'id': category_dto.id,
                'name': category_dto.name,
                'created_by': category_dto.created_by
            }
        })
    except ValueError as e:
        return JsonResponse({'success': False, 'error': str(e)})
    except Exception:
        return JsonResponse({'success': False, 'error': 'Something went wrong.'})
