import numpy
from pathlib import Path

array = numpy.array(list(map(int, Path("i7a.txt").read_text().split(","))))
guess = numpy.arange(array.min(), array.max() + 1)
distance = numpy.absolute(
    numpy.tile(guess, (array.shape[0], 1)).T - numpy.tile(array, (guess.shape[0], 1))
)
print((distance * (distance + 1) / 2).sum(axis=1).min())
