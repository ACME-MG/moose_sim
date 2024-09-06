import matplotlib.pyplot as plt
import numpy as np
import cv2

# Parameters for the video
video_filename = 'output_video.mp4'
frame_rate = 10  # Frames per second
num_frames = 100  # Number of frames in the video
frame_size = (640, 480)  # Size of the video frame (width, height)

# Set up the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
video_writer = cv2.VideoWriter(video_filename, fourcc, frame_rate, frame_size)

# Generate and save each frame
for i in range(num_frames):
    # Create a figure
    fig, ax = plt.subplots(figsize=(frame_size[0] / 100, frame_size[1] / 100))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Plot something that changes over time
    x = np.linspace(0, 10, 100)
    y = np.sin(x + i * 0.1)
    ax.plot(x, y, color='blue')
    ax.set_title(f'Frame {i+1}')

    # Save the plot to an image in memory
    fig.canvas.draw()
    img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # Resize image if necessary
    img = cv2.resize(img, frame_size)

    # Convert RGB to BGR for OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Write the frame to the video
    video_writer.write(img)

    # Close the figure to avoid memory leaks
    plt.close(fig)

# Release the video writer
video_writer.release()

print(f'Video saved as {video_filename}')