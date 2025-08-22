from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET

from travella.services.package_service import PackageService

packageService = PackageService()

@require_GET
def new_package_code(request:HttpRequest) -> JsonResponse:
    code, cname = packageService.generate_code(request.GET.get('cid'))
    return JsonResponse({'newCode': code, 'cname': cname})