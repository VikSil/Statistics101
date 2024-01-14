from .globals import ALL_SOURCES
from .models import Sample, User

# ----------------------------------------------------------------------------
# This module contains all helper functions that are not related to
# async data and chart retreival or file upload
# ----------------------------------------------------------------------------


def get_source_number(key: int) -> int:
    """
    Function takes a primary key of a source and
    returns the position of the source in the ordered sources list
    Used for referencing sources fom text in templates
    """

    # Iterrate through the sorted global variable of sources
    for index, item in enumerate(ALL_SOURCES):
        # If the source has requested id
        if item["id"] == key:
            # Return the position of the source in the QuerySet
            return index

    # If the id not found in the QuerySet, then return -1
    index = -1
    return index


def sample_allowed(user, sampleid):
    """
    Function checks if the user is allowed to access a sample
    """
    # get sample owner
    sample = Sample.objects.filter(pk=sampleid, upload_complete=True)
    # check if sample exists
    if len(sample) > 0:
        # if sample exists get the user
        sample_user = sample[0].UserID
    else:
        return False  # if sample does not exist, prohibit accessing it

    # if dataset is not public, check if it belongs to requesting user
    if sample_user != None:
        if not user.is_anonymous:  # check that current user is logged in
            usr = User.objects.get(id=user.id)  # get the current user id
            if usr != sample_user:
                return False  # user trying to access someone else's dataset
        else:  # annonymous user trying to access non-public dataset
            return False
    return True  # public dataset or dataset belongs to the current user
