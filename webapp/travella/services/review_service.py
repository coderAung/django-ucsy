from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from ..models import Review
from ..dtos.review_dto import ReviewDTO

class ReviewService:
    @staticmethod
    def list_reviews(page=1, per_page=6):
        reviews = Review.objects.all().order_by('-createdAt')
        paginator = Paginator(reviews, per_page)
        page_obj = paginator.get_page(page)
        
        dto_list = [
            ReviewDTO(
                id=r.id,
                content=r.content,
                account_name=getattr(r.account, 'username', 'Anonymous'),
                created_at=r.createdAt
            ) for r in page_obj
        ]
        return dto_list, page_obj

    @staticmethod
    def get_review_for_edit(review_id, user):
        review = get_object_or_404(Review, id=review_id, account=user)
        return ReviewDTO(
            id=review.id,
            content=review.content,
            account_name=user.username,
            created_at=review.createdAt
        )

    @staticmethod
    def save_review(data, user):
        if data.get('id'):
            review = get_object_or_404(Review, id=data['id'], account=user)
        else:
            review = Review(account=user)
        review.content = data['content']
        review.save()
        return review

    @staticmethod
    def delete_review(review_id, user):
        review = get_object_or_404(Review, id=review_id, account=user)
        review.delete()
