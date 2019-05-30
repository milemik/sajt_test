from django.shortcuts import render

# Create your views here.
def scraper(request):
	return render(request, 'scraper.html')

def scraping_results(request):
	return render(request, 'scraping_results.html')