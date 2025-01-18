import json
import multiprocessing
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mycrawler.spiders.helloworld_spider import HelloWorldSpider
from scrapy.signalmanager import dispatcher
from scrapy import signals
from .forms import URLinputForm
from django.shortcuts import render, redirect

def callback(item, result_list):
    result_list.append(item)

def run_spider(url,callback, result_list):
    """Runs the Scrapy spider in a separate process."""
    results = []

    def collect_results(item, response, spider):
        #results.append(dict(item))  # Convert Item to dict for JSON serialization
        callback(item, result_list)


    process = CrawlerProcess(get_project_settings())
    dispatcher.connect(collect_results, signal=signals.item_scraped)

    process.crawl(HelloWorldSpider, start_url=url)
    process.start()
    return results

def index(request):
    start_url = request.GET.get('url', None)
    print(start_url,"+++++++++++++++++++================================")
    if not start_url:
        return JsonResponse({'error': 'No url specified'}, status=400)


    with multiprocessing.Manager() as manager:
        result_list = manager.list()

        # Use multiprocessing to run the spider in a separate process
        with multiprocessing.Pool(processes=1) as pool:
            # Pool.apply does not support callbacks directly, so we will run the spider synchronously
            pool.apply(run_spider, (start_url, callback,result_list))

        results = list(result_list)

    if results:
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({'error': 'No data found'})
    # Use multiprocessing to run the spider in a separate process
    #with multiprocessing.Pool(processes=1) as pool: # Use a pool of 1 to avoid multiple concurrent crawls
     #   results = pool.apply(run_spider, (start_url,))

    #if results:
     #   return JsonResponse(results, safe=False)
    #else:
     #   return JsonResponse({'error': 'No data found'})
@csrf_exempt
def get_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = URLinputForm(data)
            if form.is_valid():
                url = form.cleaned_data['url']
                #print(url,"===================================")
                return redirect(f'/crawl/?url={url}')
                #return JsonResponse({'message': f'URL received:/crawl/?url= {url}'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid URL'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

"""def get_url(request):
    if request.method == 'POST':
        form = URLinputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            return render(request, 'index/index.html', {'url': url})
        else:
            form = URLInputForm()
        return render(request, 'index/index.html', {'form': form}) """