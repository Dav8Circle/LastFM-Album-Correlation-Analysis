import numpy as np
import matplotlib.pyplot as plt
import mplcursors

def main():

	# Read from playcount files 
	firstDataset = open('outputalltimeweek1.txt','r')
	secondDataset = open('outputalltimeweek2.txt','r')
	firstDataset = firstDataset.read()
	secondDataset = secondDataset.read()
	processed = 0
	H1_accepted = []
	graph_titles = []
	songs_and_plays = []

	firstDataset = firstDataset.split('\n')
	secondDataset = secondDataset.split('\n')

	def calculation(indexNo):
		counter = 0
		while counter < len(firstDataset):
			if counter % 2 == 0:
				graph_titles.append(firstDataset[counter])
				counter += 1
			else:
				songs_and_plays.append(firstDataset[counter])
				counter += 1

		n = songs_and_plays[indexNo]
		n = n.split(',')
		
		song_names = []
		plays = []
		new_songs_and_plays = []

		# Janky type conversion

		for i in n:
			i = i.replace('[', '')
			i = i.replace(']', '')
			i = i.lstrip()
			new_songs_and_plays.append(i)

		for i in new_songs_and_plays:
			if new_songs_and_plays.index(i) % 2 == 0:
				song_names.append(i)
			else:
				i = int(i)
				plays.append(i)

		second_songs_and_plays = []

		counter = 0
		while counter < len(secondDataset):
			if counter % 2 == 0:
				counter += 1
			else:
				second_songs_and_plays.append(secondDataset[counter])
				counter += 1

		o = second_songs_and_plays[indexNo]
		o = o.split(',')
		
		second_new_songs_and_plays = []
		for i in o:
			i = i.replace('[', '')
			i = i.replace(']', '')
			i = i.lstrip()
			second_new_songs_and_plays.append(i)

		# Create array and fill with change in playcounts over time
		difference = []

		for i in second_new_songs_and_plays:	
			if second_new_songs_and_plays.index(i) % 2 == 0:
				pass
			else:
				i = int(i)
				difference.append(i)


		diff = []

		for k in difference:
			N = difference.index(k)
			diff.append(k - plays[N])

		length = (np.arange(0, len(diff), 1) + 1)


		# Critical Regions
		CRTable5 = [0.9877 ,0.9000, 0.8054, 0.7293, 0.6694, 0.6215, 0.5822, 0.5494, 0.5214, 0.4973, 0.4762, 0.4575, 0.4409, 0.4259, 0.4124, 0.4000, 0.3887, 0.3783, 0.3687, 0.3598, 0.3515, 0.3438, 0.3365, 0.3297, 0.3233, 0.3172, 0.3115, 0.3061]
		sampleCheck = np.arange(3, 31, 1)

		# Line of Best Fit
		calculation_array = diff.copy()

		standard_deviation = np.std(calculation_array, axis = None)
		meanY = (sum(calculation_array) / len(length))
		for i in diff:
			if i > meanY + standard_deviation:
				calculation_array.pop(calculation_array.index(i))

			
			if i < meanY - standard_deviation:
				calculation_array.pop(calculation_array.index(i))
				
		# Calculate PMCC
		length_calculation = (np.arange(0, len(calculation_array), 1) + 1)
		meanX = sum(length_calculation) / len(length_calculation)
		xMinusMeanX = [(element - meanX)  for element in length_calculation]
		yMinusMeanY = [(element - meanY)  for element in calculation_array]
		squares = np.square(xMinusMeanX)
		sumSquares = sum(squares)
		sumOfProducts = sum(np.multiply(xMinusMeanX, yMinusMeanY))
		beta = sumOfProducts / sumSquares
		alpha = meanY - (beta * meanX)
		yAxisPoints = [((element * beta) + alpha)  for element in length]
		pmcc = (sum(np.multiply(xMinusMeanX, yMinusMeanY))) / np.sqrt(sum(np.square(xMinusMeanX)) * sum(np.square(yMinusMeanY)))
		print(song_names, diff)
		print('The Pearson correlation coefficient is', pmcc)
		sample_length = len(diff)
		for i in sampleCheck:
			try:
				if i == sample_length:
					critical_value = CRTable5[(i - 4)]
			
			except IndexError:
				pass
			except UnboundLocalError:
				pass
		
		# Hypothesis Test
		if abs(pmcc) <= critical_value:
			print('Insufficient evidence to reject H0')
		
		else:
			print('Accept the alternative hypothesis')
			H1_accepted.append(diff)

		# Graphing stage - remove if visualisation not required
		choice = int(input('Would you like to see the graphs for these statistics? \n 1: Yes \n 2: No \n'))
		if choice == 1:
			_, ax = plt.subplots()
			plt.scatter(length, diff, linewidth=3)
			plt.plot(length,yAxisPoints,'k')
			plt.ylabel('Growth in Plays')
			plt.tight_layout()
			labels = song_names
			mplcursors.cursor(ax).connect(
			"add", lambda sel: sel.annotation.set_text(labels[round(sel.target.index)]))
			plt.show()
		if choice == 2:
			pass


	for i in firstDataset:
		try:
			K = firstDataset.index(i)
			calculation(K)
			processed += 1 
		except ValueError:
			pass
		except IndexError:
			pass
		except UnboundLocalError:
			pass
		except ZeroDivisionError:
			pass

	# Summary
	print('Total possible albums: 166 \nTotal processed:', processed)
	print('Number of times H0 was rejected:', len(H1_accepted))

if __name__ == '__main__':
	main()
