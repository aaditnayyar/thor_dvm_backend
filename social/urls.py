from django.urls import path
from .views import PostListView, PostDetailView, PostEditView, PostDeleteView, ProfileView, ProfileEditView, AddFollowing, RemoveFollowing, UserSearch, FollowerListView
from .views import AddMailFollowing, RemoveMailFollowing

urlpatterns = [
	path('', PostListView.as_view(), name='post-list'),
	path('post/<int:pk>',PostDetailView.as_view(), name = 'post-detail'),
	path('post/<int:pk>/edit',PostEditView.as_view(), name = 'post-edit'),
	path('post/<int:pk>/delete',PostDeleteView.as_view(), name = 'post-delete'),
	path('profile/<int:pk>',ProfileView.as_view(), name = 'profile'),
	path('profile/<int:pk>/edit',ProfileEditView.as_view(), name = 'profile-edit'),
	path('profile/<int:pk>/follow',AddFollowing.as_view(), name = 'follow'),
	path('profile/<int:pk>?unfollow',RemoveFollowing.as_view(), name = 'unfollow'),
	path('profile/search',UserSearch.as_view(),name = 'user-search'),
	path('profile/<int:pk>/followers',FollowerListView.as_view(), name = 'followers-list'),
	path('profile/<int:pk>/mail-follow',AddMailFollowing.as_view(), name = 'mail-follow'),
	path('profile/<int:pk>?mail-unfollow',RemoveMailFollowing.as_view(), name = 'mail-unfollow'),
]
