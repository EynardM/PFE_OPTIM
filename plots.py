from util.imports import *
from util.locations import *

def generate_box_plot(input_xlsx, folder_path, filename):
    df = pd.read_excel(input_xlsx)

    plt.figure(figsize=(10, 6))
    for i, column in enumerate(['Score', 'Volume', 'Distance', 'Emergency'], start=1):
        plt.subplot(2, 2, i)
        bp = df.boxplot(column=column, by='Method', ax=plt.gca())
        plt.title(f'Boxplot {column}')
        plt.xlabel('Method')
        plt.ylabel(column)
        plt.xticks(rotation=45)
        plt.xticks(range(1, len(df['Method'].unique()) + 1), sorted(df['Method'].unique()))

    plt.suptitle('')
    plt.tight_layout()
    plt.savefig(folder_path+filename+".png")
    plt.close()

generate_box_plot(input_xlsx="results/current_run/values.xlsx", folder_path=CURRENT_RESULTS_PATH, filename="current_boxplot")