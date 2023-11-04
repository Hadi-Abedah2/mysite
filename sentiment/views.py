from django.shortcuts import render
from .forms import SentimentForm
from .sentiment_analysis_package.sentiment_analysis import sentiment_analyzer 

def sentiment_view(request):
    #result = None
    if request.method == 'POST':
        form = SentimentForm(request.POST)
        if form.is_valid():
            text_to_analyze = form.cleaned_data['text']
            result = sentiment_analyzer(text_to_analyze)
            
        else:
            result = 'invalid text input!'
        return render(request, 'sentiment.html', {'form': form, 'result':result})
    else:
        form = SentimentForm()

    return render(request, 'sentiment.html', {'form': form})
