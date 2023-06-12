from django.urls import path
from . import views
# from .views import SignUpView

urlpatterns = [

    path('schemas', views.schemas_home, name='exteor-schemas'),
    path('schemas-common', views.schemas_home_common, name='exteor-schemas-common'),
    path('schema-create', views.schema_create, name='schema-create'),
    path('schemas/<int:s_id>', views.schema_details, name='schema-detail'),
    path('schemas-common/<int:s_id>', views.schema_details_common, name='schema-detail-common'),
    path('schemas/<int:pk>/update', views.SchemaUpdateView.as_view(), name='schema-update'),
    path('schemas/<int:pk>/delete', views.SchemaDeleteView.as_view(), name='schema-delete'),
    path('schemas/<int:s_id>/const-create', views.const_create, name='const-create'),
    path('schemas/<int:s_id>/<int:c_id>/const-update', views.const_update, name='const-update'),
    path('schemas/<int:s_id>/<int:c_id>/const-delete', views.const_delete, name='const-delete'),
    path('schemas/<int:s_id>/<int:c_id>/const-view', views.const_view, name='const-view'),
    path('signup', views.SignUpView.as_view(), name="signup"),
    path('upload_file', views.upload_file, name="upload_success"),


    # path('', views.exteor_home, name='exteor-home'),
]