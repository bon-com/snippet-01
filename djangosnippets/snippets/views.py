from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Snippet, Comment
from .forms import SnippetForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_http_methods
from django.core.paginator import Paginator
from . import consts
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_GET


# Create your views here.
@require_safe # GETメソッドとHEADメソッドを受け付ける
def top(request):
    """ トップページ（スニペット一覧）を表示する """
    template = 'snippets/top.html'
    # スニペット一覧を取得（更新日順）
    snippets = Snippet.objects.filter(created_by_id=request.user.id).order_by('-created_at')
    paginator = Paginator(snippets, consts.ITEM_PER_PAGE)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.page(page_num) 
    # 画面表示カテゴリをセット
    categories = dict(consts.SNIPPET_CAG)

    ctx = {'page_obj': page_obj, 'categories': categories}
    return render(request, template, ctx)

@login_required
@require_http_methods(['GET', 'POST', 'HEAD']) # POST,GET,HEADを受け付ける
def snippets_new(request):
    """ スニペット新規登録 """
    if request.method == 'POST':
        # 新規登録
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()

            return redirect(snippets_detail, s_id=snippet.pk)
        # バリデーション失敗後の処理は未記載

    else:
        # 登録画面表示
        template = 'snippets/create_snippet.html'
        form = SnippetForm()
        ctx = {'form': form}

        return render(request, template, ctx)
    
@login_required
@require_http_methods(['GET', 'POST', 'HEAD']) # POST,GET,HEADを受け付ける
def snippets_edit(request, s_id):
    """ スニペット編集 """
    # 対象のスニペット取得
    snippet = get_object_or_404(Snippet, id=s_id)
    # スニペット作成者が編集すること
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden('このスニペットの編集は許可されていません')

    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()

            return redirect(snippets_detail, s_id=snippet.pk)
    else:
        template = 'snippets/edit_snippet.html'
        form = SnippetForm(instance=snippet)
        ctx = {'form': form}

        return render(request, template, ctx)

@login_required
@require_http_methods(['GET', 'POST', 'HEAD']) # POST,GET,HEADを受け付ける
def snippets_detail(request, s_id):
    """ スニペット詳細画面の表示 """
    template = 'snippets/snippet_detail.html'
    # スニペットの詳細 
    snippet = get_object_or_404(Snippet, pk=s_id)
    # コメント一覧
    comments = Comment.objects.filter(commented_by=request.user, commented_to=snippet)
    # コメントフォーム用
    form = CommentForm()
    ctx = {'snippet': snippet, 'comments': comments, 'form': form}
    return render(request, template, ctx)

@login_required
@require_http_methods(['POST']) # POST,GET,HEADを受け付ける
def comment_snippet(request, s_id):
    """ コメントの登録 """
    if request.method == 'POST':
        # POST通信の場合
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.commented_by = request.user
            snippet = get_object_or_404(Snippet, pk=s_id)
            comment.commented_to = snippet
            comment.save()
            return redirect(snippets_detail, s_id=s_id)

@login_required
@require_GET # GETの受け付ける
def snippets_delete(request, s_id):
    """ スニペットの削除 """
    try:
        Snippet.objects.get(pk=s_id).delete()
        if Comment.objects.filter(commented_to_id=s_id):
            Comment.objects.get(commented_to_id=s_id).delete()
    except:
        raise HttpResponseForbidden("指定したユーザーは存在しませんでした。")

    return redirect('top')

@login_required
@require_http_methods(['GET']) # POST,GET,HEADを受け付ける
def delect_comment(request, c_id):
    """ コメントを削除 """
    comment = Comment.objects.get(pk=c_id)
    s_id = comment.commented_to_id
    comment.delete()
    return redirect(snippets_detail, s_id=s_id)

@login_required
@require_http_methods(['POST'])
def search_snippets(request):
    """ スニペットを検索して表示する """
    template = 'snippets/top.html'
    search_name = request.POST['search_name']
    search_category = request.POST['search_category']
    search_type = request.POST['search_type']


    
    # スニペット一覧を取得（更新日順）
    if search_type == consts.SNIPPET_SEARCH_TYPE_ONLY_TITLE:
        # タイトルで検索
        snippets = Snippet.objects.filter(created_by_id=request.user.id, title__icontains=search_name).order_by('-created_at')
    else:
        snippets = Snippet.objects.filter(
                Q(created_by_id=request.user.id) & 
                Q(title__icontains=search_name) |
                Q(code__icontains=search_name) |
                Q(description__icontains=search_name) 
            ).order_by('-created_at')


    # カテゴリ検索
    if search_category:
        snippets = snippets.filter(category=search_category)

    paginator = Paginator(snippets, consts.ITEM_PER_PAGE)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.page(page_num) 
    # 画面表示カテゴリをセット
    categories = dict(consts.SNIPPET_CAG)

    ctx = {
        'page_obj': page_obj,
        'categories': categories,
        'search_name': search_name,
        'search_category': search_category,
        'search_type': search_type
        }
    return render(request, template, ctx)
        








