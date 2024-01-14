import datetime
from typing import List, Type

import numpy as np
import pandas as pd
from django.utils import timezone

from .models import Datapoint, Sample, User, Variable

# ----------------------------------------------------------------------------
# This module contains all functions that are called from front-end to
# async parse, check and save data from user uploaded file
# ----------------------------------------------------------------------------


def save_uploaded_file(
    input_file: Type["django.core.files.uploadedfile.InMemoryUploadedFile"],
    user_id: int,
    upload_type: str,
):
    """
    Function takes an in memory file object, saves it  to the disk
    and returns relative path to the saved file or error
    """
    result = ""
    try:
        # Timestamp will be pre-fixed to the file name
        timestamp = (
            str(timezone.now()).replace(" ", "_").replace(":", "-").replace(".", "-")
        )
        # Construct file path
        save_file_path = (
            "statistics101/media/statistics101/uploaded_files/requested/"
            + timestamp
            + "_"
            + str(user_id)
            + "_"
            + upload_type
            + "_"
            + input_file.name
        )
        # Open file
        with open(
            save_file_path,
            "wb+",
        ) as uploaded_file:
            # Write each chunk of the file to disk
            for chunk in input_file.chunks():
                uploaded_file.write(chunk)

        result = save_file_path

    except Exception as e:
        result = e

    return result


def save_sample_population(
    name: str,
    ps_type: int,
    UserID: int,
    size: int = None,
    is_population: bool = False,
    pop_size: int = None,
) -> int:
    """
    Function creates a new Sample entry and returns the id of the new object
    """
    try:
        new_sample = Sample()
        new_sample.sample_name = name
        new_sample.sample_type = ps_type
        new_sample.UserID = User.objects.get(id=UserID)
        new_sample.sample_size = size
        new_sample.is_population = is_population
        new_sample.population_size = pop_size
        new_sample.save()
        return new_sample.id

    except Exception as e:
        print(e)
        return -1


def save_variable(
    parent_id: int,
    name: str,
    is_numerical: bool = False,
    is_timeseries: bool = False,
) -> int:
    """
    Function creates a new Variable entry and returns the id of the new object
    """
    try:
        new_variable = Variable()
        new_variable.parent_id = Sample(parent_id)
        new_variable.variable_name = name
        new_variable.is_numerical = is_numerical
        new_variable.is_timeseries = is_timeseries
        new_variable.save()

    except Exception as e:
        print(e)
        return -1

    return new_variable.id


def save_datapoint(
    individual: str,
    VariableID: int,
    value: str,
    proportion: float = None,
    timestamp: Type[datetime.datetime] = None,
) -> int:
    """
    Function creates a new Datapoint entry and returns the the id of the new object
    """
    try:
        new_datapoint = Datapoint()
        new_datapoint.individual_id = individual
        new_datapoint.variable_id = Variable.objects.get(pk=VariableID)
        new_datapoint.variable_value = value
        new_datapoint.proportion = proportion
        new_datapoint.timestamp = timestamp
        new_datapoint.save()
        return new_datapoint.id

    except Exception as e:
        print("An error while saving a datapoint", e)
        return e


def check_is_numerical_df(
    df: pd.DataFrame,
    corner_upleft: list[int],
    corner_lowright: list[int],
) -> bool:
    """
    Function takes a dataframe and checks that all values in the rectangle
    defined by upper left and lower right corners are convertible to float
    """
    # Check that both corners are defined correctly
    if (
        # Either corner does not have the correct number of coordinates
        len(corner_upleft) != 2
        or len(corner_lowright) != 2
        # Isn't at least vertical rectangle or...
        or not (
            (
                corner_upleft[0] <= corner_lowright[0]
                and corner_upleft[1] < corner_lowright[1]
            )
            # ... at least a horizontal rectangle
            or (
                corner_upleft[0] < corner_lowright[0]
                and corner_upleft[1] <= corner_lowright[1]
            )
        )
    ):
        return False

    # Check that values can be cast to a float
    # iterrate over rows
    for row in range(corner_upleft[0], corner_lowright[0] + 1):
        # iterrate over cols
        for col in range(corner_upleft[1], corner_lowright[1] + 1):
            # check for each value if it floats
            try:
                floating_point = float(df.iloc[row, col])
            except Exception as e:
                print(e)
                return False
    # If neither check has failed, return True
    return True


def str_to_timestamp(string: str) -> Type[datetime.datetime]:
    """
    Function checks formats a string and coerces it to a timestamp
    """
    try:
        if len(string) == 4:  # only year passed in
            string = string + "-01-01 00:00:00"

        if len(string) == 7:  # only year and month passed in
            string = string + "-01 00:00:00"

        if len(string) == 10:  # only date passed in
            string = string + " 00:00:00"

        if len(string) == 16:  # seconds missing from the timestamp
            string = string + ":00"

        # Attempt to cast as a datetime
        timestamp = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return e

    return timestamp


def has_duplicates(arr: List[object]) -> bool:
    """
    Function takes a list of objects and returns true if the list contains duplicate objects
    """
    duplicates = [obj for obj in arr if arr.count(obj) > 1]
    return len(duplicates) > 0


def remove_data(ids: dict[str, int]) -> bool:
    """
    Function removes all data objects with keys that were passed in
    Dependent objects are removed in a cascade
    """

    result = True

    # delete samples - variables will be cascaded
    try:
        Sample.objects.filter(pk__in=ids["sample"]).delete()
    except Exception as e:
        print(e)
        result = False

    # delete variables - data points will be cascaded
    try:
        Variable.objects.filter(pk__in=ids["variable"]).delete()
    except Exception as e:
        print(e)
        result = False

    # delete datapoints
    try:
        Datapoint.objects.filter(pk__in=ids["datapoint"]).delete()
    except Exception as e:
        print(e)
        result = False

    return result


def all_checks(
    sample_name: str,
    variable_names: List[str],
    is_numerical: bool,
    df: pd.DataFrame,
    individual_names: List[str],
    column_names: List[str],
    is_timestamps: bool,
) -> bool:
    """
    Function runs all checks on a dataset before it can be saved
    """
    result = True

    try:
        # Check if the sample name is not an empty string
        if len(sample_name) <= 0:
            raise Exception("Cannot save population or sample with empty name")

        # Check if sample name already exists
        if len(Sample.objects.filter(sample_name=sample_name)) > 0:
            raise Exception("Cannot add duplicate sample")

        # Get each variable name and check that it is not an empty string
        for name in variable_names:
            if len(name) < 1:
                raise Exception("Cannot save an empty variable name")

        if is_numerical:
            # Check that all values in the df can be converted to a float
            # check_is_numerical_df expects df, upper left corner, lower right corner
            # df.shape returns lower right corner coordinates as a tuple, convert them to a list
            corner = [num - 1 for num in list(df.shape)]
            if not check_is_numerical_df(df, [0, 1], corner):
                raise Exception("Non-numerical df passed as numerical")

        # Check that all individual names are unique
        if has_duplicates(individual_names):
            raise Exception("Data contains duplicate variable names")

        # Check that all column names are unique
        if has_duplicates(column_names):
            raise Exception("Data contains duplicate column names")

        # Check that all column headers can be converted to a timestamp
        if is_timestamps:
            for name in column_names:
                output = str_to_timestamp(name)
                if not isinstance(output, datetime.datetime):
                    raise Exception(output)

        # check that there are no empty cells
        # this returns a tuple of two arrays with row and column numbers
        empty_cells = np.where(pd.isnull(df))
        if len(empty_cells[0]) > 0:
            raise Exception("Data contains empty cells")

    # An error in any of the checks will end up caught here
    except Exception as e:
        print(e)
        result = False

    return result


def save_df_as_timeseries(
    df: pd.DataFrame,
    UserID: int,
    sample_name: str,
    is_numerical: bool = False,
    is_population: bool = False,
    population_size: int = None,
) -> bool:
    """
    Function saves dataframe with timeseries into the DB
    Returns if it was successfull or not as a boolean
    """

    # This will accumulate the ids of the saved data objects
    saved_ids = {
        "sample": [],
        "variable": [],
        "datapoint": [],
    }

    variable_names = [df.columns[0]]
    individual_names = df[df.columns[0]].tolist()
    column_names = df.columns[1:].tolist()

    # Assume that save will fail, unless this gets changed
    result = False

    # Do all checks of what might fail before atttempting to save
    if all_checks(
        sample_name,
        variable_names,
        is_numerical,
        df,
        individual_names,
        column_names,
        is_timestamps=True,
    ):
        # Try to parse and save the data
        try:
            sample_size = len(df.index)

            # Unless explicitly marked as a population, assume sample data
            if is_population:
                pop_size = sample_size
            else:
                pop_size = population_size

            # Create Sample object in the DB
            parent_id = save_sample_population(
                sample_name,  # from inputs
                1,  # 1- Timeseries; 2- Proportion; 3-Survey
                UserID,  # from inputs
                size=sample_size,  # length of the dataframe
                is_population=is_population,  # from inputs or default
                pop_size=pop_size,  # from inputs or default
            )

            # Take note of the newly added sample id, for rollback
            if parent_id > 0:
                saved_ids["sample"].append(parent_id)
            else:
                raise Exception("Failed to save sample record")

            # Create Variable objects in the DB
            # This will only happen once since there is only one variable in timeseries
            for variable_name in variable_names:
                variable_id = save_variable(
                    parent_id,
                    variable_name,
                    is_numerical,
                    is_timeseries=True,
                )
                # Take note of the newly added variable id, for rollback
                if variable_id > 0:
                    saved_ids["variable"].append(variable_id)
                else:
                    raise Exception("Failed to save variable record")

                # Add all Datapoint objects into the DB
                for index, row in df.iterrows():  # iterate over the dataframe
                    for col in column_names:  # iterate over cols
                        # call function to add datapoint into the DB
                        datapoint_id = save_datapoint(
                            df.iloc[index][variable_name],  # individual name/id
                            variable_id,  # id from the Variable table
                            row[col],  # value of the datapoint
                            timestamp=str_to_timestamp(
                                col
                            ),  # timestamp of the datapoint
                        )
                        # Take note of the newly added datapoint id, for rollback
                        if datapoint_id > 0:
                            saved_ids["datapoint"].append(datapoint_id)
                        else:
                            raise Exception("Failed to save variable record")

            # Mark the Sample as complete
            Sample.objects.filter(pk=saved_ids["sample"][0]).update(
                upload_complete=True
            )
            result = True  # Save successful

        # If saving fails at any point, it will be caught here
        except Exception as e:
            print("Error occured while uploading timeseries: ", e)
            # Rollback
            remove_all = remove_data(saved_ids)
            print("Removed all uploaded ids:", remove_all)

    return result


def save_df_as_proportion(
    df: pd.DataFrame,
    UserID: int,
    sample_name: str,
    is_numerical: bool = False,
    is_population: bool = False,
    population_size: int = None,
) -> bool:
    """
    Function saves dataframe with proportions into the DB
    Returns if it was successfull or not as a boolean
    """

    # This will accumulate the ids of the saved data objects
    saved_ids = {
        "sample": [],
        "variable": [],
        "datapoint": [],
    }

    variable_names = [df.columns[0]]
    individual_names = df[df.columns[0]].tolist()
    column_names = df.columns[1:].tolist()

    # Assume that save will fail, unless this gets changed
    result = False

    # Do all checks of what might fail before atttempting to save
    if all_checks(
        sample_name,
        variable_names,
        is_numerical,
        df,
        individual_names,
        column_names,
        is_timestamps=False,
    ):
        # Try to parse and save the data
        try:
            sample_size = len(df.index)

            # Unless explicitly marked as a population, assume sample data
            if is_population:
                pop_size = sample_size
            else:
                pop_size = population_size

            # Create Sample object in the DB
            parent_id = save_sample_population(
                sample_name,  # from inputs
                2,  # 1- Timeseries; 2- Proportion; 3-Survey
                UserID,  # from inputs
                size=sample_size,  # length of the dataframe
                is_population=is_population,  # from inputs or default
                pop_size=pop_size,  # from inputs or default
            )

            # Take note of the newly added sample id, for rollback
            if parent_id > 0:
                saved_ids["sample"].append(parent_id)
            else:
                raise Exception("Failed to save sample record")

            # Create Variable objects in the DB
            # This will only happen once since there is only one variable in proportion
            for variable_name in variable_names:
                variable_id = save_variable(
                    parent_id,
                    variable_name,
                    is_numerical,
                    is_timeseries=False,
                )
                # Take note of the newly added variable id, for rollback
                if variable_id > 0:
                    saved_ids["variable"].append(variable_id)
                else:
                    raise Exception("Failed to save variable record")

                # Add all Datapoint objects into the DB
                for index, row in df.iterrows():  # iterate over the dataframe
                    for col in column_names:  # iterate over cols
                        # call function to add datapoint into the DB
                        datapoint_id = save_datapoint(
                            df.iloc[index][variable_name],  # individual name/id
                            variable_id,  # id from the Variable table
                            col,  # variable value
                            proportion=row[col],  # value of the datapoint
                        )
                        # Take note of the newly added datapoint id, for rollback
                        if datapoint_id > 0:
                            saved_ids["datapoint"].append(datapoint_id)
                        else:
                            raise Exception("Failed to save variable record")

            # Mark the Sample as complete
            Sample.objects.filter(pk=saved_ids["sample"][0]).update(
                upload_complete=True
            )
            result = True  # Save successful

        # If saving fails at any point, it will be caught her
        except Exception as e:
            print("Error occured while uploading proportion: ", e)
            # Rollback
            remove_all = remove_data(saved_ids)
            print("Removed all uploaded ids:", remove_all)

    return result


def save_df_as_survey(
    df: pd.DataFrame,
    UserID: int,
    sample_name: str,
    is_numerical: bool = False,
    is_population: bool = False,
    population_size: int = None,
) -> bool:
    """
    Function saves dataframe of survey data into the DB
    Returns if it was successfull or not as a boolean
    """

    # This will accumulate the ids of the saved data objects
    saved_ids = {
        "sample": [],
        "variable": [],
        "datapoint": [],
    }

    # Assume that save will fail, unless this gets changed
    result = False

    variable_names = df.columns[1:].tolist()
    individual_names = df[df.columns[0]].tolist()
    numerical_columns = df.columns[0].split(",")

    # Do all checks of what might fail before atttempting to save
    if all_checks(
        sample_name,
        variable_names,
        False,  # pass False for is_numerical because there may be mixed column types in survey
        df,
        individual_names,
        variable_names,
        is_timestamps=False,
    ):
        # Try to parse and save the data
        try:
            sample_size = len(df.index)

            # Unless explicitly marked as a population, assume sample data
            if is_population:
                pop_size = sample_size
            else:
                pop_size = population_size

            # Create Sample object in the DB
            parent_id = save_sample_population(
                sample_name,  # from inputs
                3,  # 1- Timeseries; 2- Proportion; 3-Survey
                UserID,  # from inputs
                size=sample_size,  # length of the dataframe
                is_population=is_population,  # from inputs or default
                pop_size=pop_size,  # from inputs or default
            )

            # Take note of the newly added sample id, for rollback
            if parent_id > 0:
                saved_ids["sample"].append(parent_id)
            else:
                raise Exception("Failed  to  save population/sample record")

            for variable_name in variable_names:
                is_numerical = False
                # Check if the variable is supposed to be numerical
                if variable_name in numerical_columns:
                    column_number = df.columns.get_loc(variable_name)
                    max_index = list(df.shape)[0] - 1
                    # Check if the variable actually is numerical
                    is_numerical = check_is_numerical_df(
                        df, [0, column_number], [max_index, column_number]
                    )

                # Create Variable object in the DB
                variable_id = save_variable(
                    parent_id,
                    variable_name,
                    is_numerical,
                    is_timeseries=False,
                )
                # Take note of the newly added variable id, for rollback
                if variable_id > 0:
                    saved_ids["variable"].append(variable_id)
                else:
                    raise Exception("Failed  to  save variable record")

                # Add all Datapoint objects into the DB
                for index, row in df.iterrows():  # iterate over the rows
                    # call function to add datapoint into the DB
                    datapoint_id = save_datapoint(
                        df.iloc[index][df.columns[0]],  # individual name/id
                        variable_id,  # id from the Variable table
                        row[variable_name],  # value of the datapoint
                    )

                    # Take note of the newly added datapoint id, for rollback
                    if datapoint_id > 0:
                        saved_ids["datapoint"].append(datapoint_id)
                    else:
                        raise Exception("Failed  to  save variable record")

            # Mark the Sample as complete
            Sample.objects.filter(pk=saved_ids["sample"][0]).update(
                upload_complete=True
            )
            result = True  # Save successful

        # If saving fails at any point, it will be caught here
        except Exception as e:
            print("Error occured while uploading survey data: ", e)
            # Rollback
            remove_all = remove_data(saved_ids)
            print("Removed all uploaded ids:", remove_all)

    return result
