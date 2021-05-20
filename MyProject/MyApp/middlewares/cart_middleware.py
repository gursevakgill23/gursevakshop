from django.shortcuts import redirect
from django.contrib import messages

def auth_middleware1(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        if not request.session.get('customer'):
            return redirect('login')
        elif not request.session.get('cart'):
            messages.error(request, 'Your cart is empty')
            return redirect('home')

        response = get_response(request)
        return response
    return middleware
