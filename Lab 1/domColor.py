# Referenced tutorial: https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097 
# GeeksforGeeks Updating Plot: https://www.geeksforgeeks.org/how-to-update-a-plot-in-matplotlib/ 
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


cap = cv2.VideoCapture(0)
plt.ion() # enable interactivity
fig = plt.figure()
ax = fig.add_subplot(111)

while(True):
    # Capture frame-by-frame
    f_, frame = cap.read() 

    # create square of interest on screen
    central_x = len(frame)//2
    central_y = len(frame[1])//2
    x_s = central_x - 25
    y_s = central_y - 25
    cv2.rectangle(frame,(x_s,y_s),(x_s + 50,y_s + 50),(0,255,0),3)

    cv2.imshow('frame', frame) # show augmented frame

    # determine dominant color in square of interest
    img = frame[y_s + 3:y_s + 44, x_s + 3:x_s+44] # exclude drawn square
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    
    clt = KMeans(n_clusters=3) #KMeans
    clt.fit(img)

    # plot histogram
    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)
    plt.axis("off")
    plt.imshow(bar)
    plt.show()

    # Print RGB / HSV values
    RGB_vals = clt.cluster_centers_.astype('uint8')
    HSV_vals = cv2.cvtColor(np.array([RGB_vals]), cv2.COLOR_RGB2HSV) # convert to HSV
    print("RGB for 3 clusters:\n", clt.cluster_centers_)
    print("\nHSV for 3 clusters:\n", HSV_vals)

    # update plot
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Listen for user input to quit program
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()