from kedro.io import AbstractDataSet

from typing import Any, Dict, List

#from pathlib import PurePosixPath

#import fsspec
#import skvideo
#import matplotlib.pyplot as plt

import numpy as np


class VideoDataSet(AbstractDataSet):
	"""´´VideoDataSet´´ loads / saves a random number of samples of frames 
	from a video in a given filepath as numpy arrays using matplotlib.pyplot.

	"""

	def __init__(self, filepath: str, num_images: int):
		"""Creates a new instance of VideoDataSet to load/save frames from 
		a video at a given filepath.

		Args:
			filepath: The location of the video file to load/save frames from. 
			num_images: Number of frames to save.

		"""

		self._filepath = filepath
		self._num_images = num_images

	def _load(self) -> List[np.ndarray]:
		"""Loads frames from the video file.

		Returns:
			Frames from the video file as a numpy array.
		"""
		# using get_filepath_str ensures that the protocol and path are appended correctly for different filesystems
		load_path = self._filepath
		with self._fs.open(load_path) as f:
			# Use vreader as it loads the video frame-by-frame
			# If it is a large video, using vread() may exhaust the memory
			videogen = skvideo.io.vreader(video_path)
			random_set = self._random_items(videogen, self._num_images)
			return random_set

	def _save(self, data: List[np.ndarray]) -> None:
		"""Saves image data to the specified filepath"""
		count = 0

		for frame in data:
			directory = "{0}/image{1}.png".format(save_to_path, count)
			plt.imsave(directory, frame)
			# if you instead want to just show the images in a notebook
			# instead of saving, use imshow()
			# plt.imshow(frame, interpolation='nearest')
			plt.show()
			count += 1

	def _describe(self) -> Dict[str, Any]:
		"""Returns a dict that describes the attributes of the dataset"""
		...


	def _random_items(self, iterator: List[np.ndarray], num_images: int) -> List[np.ndarray]: 
		"""Helper function, returns a subset of images from a frame sequence"""

		selected_items = [None] * num_images

		for item_index, item in enumerate(iterator):
			for selected_item_index in xrange(num_images):
				if not random.randint(0, item_index):
					selected_items[selected_item_index] = item

		return selected_items

"""
# Borrowed from https://alisha17.github.io/python/2017/12/29/extractimagesfromvideos.html
# Return 'num_images' no. of random images
def random_items(iterator, num_images=1):
    selected_items = [None] * num_images

    for item_index, item in enumerate(iterator):
        for selected_item_index in xrange(num_images):
            if not random.randint(0, item_index):
                selected_items[selected_item_index] = item

    return selected_items

# Read the video, extract images and save them to a directory
def extract_images(video_path, num_images, save_to_path):
    # Use vreader as it loads the video frame-by-frame
    # If it is a large video, using vread() may exhaust the memory
    videogen = skvideo.io.vreader(video_path)
    random_set = random_items(videogen, num_images)

    count = 0

    for frame in random_set:
        directory = "{0}/image{1}.png".format(save_to_path, count)
        plt.imsave(directory, frame)
        # if you instead want to just show the images in a notebook
        # instead of saving, use imshow()
        # plt.imshow(frame, interpolation='nearest')
        plt.show()
        count += 1
"""