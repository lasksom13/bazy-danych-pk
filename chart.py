import matplotlib.pyplot as plt

def generate_chart(data_json, filename, title):
    xAxis = [key for key, value in data_json.items()]
    yAxis = [value for key, value in data_json.items()]

    plt.grid(True)

    fig = plt.figure()
    plt.bar(xAxis, yAxis , color='maroon')
    plt.xlabel('Database')
    plt.ylabel('Time [s]')
    plt.title(title)
    plt.savefig("charts/" +filename, dpi='figure', format=None)

if __name__ == "__main__":
    data = {
        "variable-1": 1.0,
        "variable-2": 4.5,
        "variable-3": 2.3,
        "variable-4": 1.4,
        "variable-5": 1.3
    }

    generate_chart(data, "title", "test")
