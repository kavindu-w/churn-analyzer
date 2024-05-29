from h2o_wave import ui, site, TableColumn
import re

from src.utils import (
    load_data,
    describe_data,
    plot_correlation_matrix,
    plot_missing_values,
    plot_categorical,
    plot_boxplot,
    display_histograms
)
from loguru import logger

async def analyze_page_impl(q:dict, details: dict) -> dict:
    q.client.tab = "analyze"
    if "path" in details: 
        df = load_data(q, details["path"])
    else:
        # Load the default dataset
        df = load_data(q, "data/Bank Customer Churn Prediction.csv")
        q.page["meta"].notification_bar = ui.notification_bar(
            text="Loaded the default dataset: Bank Customer Churn Prediction.csv",
            type="error",
            name="error_bar"
        )
    describe_df = describe_data(df)
    columns = [TableColumn(name=col, label=col) for col in describe_df.columns]
    rows = [ui.table_row(name=str(i), cells=list(map(str, row))) for i, row in enumerate(describe_df.values.tolist())]
    
    stats_tables = [
        ui.markup(content= f"<center><h2>Dataset Summary</h2></center>"),
        ui.separator(label="Descriptive Statistics"),
        # add the describe data
        ui.markup(content= "<center>" + describe_data(df).to_html().replace('<table', '<table style="border: 2px solid black;"').replace('<th>', '<th style="background-color: royalblue; color: white; border: 0px solid black; text-align: center; padding: 5px;">').replace('<td>', '<td style="border: 1px solid black;">') + "</center>"),
        ui.separator(label="First 5 Rows of the Dataset"),
        ui.markup(content=  "<center>" + df.head().to_html().replace('<table', '<table style="border: 2px solid black;"').replace('<th>', '<th style="background-color: royalblue; color: white; border: 0px solid black; text-align: center; padding: 5px;">').replace('<td>', '<td style="border: 1px solid black;">') + "</center>"),
    ]
    stats_left = [
                ui.stat(label='Records', value=str(df.shape[0])),
                ui.stat(label='Attributes', value=str(df.shape[1])),
                # categorical and numerical columns
                ui.stat(label='Categorical', value=str(len(df.select_dtypes(include=['object']).columns))),
                ui.stat(label='Numerical', value=str(len(df.select_dtypes(include=['int64', 'float64']).columns))),
    ]
    
    # check the columns of the df and find the column name containing the target variable
    churn_columns = df.filter(regex='(?i)churn', axis=1).columns
    # logger.debug(f"Churn Columns: {churn_columns}")
    churn_column = churn_columns[0] if len(churn_columns) != 0 else None
    
    if churn_column is None:
        q.page["meta"].notification_bar = ui.notification_bar(
            text="No target variable found in the dataset",
            type="error",
            name="error_bar"
        )
    
    cfg = {
        "tag": "analyze",
        "stats_tables": stats_tables,
        "stats_left": stats_left,
        "correlation_matrix": plot_correlation_matrix(df),
        "missing_values": plot_missing_values(df),
        "categorical_plots": plot_categorical(df),
        "numerical_plots": plot_boxplot(df),
        "histograms": display_histograms(df, churn_column)
    }
    
    return cfg