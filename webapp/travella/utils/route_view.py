class RouteView:
    def __init__(self, base = '', suffix = 'html'):
        self._base = base if not base.endswith('/') else base[:-1]
        self._suffix = suffix
    
    def view(self, name:str) -> str:
        return f'{self._base}/{name}.{self._suffix}'
    
    @staticmethod
    def get(base:str, suffix = 'html'):
        return RouteView(base, suffix).view