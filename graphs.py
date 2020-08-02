import csv
import matplotlib.pyplot as plt
plt.style.use("ggplot")


def read_from_csv(csv_file, only_average):
    values = []
    dates = []
    with open(csv_file, newline='') as file:
        reader = csv.reader(file, delimiter=",")
        headers = next(reader)
        for row in reader:
            dates.append(row[headers.index('Date')])
            if only_average:
                values.append(row[headers.index('Average')])
            else:
                del row[headers.index('Date')]
                values.append(row)
    return dates, values

def visualize_observations(dates, values_array, series_info, group_names, only_average):
    fig, axs = plt.subplots(len(values_array))

    for index, values in enumerate(values_array):
        if only_average:
            values_floats = [float(i) for i in values]
            axs[index].plot(dates, values_floats)
        else:
            average = [float(i[0]) for i in values]
            min_rates = [float(i[1]) for i in values]
            max_rates = [float(i[2]) for i in values]
            ultimo_rates = [float(i[3]) for i in values]

            axs[index].plot(dates, average, color="green", label="Average")
            axs[index].plot(dates, min_rates, color="red", label="Min")
            axs[index].plot(dates, max_rates, color="blue", label="Max")
            #axs[index].plot(dates, ultimo_rates, color="orange", label="Ultimo")

        axs[index].set_xlabel("Date")
        axs[index].set_ylabel(series_info[index].description)
        axs[index].set_title(group_names[index])
        axs[index].legend(["Average", "Minimum", "Maximum"])

    plt.tight_layout()
    plt.show()