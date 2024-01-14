from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .globals import NAVIGATION_PANE

# Dynamically generate urls from global NAVIGATION_PANE variable
urls = []
# Pick each key-value pair from the list
for key, value in NAVIGATION_PANE.items():
    # If there are no subcategories - create path for the main category
    if value["type"] == "str":
        urls.append(f"{key}")
    # For subcategories check links
    else:
        for subkey, subvalue in value["links"].items():
            urls.append(f"{subkey}")

# App name puts the website on /statistics101 url endpoint
app_name = "statistics101"
urlpatterns = [
    # Default landing page
    path("", views.index, name="index"),
    # User management pages
    path("/register", views.register, name="register"),
    path("/login", views.login_view, name="login"),
    path("/logout", views.logout_view, name="logout"),
    # Url to POST and upload user data file, gets called from Dropzone
    path("/processfile", views.process_file, name="process"),
    # Url used to dynamically output dataset, gets called via JS fetch
    path(
        "/dataset=<int:sampleid>&func=<str:function_name>",
        views.dataset,
        name="dataset",
    ),
    #
    # Url used to dynamically update charts via JS fetch
    path("/chart=<int:chartid>&func=<str:function_name>", views.chart, name="chart"),
    #
    # Add paths from navigation pane
    *[path(f"/{name}", getattr(views, name), name=name) for name in urls],
    # Add media path where uploaded files are stored
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
