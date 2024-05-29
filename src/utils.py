import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import math
from loguru import logger
from h2o_wave import Q, app, main, run_on, ui
from sklearn.preprocessing import OrdinalEncoder

def load_data(q, path):
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
    return data.describe(include="all").round(2)

def plot_correlation_matrix(data):
    # Encode the categorical columns
    encoder = OrdinalEncoder()
    data_encoded = encoder.fit_transform(data)
    data_encoded = pd.DataFrame(data_encoded, columns=data.columns)
    corr = data_encoded.corr()

    # Create heatmap
    sns.set(style="white")
    f, ax = plt.subplots(figsize=(18, 14))  
    f.set_facecolor('none')  # Make background transparent
    ax.set_facecolor('none') 
    sns.heatmap(corr, cmap='coolwarm')

    plt.title("Correlation Matrix", fontsize=40, fontweight='bold', pad=20) 
    plt.xticks(fontsize=27, rotation=45, horizontalalignment='right') 
    plt.yticks(fontsize=27) 
    plt.tight_layout()

    # Save the plot to a buffer (wave requires a base64 encoded image)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    return image

def plot_missing_values(data):
    plt.figure(figsize=(18,16))
    fig = plt.gcf() 
    ax = plt.gca()      
    fig.set_facecolor('none')  # Make background transparent
    ax.set_facecolor('none')  
    sns.heatmap(data.isnull(),yticklabels=False,cbar=False,cmap='Paired')
    plt.title("Missing Value Analysis", fontsize=40, fontweight='bold', pad=20) 
    plt.xticks(fontsize=27, rotation=45, horizontalalignment='right') 
    plt.tight_layout() 
    
    # Save the plot to a buffer (wave requires a base64 encoded image)
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

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))
    fig.set_facecolor('none')  # Make background transparent
    axs = axs.flat
    # common title for the entire figure
    fig.suptitle('Categorical Attribute Counts', fontsize=20, fontweight='bold')

    # Plot the count of each categorical variable
    for i, col in enumerate(categorical_cols):
        sns.countplot(data[col], ax=axs[i], color='royalblue')
        axs[i].set_title(f"{col}", fontsize=20,  pad=20)
        axs[i].tick_params(axis='x', labelsize=15)
        axs[i].tick_params(axis='y', labelsize=15)
        axs[i].set_xlabel(col, fontsize=15)
        axs[i].set_ylabel('Count', fontsize=15)
        axs[i].set_facecolor('none')

    # Remove unused subplots
    for ax in axs[i+1:]:
        ax.remove()
    plt.tight_layout()
    
    # Save the plot to a buffer (wave requires a base64 encoded image)
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

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))
    fig.set_facecolor('none')  # Make background transparent

    # common title for the entire figure
    fig.suptitle('Numerical Attribute Boxplots', fontsize=20, fontweight='bold')
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

    for ax in axs[i+1:]:
        ax.remove()
    plt.tight_layout()
    
    # Save the plot to a buffer (wave requires a base64 encoded image)
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

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))
    fig.set_facecolor('none')  # Make the figure background transparent
    fig.suptitle('Histograms', fontsize=20, fontweight='bold')
    axs = axs.flat
    
    # Define the color palette for the hue classes
    hue_classes = df[target_column].unique()
    hue_colors = {hue_classes[0]: 'royalblue', hue_classes[1]: 'yellow'}

    # Plot the histogram of each column
    for i, col in enumerate(cols):
        sns.histplot(data=df, x=col, hue=target_column, ax=axs[i], palette=hue_colors)
        axs[i].set_title(f"{col}", fontsize=20, pad=20)
        axs[i].tick_params(axis='x', rotation=45, labelsize=15)
        axs[i].tick_params(axis='y', labelsize=15)
        axs[i].set_xlabel(col, fontsize=15)
        axs[i].set_ylabel('Count', fontsize=15)
        axs[i].set_facecolor('none')

    for ax in axs[i+1:]:
        ax.remove()
    plt.tight_layout()
    
    # Save the plot to a buffer (wave requires a base64 encoded image)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    return image