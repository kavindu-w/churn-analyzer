from h2o_wave import ui, site

async def home_page_impl(q:dict, details: dict) -> dict:
    q.client.tab = "home"
    about = [
        ui.markup(content=
            """
            <center><h2> Customer Retention Analyzer Application </h2></center>
            <br>
            <center>
            <img src="https://img.icons8.com/?size=100&id=F1NA2BfIY6Bf&format=png&color=000000" alt="Churn Analysis">
            <p>
            Welcome to Churn Analyzer, a cutting-edge application designed to empower businesses with predictive insights into customer retention.
            </p>
            <strong>Key Features:</strong>
            </center>
            <ul>
            <li><strong>Intuitive Data Import</strong><br>
                User-friendly interface with a seamless import of your customer data in CSV format.
            </li>
            <li><strong>Automated Data Preprocessing</strong><br>
                Automatically preprocesses your data to prepare it for analysis.
            </li>
            <li><strong>Insightful Visualizations</strong><br>
                Innovate visualizations according to the latest research to help you understand the data and derive meaningful insights at a glance.
            </li>
        </ul>
        """
        )
    ]
    items = [
        ui.dropdown(
            name="dataset",
            label="Select a Sample Dataset",
            value="bank",
            choices=[
                ui.choice(name="bank", label="Bank Churn Dataset"),
                ui.choice(name="telco", label="Telco Churn Dataset"),
            ],
        ),
        ui.button(name="button_analyze_data", label="Analyze Data", primary=True),
        ui.separator("OR"),
        ui.file_upload(name="file_upload", label="Upload a CSV file", multiple=False),
        
    ]
    
    
    cfg = {
        "tag": "home",
        "items": items,
        "about": about
    }
    
    return cfg