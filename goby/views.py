from django.shortcuts import render
def landing(request):
    return render(request, 'index.html')
def for_restaurants(request):
    return render(request, 'for-restaurants.html')
def privacy_policy(request):
    return render(request, 'privacy-policy.html')
def terms_of_service(request):
    return render(request, 'terms-of-service.html')
def login(request):
    return render(request, 'login-signup.html')
