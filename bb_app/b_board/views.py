import time

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect

from b_board.models import Post, Comment


def bb_list(request):
    """
    Render and show list of all ads from a DB. Func try get data from a caches,
    if data not exist in cache, func make request in a DB and write data in a cache.
    """
    error_message = 'Sorry, but your cache is not working'
    ads = cache.get('ads_in_caches')


    if ads:
        print(f'List of the ads has been used from a cache.')
        return render(request, 'bbList.html', {'ads': ads,
                                               'cache_error': error_message})
    else:
        ads = Post.objects.all()
        if not ads:
            error_message = 'Sorry, but now your data base has no a data.'
            print('Has no data for caching.')
        else:
            cache.set('ads_in_caches', ads)
            print(f'List of the ads has been seated in a cache.')

        return render(request, 'bbList.html', {'ads': ads,
                                           'error': error_message})


def ad_creation(request):
    """
    Rendering the ad_create page.
    """
    return render(request, 'ad_create.html')


def ad_create(request):
    """
    Take data about new ad from request and create a new Post object in a DB.
    Then write this data in a cache.
    """
    if request.method == 'POST':
        title = request.POST['ad_title']
        text = request.POST['ad_text']
        tag_str = request.POST['ad_tags']

        tags = []
        for tag in tag_str.split('#'):
            tag.rstrip()
            if tag != '' and len(tag) < 60:
                tags.append(tag)

        post = Post(title=title, text=text, tags=tags)
        post.save()

        ads = Post.objects.all()
        cache.set('ads_in_caches', ads)
        print(f'List of the ads has been seated in a cache.')

        return redirect('/success/')
    else:
        return redirect('/list/')


def ad_details(request):
    """
    Rendering and show all details about the particular Post object. Try get this data in caches,
    if data not exist, make request in a DB and write this data in a cache.
    """
    if request.method == 'POST':
        ad_id = request.POST['ad_id']
        cache_data = cache.get(f'{ad_id}')

        if cache_data:
            ad = cache_data[0]
            comments = cache_data[1]
            print(f'Ad details and a comments has been used from a cache.')
            return render(request, 'details.html', {'ad': ad,
                                                    'comments': comments})
        else:
            ad = Post.objects.filter(id=ad_id).first()
            comments = Comment.objects.filter(id__in=ad.comments)
            cache.set(f'{ad_id}', [ad, comments])
            print(f'Ad details and a comments has been seated in a cache.')
            return render(request, 'details.html', {'ad': ad,
                                                    'comments': comments})
    else:
        return redirect('/list/')


def add_comment(request):
    """
    Create new Comment object based on data from a request. Then write this data in a cache.
    """
    if request.method == 'POST':
        ad_id = request.POST['ad_id']
        ad_name = request.POST['ad_name']
        ad_text = request.POST['ad_text']
        comment = Comment(name=ad_name, text=ad_text)
        comment.save()
        post = Post.objects.filter(id=ad_id).first()
        post.comments.append(comment.id)
        post.save()

        ad = Post.objects.filter(id=ad_id).first()
        comments = Comment.objects.filter(id__in=ad.comments)
        cache.set(f'{ad_id}', [ad, comments])
        print('All data about the ad has been rewritten in a cache.')

        return redirect(reverse('b_board:ad_details'))
    else:
        return redirect('/list/')


def add_tag(request):
    """
    Create new tag based on data from a request. Then write this data in a cache.
    """
    if request.method == 'POST':
        ad_id = request.POST['ad_id']
        tag_str = request.POST['ad_tag']
        post = Post.objects.filter(id=ad_id).first()
        for tag in tag_str.split('#'):
            tag.rstrip()
            if tag != '' and len(tag) < 60:
                post.tags.append(tag)
        post.save()

        ad = Post.objects.filter(id=ad_id).first()
        comments = Comment.objects.filter(id__in=ad.comments)
        cache.set(f'{ad_id}', [ad, comments])
        print('All data about the ad has been rewritten in a cache.')

        return redirect('/success/')
    else:
        return redirect('/list/')


def ad_statistic(request):
    """
    Rendering and show statistic page, where showing statistic about a tag and a comment
    counters of the particular Post object.
    """
    if request.method == 'POST':
        ad_id = request.POST['ad_id']
        post = Post.objects.filter(id=ad_id).first()
        tag_count = len(post.tags)
        comment_count = len(post.comments)
        return render(request, 'ad_statistic.html', {'tag_count': tag_count,
                                                'comment_count': comment_count,
                                                'ad_id': ad_id})
    else:
        return redirect('/list/')


def success(request):
    return render(request, 'success.html')