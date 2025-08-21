from io import BytesIO
import base64
import matplotlib.pyplot as plt


def get_graph():
    # creates ByteIO buff for image
    buffer = BytesIO()

    # create a plot with a bytesIO object as a file-like object. Set format to png
    plt.savefig(buffer, format='png')

    # set cursor to the ginning of the stream
    buffer.seek(0)

    # retrieve content of that file
    image_png = buffer.getvalue()

    # encode the bytes-like object
    graph = base64.b64encode(image_png)

    # decode to ge tthe string as output
    graph = graph.decode('utf-8')

    # freeup the memory of buffer
    buffer.close()

    # retu the image/graph to user
    return graph


# chart_type: user input of type of chart,
# data: pandas dataframe
def get_chart(chart_type, data, **kwargs):
    # switch plot backend to AGG (Anti-Grain Geometry) - to write to file
    # AGG is preferred solution to write PNG files
    plt.switch_backend('AGG')

    # figure size
    fig = plt.figure(figsize=(10, 6))

    # select chart_type based on user input from the form
    if chart_type == '#1':
        # plot bar chart between difficulty on x-axis and quantity on y-axis
        bars = plt.bar(data['difficulty'], data['quantity'], color=[
                       '#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
        plt.xlabel('Difficulty Level', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Recipes', fontsize=12, fontweight='bold')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                     f'{int(height)}', ha='center', va='bottom', fontweight='bold')

    elif chart_type == '#2':
        # generate pie chart based on difficulty distribution
        labels = kwargs.get('labels')
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        plt.pie(data['quantity'], labels=labels,
                autopct='%1.1f%%', colors=colors, startangle=90)

    elif chart_type == '#3':
        # plot line chart based on difficulty on x-axis and quantity on y-axis
        plt.plot(data['difficulty'], data['quantity'], marker='o',
                 linewidth=2, markersize=8, color='#3498db')
        plt.xlabel('Difficulty Level', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Recipes', fontsize=12, fontweight='bold')

        # Add value labels on points
        for i, (x, y) in enumerate(zip(data['difficulty'], data['quantity'])):
            plt.text(x, y + 0.1, f'{int(y)}', ha='center',
                     va='bottom', fontweight='bold')
    else:
        print('unknown chart type')

    # specify layout details
    plt.tight_layout()

    # render the graph to file
    chart = get_graph()
    return chart
