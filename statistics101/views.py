import json
import logging
import os
import re

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .globals import *
from .utils import *
from .utils_async import *
from .utils_upload import *

infologer = logging.getLogger("django")
warninger = logging.getLogger("django.request")
debugger = logging.getLogger("django.template")

# ----------------------------------------------------------------------------
# This module contains all views that are reachable via endpoints in urls.py
# ----------------------------------------------------------------------------


def index(request):
    """
    Function for the main landing page
    """
    source_1 = get_source_number(1) + 1
    source_2 = get_source_number(2) + 1
    source_10 = get_source_number(10) + 1

    return render(
        request,
        "statistics101/index.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "source_2": source_2,
            "source_10": source_10,
        },
    )


# ----------------------------------------------------------------------------
# All access points to templates in alphabetical order
# ----------------------------------------------------------------------------


def barchart(request):
    # Get the user id
    if request.user.is_anonymous:
        usr = None
    else:
        usr = User.objects.get(id=request.user.id)

    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1

    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=1, upload_complete=True
    )
    proportions = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=2, upload_complete=True
    )
    surveys = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=3, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/barchart.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "timeseries": timeseries,
            "proportions": proportions,
            "surveys": surveys,
            "chart": "",  # placeholder for where the async chart html will be added
        },
    )


def boxplot(request):
    # Get the user id
    if request.user.is_anonymous:
        usr = None
    else:
        usr = User.objects.get(id=request.user.id)

    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1
    source_11 = get_source_number(11) + 1
    source_12 = get_source_number(12) + 1

    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=1, upload_complete=True
    )
    surveys = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=3, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/boxplot.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "source_11": source_11,
            "source_12": source_12,
            "timeseries": timeseries,
            "surveys": surveys,
            "chart": "",  # placeholder for where the async chart html will be added
        },
    )


def experiments(request):
    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1

    # Send template to the end-user
    return render(
        request,
        "statistics101/experiments.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
        },
    )


def histogram(request):
    # Get the user id
    if request.user.is_anonymous:
        usr = None
    else:
        usr = User.objects.get(id=request.user.id)

    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1

    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=1, upload_complete=True
    )
    proportions = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=2, upload_complete=True
    )
    surveys = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=3, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/histogram.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "timeseries": timeseries,
            "proportions": proportions,
            "surveys": surveys,
            "chart": "",  # placeholder for where the async chart html will be added
        },
    )


# View for inbuilt datasets template
def inbuilts(request):
    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        sample_type=1, UserID__isnull=True, upload_complete=True
    )
    proportions = Sample.objects.filter(
        sample_type=2, UserID__isnull=True, upload_complete=True
    )
    surveys = Sample.objects.filter(
        sample_type=3, UserID__isnull=True, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/inbuilts.html",
        {
            "navigation": NAVIGATION_PANE,
            "timeseries": timeseries,
            "proportions": proportions,
            "surveys": surveys,
            "dataset": dataset,
        },
    )


def linechart(request):
    # Get the user id
    if request.user.is_anonymous:
        usr = None
    else:
        usr = User.objects.get(id=request.user.id)

    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1

    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=1, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/linechart.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "timeseries": timeseries,
            "chart": "",  # placeholder for where the async chart html will be added
        },
    )


def mean(request):
    # Get the user id
    if request.user.is_anonymous:
        usr = None
    else:
        usr = User.objects.get(id=request.user.id)

    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1
    source_6 = get_source_number(6) + 1
    source_7 = get_source_number(7) + 1

    # Formulas in plain TeX to be formatted by MathJax
    mean_formula = "$$\overline x  = {{\sum {{x_i}} } \over n}$$"

    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=1, upload_complete=True
    )
    proportions = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=2, upload_complete=True
    )
    surveys = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=3, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/mean.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "source_6": source_6,
            "source_7": source_7,
            "mean_formula": mean_formula,
            "timeseries": timeseries,
            "proportions": proportions,
            "surveys": surveys,
            "dataset": "",
        },
    )


def median(request):
    # Get the user id
    if request.user.is_anonymous:
        usr = None
    else:
        usr = User.objects.get(id=request.user.id)

    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1

    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=1, upload_complete=True
    )
    proportions = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=2, upload_complete=True
    )
    surveys = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=3, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/median.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "timeseries": timeseries,
            "proportions": proportions,
            "surveys": surveys,
            "dataset": dataset,
        },
    )


def percentiles(request):
    # Get the user id
    if request.user.is_anonymous:
        usr = None
    else:
        usr = User.objects.get(id=request.user.id)

    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1
    source_5 = get_source_number(5) + 1

    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=1, upload_complete=True
    )
    surveys = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=3, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/percentiles.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "source_5": source_5,
            "timeseries": timeseries,
            "surveys": surveys,
            "dataset": dataset,
        },
    )


def piechart(request):
    # Get the user id
    if request.user.is_anonymous:
        usr = None
    else:
        usr = User.objects.get(id=request.user.id)

    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1

    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=1, upload_complete=True
    )
    proportions = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=2, upload_complete=True
    )
    surveys = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=3, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/piechart.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "timeseries": timeseries,
            "proportions": proportions,
            "surveys": surveys,
            "chart": "",  # placeholder for where the async chart html will be added
        },
    )


def popsample(request):
    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1
    source_5 = get_source_number(5) + 1

    # Send template to the end-user
    return render(
        request,
        "statistics101/popsample.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "source_5": source_5,
        },
    )


def qqdata(request):
    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1
    source_3 = get_source_number(3) + 1
    source_4 = get_source_number(4) + 1
    source_10 = get_source_number(10) + 1

    # Send template to the end-user
    return render(
        request,
        "statistics101/qqdata.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
            "source_3": source_3,
            "source_4": source_4,
            "source_10": source_10,
        },
    )


def sources(request):
    # list of all sources in correct order
    sources = ALL_SOURCES
    # Count of each type of source is needed to output headers correctly in the template
    book_count = Source.objects.filter(SourceType=1).count()
    video_count = book_count + Source.objects.filter(SourceType=2).count()
    publication_count = video_count + Source.objects.filter(SourceType=3).count()
    website_count = publication_count + Source.objects.filter(SourceType=4).count()
    datasets_count = website_count + Source.objects.filter(SourceType=5).count()

    # Send template to the end-user
    return render(
        request,
        "statistics101/sources.html",
        {
            "navigation": NAVIGATION_PANE,
            "sources": sources,
            "book_count": book_count,
            "video_count": video_count,
            "publication_count": publication_count,
            "website_count": website_count,
            "datasets_count": datasets_count,
        },
    )


def stdev(request):
    # Get the user id
    if request.user.is_anonymous:
        usr = None
    else:
        usr = User.objects.get(id=request.user.id)

    # Formulas in plain TeX to be formatted by MathJax
    standard_deviation_formula = (
        "$$s = \sqrt {\sum {{{{{(x - \overline x )}^2}} \over {n - 1}}} } $$"
    )

    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1
    source_5 = get_source_number(5) + 1

    # Get all datasets that (belong to this user OR are public) AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=1, upload_complete=True
    )
    proportions = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=2, upload_complete=True
    )
    surveys = Sample.objects.filter(
        Q(UserID=usr) | Q(UserID=None), sample_type=3, upload_complete=True
    )

    # Send template to the end-user
    return render(
        request,
        "statistics101/stdev.html",
        {
            "navigation": NAVIGATION_PANE,
            "stdev_formula": standard_deviation_formula,
            "source_1": source_1,
            "source_5": source_5,
            "timeseries": timeseries,
            "proportions": proportions,
            "surveys": surveys,
            "dataset": dataset,
        },
    )


def surveys(request):
    # Get all the sources that are referenced in this page
    source_1 = get_source_number(1) + 1

    # Send template to the end-user
    return render(
        request,
        "statistics101/surveys.html",
        {
            "navigation": NAVIGATION_PANE,
            "source_1": source_1,
        },
    )


# View for user datasets - vuew and upload
def userdata(request):
    # If a delete request was received
    if request.method == "PUT":
        # If user not logged in, they should not be able to delete anything
        if request.user.is_anonymous:
            return HttpResponse(status=401)
        else:
            usr = User.objects.get(id=request.user.id)  # Get the user id
            data = json.loads(request.body)  # Get details of the request
            sample_id = data["sampleid"]  # Find id of which sample to delete
            sample = Sample.objects.filter(pk=sample_id)[0]  # Get the sample
            if sample.UserID != usr:  # If the sample does not belong to the user
                return HttpResponse(status=401)  # They should not be able to delete
            else:  # If user's own sample
                Sample.objects.filter(pk=sample_id).delete()  # Delete
                return HttpResponse(status=204)  # Tell the user it was deleted

    # If a new dataset was submitted to upload
    elif request.method == "POST":
        # Get the authorised user id
        if not (request.user.is_anonymous):
            this_user_id = request.user.id

        else:  # if user is not authorised - return error
            return HttpResponse(status=403, content="Unauthorised user")

        # Depending on which Dropzone it was only one of the below will be not None
        ts_file = request.FILES.get("timeseries")
        pr_file = request.FILES.get("proportion")
        sur_file = request.FILES.get("survey")

        # timeseries to upload
        if ts_file:
            try:
                # save the file to disk
                save_uploaded_file(ts_file, this_user_id, "t")
                return HttpResponse(status=202)

            except Exception as e:
                return HttpResponse(status=422, content=e)

        # proprotions to upload
        if pr_file:
            try:
                # save the file to disk
                save_uploaded_file(pr_file, this_user_id, "p")
                return HttpResponse(status=202)

            except Exception as e:
                return HttpResponse(status=422, content=e)

        # survey to upload
        if sur_file:
            try:
                # save the file to disk
                save_uploaded_file(sur_file, this_user_id, "s")
                return HttpResponse(status=202)

            except Exception as e:
                return HttpResponse(status=422, content=e)

    # GET request (most likely)
    else:
        if request.user.is_anonymous:  # return an empty page
            return render(
                request,
                "statistics101/userdata.html",
                {
                    "navigation": NAVIGATION_PANE,
                    "timeseries": None,
                    "proportions": None,
                    "surveys": None,
                    "dataset": None,
                },
            )

    # GET request, authorised user
    usr = User.objects.get(id=request.user.id)  # Get the user id
    # Get all datasets that belong to this user AND
    # are of the correct type AND have finished uploading
    timeseries = Sample.objects.filter(UserID=usr, sample_type=1, upload_complete=True)
    proportions = Sample.objects.filter(UserID=usr, sample_type=2, upload_complete=True)
    surveys = Sample.objects.filter(UserID=usr, sample_type=3, upload_complete=True)

    # Send template to the end-user
    return render(
        request,
        "statistics101/userdata.html",
        {
            "navigation": NAVIGATION_PANE,
            "timeseries": timeseries,
            "proportions": proportions,
            "surveys": surveys,
            "dataset": dataset,
        },
    )


# ----------------------------------------------------------------------------
# All included async templates/functions in alphabetical order
# ----------------------------------------------------------------------------


# Included template for Charts section
def chart(request, chartid, function_name):
    # Check if the user is authorised to see the particular chart
    # sample_allowed() lives in utils.py
    if not sample_allowed(request.user, chartid):
        return HttpResponse(status=403, content="Dataset not allowed")

    # Call appropriate function and calculate chart
    # function_name is passed from the dataset of the button that was pressed
    # chart will be a string - the html representation of the chart
    if function_name == "get_linechart":
        chart = get_linechart(chartid)
    elif function_name == "get_boxplot":
        chart = get_boxplot(chartid)
    elif function_name == "get_piechart":
        chart = get_piechart(chartid)
    elif function_name == "get_barchart":
        chart = get_barchart(chartid)
    elif function_name == "get_histogram":
        chart = get_histogram(chartid)
    else:
        return HttpResponse(status=400, content="Unrecognised chart")

    # Return the included template with chart html
    return render(
        request,
        "statistics101/chart.html",
        {
            "chart": chart,
        },
    )


# Included template for Statistics and Data Sets section
def dataset(request, sampleid, function_name):
    # Check if the user is authorised to see the particular dataset
    # sample_allowed() lives in utils.py
    if not sample_allowed(request.user, sampleid):
        return HttpResponse(status=403, content="Dataset not allowed")

    # Call appropriate function and calculate dataset
    # function_name is passed from the dataset of the button that was pressed
    if function_name == "get_dataset":
        dataset = get_dataset(sampleid)
    elif function_name == "get_mean":
        dataset = get_m_m_stdev(sampleid, "mean")
    elif function_name == "get_median":
        dataset = get_m_m_stdev(sampleid, "median")
    elif function_name == "get_stdev":
        dataset = get_m_m_stdev(sampleid, "standard deviation")
    elif function_name == "get_percentiles":
        dataset = get_percentiles(sampleid)
    else:
        return HttpResponse(status=400, content="Unrecognised function")

    # Return the included template with dataset html
    return render(
        request,
        "statistics101/dataset.html",
        {
            "dataset": dataset,
        },
    )


def process_file(request):
    """
    Function to process a file uploaded by the user
    Is called by Dropzone when the file has been received
    """
    if request.method == "POST":
        # File must be recieved from a known user to whom the dataset belongs
        if not request.user.is_anonymous:
            this_user_id = request.user.id  # Get user id
            json_obj = json.loads(request.body)  # Get request details

            # Directories to move the files around
            parent_dir = "statistics101/media/statistics101/uploaded_files/"
            request_dir = "requested/"
            process_dir = "processing/"
            done_dir = "uploaded/"
            failed_dir = "failed/"

            # File name must match this regex - as constructed by save_uploaded_file() in utils_async.py
            regex = f"^20\d\d-\d\d-\d\d_\d\d-\d\d-\d\d-\d\d\d\d\d\d_{this_user_id}_\w+{json_obj['filename']}$"

            # Check each file in request dir
            for file in os.listdir(parent_dir + request_dir):
                if re.search(regex, file):  # There should only be one matching file
                    source_path = parent_dir + request_dir + file
                    dest_path = parent_dir + process_dir + file
                    os.rename(source_path, dest_path)  # Move the file to processing dir

                    # Check that the user has not exceeded their upload limit
                    sample_count = Sample.objects.filter(
                        UserID=this_user_id, upload_complete=True
                    ).count()
                    if (
                        sample_count > 5
                    ):  # Once 6 samples are uploaded this check will fail
                        result = False  # Set resutl flag to return error message
                    else:  # If the sample upload limit is not exceeded
                        filename = json_obj["filename"].rstrip(".csv")
                        sample_type = file.split("_")[
                            3
                        ]  # Get the sample type off the filename
                        data = pd.read_csv(dest_path)  # Get the data out of the file

                        # Save Timeseries data
                        if sample_type == "t":
                            result = save_df_as_timeseries(
                                df=data,
                                UserID=this_user_id,
                                sample_name=filename,
                                is_numerical=True,
                                is_population=False,
                            )

                        # Save Proportions data
                        elif sample_type == "p":
                            result = save_df_as_proportion(
                                df=data,
                                UserID=this_user_id,
                                sample_name=filename,
                                is_numerical=True,
                                is_population=False,
                            )

                        # Save Survey data
                        else:
                            result = save_df_as_survey(
                                df=data,
                                UserID=this_user_id,
                                sample_name=filename,
                                is_numerical=False,
                                is_population=False,
                            )

                    source_path = parent_dir + process_dir + file
                    if (
                        result
                    ):  # if file upload successful - move the file into success dir
                        dest_path = parent_dir + done_dir + file
                        os.rename(source_path, dest_path)
                        return HttpResponse(status=201)
                    else:  # if file upload failed = move the file into fail dir
                        dest_path = parent_dir + failed_dir + file
                        os.rename(source_path, dest_path)
                        return HttpResponse(status=400)

    # This function can only be reached by POST
    # If response is not returned already, it's a request error
    return HttpResponse(status=400)


# ----------------------------------------------------------------------------
# User management functions
# ----------------------------------------------------------------------------


def login_view(request):
    # User credentials sent via POST
    if request.method == "POST":
        # Get the user details
        username = request.POST["username"]
        password = request.POST["password"]
        # Attempt to find the user in the DB
        user = authenticate(request, username=username, password=password)

        # if registered user
        if user is not None:
            login(request, user)  # Log them in
            # And display the landing page
            return HttpResponseRedirect(reverse("statistics101:index"))
        else:  # if user not found, return the login form with an error message
            emptyform = Login()
            return render(
                request,
                "statistics101/login.html",
                {
                    "message": "Invalid username and/or password.",
                    "loginform": emptyform,
                    "navigation": NAVIGATION_PANE,
                },
            )
    # GET request
    else:
        emptyform = Login()  # Get the login form
        # And display it to the user
        return render(
            request,
            "statistics101/login.html",
            {
                "loginform": emptyform,
                "navigation": NAVIGATION_PANE,
            },
        )


def logout_view(request):
    logout(request)  # Log the user out
    # Display the website landing page
    return HttpResponseRedirect(reverse("statistics101:index"))


def register(request):
    # New user credentials sent via POST
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Validate e-mail, solution from:
        # https://stackoverflow.com/questions/3217682/how-to-validate-an-email-address-in-django
        try:
            validate_email(email)
        except ValidationError as e:
            emptyform = Register()
            # if invalid e-mail return an empty registration form with an error message
            return render(
                request,
                "statistics101/register.html",
                {
                    "message": "Invalid email",
                    "registrationform": emptyform,
                    "navigation": NAVIGATION_PANE,
                },
            )

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            emptyform = Register()
            # if paswords don't match return an empty registration form with an error message
            return render(
                request,
                "statistics101/register.html",
                {
                    "message": "Passwords must match.",
                    "registrationform": emptyform,
                    "navigation": NAVIGATION_PANE,
                },
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            emptyform = Register()
            # If user name already exists return an empty registration form with an error message
            return render(
                request,
                "statistics101/register.html",
                {
                    "message": "Username already taken.",
                    "registrationform": emptyform,
                    "navigation": NAVIGATION_PANE,
                },
            )

        # If all the checks passed without an error - log the user in
        login(request, user)
        # And show them the landing page
        return HttpResponseRedirect(reverse("statistics101:index"))

    # GET request
    else:
        emptyform = Register()
        return render(
            request,
            "statistics101/register.html",
            {
                "registrationform": emptyform,
                "navigation": NAVIGATION_PANE,
            },
        )
