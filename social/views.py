from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from .models import Post,Comment, UserProfile
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import reversion
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from socialmedia import settings


class PostListView(View):
	def get(self,request,*args,**kwargs):
		following_list = []
		profiles = UserProfile.objects.all()
		current = request.user.profile
		for profile in profiles:
			if current in profile.followers.all():
				following_list += [profile]

		posts_all = Post.objects.all().order_by('-created_on')
		posts = []
		posts_secondary = []
		for post in posts_all:
			if post.author.profile in following_list:
				posts += [post]
			else:
				posts_secondary += [post]
		
		form = PostForm()
		context = {
			'post_list': posts,
			'posts_secondary': posts_secondary,
			'form' : form,
		}

		return render(request, 'social/post_list.html', context)

	def post(self,request,*args,**kwargs):
		posts = Post.objects.all().order_by('-created_on')
		form = PostForm(request.POST)

		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			##body = Version(text = new_post.body, post = new_post)
			new_post.save()
			for userr in new_post.author.profile.mail_followers.all():
				message = Mail(
   				 			   from_email='aadit.nayyar@gmail.com',
    						   to_emails=userr.email,
    						   subject='New Post',
    						   html_content='<strong>Check out a new post by ' + userr.profile.name + ' at Thor!</strong><p>' + userr.profile.name+':'+new_post.body + '</p>')
			try:
				sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
				response = sg.send(message)
				print(response.status_code)
				print(response.body)
				print(response.headers)
			except Exception as e:
				print(e.message)
			##body.save()
		context = {
			'post_list': posts,
			'form' : form,
		}

		return render(request, 'social/post_list.html', context)

class PostDetailView(View):
	def get(self,request,pk,*args,**kwargs):
		post = Post.objects.get(pk=pk)
		comments = Comment.objects.all().filter(post=post).order_by('-created_on')
		form = CommentForm()

		context = {
			'post': post,
			'comments':comments,
			'form':form,
			'post_author':post.author,
		}

		return render(request, 'social/post_detail.html',context)

	def post(self,request,pk,*args,**kwargs):
		post = Post.objects.get(pk=pk)
		form = CommentForm(request.POST)

		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.author = request.user
			new_comment.save()

		comments = Comment.objects.all().filter(post=post).order_by('-created_on')
		context = {
			'post': post,
			'form' : form,
			'comments':comments,
		}

		return render(request, 'social/post_detail.html', context)

class PostEditView(UserPassesTestMixin,UpdateView):
	model = Post
	template_name = 'social/edit_post.html'
	fields = ['body']
	# def get_object(self, queryset=None):
	# 	obj = super(PostEditView, self).get_object(queryset)
	# 	#body = Version.objects.create(text = obj.body, post =obj)
	# 	#body.save()
	# 	obj.save()
	# 	return obj
	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse('post-detail', kwargs={'pk':pk})
	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class PostDeleteView(UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/social'

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class ProfileView(View):
	def get(self, request, pk, *args, **kwargs):
		form = PostForm()
		profile = UserProfile.objects.get(pk=pk)
		username = profile.name
		bio = profile.bio
		user = profile.user
		current_user = request.user
		posts = Post.objects.filter(author = user).order_by('-created_on')
		is_following = False
		followers = profile.followers.all()
		number_of_followers = len(followers)
		for follower in followers:
			if follower == request.user:
				is_following = True
				break

		is_mail_following = False
		for mail_follower in profile.mail_followers.all():
			if mail_follower == request.user:
				is_mail_following = True
				break

		context = {
		'posts': posts,
		'form':form,
		'name':username,
		'bio':bio,
		'profile_user':user,
		'profile': profile,
		'user' : current_user,
		'is_following' : is_following,
		'is_mail_following' : is_mail_following,
		'number_of_followers' : number_of_followers,
		}
		return render(request, 'social/profile.html', context)

	def post(self,request,pk,*args,**kwargs):
		profile = UserProfile.objects.get(pk=pk)
		username = profile.name
		bio = profile.bio
		user = profile.user
		current_user = request.user
		posts = Post.objects.filter(author = user).order_by('-created_on')
		form = PostForm(request.POST)

		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			##body = Version(text = new_post.body, post = new_post)
			new_post.save()
			##body.save()
		context = {
		'posts': posts,
		'form':form,
		'name':username,
		'bio':bio,
		'profile_user':user,
		'profile': profile,
		'user' : current_user,
		}

		return render(request, 'social/profile.html', context)

class ProfileEditView(UserPassesTestMixin, UpdateView):
	model = UserProfile
	template_name = 'social/profile_edit.html'
	fields = ['name','bio','dp']
	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('profile', kwargs={'pk':pk})

	def test_func(self):
		profile = self.get_object()
		return self.request.user == profile.user

class AddFollowing(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		user = self.request.user
		profile.followers.add(user)
		return redirect('profile', pk=profile.pk)

class AddMailFollowing(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		user = self.request.user
		profile.mail_followers.add(user)
		print('x')
		return redirect('profile', pk=profile.pk)

class RemoveFollowing(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		user = self.request.user
		profile.followers.remove(user)
		if user in profile.mail_followers.all():
			profile.mail_followers.remove(user)

		return redirect('profile', pk=profile.pk)

class RemoveMailFollowing(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		user = self.request.user
		profile.mail_followers.remove(user)

		return redirect('profile', pk=profile.pk)

	# def test_func(self):
	# 	profile = UserProfile.objects.get(pk=pk)
	# 	user = request.user
	# 	is_following = False
	# 	followers = profile.followers.all()
	# 	for follower in followers:
	# 		if follower == request.user:
	# 			is_following = True
	# 			break
	# 	return is_following

class UserSearch(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
			query = self.request.GET.get('query')
			query.strip()
			profile_list = UserProfile.objects.all()
			for profile in profile_list:
				if profile.user.username == query:
					return redirect('profile', pk = profile.pk)

			next = request.GET.get('next','/')
			return HttpResponseRedirect(next)
		
class FollowerListView(LoginRequiredMixin, View):
	def get(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		followers_list = profile.followers.all()

		context = {'followers_list':followers_list, 'profile_user' : profile.user}
		return render(request, 'social/follower_list.html',context)

