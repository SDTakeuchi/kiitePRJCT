from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .filters import PostFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .decorators import unauthenticated_user, allowed_users
from django.core.mail import EmailMessage
from kiite_me.settings import EMAIL_HOST_USER
from . import forms
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

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"
# Create your views here.
def homeView (request):
	return render(request, 'home.html')
	
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
			if user.introduction == "まだプロフィールを記入していないようです、、、" or "":
				messages.success(request,"プロフィールの記入がまだのようです！マイページから記入しましょう！")   ###########
			return redirect('postIndex')
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
	all_posts = Post.objects.all().order_by('-date_updated')

	myFilter = PostFilter(request.GET, queryset=all_posts)
	all_posts = myFilter.qs

	paginator = Paginator(all_posts, 10) # 1ページに10件表示
	p = request.GET.get('p') # URLのパラメータから現在のページ番号を取得
	posts = paginator.get_page(p) # 指定のページのPostを取得

	context = {'posts':posts, 'myFilter':myFilter, 'all_posts':all_posts}
	return render(request, 'posts/index.html', context)

@login_required(login_url='login')
def showView (request, pk):
	post = Post.objects.get(id=pk)
	return render(request, 'posts/show.html', {'post':post})

@login_required(login_url='login')
def newView (request):
	form = PostForm()
	current_user = request.user
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post_user = form.save(commit=False)
			post_user.user = current_user
			post_user.save()
			messages.info(request, "質問が投稿されました")
			return redirect('postIndex')
#.save(commit=False) this is so helpful...

	context={'form':form}
	return render(request, 'posts/new.html', context)

@login_required(login_url='login')
def editView (request, pk):
	post = Post.objects.get(id = pk)
	form = PostForm(instance=post)

	if post.user != request.user:
		return redirect('postIndex')

	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
			messages.info(request, "質問が編集されました")
			return redirect('/posts/index')

	context={'post':post,'form':form}
	return render(request, 'posts/edit.html', context)

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

			# subject = '【kiite-me】質問にコメントがつきました！'
			# message = str(f'{post.user.name}さんの質問「{post.title}」に{comment_instance.user.name}さんからのコメントがつきました！\n\nログインして確認してください。\nhttps://kiite-me.site/login/')
			# message += '\n\n--\n====================================\n● 配信元：キイテミ運営事務局\n\n▼お問い合わせは下記までお願いいたします。\nキイテミ運営事務局\nkiiteme.info@gmail.com\n===================================='#署名
			# recepient = str(post.user.email)
			# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
			# msg.send()

			messages.info(request, "コメントが投稿されました")
			return redirect('postShow', pk=post.id)

	context={'post':post,'form':form}
	return render(request, 'posts/comment.html', context)

@login_required(login_url='login')
def deleteCommentView(request, pk):
	comment = Comment.objects.get(id = pk)
	comment.delete()
	messages.info(request, "コメントが削除されました")
	return redirect('postShow', pk=comment.post.id)

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
	comment = Comment.objects.get(id = pk)
	post = comment.post
	form = CommentForm()
	current_user = request.user

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment_instance = form.save(commit=False)
			comment_instance.body = str(f' > {comment.user.name}\r\n') + comment_instance.body
			comment_instance.user = current_user
			comment_instance.post = post
			comment_instance.save()

			# subject = '【kiite-me】コメントに返信がつきました！'
			# message = str(f'{comment.user.name}さんの「{post.title}」へのコメントに{comment_instance.user.name}さんから返信が届きました！\n\nログインして確認してください。\nhttps://kiite-me.site/login/')
			# message += '\n\n--\n====================================\n● 配信元：キイテミ運営事務局\n\n▼お問い合わせは下記までお願いいたします。\nキイテミ運営事務局\nkiiteme.info@gmail.com\n===================================='#署名
			# recepient = str(post.user.email)
			# msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
			# msg.send()

			messages.info(request, "コメントへの返信が投稿されました")
			return redirect('postShow', pk=post.id)

	context={'post':post,'comment':comment,'form':form}
	return render(request, 'posts/comment_back.html', context)

	
#-----user section------------------------------------------------------

@login_required(login_url='login')           ####################
def userListView(request,pk):
	user  = CustomUser.objects.get(id=pk)   
	context={'user':user}
	return render(request, 'user/user_list.html', context)           ####################

@login_required(login_url='login')
def userMypageView(request):
	
	student = request.user
	context={'student':student}
	return render(request, 'user/mypage.html', context)
	
@login_required(login_url='login')
def userMypageEditView(request):
	
	student = request.user
	form = StudentForm(instance=student)

	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, request.FILES, instance=student)
		if form.is_valid():
			form.save()
			messages.info(request, "プロフィールが更新されました")
			return redirect('/user/mypage/')
		else:
			messages.error(request,'正しくフォームが入力されていないようです...')

	email = request.user.email
	context={'form':form, 'email':email, 'DATA_UPLOAD_MAX_MEMORY_SIZE':settings.DATA_UPLOAD_MAX_MEMORY_SIZE}
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

def contactFormView(request):

	cont = forms.ContactForm()

	if request.method == 'POST':
		# cont = forms.ContactForm(request.POST)
		# subject = '【kiite-me】お問い合わせが送信されました ※自動送信です'
		# message = '速やかに運営事務局よりご返信をお送りします！しばらくお待ちください。\n下記が送信されたメッセージです。\nーーーーーーーーーーーーーーーーーーーーーーーー\n\n'
		# message += str(cont['title'].value())
		# message += '\n'
		# message += str(cont['body'].value())
		# message += '\n\n--\n====================================\n● 配信元：キイテミ運営事務局\n\n▼お問い合わせは下記までお願いいたします。\nキイテミ運営事務局\nkiiteme.info@gmail.com\n===================================='#署名
		# recepient = str(cont['toEmail'].value())
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
		# notiForm = forms.adminNotificationForm(request.POST)
		# subject = '【kiite-me】' + str(notiForm['title'].value())
		# message = str(notiForm['toGroup'].value())
		# message += '\n'
		# message += str(notiForm['body'].value())
		# message += '\n\n--\n====================================\n● 配信元：キイテミ運営事務局\n\n▼お問い合わせは下記までお願いいたします。\nキイテミ運営事務局\nkiiteme.info@gmail.com\n===================================='#署名

		# if str(notiForm['toGroup'].value()) == 'ユーザーの皆様':
		# 	recepient = CustomUser.objects.filter(is_active__isnull=False).values_list('email', flat=True)
		# elif str(notiForm['toGroup'].value()) == 'ユーザー（在学生）の皆様' or str(notiForm['toGroup'].value()) == 'ユーザー（卒業生）の皆様':
		# 	recepient = CustomUser.objects.filter(student_status__contains=str(notiForm['toGroup'].value()))
		# elif  str(notiForm['toGroup'].value()) == 'スタッフの皆様':
		# 	recepient = CustomUser.objects.filter(is_staff=True).values_list('email', flat=True)
		# recepient = list(recepient)
		# msg = EmailMessage(subject, message, EMAIL_HOST_USER, bcc=recepient)
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

			cv2.imwrite(url, crop_img)

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