from django.conf.urls import url
from app import views

# Template urls
app_name = "app"

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^home', views.home, name='home'),
    url(r'^clusters', views.clusters, name='clusters'),
    url(r'^page_cluster', views.page_cluster, name='page_cluster'),
    url(r'^filters', views.filters, name='filters'),
    # url(r'^list_catalogs', views.list_catalogs, name='list_catalogs'),
    url(r'^schedule_process', views.schedule_process, name='schedule_process'),
    url(r'^process_catalog_finished', views.process_catalog_finished, name='process_catalog_finished'),
    url(r'^publish_catalog', views.publish_catalog, name='publish_catalog'),
    url(r'^set_catalog', views.set_catalog, name='set_catalog'),
    url(r'^get_catalog_info', views.get_catalog_info, name='get_catalog_info'),
    url(r'^get_statistics_info', views.get_statistics_info, name='get_statistics_info'),
    url(r'^testebq', views.testebq, name='testebq'),
    url(r'^set_row_main', views.set_row_main, name='set_row_main'),
    url(r'^set_wrong', views.set_wrong, name='set_wrong'),
    url(r'^set_comment', views.set_comment, name='set_comment'),
    url(r'^get_comment', views.get_comment, name='get_comment'),
    url(r'^report_n1_headers', views.report_n1_headers, name='report_n1_headers'),
    url(r'^report_n2_headers', views.report_n2_headers, name='report_n2_headers'),
    url(r'^report_n1_items', views.report_n1_items, name='report_n1_items'),
    url(r'^report_n2_items', views.report_n2_items, name='report_n2_items'),
    url(r'^settings', views.settings, name='settings'),
    url(r'^report', views.report, name='report'),
    url(r'^graph', views.graph, name='graph'),
    url(r'^graph_render', views.graph_render, name='graph_render'),
    url(r'^set_filter', views.set_filter, name='set_filter'),
    url(r'^clear_filters', views.clear_filters, name='clear_filters'),
    url(r'^quantity_per_page', views.quantity_per_page, name='quantity_per_page'),
    url(r'^set_quantity_per_page', views.set_quantity_per_page, name='set_quantity_per_page'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
