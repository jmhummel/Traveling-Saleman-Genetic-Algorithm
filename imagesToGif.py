import imageio
import os

images = []
filenames = os.listdir('pics')
print filenames

movWriter = imageio.get_writer('stats.mp4', fps=2)
gifWriter = imageio.get_writer('stats.gif', fps=2)
for filename in filenames:
	img = imageio.imread('pics/' + filename)
	movWriter.append_data(img)
	gifWriter.append_data(img)
movWriter.close()
gifWriter.close()
# imageio.mimsave('stats.gif', images, duration=0.5)