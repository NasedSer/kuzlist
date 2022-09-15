from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('oks/<int:pk>', OksViewUpdate.as_view(), name='oks_update'),
    path('add_to_per/<int:pk_obj>', ObjPerCreate.as_view(), name='add_to_per'),
    path('tips', TipListView.as_view(), name='tips'),
    path('tip/<int:tip_id>', OksTipListView.as_view(), name='tip'),
    path('addtip', add_tip, name='add_tip'),
    path('export_xls', export_xls, name='export_to_xls'),
    path('export_xml', export_xml, name='export_to_xml'),
    path('export_word/<int:pk>', export_word, name='export_word'),
    path('add_obj', OksListView.as_view(), name='add_obj'),
    path('add_obj_inline', OksViewCreate.as_view(), name='add_obj_inline'),
    path('', PerListGestView.as_view(), name='home'),
    path('per', PerListView.as_view(), name='per'),
    path('list_add_to_per', ObjsAddToPerListView.as_view(), name='add_obj_to_per'),
    path('years/add/', YearPerCreate.as_view(), name='year-add'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
]