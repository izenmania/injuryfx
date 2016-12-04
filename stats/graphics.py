import numpy as np
from matplotlib.figure import Figure
from matplotlib import cm as cm
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def generate_heatmap(coords):

    # Number of points
    n = 500

    # Takes a list of coordinate pairs and generates a heatmap, formatted for the site
    # Dummy numbers - placeholders.  In future will be generated from coords.
    x = 6*np.random.randn(n)
    y = 8*np.random.randn(n) + 30

    # Generate the 2d histogram
    # The domain is -24 to 24 inches horizontally and 0 to 60 inches vertically
    z, xedges, yedges = np.histogram2d(x, y, bins=[12,15], range = [[-24,24],[0,60]])

    # We need center coordinates instead of edges coordinates for the contour function
    # We add two because the bins are four inches wide
    xcenter = xedges + 2
    ycenter = yedges + 2
    xcenter = xcenter[:-1]
    ycenter = ycenter[:-1]
    Xcentermesh, Ycentermesh = np.meshgrid(xcenter, ycenter)

    # Create the figure object
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    # Create the contour plot
    CS = ax.contourf(Xcentermesh,Ycentermesh,z.T, 9, cmap = cm.YlOrRd)
    ax.axis([-22,22,2,58])
    ax.set_aspect('equal')
    fig.colorbar(CS)


    # Add the strike zone as a black box
    ax.plot([-12,12],[18,18],'k')
    ax.plot([-12,12],[42,42],'k')
    ax.plot([-12,-12],[18,42],'k')
    ax.plot([12,12],[18,42],'k')

    return fig

def get_pitch_count_list(pitch_types, pitches_df):
    'get a list of pinch counts that include 0 for pitches not in this dataframe'
    counts = []
    for pitch_type in pitch_types:
       for row in pitches_df.iterrows():
          if row[1]["pitch_type"] == pitch_type:
             counts.append(row[1]["pitch_count"])
             break
       else:
          counts.append(0)

    return counts

def create_bar_chart(pre_pitches_df, post_pitches_df, injury_id, window_size):
    'Create graph comparing pre injury pitch and post injury pitch selection'
    fig, ax = plt.subplots()
    x = list(set(pre_pitches_df["pitch_type"]) | set(post_pitches_df["pitch_type"]))
    n_groups = len(x)
    pre_counts = get_pitch_count_list(x, pre_pitches_df)
    post_counts = get_pitch_count_list(x, post_pitches_df)

    bar_width = 0.35
    opacity = .4
    index = np.arange(n_groups)

    rects1 = plt.bar(index, pre_counts, bar_width, alpha=opacity, color='r', label="Pre Injury")
    rects2 = plt.bar(index + bar_width, post_counts, bar_width, alpha=opacity, color='b', label="Post Injury")

    plt.xlabel('Pitch Type')
    plt.ylabel('Count')
    plt.xticks(index + bar_width, x)
    plt.legend()
    plt.title('Pitch Selection. injury_id = ' + str(injury_id) + "; window size = " + str(window_size))

    return fig

#    fig.savefig("/home/ubuntu/injuryfx/app/static/graphs/" + str(injury_id) + "-" +
#                str(window_size) + ".png") 

