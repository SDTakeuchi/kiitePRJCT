from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .filters import PostFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .decorators import unauthenticated_user, allowed_users
from django.core.mail import EmailMessage
from kiite_me.settings import EMAIL_HOST_USER
from . import forms
import random
#---------------below are for cropping the image
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import os
import json
import cv2
import base64
import requests
from django.core import files
from django.conf import settings
from django.http import HttpResponse
#--------forNewUser----------------
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.views import generic
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, DetailView
import re

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

def truncate(string, length, ellipsis='...'):
    return string[:length] + (ellipsis if string[length:] else '')

def homeView (request):
	random_num = random.randint(0,7)
	context = {'random_num':random_num}
	return render(request, 'home.html', context)

#-----auth section------------------------------------------------------

@unauthenticated_user
def signupView (request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('name')

			messages.success(request, "ようこそ" + username +"さん、アカウントが作成されました！")

			return redirect('login')

	context={'form':form}
	return render(request, 'signup.html', context)


@unauthenticated_user
def loginView (request):

	if request.method == 'POST':
		username = request.POST.get('email')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			article_url = request.GET.get('next')
			if article_url is not None:
				return redirect(article_url)
			if user.introduction == "まだプロフィールを記入していないようです、、、" or "":
				messages.success(request,"プロフィールの記入がまだのようです！マイページから記入しましょう！")
			return redirect('/posts/index')
		else:
			messages.info(request, "メールアドレスかパスワードが誤っています。")

	context={}
	return render(request, 'login.html', context)

def logoutView (request):
	logout(request)
	messages.success(request, "ログアウトしました")
	return redirect('login')


#-----post section------------------------------------------------------

@login_required(login_url='login')
def indexView (request):
    post_list = Post.objects.all().order_by('-date_created')
    if request.user.student_status == '在学生':
        post_list = post_list.filter(user=request.user)
    page = request.GET.get('page', 1)

    myFilter = PostFilter(request.GET, queryset=post_list)
    post_list = myFilter.qs

    numOneView = 10
    paginator = Paginator(post_list, numOneView)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    pageNum = int(page)
    fromNum = pageNum * numOneView - numOneView + 1
    toNum = pageNum * numOneView
    if toNum > len(post_list):
        toNum = int(len(post_list))

    context = {'posts':posts, 'myFilter':myFilter, 'post_list':post_list, 'fromNum':fromNum, 'toNum':toNum}
    return render(request, 'posts/index.html', context)

@login_required(login_url='login')
def indexOthersView (request):
    post_list = Post.objects.filter(is_public=True).order_by('-date_created')
    if request.user.student_status != '在学生':
        return redirect('postIndex')
    page = request.GET.get('page', 1)

    myFilter = PostFilter(request.GET, queryset=post_list)
    post_list = myFilter.qs

    numOneView = 10
    paginator = Paginator(post_list, numOneView)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    pageNum = int(page)
    fromNum = pageNum * numOneView - numOneView + 1
    toNum = pageNum * numOneView
    if toNum > len(post_list):
        toNum = int(len(post_list))

    context = {'posts':posts, 'myFilter':myFilter, 'post_list':post_list, 'fromNum':fromNum, 'toNum':toNum}
    return render(request, 'posts/index_others_q.html', context)

@login_required(login_url='login')
def showView (request, pk):
	post = get_object_or_404(Post, id=pk)
	comments = Comment.objects.filter(post=post).filter(is_reply_to__isnull=True)
	cmtbks = Comment.objects.filter(post=post).exclude(is_reply_to__isnull=True)
	context = {'post': post, 'comments':comments, 'cmtbks':cmtbks}
	if request.user.student_status == '在学生':
		if post.user != request.user:
			if post.is_public == False:
				return redirect('postIndex')
	return render(request, 'posts/show.html', context)

# class PostDetailView(DetailView):

# 	template_name = 'posts/show.html'
# 	model = Post
# 	context_object_name = 'post'

# 	def get_context_data(self, **kwargs):
# 		ctx = super().get_context_data(**kwargs)
# 		self.this_post = get_object_or_404(Post, pk=self.kwargs['pk'])
# 		ctx['comments'] = Comment.objects.filter(post=self.this_post).filter(is_reply_to__isnull=True)
# 		ctx['cmtbks'] = Comment.objects.filter(post=self.this_post).exclude(is_reply_to__isnull=True)
# 		return ctx


@login_required(login_url='login')
def newView (request):
	form = PostForm()
	current_user = request.user
	parent_category_list = AlumniJobParentCategory.objects.all()
	alumni_list = CustomUser.objects.filter(student_status='卒業生')
	offered_job_list = OfferedJobJoinTable.objects.all()

	available_parent_industry_list = []
	available_child_industry_list = []

	for alumni_current_industry in alumni_list:
		if int(alumni_current_industry.job_category.pk) not in available_child_industry_list:
			available_child_industry_list.append(int(alumni_current_industry.job_category.pk))
			if int(alumni_current_industry.job_category.parent.pk) not in available_parent_industry_list:
				available_parent_industry_list.append(int(alumni_current_industry.job_category.parent.pk))
			
	for offered_job in offered_job_list:
		if int(offered_job.offered_job_child_category.pk) not in available_child_industry_list:
			available_child_industry_list.append(int(offered_job.offered_job_child_category.pk))
			if int(offered_job.offered_job_parent_category.pk) not in available_parent_industry_list:
				available_parent_industry_list.append(int(offered_job.offered_job_parent_category.pk))


	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post_user = form.save(commit=False)
			post_user.user = current_user
			post_user.save()

			if post_user.requested_industry is not None:
				matching_join_table = OfferedJobJoinTable.objects.filter(
					offered_job_child_category=post_user.requested_industry
				)
				recepient_alumni = CustomUser.objects.filter(
					student_status='卒業生',
					job_category=post_user.requested_industry
				)
				recepient = []
				for alumni in recepient_alumni:
					if alumni not in recepient:
						recepient.append(alumni.email)

				for table in matching_join_table:
					if table.user not in recepient:
						recepient.append(table.user.email)

				context={'current_user':current_user,'post': post_user, 'requested_industry': post_user.requested_industry}

				subject = render_to_string('email_template/industry_requested/subject.txt', context)
				message = render_to_string('email_template/industry_requested/message.txt', context)

				# msg = EmailMessage(subject, message, EMAIL_HOST_USER, bcc=recepient)
				# msg.send()

			messages.info(request, "質問が投稿されました")
			return redirect('postIndex')

	context={
		'form':form,
		'parent_category_list': parent_category_list,
		'available_parent_industry_list': available_parent_industry_list,
		'available_child_industry_list': available_child_industry_list,
		}
	return render(request, 'posts/new.html', context)

@login_required(login_url='login')
def newMentionedView (request, pk):
	mentioned_user = CustomUser.objects.all().get(id = pk)
	if mentioned_user.can_ask == False:
		return redirect('postIndex')

	form = PostForm()
	current_user = request.user
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post_user = form.save(commit=False)
			post_user.user = current_user
			post_user.mentioned_user = mentioned_user
			post_user.save()

			context={'current_user':current_user,'post_user': post_user, 'mentioned_user':mentioned_user}

			subject = render_to_string('email_template/mentioned_post/subject.txt', context)
			message = render_to_string('email_template/mentioned_post/message.txt', context)

			recepient = str(mentioned_user.email)
			# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
			# msg.send()

			messages.info(request, "質問が投稿されました")
			return redirect('postIndex')

	context={'form':form, 'mentioned_user':mentioned_user}
	return render(request, 'posts/new.html', context)

@login_required(login_url='login')
def editView (request, pk):
	post = get_object_or_404(Post, id=pk)
	form = PostForm(instance=post)

	if post.user != request.user:
		return redirect('postIndex')

	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
			messages.info(request, "質問が編集されました")
			return redirect('postShow', pk=pk)

	context={'post':post,'form':form}
	return render(request, 'posts/edit.html', context)

@login_required(login_url='login')
def likeUnlikeCommentView(request, pk):
	comment = Comment.objects.get(id = pk)
	if comment.user == request.user:
		pass
	elif request.user in comment.like_user_list.all():
		comment.like_user_list.remove(request.user)
	elif comment.user is None:
		if not request.user in comment.like_user_list.all():
			comment.like_user_list.add(request.user)
	else:
		comment.like_user_list.add(request.user)
		context={'comment': comment, 'user': request.user, 'liked_user': comment.user}

		subject = render_to_string('email_template/like_comment/subject.txt',context)
		message = render_to_string('email_template/like_comment/message.txt',context)

		recepient = str(comment.user.email)
		# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
		# msg.send()

	return redirect('postShow', pk=comment.post.id)

@login_required(login_url='login')
def commentView (request, pk):
	post = Post.objects.get(id = pk)
	form = CommentForm()
	current_user = request.user

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment_instance = form.save(commit=False)
			comment_instance.user = current_user
			comment_instance.post = post
			comment_instance.save()

			if post.user != None:
				if comment_instance.user != post.user:
					comment_body = truncate(comment_instance.body, 200)
					context={'post':post,'comment_instance': comment_instance,'comment_body':comment_body}

					subject = render_to_string('email_template/newcomment/subject.txt')
					message = render_to_string('email_template/newcomment/message.txt',context)

					recepient = str(post.user.email)
					msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
					msg.send()

			messages.info(request, "コメントが投稿されました")
			return redirect('postShow', pk=post.id)

	context={'post':post,'form':form}
	return render(request, 'posts/comment.html', context)

@login_required(login_url='login')
def deleteCommentView(request, pk):
	comment = get_object_or_404(Comment, id=pk)
	comment.delete()
	messages.info(request, "コメントが削除されました")
	return redirect('postShow', pk=comment.post.id)

@login_required(login_url='login')
def editCommentView(request, pk):
	comment = Comment.objects.get(id = pk)
	form = CommentForm(instance=comment)
	post = comment.post

	if comment.user != request.user:
		return redirect('postIndex')

	if request.method == 'POST':
		form = CommentForm(request.POST, instance=comment)
		if form.is_valid():
			form.save()
			messages.info(request, "コメントが編集されました")
			return redirect('postShow', pk=comment.post.id)

	context={'comment':comment,'post':post, 'form':form}
	return render(request, 'posts/comment_edit.html', context)

@login_required(login_url='login')
def deleteView(request, pk):
	post = Post.objects.get(id = pk)

	if post.user != request.user:
		return redirect('postIndex')

	if request.method == 'POST':
		post.delete()
		messages.info(request, "質問が削除されました")
		return redirect('postIndex')

	context={'post':post}
	return render(request, 'posts/delete.html', context)

@login_required(login_url='login')
def commentBackView (request, pk):
	comment = Comment.objects.get(id=pk)
	post = comment.post
	form = CommentForm()
	current_user = request.user
	cmtbk_to_id = request.GET.get("comment_back")

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment_instance = form.save(commit=False)
			comment_instance.is_reply_to = comment
			if cmtbk_to_id is not None:
				replying_comment = Comment.objects.get(id=cmtbk_to_id)
				if replying_comment.user is not None:
					comment_instance.body = str(f' > {replying_comment.user.name}さん\r\n') + comment_instance.body
				else:
					comment_instance.body = ' > 退会済みユーザー\r\n' + comment_instance.body
			elif comment.user is not None:
				comment_instance.body = str(f' > {comment.user.name}さん\r\n') + comment_instance.body
			else:
				comment_instance.body = ' > 退会済みユーザー\r\n' + comment_instance.body
			comment_instance.user = current_user
			comment_instance.post = post
			comment_instance.save()

			comment_body = '\n'.join(comment_instance.body.splitlines()[1:])
			context={'post':post,'comment':comment,'comment_instance': comment_instance,'comment_body':comment_body}

			if Comment.objects.get(id=cmtbk_to_id).user is not None:
				recepient = str(Comment.objects.get(id=cmtbk_to_id).user.email)
				subject = render_to_string('email_template/commentback/subject.txt')
				message = render_to_string('email_template/commentback/message.txt',context)
				# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
				# msg.send()

			if comment.user is not None:
				if Comment.objects.get(id=cmtbk_to_id).user != comment.user:
					recepient = str(comment.user.email)
					subject = render_to_string('email_template/commentback/subject.txt')
					message = render_to_string('email_template/commentback/message.txt',context)
					# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
					# msg.send()

				if comment_instance.user != post.user and comment.user != post.user:
					recepient = str(post.user.email)
					subject = render_to_string('email_template/newcomment/subject.txt')
					message = render_to_string('email_template/newcomment/message.txt',context)
					# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
					# msg.send()

			messages.info(request, "コメントへの返信が投稿されました")
			return redirect('postShow', pk=post.id)

	context={'post':post,'comment':comment,'form':form}
	return render(request, 'posts/comment_back.html', context)

@login_required(login_url='login')
def reportPostView(request,pk):
	post = Post.objects.get(id = pk)
	form = forms.ContactForm()
	current_user = request.user

	if request.method == 'POST':
		form = forms.ContactForm(request.POST)
		context={'form':form}
		context={'post_or_comment':post, 'post':post, 'form':form,'current_user':current_user}
		subject = render_to_string('email_template/report/subject.txt')
		message = render_to_string('email_template/report/message.txt', context)
		# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
		# msg.send()
		messages.info(request, "運営にメッセージが送信されました")
		return redirect('postShow', pk=post.id)

	context={'post_or_comment':post, 'post':post, 'form':form,'current_user':current_user}
	return render(request, 'contact/report.html', context)

@login_required(login_url='login')
def reportCommentView(request,pk):
	comment = Comment.objects.get(id = pk)
	post = comment.post
	form = forms.ContactForm()
	current_user = request.user

	if request.method == 'POST':
		form = forms.ContactForm(request.POST)
		context={'post_or_comment':comment, 'post':post, 'form':form,'current_user':current_user}
		subject = render_to_string('email_template/report/subject.txt')
		message = render_to_string('email_template/report/message.txt', context)
		# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
		# msg.send()
		messages.info(request, "運営にメッセージが送信されました")
		return redirect('postShow', pk=post.id)

	context={'post_or_comment':comment, 'post':post, 'form':form,'current_user':current_user}
	return render(request, 'contact/report.html', context)

#-----user section------------------------------------------------------

@login_required(login_url='login')
def userListView(request,pk):
	user  = CustomUser.objects.get(id=pk)
	context={'user':user}
	return render(request, 'user/user_list.html', context)

@login_required(login_url='login')
def userMypageView(request):

	student = request.user
	context={'student':student}
	return render(request, 'user/mypage.html', context)

@login_required(login_url='login')
def userMypageEditView(request):

	student = request.user
	form = StudentForm(instance=student)
	formset = OfferedJobFormset(
		# queryset=OfferedJobJoinTable.objects.filter(user=student),
		instance=student
		)

	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, request.FILES, instance=student)
		if student.student_status == '卒業生':
			formset = OfferedJobFormset(request.POST, instance=student)

		if form.is_valid():
			form.save()
			if student.student_status == '卒業生' and formset.is_valid():
				formset.save()
			messages.info(request, "プロフィールが更新されました")
			return redirect('/user/mypage/')
		else:
			messages.error(request,'正しくフォームが入力されていないようです...')
			email = request.user.email
			context={
				'form':form,
				'formset':formset,
				'email':email,
				'DATA_UPLOAD_MAX_MEMORY_SIZE':settings.DATA_UPLOAD_MAX_MEMORY_SIZE
				}

			if student.student_status == '卒業生':
				job_parent_category = AlumniJobChildCategory.objects.get(customuser=request.user).parent.pk
				parent_category_list = AlumniJobParentCategory.objects.all()
				context['job_parent_category'] = job_parent_category
				context['parent_category_list'] = parent_category_list

			return render(request, 'user/mypage_edit.html', context)

	email = request.user.email

	context={
		'form':form,
		'formset':formset,
		'email':email,
		'DATA_UPLOAD_MAX_MEMORY_SIZE':settings.DATA_UPLOAD_MAX_MEMORY_SIZE
		}

	if student.student_status == '卒業生':
		job_parent_category = AlumniJobChildCategory.objects.get(customuser=request.user).parent.pk
		parent_category_list = AlumniJobParentCategory.objects.all()
		context['job_parent_category'] = job_parent_category
		context['parent_category_list'] = parent_category_list
		
	return render(request, 'user/mypage_edit.html', context)

@login_required(login_url='login')
def userDeleteView(request):
	student = request.user
	if request.method == 'POST':
		student.delete()
		messages.info(request, "ユーザーが削除されました")
		return redirect('home')

	return render(request, 'user/user_delete.html')
#----------policies-----------------

def termsOfUseView(request):
	return render(request, 'policies/terms_of_use.html')

def privacyPolicyView(request):
	return render(request, 'policies/privacy_policy.html')

#----------contact-----------------
BLACKLIST = [
	'amparo.maguire',
	'andersongervasi2985',
	'andersongervasi',
	'albertmcclellan3867',
	'baasiminvestment',
	'castlesarro8899',
	'charmainfarm',
	'coltonclevand',
	'coltonclevand80154'
	'coltonbourget',
	'coltonbourget80365',
	'contact',
	'eric.jones.z.mail',
	'eberlekinard7910',
	'frank.moye',
	'jamesfernando87516',
	'msrk4139',
	'no-replyVow',
	'nancyshaylahy',
	'harleayanderson96425',
	'oslerprato6887',
	'shareboss.jp',
	'tommyfishman35624',
	'woods.sharon',
]

def contactFormView(request):
	cont = forms.ContactForm()
	blacklistRegex = re.compile('([^@]+)')

	if request.method == 'POST':
		cont = forms.ContactForm(request.POST)
		recepient = str(cont['toEmail'].value())
		body = str(cont['body'].value())
		if "http" in body:
			return render(request, 'contact/contact_sent.html', {'recepient': recepient})
		if blacklistRegex.search(recepient).group() in BLACKLIST:
			return render(request, 'contact/contact_sent.html', {'recepient': recepient})
		subject = '【kiite-me】お問い合わせが送信されました ※自動送信です'
		message = '速やかに運営事務局よりご返信をお送りします！しばらくお待ちください。\n下記が送信されたメッセージです。\nーーーーーーーーーーーーーーーーーーーーーーーー\n\n'
		message += str(cont['title'].value())
		message += '\n'
		message += body
		message += '\n\n--\n====================================\n● 配信元：キイテミ運営事務局\n\n▼お問い合わせは下記までお願いいたします。\nキイテミ運営事務局\nkiiteme.info@gmail.com\n===================================='
		# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient], [EMAIL_HOST_USER])
		# msg.send()
		return render(request, 'contact/contact_sent.html', {'recepient': recepient})

	return render(request, 'contact/contact_form.html', {'form': cont})

@login_required(login_url='login')
def adminNotificationView(request):
	if not request.user.is_staff:
		return redirect('home')

	notiForm = forms.adminNotificationForm()
	if request.method == 'POST':
		notiForm = forms.adminNotificationForm(request.POST)
		subject = '【Kiite-me!】' + str(notiForm['title'].value())
		message = str(notiForm['toGroup'].value())
		message += '\n\n'
		message += str(notiForm['body'].value())
		message += '\n\n--\n\n====================================\n● 配信元：キイテミ運営事務局\n\n▼お問い合わせは下記までお願いいたします。\nキイテミ運営事務局\nkiiteme.info@gmail.com\n===================================='#署名

		if str(notiForm['toGroup'].value()) == 'ユーザーの皆様':
			recepient = CustomUser.objects.filter(is_active__isnull=False).values_list('email', flat=True)
		elif str(notiForm['toGroup'].value()) == 'スタッフの皆様':
			recepient = CustomUser.objects.filter(is_staff=True).values_list('email', flat=True)
		else:
			recepient = CustomUser.objects.filter(student_status__contains=str(notiForm['toGroup'].value()[5:7])).values_list('email', flat=True)
		recepient = list(recepient)
		msg = EmailMessage(subject, message, EMAIL_HOST_USER, bcc=recepient)
		# msg.send()
		return render(request, 'contact/sent_admin_notification.html', {'recepient': recepient})

	return render(request, 'contact/admin_notification.html', {'form': notiForm})

#below is for cropping the image

def save_temp_profile_image_from_base64String(imageString, user):
	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
			os.mkdir(settings.TEMP + "/" + str(user.pk))
		url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_PROFILE_IMAGE_NAME)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imageString)
		with storage.open('', 'wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		# workaround for an issue I found
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4)
			return save_temp_profile_image_from_base64String(imageString, user)
	return None

@login_required(login_url='login')
def crop_image(request, *args, **kwargs):
	payload = {}
	user = request.user
	if request.POST:
		try:
			imageString = request.POST.get("image")
			url = save_temp_profile_image_from_base64String(imageString, user)
			img = cv2.imread(url)

			cropX = int(float(str(request.POST.get("cropX"))))
			cropY = int(float(str(request.POST.get("cropY"))))
			cropWidth = int(float(str(request.POST.get("cropWidth"))))
			cropHeight = int(float(str(request.POST.get("cropHeight"))))
			if cropX < 0:
				cropX = 0
			if cropY < 0: # There is a bug with cropperjs. y can be negative.
				cropY = 0
			crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

			img_height = crop_img.shape[0]
			img_width = crop_img.shape[1]
			while img_width > 300 or img_height > 300:
				img_height = int(img_height*0.6)
				img_width = int(img_width*0.6)
				crop_img = cv2.resize(crop_img, (img_width, img_height))

			cv2.imwrite(url, crop_img, [cv2.IMWRITE_PNG_COMPRESSION, 1])

			# delete the old image
			user.profile_pic.delete()

			# Save the cropped image to user model
			user.profile_pic.save("profile_image.png", files.File(open(url, 'rb')))
			user.save()

			payload['result'] = "success"
			payload['cropped_profile_image'] = user.profile_pic.url

			# delete temp file
			os.remove(url)
			messages.info(request, "プロフィール画像が更新されました")

		except Exception as e:
			print("exception: " + str(e))
			payload['result'] = "error"
			payload['exception'] = str(e)
	return HttpResponse(json.dumps(payload), content_type="application/json")

# 下記Narito Blog様を参考に作成(仮登録機能)--https://blog.narito.ninja/detail/42/#url
class UserCreate(generic.CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    formset = OfferedJobFormset

    def get(self, request, **kwargs):
        # アクティブユーザーでなければログインページ
        formset = OfferedJobFormset(
                queryset=OfferedJobJoinTable.objects.none(),
        )
        if request.user.is_authenticated:
            return redirect('postIndex')
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset']              = self.formset
        context['parent_category_list'] = AlumniJobParentCategory.objects.all()
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        formset = OfferedJobFormset(
                data=self.request.POST,
                instance=user,
                queryset=AlumniJobParentCategory.objects.none()
                )
        user.save()

        if formset.is_valid():
                formset.save()

        if user.student_status == '卒業生':
            context={'user': user}
            subject = render_to_string('email_template/create_alumni/subject.txt', context)
            message = render_to_string('email_template/create_alumni/message.txt', context)

            recepient = str(user.email)
            msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient], bcc=[EMAIL_HOST_USER])
            msg.send()
            return redirect('signupAlumni')

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('email_template/create/subject.txt', context)
        message = render_to_string('email_template/create/message.txt', context)

        recepient = str(user.email)
        msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
        msg.send()

        return redirect('createDone')

def signupAlumni(request):
	return render(request, 'user/signup_alumni.html')

class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'user/create_done.html'

    def get(self, request, **kwargs):
        # アクティブユーザーでなければログインページ
        if request.user.is_authenticated:
            return redirect('postIndex')
        return super().get(request)

class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'user/create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    User = get_user_model()

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            context={}
            return render (request, 'user/went_wrong.html', context)

        # tokenが間違っている
        except BadSignature:
            context={}
            return render (request, 'user/went_wrong.html', context)

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return render (request, 'user/went_wrong.html', context)
            else:
                if not user.is_active:
                    # 問題なければ本登録とする

                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return render (request, 'user/went_wrong.html', context)

#--------------story-section-----------------------
def storyIndexView(request):
	articles = Article.objects.all().order_by('date_added')
	context = {'articles': articles}
	return render(request, 'story/story_index.html', context)

def story1View(request):
	return render(request, 'story/story1doug.html')

def story2View(request):
	return render(request, 'story/story2toda.html')

def storyShowView(request, pk):
	article = Article.objects.all().get(id = pk)
	return render(request, 'story/story_show.html',{'article': article})