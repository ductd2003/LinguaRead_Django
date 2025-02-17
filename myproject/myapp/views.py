from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib import messages
from .utils import check_password_with_salt, login_required_custom
from django.utils.timezone import now
from django.core.paginator import Paginator
from .forms import *
from django.core.cache import cache
from datetime import datetime
from types import SimpleNamespace
import base64
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import re
from django.utils.html import mark_safe



def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Lấy thông tin người dùng từ database
            user = Users.objects.get(username=username)

            # Kiểm tra mật khẩu
            if check_password_with_salt(password, user.passwordhash):
                # Lưu thông tin vào session
                request.session['userid'] = user.userid
                request.session['username'] = user.username

                # Chuyển hướng tới trang dashboard
                return redirect('/manager/dashboard/')
            else:
                messages.error(request, 'Sai mật khẩu!')
        except Users.DoesNotExist:
            messages.error(request, 'Người dùng không tồn tại!')

    return render(request, 'manager/login.html')

def admin_logout(request):
    request.session.flush()  # Xóa toàn bộ session
    return redirect('/manager/admin-login/')

@login_required_custom
def dashboard(request):
    # Xử lý yêu cầu xóa cache
    if request.method == "POST" and request.POST.get('action') == "clear_cache":
        cache.delete_pattern('user_posts_list_*')  # Xóa toàn bộ cache liên quan
        message = "Cache đã được xóa thành công!"
    else:
        message = None

    # Lấy tổng số lượt xem
    total_views = Sitestats.objects.first().totalviews if Sitestats.objects.exists() else 0

    # Lấy tổng số bài viết
    total_posts = Posts.objects.count()

    return render(request, 'manager/dashboard.html', {
        'total_views': total_views,
        'total_posts': total_posts,
        'message': message,  # Gửi thông báo nếu cần
    })

def manage_post(request):
    """
    Hiển thị danh sách bài viết, tìm kiếm theo ID, và phân trang.
    """
    # Lấy từ khóa tìm kiếm từ request
    search_query = request.GET.get('search', '')

    # Lọc danh sách bài viết theo ID (nếu có tìm kiếm)
    if search_query:
    # Lọc theo Post ID và sắp xếp theo ngày mới nhất
        posts = Posts.objects.filter(postid=search_query).order_by('-createdat')
    else:
    # Sắp xếp tất cả bài viết theo ngày mới nhất
        posts = Posts.objects.all().order_by('-createdat')


    # Phân trang: mỗi trang 10 bài viết
    paginator = Paginator(posts, 9)  # 10 bài viết mỗi trang
    page_number = request.GET.get('page')  # Lấy số trang hiện tại từ query parameters
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        # Xử lý tạo bài viết mới
        Posts.objects.create(
            createdat=now(),
            updatedat=now(),
            authorid_id=request.session.get('userid'),  # Lấy ID người dùng từ session
            status='Draft',
        )
        return redirect('manage_post')  # Chuyển hướng lại danh sách bài viết

    return render(request, 'manager/manage-post.html', {'page_obj': page_obj, 'search_query': search_query})

def publish_post(request, post_id):
    """
    Cập nhật trạng thái bài viết thành Published.
    """
    # Lấy bài viết theo ID
    post = get_object_or_404(Posts, postid=post_id)
    
    # Cập nhật trạng thái bài viết
    post.status = 'Published'
    post.save()
    
    # Chuyển hướng lại danh sách bài viết
    return redirect('manage_post')

def revert_to_draft(request, post_id):
    """
    Cập nhật trạng thái bài viết về Draft.
    """
    # Lấy bài viết theo ID
    post = get_object_or_404(Posts, postid=post_id)
    
    # Cập nhật trạng thái bài viết
    post.status = 'Draft'
    post.save()
    
    # Chuyển hướng lại danh sách bài viết
    return redirect('manage_post')

def update_image(request, post_id):
    if request.method == 'POST' and request.FILES.get('image'):
        post = get_object_or_404(Posts, pk=post_id)
        image_file = request.FILES['image']
        post.image = base64.b64encode(image_file.read()).decode('utf-8')
        post.save()
        return JsonResponse({'message': 'Image updated successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def levels_list(request):
    levels = Levels.objects.all()
    return render(request, 'manager/manage-level.html', {'levels': levels})

def levels_save(request):
    if request.method == 'POST':
        if 'id' in request.POST and request.POST['id']:
            level = get_object_or_404(Levels, pk=request.POST['id'])
            form = LevelsForm(request.POST, instance=level)
        else:
            form = LevelsForm(request.POST)
        if form.is_valid():
            level = form.save()
            return JsonResponse({'status': 'success', 'id': level.levelid, 'name': level.levelname})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def languages_list(request):
    languages = Languages.objects.all()
    return render(request, 'manager/manage-language.html', {'languages': languages})

def languages_save(request):
    if request.method == 'POST':
        if 'id' in request.POST and request.POST['id']:
            language = get_object_or_404(Languages, pk=request.POST['id'])
            form = LanguagesForm(request.POST, instance=language)
        else:
            form = LanguagesForm(request.POST)
        if form.is_valid():
            language = form.save()
            return JsonResponse({'status': 'success', 'id': language.languageid, 'name': language.languagename})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def postcontent_list(request):
    query = request.GET.get('search', '')  # Lấy giá trị tìm kiếm từ request
    postcontents = Postcontent.objects.all()
    
    if query:  # Nếu có tìm kiếm, lọc kết quả theo ID
        postcontents = postcontents.filter(postid=query)
    
    levels = Levels.objects.all()
    languages = Languages.objects.all()
    
    # Phân trang với 10 bản ghi mỗi trang
    paginator = Paginator(postcontents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'manager/add-post-content.html', {
        'page_obj': page_obj,
        'levels': levels,
        'languages': languages,
        'search': query,  # Truyền giá trị tìm kiếm về template để hiển thị lại
    })

def postcontent_save(request):
    if request.method == 'POST':
        if 'id' in request.POST and request.POST['id']:
            postcontent = get_object_or_404(Postcontent, pk=request.POST['id'])
            form = PostcontentForm(request.POST, instance=postcontent)
        else:
            form = PostcontentForm(request.POST)
        if form.is_valid():
            postcontent = form.save()
            return JsonResponse({
                'status': 'success',
                'id': postcontent.postcontentid,
                'postid': postcontent.postid_id,  # Chỉ trả về ID của Post
                'languageid': postcontent.languageid.languageid,
                'levelid': postcontent.levelid.levelid,
                'title': postcontent.title,
                'content': postcontent.content,
                })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def manage_postcontent_detail(request, pk):
    # Lấy dữ liệu từ cơ sở dữ liệu
    postcontent = get_object_or_404(Postcontent, pk=pk)
    return JsonResponse({
        'id': postcontent.postcontentid,
        'postid': postcontent.postid_id,  # Chỉ lấy ID
        'languageid': postcontent.languageid.languageid,
        'levelid': postcontent.levelid.levelid,
        'title': postcontent.title,
        'content': postcontent.content,
    })

@csrf_exempt
def question_manager(request):
    # Xử lý kiểm tra câu hỏi
    if request.method == 'POST' and 'check_post_content_id' in request.POST:
        post_content_id = request.POST.get('check_post_content_id')
        if not post_content_id:
            return JsonResponse({'success': False, 'error': 'Vui lòng nhập PostContent ID'})

        try:
            post_content_id = int(post_content_id)
            post_content = get_object_or_404(Postcontent, pk=post_content_id)
            questions = Questions.objects.filter(postcontentid=post_content)
            html = render_to_string('manager/partial_questions_list.html', {'questions': questions})
            return JsonResponse({'success': True, 'html': html})
        except (ValueError, Postcontent.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'PostContent không tồn tại hoặc ID không hợp lệ'})

    # Xử lý thêm câu hỏi
    if request.method == 'POST' and 'add_post_content_id' in request.POST:
        post_content_id = request.POST.get('add_post_content_id')
        question_text = request.POST.get('question_text')
        answer = request.POST.get('answer')

        if not post_content_id or not question_text or not answer:
            return JsonResponse({'success': False, 'error': 'Vui lòng điền đầy đủ thông tin'})

        try:
            post_content_id = int(post_content_id)
            post_content = get_object_or_404(Postcontent, pk=post_content_id)
            new_question = Questions(
                postcontentid=post_content,
                questiontext=question_text,
                answer=answer
            )
            new_question.save()
            return JsonResponse({'success': True, 'message': 'Câu hỏi đã được thêm thành công!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # Xử lý cập nhật câu hỏi
    if request.method == 'POST' and 'update_question_id' in request.POST:
        question_id = request.POST.get('update_question_id')
        question_text = request.POST.get('question_text')
        answer = request.POST.get('answer')

        if not question_id or not question_text or not answer:
            return JsonResponse({'success': False, 'error': 'Vui lòng điền đầy đủ thông tin để cập nhật'})

        try:
            question = get_object_or_404(Questions, pk=question_id)
            question.questiontext = question_text
            question.answer = answer
            question.save()
            return JsonResponse({'success': True, 'message': 'Câu hỏi đã được cập nhật thành công!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'manager/manage-question.html')


# ---------------------------------

def get_levels_and_languages():
    # Lấy levels từ cache
    levels = cache.get('levels')
    if not levels:
        levels = Levels.objects.all()
        cache.set('levels', levels, 60 * 60 * 24)  # Cache 24 giờ
        print("Cache for levels has been updated.")

    # Lấy languages từ cache
    languages = cache.get('languages')
    if not languages:
        languages = Languages.objects.all()
        cache.set('languages', languages, 60 * 60 * 24)  # Cache 24 giờ
        print("Cache for languages has been updated.")

    return levels, languages


def refresh_levels_and_languages_cache():
    # Làm mới cache bằng cách gọi `get_levels_and_languages`
    get_levels_and_languages()
    print("Cache for levels and languages has been refreshed.")


def user_posts_list(request):
    level_id = request.GET.get('levelId', 1)
    language_id = request.GET.get('languageId', 1)
    search = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)

    today = datetime.now().date()
    cache_key = f"user_posts_page_{today}_{level_id}_{language_id}_{search}_{page_number}"

    cached_page = cache.get(cache_key)
    if cached_page:
        return render(request, 'user/list-posts.html', cached_page)

    postcontents = Postcontent.objects.filter(
        levelid_id=level_id,
        languageid_id=language_id,
        title__icontains=search
    )

    posts = Posts.objects.filter(
        postid__in=postcontents.values('postid'),
        status='Published'
    ).order_by('-createdat')

    # Lấy Postcontent tương ứng với languageid và levelid đã chọn
    for post in posts:
        post.selected_postcontent = post.postcontent_set.filter(
            languageid_id=language_id,
            levelid_id=level_id
        ).first()

    paginator = Paginator(posts, 10)  # 10 bài viết mỗi trang
    page_obj = paginator.get_page(page_number)

    levels, languages = get_levels_and_languages()

    context = {
        'page_obj': page_obj,
        'levels': levels,
        'languages': languages,
        'selected_level': int(level_id),
        'selected_language': int(language_id),
        'search': search,
    }

    remaining_time_today = (datetime.combine(today, datetime.max.time()) - datetime.now()).seconds
    cache.set(cache_key, context, remaining_time_today)

    return render(request, 'user/list-posts.html', context)


def user_post_detail(request):
    post_id = int(request.GET.get('postId', 1))
    level_id = int(request.GET.get('levelId', 1))
    language_id = int(request.GET.get('languageId', 1))

    try:
        postcontent = Postcontent.objects.get(
            postid_id=post_id,
            levelid_id=level_id,
            languageid_id=language_id
        )
        post = Posts.objects.get(postid=post_id)
        post_image = post.image
        post_title = postcontent.title
        post_description = postcontent.content[:150]

        # Lấy danh sách câu hỏi
        questions = Questions.objects.filter(postcontentid=postcontent)

        processed_questions = []
        for question in questions:
            question_html = question.questiontext  # Giữ nguyên HTML

            # Tìm vị trí của phần đáp án (sau "::::")
            split_match = re.search(r'(.*?)<p>::::(.+)</p>', question_html, re.DOTALL)
            
            if split_match:
                question_text = split_match.group(1).strip()  # Giữ nguyên phần câu hỏi (HTML)
                answers_text = split_match.group(2).strip()  # Lấy danh sách đáp án

                # Tách đáp án bằng "::::" và giữ nguyên định dạng
                answer_list = [ans.strip() for ans in answers_text.split("::::")]

                processed_questions.append({
                    "question": mark_safe(question_text),  # Giữ nguyên HTML
                    "answers": answer_list,
                    "answer": question.answer
                })
            else:
                # Nếu không tìm thấy "::::", giữ nguyên question_html
                processed_questions.append({
                    "question": mark_safe(question_html),
                    "answers": [],
                    "answer": question.answer
                })

    except Postcontent.DoesNotExist:
        postcontent = SimpleNamespace(
            title='Xin lỗi, không tìm thấy bài viết',
            content='Bài viết bạn đang tìm không tồn tại hoặc đã bị xóa.'
        )
        post = Posts.objects.get(postid=post_id)
        post_image = post.image
        post_title = 'Bài viết không tồn tại'
        post_description = 'Bài viết bạn đang tìm không tồn tại hoặc đã bị xóa.'
        processed_questions = []

    levels, languages = get_levels_and_languages()

    return render(request, 'user/post-detail.html', {
        'postcontent': postcontent,
        'levels': levels,
        'languages': languages,
        'selected_level': level_id,
        'selected_language': language_id,
        'postId': post_id,
        'post_image': post_image,
        'post_title': post_title,
        'post_description': post_description,
        'questions': processed_questions
    })


def about_us(request):
    return render(request, "user/about-us.html")
