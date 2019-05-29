from django.shortcuts import render

# Create your views here.
def scraper(request):
	return render(request, 'scraper.html')