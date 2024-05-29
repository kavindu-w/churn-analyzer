from h2o_wave import ui, site, TableColumn
from src.utils import (
    load_data,
    describe_data,
    plot_correlation_matrix,
    plot_missing_values,
    plot_categorical,
    plot_boxplot,
    display_histograms

)
import pandas as pd

async def analyze_page_impl(q:dict, details: dict) -> dict:
    q.client.tab = "analyze"
    if details["path"]:
        df = load_data(details["path"])
    else:
        # Load the default dataset
        df = load_data("data/Bank Customer Churn Prediction.csv")
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
        # ui.inline(align='center', justify='around', height='100px',
        #     items=[
        #         ui.markup(content= f"""
        #         <b>Numerical Attributes:</b> <br> {', '.join(df.select_dtypes(include=['int64', 'float64']).columns)}
        #         """),
        #         ui.markup(content= f"""
        #         <b>Categorical Attributes:</b> <br> {', '.join(df.select_dtypes(include=['object']).columns)}
        #         """),
        #         ]),
        ui.separator(label="Descriptive Statistics"),
        # add the describe data
        ui.markup(content= describe_data(df).to_html().replace('<table', '<table style="border: 2px solid black;"').replace('<th>', '<th style="background-color: royalblue; color: white; border: 0px solid black; text-align: center;">').replace('<td>', '<td style="border: 1px solid black;">')),
        ui.separator(label="First 5 Rows of the Dataset"),
        ui.markup(content= df.head().to_html().replace('<table', '<table style="border: 2px solid black;"').replace('<th>', '<th style="background-color: royalblue; color: white; border: 0px solid black; text-align: center;">').replace('<td>', '<td style="border: 1px solid black;">')),
    ]
    stats_left = [
                ui.stat(label='Records', value=str(df.shape[0])),
                ui.stat(label='Attributes', value=str(df.shape[1])),
                # categorical and numerical columns
                ui.stat(label='Categorical', value=str(len(df.select_dtypes(include=['object']).columns))),
                ui.stat(label='Numerical', value=str(len(df.select_dtypes(include=['int64', 'float64']).columns))),
    ]
    about = [
        ui.markup(content=
        """
        <center><h2> Customer Retention Analyzer Application </h2></center>
        """
        )
    ]
    items = [    
    ]
    
    
    cfg = {
        "tag": "analyze",
        "items": items,
        "about": about,
        "stats_tables": stats_tables,
        "stats_left": stats_left,
        "correlation_matrix": plot_correlation_matrix(df),
        "missing_values": plot_missing_values(df),
        "categorical_plots": plot_categorical(df),
        "numerical_plots": plot_boxplot(df),
        "histograms": display_histograms(df, "churn")
    }
    
    return cfg