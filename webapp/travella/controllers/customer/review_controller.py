from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from ...services.review_service import ReviewService
from ...domains.forms.review_form import ReviewForm
from ...dtos.review_dto import ReviewDTO
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from travella.utils.route_view import RouteView

base = 'customer/reviews/'
view = RouteView.get(base)

# def list(request:HttpRequest) -> HttpResponse:
#     page = request.GET.get('page',1)
#     reviews, page_obj = ReviewService.list_reviews(request.user, page)
#     return render(request, view('list'), {'reviews': page_obj})

def list(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    reviews, page_obj = ReviewService.list_reviews(request.user, page)

    edit_review_id = request.GET.get('edit')
    edit_review = None
    if edit_review_id:
        edit_review = ReviewService.get_review_for_edit(edit_review_id, request.user)

    return render(request, view('list'), {
        'reviews': page_obj,
        'user': request.user,
        'edit_review': edit_review
    })


def detail(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('detail'))

def new(request:HttpRequest) -> HttpResponse:
    form = ReviewForm()
    return render(request, view('form'), {'form': form})

def edit(request:HttpRequest, id:int) -> HttpResponse:
    review_dto = ReviewService.get_review_for_edit(id, request.user)
    form = ReviewForm(initial={'content':review_dto.content})
    return render(request, view('form'), {'form': form, 'edit': True, 'id': review_dto.id})

@login_required
@require_POST
def save(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            ReviewService.save_review(form.cleaned_data, request.user)
            messages.success(request, "Your review has been submitted successfully")
            return redirect('review_list')
        return render(request, view('form'), {'form': form})
    return redirect('review_list')

@require_POST
@login_required
def delete(request, id):
    ReviewService.delete_review(id, request.user)
    messages.success(request, "Review deleted successfully.")
    return redirect('review_list')