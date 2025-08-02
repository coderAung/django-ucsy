from ..domains.models.tour_models import Package
from ..dtos.package_dto import PackageItem, PackageDetail


class PackageService:

    def get_all(self) -> list[PackageItem]:
        packages = Package.objects.all()
        items = [PackageItem.of(p) for p in packages]
        return items

    def get_one(self, code:str) -> PackageDetail:
        package = Package.objects.get(code = code)
        return PackageDetail.of(package)