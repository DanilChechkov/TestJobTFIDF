from django.core import files
from django.shortcuts import render
from job1.settings import BASE_DIR

from django.http import HttpResponse
from .forms import PostForm
from .models import Post
from django.core.files import File
import math


def index(request):
    text = None
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            print(Post.objects.latest('id').wholeTxt)
            with open(str(BASE_DIR)+'/media/' +str(Post.objects.latest('id').wholeTxt),'r') as f:
                text = f.read()                                             #Получаем строкой весь текст
                words = {}                                                  #Создаем словарь - так практичнее, он сразу уберет дубликаты
                for word in text.split():                                   #В цикле проходимся по тексту и высчитываем кол-во повторений для каждого слова
                    if word not in words.keys():
                        words[word] = [1]
                    else:
                        words[word][0] +=1
                for word in words:                                          #В цикле высчитываем значения TF,IDF соответственно
                    words[word].append(words[word][0]/len(text.split()))
                    words[word].append(math.log2(1/words[word][1]))         #Не совсем понял момент с IDF - У нас только один документ, соответственно формально получается это просто логарифмическая обратная от TF
                
                #Сортировка по IDF
                sorted_words = list(words.items())                  
                sorted_words.sort(key=lambda i: i[1][2])
                sorted_words = list(reversed(sorted_words))                 #Сортируем в сторону уменьшения, если вдруг выяснится, что нужна обратная сортировка - эту строчку удалить
                for word in sorted_words:
                    print(word)
                return render(request, 'html2.html',{'list':sorted_words})
    else:
        form = PostForm()
    context = {
        "form": form,
        "text": text
    }
    return render(request, 'html.html',{'form':form})
    
# Create your views here.
