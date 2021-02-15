from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('snippets/', views.snippet_list, name='snippet_list'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)



# def some_func(argg1, arg2, arg3=1, arg4=2):
#     pass

# some_func(1, 2, 3, 4)
# some_func(argg1=1, argg2=2, argg3=3, argg4=4)

# args = [1, 2, 3, 4]
# some_func(*args)

# kwargs = {
#     'arg1': 1,
#     'arg2': 2,
#     'arg3': 3,
#     'arg4': 4,
# }

# some_func(**kwargs)s