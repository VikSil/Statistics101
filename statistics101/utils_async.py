import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from .models import Datapoint, Sample, Variable

# ----------------------------------------------------------------------------
# This module contains all functions that are called from front-end to
# async retrieve, calculate and display datasets, statistics and charts
# ----------------------------------------------------------------------------

# Adjust the color scheme for plotly to match the Bootstrap color scheme for the website
pio.templates["custom_theme"] = go.layout.Template(
    layout=go.Layout(
        colorway=[
            "#6a4d83",
            "#7d3a5b",
            "#a4ad9a",
            "#435505",
            "#43A405",
            "#003D00",
            "#66023C",
            "#EB86C3",
            "#710014",
            "#422543",
            "#800080",
            "#800000",
            "#808000",
            "#008000",
            "#000080",
            "#008080",
            "#808080",
            "#0000FF",
            "#FF00FF",
            "#00FFFF",
            "#FFFF00",
            "#00FF00",
            "#FF0000",
            "#FF7F00",
            "#FFD400",
            "#00EAFF",
            "#FF7F00",
            "#0095FF",
            "#FF00AA",
            "#EDB9B9",
            "#DCB9ED",
            "#8F6A23",
            "#8F2323",
            "#4F8F23",
            "#000000",
            "#FFFFFF",
        ],
        paper_bgcolor="#fdeafb",
        font_color="#422543",
        separators=". ",
        plot_bgcolor="#fdeafb",
    )
)

pio.templates.default = "custom_theme"


def get_dataset(id):
    """
    Function retrieves data set from the database and returns it in an html table
    """
    sample = Sample.objects.filter(pk=id)[0]
    sampletype = sample.sample_type

    if sampletype < 3:  # If 1- timeseries or 2- proportion
        variable = Variable.objects.filter(parent_id__pk=id)[0]
        var = variable.id
        # Get the raw data
        data = pd.DataFrame(Datapoint.objects.filter(variable_id__pk=var).values())
        if sampletype == 1:  # Data transformation for timeseries
            data = data.drop(
                columns=["id", "variable_id_id", "proportion", "upload_dt", "update_dt"]
            )
            data = data.pivot(
                index="individual_id", columns="timestamp", values="variable_value"
            )
        else:  # Data transformation for proportion
            data = data.drop(
                columns=[
                    "id",
                    "variable_id_id",
                    "timestamp",
                    "upload_dt",
                    "update_dt",
                ]
            )
            var_values = data.variable_value.unique()
            data = data.pivot(
                index="individual_id", values="proportion", columns="variable_value"
            )
            # Fix pivot table by ordering columns alphabetically
            data = data.reindex(var_values, axis=1)

        data = data.reset_index()  # Remove visible indexing
        # Set first column header to uppercase
        data = data.rename(columns={"individual_id": variable.variable_name.upper()})

    else:  # If 3- survey
        # Surveys will have several variables
        variables = Variable.objects.filter(parent_id__pk=id)
        data_list = []
        for var in variables:
            # Process data for each variable
            var_data = Datapoint.objects.filter(variable_id__pk=var.id).values()
            for datapoint in var_data:
                del datapoint["id"]
                del datapoint["variable_id_id"]
                del datapoint["proportion"]
                del datapoint["timestamp"]
                del datapoint["upload_dt"]
                del datapoint["update_dt"]
                datapoint["variable"] = var.variable_name
                # Uppend the cleaned data to the data set
                data_list.append(list(datapoint.values()))
        # Adjust the data set to display correctly
        data = pd.DataFrame(
            data_list, columns=["individual_id", "variable_value", "variable_name"]
        )
        data = data.pivot(
            index="individual_id", values="variable_value", columns="variable_name"
        )
        data = data.reset_index()  # Remove visible indexing
        data = data.rename(
            columns={"individual_id": ""}
        )  # Remove header of the first column

    if sampletype > 1:  # For proportions and surveys
        # Uppercase all columns, not for timeseries, because headers will be timestamps
        data = data.rename(columns=str.upper)

    # Transform dataframe to html
    data = data.to_html(index=False, index_names=False)
    return data


def get_statistic(df, func, value_col_name):
    """
    Function returns a numerical value of a column statistic over all rows of a df
    """
    if func == "mean":
        # df.location[first row:last row, given column].apply function
        stat = round((df.loc[:, value_col_name].mean()), 2)
    elif func == "median":
        stat = round((df.loc[:, value_col_name].median()), 2)
    elif func == "standard deviation":
        stat = round((df.loc[:, value_col_name].std()), 2)
    else:
        ...
    return stat


def get_m_m_stdev(id, func):
    """
    Function returns an html table with mean, median or standard deviation calculated for
    each variable in a data set
    """
    statistics = {}
    # Get the sample data from DB
    sample = Sample.objects.filter(pk=id)[0]
    sampletype = sample.sample_type
    # Find all variables and iterrate through them
    vars = Variable.objects.filter(parent_id__pk=id, is_numerical=True)
    for var in vars:
        # Get data relevant to the variable
        data = pd.DataFrame(Datapoint.objects.filter(variable_id__pk=var.id).values())

        # Abstract the iterration depending on the sample type
        if sampletype == 2:  # Sample type 2 - Proportions
            value_col_name = "proportion"
            iterrable = data.variable_value.unique()
            iter_col_name = "variable_value"
        else:  # Sample type 1 - Timeseries, 3 - Survey
            value_col_name = "variable_value"
            iterrable = data.individual_id.unique()
            iter_col_name = "individual_id"

        # Cast the numerical values as float to perform maths on them
        data[value_col_name] = data[value_col_name].astype(float)

        # If it is not a survey (one variable, multiple individuals) - use iterrable
        if sampletype < 3:
            for el in iterrable:
                # Get the data for the individual
                subdata = data[data[iter_col_name] == el]
                # Get the statistic calculated for that individual
                statistics[el] = get_statistic(subdata, func, value_col_name)

        else:  # If if a survey (multiple variables, multiple individuals)
            # Get statistic on the variable level, aggregate individuals into one
            statistics[var.variable_name] = get_statistic(data, func, value_col_name)

    # Set column headers to uppercase
    data = pd.DataFrame.from_dict(statistics, orient="index", columns=[func.upper()])
    if sampletype == 1:
        data.insert(0, "INDIVIDUAL", data.index)
    else:
        data.insert(0, "VARIABLE", data.index)

    # Transform dataframe to html
    data = data.to_html(index=False, index_names=False)
    return data


def get_five_numbers(series):
    """
    Function returns The Five Number Summary for data series
    """
    percentiles = []
    percentiles.append(round(series.min(), 2))
    percentiles.append(round(series.quantile(0.25), 2))
    percentiles.append(round(series.median(), 2))
    percentiles.append(round(series.quantile(0.25), 2))
    percentiles.append(round(series.max(), 2))
    return percentiles


def get_percentiles(id):
    """ "
    Function returns an html table with percentiles calculated for
    each variable in a data set
    """
    five_numbers = {}
    # Get the sample data from DB
    sample = Sample.objects.filter(pk=id)[0]
    sampletype = sample.sample_type
    # Find all variables and iterrate through them
    vars = Variable.objects.filter(parent_id__pk=id, is_numerical=True)
    for var in vars:
        # Get data relevant to the variable
        data = pd.DataFrame(Datapoint.objects.filter(variable_id__pk=var.id).values())
        # Cast the numerical values as float to perform maths on them
        data["variable_value"] = data["variable_value"].astype(float)

        if sampletype == 1:  # If timeseries
            individuals = data.individual_id.unique()
            # Get the percentiles for each individual
            for individual in individuals:
                subdata = data[data["individual_id"] == individual]
                five_numbers[individual] = get_five_numbers(
                    subdata.loc[:, "variable_value"]
                )

        # sampletype == 2 is itself a Percentiles dataset, hence not included here

        if sampletype == 3:  # If survey get percentiles for every variable
            five_numbers[var.variable_name] = get_five_numbers(
                data.loc[:, "variable_value"]
            )

    # Set proper column headers
    data = pd.DataFrame.from_dict(
        five_numbers,
        orient="index",
        columns=["MIN", "25TH PERCENTILE", "MEDIAN", "75TH PERCENTILE", "MAX"],
    )
    if sampletype == 1:
        data.insert(0, "INDIVIDUAL", data.index)
    else:
        data.insert(0, "VARIABLE", data.index)

    # Transform dataframe to html
    data = data.to_html(index=False, index_names=False)
    return data


def get_linechart(id):
    """
    Function returns a plot of a timeseries data set
    """
    # Get the variable (timeseries will only have one variable)
    var = Variable.objects.filter(parent_id__pk=id)[0].id
    # Get the data
    data = pd.DataFrame(Datapoint.objects.filter(variable_id__pk=var).values())
    # Cast the numerical values as float to perform maths on them
    data["variable_value"] = data["variable_value"].astype(float)

    # Use plotly to calculate the chart
    fig = px.line(data, x="timestamp", y="variable_value", color="individual_id")
    # Cosmetic updates
    fig.update_layout(
        yaxis=dict(title=""),
        xaxis=dict(title=""),
        legend_title=dict(text="", side="top center"),
    )
    # Tansform the plot to html
    plot = fig.to_html()
    return plot


def get_boxplot(id):
    """
    Function returns boxplot(s) for timeseries and survey datasets
    """
    # Get the sample
    sample = Sample.objects.filter(pk=id)[0]
    sampletype = sample.sample_type
    plots = ""
    # Get all the variables (timeseries will only have one, surveys - many)
    vars = Variable.objects.filter(parent_id__pk=id, is_numerical=True)
    for var in vars:
        # Get the data
        data = pd.DataFrame(Datapoint.objects.filter(variable_id__pk=var.id).values())
        # Cast the numerical values as float to perform maths on them
        data["variable_value"] = data["variable_value"].astype(float)

        if sampletype == 1:  # For timeseries
            # Use plotly to calculate the chart
            fig = px.box(data, x="individual_id", y="variable_value")

        if sampletype == 3:  # For surveys
            # Use plotly to calculate the chart
            fig = px.box(data, y="variable_value")
            # Cosmetic updates
            fig.update_layout(title_text=var.variable_name, paper_bgcolor="#fdeafb")

        # Cosmetic updates
        fig.update_layout(
            yaxis=dict(title=""),
            xaxis=dict(title=""),
        )
        # For each variable, add the html of calculated plot to output
        plots = plots + fig.to_html()
    return plots


def calc_five_buckets(data):
    """
    Function divides a numerical df into five buckets and labels each data point
    """
    # Cast the numerical values as float to perform maths on them
    data["value"] = data["variable_value"].astype(float)
    # Aggregate by value
    data = data.sort_values(by=["value"])
    # If there are more than 5 distinct values
    if len(data) > 5:
        # Divide the range of data into five buckets
        min = round(data["value"].min(), 2)
        max = round(data["value"].max(), 2)
        range = round((max - min), 2)
        step = round((range / 5), 2)
        # Find the boundaries of each bucket
        bound1 = round((min + step), 2)
        bound2 = round((bound1 + step), 2)
        bound3 = round((bound2 + step), 2)
        bound4 = round((bound3 + step), 2)
        # Add the boundaries into the labels for the pie chart legend
        label1 = f"{min:_.2f}  to  {bound1:_.2f}".replace("_", " ")
        label2 = f"{bound1:_.2f}  to  {bound2:_.2f}".replace("_", " ")
        label3 = f"{bound2:_.2f}  to  {bound3:_.2f}".replace("_", " ")
        label4 = f"{bound3:_.2f}  to  {bound4:_.2f}".replace("_", " ")
        label5 = f"{bound4:_.2f}  to  {max:_.2f}".replace("_", " ")
        # For each value in the data, assign it to the correct label
        data.loc[data["value"] < bound1, "variable_value"] = label1
        data.loc[
            data["value"].between(bound1, bound2, inclusive="left"),
            "variable_value",
        ] = label2
        data.loc[
            data["value"].between(bound2, bound3, inclusive="left"),
            "variable_value",
        ] = label3
        data.loc[
            data["value"].between(bound3, bound4, inclusive="left"),
            "variable_value",
        ] = label4
        data.loc[
            data["value"] >= bound4,
            "variable_value",
        ] = label5

    # return the data, each value marked with correct label
    return data


def get_pie_figure(data, value_col_name, title, legend):
    """
    Function transforms data into pie chart html
    """
    # Use plotly to calculate the chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=data["variable_value"],
                values=data[value_col_name],
                sort=False,  # basic px rearranges labels, hence use go instead
            )
        ],
        layout={"title": title},
    )
    # Cosmetic updates
    fig.update_traces(insidetextfont=dict(color=["#fdeafb"]))
    fig.update_layout(legend_title=dict(text=legend, side="top center"))
    # Tansform the plot to html
    fig = fig.to_html()
    return fig


def get_piechart(id):
    """
    Function returns pie chart(s) for a given data set
    """
    # Get the sample
    sample = Sample.objects.filter(pk=id)[0]
    sampletype = sample.sample_type
    # Get all the variables (timeseries and proportions will have one, surveys - many)
    vars = Variable.objects.filter(parent_id__pk=id)
    plots = ""
    for var in vars:
        # Get the variable data
        data = pd.DataFrame(Datapoint.objects.filter(variable_id__pk=var.id).values())

        if (
            sampletype < 3
        ):  # For Timeseries and Proportions will iterrate over individuals
            individuals = data.individual_id.unique()

        if sampletype == 1:  # Timeseries
            for individual in individuals:
                # Get each individuals data
                subdata = data[data["individual_id"] == individual]
                # Add a counter column to agregate over
                subdata["counter"] = 1
                # Label each data point with appropriate segment
                subdata = calc_five_buckets(subdata)
                # Get the individual pie chart html and upend to output
                plots = plots + get_pie_figure(
                    subdata, "counter", individual, var.variable_name
                )

        if sampletype == 2:  # Proportions
            for individual in individuals:
                # Get each individuals data
                subdata = data[data["individual_id"] == individual]
                # Get the individual pie chart html and upend to output
                plots = plots + get_pie_figure(
                    subdata, "proportion", individual, var.variable_name
                )

        if sampletype == 3:  # Surveys
            # Add a counter column to agregate over
            data["counter"] = 1
            if var.is_numerical:
                # For numerical data label each data point with appropriate segment
                data = calc_five_buckets(data)
            # Get the variable pie chart html and upend to output
            plots = plots + get_pie_figure(
                data, "counter", var.variable_name, var.variable_name
            )

    return plots


def get_barchart(id):
    """
    Function returns bar chart(s) for a given data set
    """
    # Get the sample
    sample = Sample.objects.filter(pk=id)[0]
    sampletype = sample.sample_type
    # Get all the variables (timeseries and proportions will have one, surveys - many)
    vars = Variable.objects.filter(parent_id__pk=id)
    plots = ""
    for var in vars:
        # Get the variable data
        data = pd.DataFrame(Datapoint.objects.filter(variable_id__pk=var.id).values())

        if sampletype == 1:  # Timeseries
            # Allocate the data into buckets for a stacked bar
            data = calc_five_buckets(data)

            # Use plotly to calculate the chart - stacked bar
            fig = px.bar(
                data,
                x="individual_id",
                y="value",
                color="variable_value",
            )
            # Cosmetic updates
            fig.update_layout(yaxis=dict(title=""))

        if sampletype == 2:  # Proportions
            # Use plotly to calculate the chart - stacked bar
            fig = px.bar(
                data,
                x="individual_id",
                y="proportion",
                color="variable_value",
            )
            # Cosmetic updates
            fig.update_layout(
                yaxis=dict(title="Proportion / Percentage"),
            )

        if sampletype == 3:  # Surveys
            if var.is_numerical:  # Numerical variables
                # Cast the numerical values as float to perform maths on them
                data["variable_value"] = data["variable_value"].astype(float)
                # Aggregate by individual
                data = data.sort_values(by=["individual_id"])
                # Use plotly to calculate the chart - one bar per individual
                fig = px.bar(
                    data, x="individual_id", y="variable_value", title=var.variable_name
                )
                # Cosmetic updates
                fig.update_layout(yaxis=dict(title=""))
            else:  # Non-numeric variables
                # Remove unnecessary columns
                data = data.drop(
                    columns=[
                        "id",
                        "individual_id",
                        "variable_id_id",
                        "proportion",
                        "timestamp",
                        "upload_dt",
                        "update_dt",
                    ]
                )
                # Add a counter column to agregate over
                data["counter"] = 1
                # Group by variable value
                data = data.groupby(["variable_value"])["counter"].sum().reset_index()
                # Use plotly to calculate the chart - one bar per variable value
                fig = px.bar(
                    data, x="variable_value", y="counter", title=var.variable_name
                )
                # Cosmetic updates
                fig.update_layout(yaxis=dict(title="Number of individuals"))

        # Cosmetic updates
        fig.update_layout(
            legend_title=dict(text=var.variable_name, side="top center"),
            xaxis=dict(title=""),
        )
        # For each variable, add the html of calculated plot to output
        plots = plots + fig.to_html()

    return plots


def get_histogram_figure(data, title, x_column_name, x_title):
    """
    Function transforms data into histogram html
    """
    # Use plotly to calculate the chart
    fig = px.histogram(data, x=x_column_name, title=title)
    # Cosmetic updates
    fig.update_layout(
        yaxis=dict(title="Number of occurances"),
        xaxis=dict(title=x_title),
    )
    # Tansform the plot to html
    fig = fig.to_html()
    return fig


def get_histogram(id):
    """
    Function returns histogram(s) for a given data set
    """
    # Get the sample
    sample = Sample.objects.filter(pk=id)[0]
    sampletype = sample.sample_type
    plots = ""
    # Get all the variables (timeseries and proportions will have one, surveys - many)
    vars = Variable.objects.filter(parent_id__pk=id, is_numerical=True)
    for var in vars:
        # Get the variable data
        data = pd.DataFrame(Datapoint.objects.filter(variable_id__pk=var.id).values())

        # Cast the appropriate numerical values as float to perform maths on them
        if sampletype == 2:
            data["proportion"] = data["proportion"].astype(float)
        else:
            data["variable_value"] = data["variable_value"].astype(float)

        if sampletype == 1:  # Timeseries
            # Iterrate over individuals
            individuals = data.individual_id.unique()
            for individual in individuals:
                # Get individual data
                subdata = data[data["individual_id"] == individual]
                # Get histogram html and add to the output
                plots = plots + get_histogram_figure(
                    subdata, individual, "variable_value", var.variable_name
                )

        elif sampletype == 2:  # Proportions
            # Iterrate over individuals
            individuals = data.individual_id.unique()
            for individual in individuals:
                # Get individual data
                subdata = data[data["individual_id"] == individual]
                # Use barchart to simulate a histogram, since proportions data is already in buckets
                fig = px.bar(
                    subdata, x="variable_value", y="proportion", title=individual
                )
                # Cosmetic updates
                fig.update_layout(
                    yaxis=dict(title="Percent"),
                    xaxis=dict(title=var.variable_name),
                    bargap=0,
                )
                plots = plots + fig.to_html()

        else:  # Surveys
            # Get histogram html for the variable and add to the output
            plots = plots + get_histogram_figure(
                data, var.variable_name, "variable_value", ""
            )

    return plots
