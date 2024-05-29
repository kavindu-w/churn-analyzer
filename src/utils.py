import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import math

def load_data(path):
    try:
        data = pd.read_csv(path)
        return data
    except Exception as e:
        logger.exception(e)
        q.page["meta"].notification_bar = ui.notification_bar(
            text="Error loading the file, please try again later",
            type="error",
            name="error_bar"
        )

def describe_data(data):
    # Return the summary statistics of the dataset
    return data.describe().round(2)

def plot_correlation_matrix(data):
    # Compute the correlation matrix and return the heatmap
    data_encoded = pd.get_dummies(data, drop_first=True)
    # Calculate correlation matrix
    corr = data_encoded.corr()
    # Create heatmap
    sns.set(style="white")
    f, ax = plt.subplots(figsize=(18, 14))  # Increase the size of the plot
    f.set_facecolor('none')  # Make the figure background transparent
    ax.set_facecolor('none')  # Make the axes background transparent
    cmap = sns.light_palette("royalblue", as_cmap=True)  # Change the color map to royal blue
    sns.heatmap(corr, cmap='coolwarm')

    plt.title("Correlation Matrix", fontsize=40, fontweight='bold', pad=20)  # Make the title bold and larger
    plt.xticks(fontsize=27, rotation=45)  # Increase x-axis label size
    plt.yticks(fontsize=27)  # Increase y-axis label size
    plt.tight_layout()  # Adjust the layout to prevent labels from cutting off

    # save the plot as a png file
    # plt.savefig('./data/outputs/correlation_matrix.png')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    return image

def plot_missing_values(data):
    plt.figure(figsize=(18,16))
    fig = plt.gcf()  # Get the current figure
    fig.set_facecolor('none')  # Make the figure background transparent

    ax = plt.gca()  # Get the current axes
    ax.set_facecolor('none')  # Make the axes background transparent

    sns.heatmap(data.isnull(),yticklabels=False,cbar=False,cmap='Paired')
    plt.title("Missing Value Analysis", fontsize=40, fontweight='bold', pad=20)  # Make the title bold and larger
    plt.xticks(fontsize=27, rotation=45)  # Increase x-axis label size
    plt.tight_layout()  # Adjust the layout to prevent labels from cutting off

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    return image


def plot_categorical(data):
    # Select categorical columns
    categorical_cols = data.select_dtypes(include=['object']).columns

    # Determine the number of rows and columns for the subplots
    num_plots = len(categorical_cols)
    ncols = math.ceil(math.sqrt(num_plots))
    nrows = math.ceil(num_plots / ncols)

    # Create subplots
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))
    fig.set_facecolor('none')  # Make the figure background transparent
    # Flatten the axes array
    axs = axs.flat
    # Set a common title for the entire figure
    fig.suptitle('Categorical Attribute Counts', fontsize=20, fontweight='bold')

    # Plot the count of each categorical variable
    for i, col in enumerate(categorical_cols):
        sns.countplot(data[col], ax=axs[i], color='royalblue')
        axs[i].set_title(f"Count of {col}", fontsize=20,  pad=20)
        axs[i].tick_params(axis='x', rotation=45, labelsize=15)
        axs[i].tick_params(axis='y', labelsize=15)
        # x-axis label size
        axs[i].set_xlabel(col, fontsize=15)
        axs[i].set_ylabel('Count', fontsize=15)
        # transparent background
        axs[i].set_facecolor('none')
        

    # Remove unused subplots
    for ax in axs[i+1:]:
        ax.remove()

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    return image

def plot_boxplot(data):
    # Select numerical columns
    numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns

    # Determine the number of rows and columns for the subplots
    num_plots = len(numerical_cols)
    ncols = math.ceil(math.sqrt(num_plots))
    nrows = math.ceil(num_plots / ncols)

    # Create subplots
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))
    fig.set_facecolor('none')  # Make the figure background transparent

    # Set a common title for the entire figure
    fig.suptitle('Numerical Attribute Boxplots', fontsize=20, fontweight='bold')

    # Flatten the axes array
    axs = axs.flat

    # Plot the boxplot of each numerical variable
    for i, col in enumerate(numerical_cols):
        sns.boxplot(x=data[col], ax=axs[i], color='royalblue')
        axs[i].set_title(f"{col}", fontsize=20, pad=20)
        axs[i].tick_params(axis='x', rotation=45, labelsize=15)
        axs[i].tick_params(axis='y', labelsize=15)
        axs[i].set_xlabel(col, fontsize=15)
        axs[i].set_ylabel('Count', fontsize=15)
        axs[i].set_facecolor('none')

    # Remove unused subplots
    for ax in axs[i+1:]:
        ax.remove()

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    return image


def display_histograms(df, target_column):
    # Exclude the target column
    cols = [col for col in df.columns if col != target_column]

    # Determine the number of rows and columns for the subplots
    num_plots = len(cols)
    ncols = math.ceil(math.sqrt(num_plots))
    nrows = math.ceil(num_plots / ncols)

    # Create subplots
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))
    fig.set_facecolor('none')  # Make the figure background transparent

    # Set a common title for the entire figure
    fig.suptitle('Histograms', fontsize=20, fontweight='bold')

    # Flatten the axes array
    axs = axs.flat
    # Define the color palette for the hue classes
    hue_colors = {0: 'royalblue', 1: 'yellow'}

    # Plot the histogram of each column
    for i, col in enumerate(cols):
        sns.histplot(data=df, x=col, hue=target_column, ax=axs[i], palette=hue_colors)
        axs[i].set_title(f"{col}", fontsize=20, pad=20)
        axs[i].tick_params(axis='x', rotation=45, labelsize=15)
        axs[i].tick_params(axis='y', labelsize=15)
        axs[i].set_xlabel(col, fontsize=15)
        axs[i].set_ylabel('Count', fontsize=15)
        axs[i].set_facecolor('none')

    # Remove unused subplots
    for ax in axs[i+1:]:
        ax.remove()

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    return image