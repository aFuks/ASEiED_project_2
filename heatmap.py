import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def draw_heatmap(file_path, cmap='Reds'):
    """
    Draw a heatmap from a CSV file with columns 'date', 'region', and 'count'.

    :param file_path: Path to the CSV file.
    :param cmap: Color map for the heatmap.
    """
    try:
        # Load data from CSV file
        data = pd.read_csv(file_path, delimiter=';')
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    # Map regions to specific events
    region_mapping = {
        'louisiana': 'Huragan ( Louisiana )',
        'ukraine': 'War ( Ukraine )',
        'warszawa': 'Covid ( Warszawa )'
    }

    # Replace region names with mapped values
    data['region'] = data['region'].replace(region_mapping)

    # Create a pivot table to aggregate flight counts by date and event
    pivot_table = data.pivot_table(index='date', columns='region', values='count', aggfunc='sum', fill_value=0)

    # Set up the heatmap plot
    plt.figure(figsize=(14, 12))
    heatmap = sns.heatmap(pivot_table, annot=True, fmt="g", cmap=cmap, cbar=False)

    # Add titles and labels
    plt.title('Heatmap of Flights by Date and Events')
    plt.xlabel('Event')
    plt.ylabel('Date')

    # Adjust the position of x-axis labels to the top
    heatmap.xaxis.tick_top()
    heatmap.xaxis.set_label_position('top')

    # Display the heatmap
    plt.show()

if __name__ == "__main__":
    # Call the function with the path to the CSV file and optional color map
    draw_heatmap('data.csv')
