from django.shortcuts import redirect, reverse
def validate(request):
    if 'user' not in request.session:
        return redirect(reverse('login'))
    return True