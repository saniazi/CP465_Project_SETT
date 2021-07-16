from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
 
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func

def allowed_users(allowed=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			for user in allowed:
				if hasattr(request.user, user):
					return view_func(request, *args, **kwargs)
			raise PermissionDenied
		return wrapper_func
	return decorator 