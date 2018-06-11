# A module for drawing a chart with the turtle
import turtle  # import module
import math

WINDOW_WIDTH = 800  # size constants for easy changing
WINDOW_HEIGHT = 500


def draw_axes(my_turtle, file_loc, chart_title):
    """
    Function
    -------------
    Draw x and y axis for the chart and give the chart title on top
    Expected Arguments
    ------------------
    my_turtle: turtle.Turle, turtle object
    file_loc: str, location of file entered by the user
    chart_title: str, Chart Title entered by the user
    Returns
    --------
    chart_width: width of the chart
    pixels_per_val: Number of pixels used per ytick
    start_x: starting x-coordinate of chart
    start_y: starting y-coordinate of chart
    """
    # create x axis
    chart_width, chart_height, start_x, start_y = draw_x_axis(my_turtle)
    # create y axis
    draw_y_axis(my_turtle, chart_height, start_x, start_y)
    # draw ytick marks for the chart
    pixels_per_val = draw_y_tick_marks(
        my_turtle, chart_height, start_x, start_y, file_loc)
    # give title for the chart
    write_chart_title(my_turtle, chart_title, start_x, start_y + chart_height)

    return (chart_width, pixels_per_val, start_x, start_y)


def write_chart_title(my_turtle, chart_title, x, y):
    """
    Write the chart title on top
    Expected Arguments
    ------------------
    my_turtle: turtle.Turle, turtle object
    chart_title: str, Chart Title entered by user
    x: int, starting x-coordinate of chart
    y: int, y-coordinate of the top most ytick
    """
    my_turtle.penup()
    my_turtle.goto(x+20, y+10)
    my_turtle.pendown()
    my_turtle.write(chart_title.upper(), font=("Arial", 20, "normal"))


def draw_x_axis(my_turtle):
    """
    Calculate initial x and y coordinates and draw x axis for the chart
    Expected Arguments
    ------------------
    my_turtle: turtle.Turle, turtle object
    Returns
    --------
    chart_width: width of the chart
    chart_height: height of the chart
    start_x: starting x-coordinate of chart
    start_y: starting y-coordinate of chart
    """
    scale_factor = 0.85
    # use scale_factor to dynamically set the chart size
    chart_height = scale_factor * WINDOW_HEIGHT
    chart_width = scale_factor * WINDOW_WIDTH
    # calculate starting x and y coordinates of the chart
    start_x = chart_width*(1-scale_factor)/2
    start_y = chart_height*(1-scale_factor)/2

    my_turtle.penup()       # do not draw while moving
    my_turtle.goto(start_x, start_y)  # walk to coordinates
    my_turtle.pendown()     # start drawing again
    my_turtle.forward(chart_width)   # move forward
    return (chart_width, chart_height, start_x, start_y)


def draw_y_axis(my_turtle, chart_height, start_x, start_y):
    """
    Draw y axis for the chart
    Expected Arguments
    ------------------
    my_turtle: turtle.Turle, turtle object
    chart_height: int, height of the chart
    start_x: int, starting x-coordinate of chart
    start_y: int, starting y-coordinate of chart
    """
    my_turtle.penup()       # do not draw while moving
    my_turtle.goto(start_x, start_y)  # walk to coordinates
    my_turtle.pendown()     # start drawing again
    my_turtle.left(90)      # turn left
    my_turtle.forward(chart_height)  # move forward


def draw_y_tick_marks(my_turtle, chart_height, start_x, start_y, file_loc):
    """
    Function
    -------------
    Draw tick marks and write labels for y-axis of the chart
    Expected Arguments
    -------------
    my_turtle: turtle.Turle, turtle object
    chart_height: int, height of the chart
    start_x: int, starting x-coordinate of chart
    start_y: int, starting y-coordinate of chart
    file_loc: str, location of file entered by user
    Returns
    ------------
    pixels_per_val: Number of pixels used per ytick
    """
    num_ticks = 10
    max_value = get_max_value(file_loc, 1)
    # calculate label of ytick
    y_tick_val = round(max_value/num_ticks, 2)
    # calculate number of pixels to move for one ytick
    pixels_per_val = chart_height/max_value
    # calculate number of pixels moved for each ytick
    pixels_per_label = max_value / num_ticks * pixels_per_val
    # Loop over number of yticks to write the labels
    for i in range(num_ticks+1):
        my_turtle.penup()
        my_turtle.goto(start_x, start_y+pixels_per_label*(i))
        my_turtle.pendown()
        my_turtle.left(90)
        my_turtle.forward(12)
        my_turtle.penup()
        my_turtle.forward(20)
        my_turtle.pendown()
        my_turtle.write(round(y_tick_val*i, 2), font=("Arial", 10, "normal"))
        my_turtle.penup()
        my_turtle.right(180)
        my_turtle.forward(10)
        my_turtle.left(90)
    return pixels_per_val


def draw_rectangle(my_turtle, pos_x, pos_y, width, height, order_val):
    """
    Draw x and y axis for the chart and give the chart title on top
    Expected Arguments
    ------------------
    my_turtle: turtle.Turle, turtle object
    pos_x: int, x-coordinate of starting point of rectangle
    pos_y: int, y-coordinate of starting point of rectangle
    width: int, width of the rectangle
    height: int, height of the rectangle
    order_val: int, position of observation in the file 
    """
    my_turtle.begin_fill()
    col = choose_color(order_val)
    my_turtle.color('black', col)
    my_turtle.penup()
    my_turtle.goto(pos_x, pos_y)
    my_turtle.pendown()
    my_turtle.forward(height)
    my_turtle.right(90)
    my_turtle.forward(width)
    my_turtle.right(90)
    my_turtle.forward(height)
    my_turtle.right(90)
    my_turtle.forward(width)
    my_turtle.end_fill()


def draw_bars(my_turtle, file_loc, chart_width, pixels_per_val, start_x, start_y):
    """
    Draw bars for the chart
    Expected Arguments
    ------------------
    my_turtle: turtle.Turle, turtle object
    file_loc: str, location of file entered by user
    chart_width: width of the chart
    pixels_per_val: Number of pixels used per ytick
    start_x: starting x-coordinate of chart
    start_y: starting y-coordinate of chart
    """
    # calculate total number of observations in file
    num_obs = count_observations(file_loc)
    # scale_factor to scale the width of each bar
    scale_factor = 0.8
    # calculate width of each bar
    width = (chart_width/num_obs) * scale_factor
    # calculate x and y coordinates of the starting bar using scale factor
    pos_x = ((1-scale_factor)/2)*width + start_x
    pos_y = start_y
    # Loop over the file to extract name and feature value and draw bar for each observation
    with open(file_loc) as file:
        for i in range(num_obs):
            name = file.readline()
            val = file.readline()
            next(file)
            draw_rectangle(my_turtle, pos_x, pos_y, width,
                           int(val)*pixels_per_val, i)
            draw_xaxis_labels(my_turtle, name, width)
            pos_x = pos_x + width/scale_factor


def draw_xaxis_labels(my_turtle, label, width):
    """
    Function
    -------------
    Draw x-axis labels for the chart
    Expected Arguments
    ------------------
    my_turtle: turtle.Turle, turtle object
    label: str, label on x-axis for each bar
    width: int, width of each bar 
    """
    my_turtle.penup()
    my_turtle.left(90)
    my_turtle.forward(40)
    my_turtle.left(90)
    my_turtle.forward(width/2)
    my_turtle.left(90)
    my_turtle.pendown()
    my_turtle.write(label, font=("Arial", 10, "normal"), align='center')


def choose_color(order_val):
    """
    Function
    -------------
    Choose color for each bar based on the index of each observation
    Expected Arguments
    ------------------
    order_val: int, observation number in the file
    """
    # create a list for the color palette
    list_colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3']
    # iterate over the list and choose color based on each observation
    while(order_val >= len(list_colors)):
        order_val = order_val - len(list_colors)
    return list_colors[order_val]


def count_observations(file_path):
    """
    Function
    -------------
    Count and return number of observations in the file(considering 3 lines per observation)
    Expected Arguments
    ------------------
    file_path: str, file name along with path, entered by the user
    Returns
    ---------------
    count_obs: int, total number of observations in the file
    """
    count_lin, count_obs = 0, 0
    with open(file_path) as file:
        for line in file:
            count_lin = count_lin + 1
            if(count_lin % 3 == 0):
                count_obs += 1
    return (count_obs)


def get_max_value(file_path, feature):
    """
    Function
    -------------
    Get maximum value of feature in tht input file
    Expected Arguments
    ------------------
    file_path: str, file name along with path, entered by the user
    feature: int, which feature to consider
    Returns
    ----------------
    max_val: int, returns maximum value of feature
    """
    num_obs = count_observations(file_path)
    max_val = -1*math.inf
    with open(file_path) as file:
        # iterate over number of observations and compare each value with max_val
        for i in range(num_obs):
            next(file)
            if(feature == 1):
                val = file.readline()
                # if value is greater than max_val, assign that value to max_val variable
                if(int(val) > max_val):
                    max_val = int(val)
                next(file)
            elif(feature == 2):
                next(file)
                val = file.readline()
                # if value is greater than max_val, assign that value to max_val variable
                if(int(val) > max_val):
                    max_val = int(val)
            else:
                print("Invalid feature")
    return max_val


def main():
    """
    First function to be executed
    """
    # get inputs of file name and chart title from the user
    file_input = input("Which file do you want to visualize?")
    chart_title = input("What should the chart be named?")

    # Define window size as constants
    window = turtle.Screen()  # create a window for the turtle to draw on
    # specify window size (width, height)
    window.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    # coordinate system: origin at lower-left
    window.setworldcoordinates(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Create the turtle
    my_turtle = turtle.Turtle()
    my_turtle.speed("fastest")  # how fast the turtle should move

    # the title to show at the top of the window
    window.title('Turtle Graphics')

    # draw x and y axis of the chart
    chart_width, pixels_per_val, start_x, start_y = draw_axes(
        my_turtle, file_input, chart_title)
    # draw bars of the chart
    draw_bars(my_turtle, file_input, chart_width,
              pixels_per_val, start_x, start_y)

    # hide turtle after processing is done
    my_turtle.hideturtle()

    # Make the turtle graphics appear and run, waiting for the user to close the screen
    # This MUST be the last statement executed in the script
    window.mainloop()


if __name__ == "__main__":
    main()
