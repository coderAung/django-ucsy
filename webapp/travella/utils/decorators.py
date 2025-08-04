from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        print('Checking admin session...') 
        if not request.session.get('admin_id'):
            print('Admin not logged in, redirecting...')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper