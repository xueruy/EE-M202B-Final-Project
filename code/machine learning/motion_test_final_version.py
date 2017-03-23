# EE M202 Final Project Code Final Version
# Xuerui Yan, Boyang Cai

import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from scipy.signal import argrelextrema #find local max and local min

import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from sklearn.linear_model import (
    LinearRegression, TheilSenRegressor, RANSACRegressor)


total_days = 1 #total day(s) combined in our dataset

###############################################################################################################
############################################ Data Read ########################################################
motion_data_file = open('weekday_data_new.csv', 'rb')
motion_data_raw = csv.reader(motion_data_file) #could keep read other files if more than one day

last_onezero_check = 1 # for removing all 0's before 1st 1. Also remember to remove all 0 in the end of raw data if there is no 1 after those.
last_hour = 0
last_minute = 0
last_second = 0
count = 0 #total data size

time = [] #time data array
time_difference = [] # the real data we will use in regression, unit: min
sensor_status = [] #'0','1' array
x_zero_moment = []

# Mining and tunning dataset, only need time interval between "0 -> 1"
# Min time unit: minute, data should be analyzed in one-day chronological order (~0:00 - 23:59)

###############################################################################################################
######################################## Select Motion Area ###################################################
#Motion 1 at Area 1
for raw in motion_data_raw:
	if raw[0][0] not in ('0','1','2','3','4','5','6','7','8','9'):
		pass
	elif (not raw[1]) or (int(raw[1]) == last_onezero_check):
		pass
	else:
		time.append(raw[0])
		sensor_status.append(raw[1])
		count += 1
		last_onezero_check = int(raw[1])

# #Motion 2 at Area 2
# for raw in motion_data_raw:
# 	if raw[0][0] not in ('0','1','2','3','4','5','6','7','8','9'):
# 		pass
# 	elif (not raw[2]) or (int(raw[2]) == last_onezero_check):
# 		pass
# 	else:
# 		time.append(raw[0])
# 		sensor_status.append(raw[2])
# 		count += 1
# 		last_onezero_check = int(raw[2])

# #Motion 3 at Area 3
# for raw in motion_data_raw:
# 	if raw[0][0] not in ('0','1','2','3','4','5','6','7','8','9'):
# 		pass
# 	elif (not raw[3]) or (int(raw[3]) == last_onezero_check):
# 		pass
# 	else:
# 		time.append(raw[0])
# 		sensor_status.append(raw[3])
# 		count += 1
# 		last_onezero_check = int(raw[3])

# #Motion 4 at Area 4
# for raw in motion_data_raw:
# 	if raw[0][0] not in ('0','1','2','3','4','5','6','7','8','9'):
# 		pass
# 	elif (not raw[4]) or (int(raw[4]) == last_onezero_check):
# 		pass
# 	else:
# 		time.append(raw[0])
# 		sensor_status.append(raw[4])
# 		count += 1
# 		last_onezero_check = int(raw[4])

##############################################################################################################
##################################### Mining the x,y data for regression #####################################
## get time difference between '0' and '1'
for item in range(len(sensor_status)):
	if int(sensor_status[item]) == 0:
		last_hour = int(time[item][:2])
		last_minute = int(time[item][3:5])
		last_second = int(time[item][6:8])
		x_zero_moment.append(time[item][:8])
		
	else:
		time_difference.append((int(time[item][:2]) * 3600 + int(time[item][3:5]) * 60 + int(time[item][6:8])) - (last_hour * 3600 + last_minute * 60 + last_second)) 

# print sensor_status
x_zero_moment_tosec = [int(time[:2]) * 3600 + int(time[3:5]) * 60 + int(time[6:8]) for time in x_zero_moment]

##############################################################################################################
#### If the data are from more than one days, use the following method to combine and integrate the data #####

# total_days = 2

# #days' data example
# time_tosec_1 = [10000,37333,50000,70000,99998,100000]
# time_dfference_1 = [13.23,118.7,25.9,96.8,77,111.2]

# time_tosec_2 = [10000,37333,50010,77000,98998,100030]
# time_dfference_2 = [70,88,611,32.3,19.9]




# data_day1 = zip(time_tosec_1, time_dfference_1)
# data_day2 = zip(time_tosec_2, time_dfference_2)

# print data_day1
# print data_day2


# data_dic = {}
# count_dic = {}

# for index in range(len(data_day1)):
# 	count_dic.update({data_day1[index][0]:0})
# 	data_dic.update({data_day1[index][0]:data_day1[index][1]})

# #keep using this method to get the integrated data till total days if total days >= 2
# for index in range(len(data_day2)):
# 	if data_day2[index][0] not in data_dic.keys():
# 		count_dic.update({data_day2[index][0]:0})
# 		data_dic.update({data_day2[index][0]:data_day2[index][1]})
# 	else:
# 		count_dic[data_day2[index][0]] += 1
# 		data_dic[data_day2[index][0]] = float(data_dic[data_day2[index][0]] + data_day2[index][1]) / (count_dic[data_day2[index][0]] + 1)



# print data_dic
# # print data_dic[0][0]


# combined_time = data_dic.keys()
# combined_time.sort()
# print combined_time # time_tosec (x) ready to be used in machine learning and regression
# combined_time_difference = data_dic.values()
# print combined_time_difference # time_difference (y) ready to be used in machine learning and regression

##############################################################################################################
############################ Using data do regression with different regressors ##############################


# LSE way to solve by Numpy, error large for now, think to optimize

# x = np.arange(0, len(time_difference), 1)
# y = np.array(time_difference)
# def func(x,a,b):
#     return a * np.exp(b/x) #not good model

# popt, pcov = curve_fit(func, x, y)
# a=popt[0]
# b=popt[1]
# yvals=func(x,a,b)
# plot1=plt.plot(x, y, '*',label='original values')
# plot2=plt.plot(x, yvals, 'r',label='curve_fit values')
# plt.xlabel('x axis')
# plt.ylabel('y axis')
# plt.legend(loc=2)
# plt.title('curve_fit')
# plt.show()
# # plt.savefig('p2.png')





#Polynomial fit by Numpy,perform better for now

#time interval cant use single time point represent the plot,
#so use number(0 - some num) instead, when calculate the avg time difference by integral,
#use time interval to replace those numbers (length of time_difference)

# x = np.arange(1, len(time_difference) + 1, 1) 
# y = np.array(time_difference)
# z1 = np.polyfit(x, y, 7) # determine function coeffs
# p1 = np.poly1d(z1) # for display function
# print(p1) # print function in the console
# y_vals = np.polyval(z1,x)
# plot1 = plt.plot(x, y, '*',label='original values')
# plot2 = plt.plot(x, y_vals, 'r',label='polyfit values')
# plt.xlabel('x axis')
# plt.ylabel('y axis')
# plt.legend(loc = 2) # choose legend location
# plt.title('polyfitting')
# plt.show()

# plt.savefig('p1.png')






#Polynomial fit with machine learning by sklearn

# generate points used to plot, all real x values

# x_zero_moment_tosec = [int(time[:2]) * 3600 + int(time[3:5]) * 60 + int(time[6:8]) for time in x_zero_moment]
x_plot = x_zero_moment_tosec
y_plot = np.array(time_difference)

# generate points and keep a subset of them
train_x_index = np.arange(0, len(time_difference), 1)
rng = np.random.RandomState(0)
rng.shuffle(train_x_index)
train_x_index = np.sort(train_x_index[:1000]) #change size of train data
train_x = []
train_y = []
for i in train_x_index:
	if time_difference[i] > 60: #sensor 1 -> 0 reset time
		train_x.append(x_zero_moment_tosec[i])
		train_y.append(time_difference[i])
	# train_x.append(x_zero_moment_tosec[i])
	# train_y.append(time_difference[i])

# print x_zero_moment_tosec
# print time_difference
# create matrix versions of these arrays
train_x = np.asarray(train_x)
x_plot = np.asarray(x_plot)
X = train_x[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]
Y_plot = y_plot[:, np.newaxis]

lw = 2

plt.plot(x_zero_moment_tosec, y_plot, color='darkgrey', linewidth=lw, label="ground truth")
plt.scatter(train_x, train_y, color='grey', s=30, marker='o', label="training points")

# #for print three poly-plots together
# for count, degree in enumerate([8]): #change poly-degree
#     model = make_pipeline(PolynomialFeatures(degree), Ridge())
#     model.fit(X, train_y)
#     y_predict = model.predict(X_plot)
#     plt.plot(x_plot, y_predict, color=colors[count], linewidth=lw,
#              label="degree %d" % degree)

degree = 5 #change poly-degree

model = make_pipeline(PolynomialFeatures(degree = degree), Ridge(alpha=1)) #Ridge, alpha, regularization strength
# model = make_pipeline(PolynomialFeatures(degree = degree), LinearRegression(fit_intercept=True, normalize=True)) #LR
# model = make_pipeline(PolynomialFeatures(degree = degree), TheilSenRegressor(random_state=42)) #TSR
# model = make_pipeline(PolynomialFeatures(degree = degree), RANSACRegressor(random_state=42)) #RR


model.fit(X, train_y)
y_predict = model.predict(X_plot)
plt.plot(x_zero_moment_tosec, y_predict, color='blue', linewidth=lw, label="degree %d" % degree)
plt.legend(loc = 2)
plt.xlabel('Time Difference Moment (absolute sec)')
plt.ylabel('Time Difference')
plt.title('Time Difference vs. moments by Machine Learning')
plt.show()
score = model.score(X_plot, y_plot)
# print score


#Then put the y_predict data and x_plot data to the Numpy to output the readable polynomial equation
z1 = np.polyfit(x_plot, y_predict, degree) # determine function degree
p1 = np.poly1d(z1) # for display function
print(p1) # print function in the console
y_vals = np.polyval(z1,x_plot)
# print y_predict
# print y_vals
plot1 = plt.plot(x_zero_moment_tosec, y_predict, '*', color='dodgerblue', label='predict values')
plot2 = plt.plot(x_zero_moment_tosec, y_vals, 'r', linewidth=2.5, label='polyfit values')
# plt.scatter(train_x, train_y, color='blue', s=30, marker='o', label="training points")
plt.xlabel('Time Difference Moment (absolute sec)')
plt.ylabel('Time Difference')
plt.legend(loc = 2) # choose legend location
plt.title('Final Poly-fitting Time Model')
plt.show()

############################################################################################################################################
####### Calculate and plot final average time differences by utilizing second derivative and integral exerted on the regression result #####

#First, Find second derivitive = 0 to determin the time intervals we will select
time_difference_new = np.asarray(time_difference)

second_deriv_p1 = p1.deriv().deriv()
root_points = second_deriv_p1.r # p1'' result

#Note that roots for choosing time interval, need to check, in case of the roots that f'' = 0, but it is not inflection point
root_points.sort()
# print 'root_points', root_points # f'' = 0 found, now we could assign the time intervals by ourselves based on the second deriv help. 


#Secondly we calculate the (definate) integral in the different time intervals
i = p1.integ() #entire fitting function's integral

thresholdTime = 5 * 60 #seconds
def calculateEnergy(deltaT, occurTime, totalTime, lightOffProbability, totalLightOffTime, lightOffTime, tdMean):
	 #occurTime is the time where each "1" event that larger than threshold time happened within the current deltaT
	 #setupEnergy in W*sec and maintainPower in W
	 #Energy in W*sec
	 maintainPower = 26 #W
	 setupEnergy = 26 * thresholdTime
	 waitTime = 0 # customize
	 if lightOffProbability > 0.6:#time interval is not reliable if (tdMean * totalTime) > (totalLightOffTime)
	 	lightOnTime = deltaT - totalLightOffTime - totalTime * 1 + waitTime # can not exceed delta T
		optimized_Energy = lightOnTime * maintainPower + (1 - lightOffProbability) * totalTime * setupEnergy# still use 5min rule, occurTime dominate, assume 'occurtime' number of ppl come to calculate on/off times
	 else:
	 	lightOnTime = deltaT - (tdMean * occurTime) - totalTime * 1 + waitTime #can not exceed delta T, occurTime not dominate, turnoff time follow tMean
	 	optimized_Energy = lightOnTime * maintainPower + occurTime * setupEnergy

	 sensor_Energy = occurTime * setupEnergy + maintainPower * (deltaT - lightOffTime + occurTime * 5 * 60 - totalTime * 1)
	 regular_Energy = deltaT * maintainPower + setupEnergy * 1
	 return optimized_Energy/3600, regular_Energy/3600, sensor_Energy/3600 #unit: W*h

#Then Calculate avg time difference(0->1) in specific time interval
def avg_td(x1,x2):
	integ_td = i(x2) - i(x1)
	avg_td_value = integ_td / (x2 - x1) # way of calculating avg for continuous function
	occurTime = 0
	lightOffTime = 0
	totalTime = 0
	totalLightOffTime = 0
	for index in range(len(x_zero_moment_tosec)):
		j = x_zero_moment_tosec[index]
		if y_plot[index] < thresholdTime:
			pass
		elif j >= x1 and j < x2: #think about adding occurtime counts around its time interval
			occurTime += 1
			lightOffTime += y_plot[index]
		if j >= x1 and j < x2:
			totalLightOffTime += y_plot[index]
			totalTime += 1

	print 'occurTime', occurTime
	# print totalLightOffTime, avg_td_value * totalTime
	lightOffProbability = float(lightOffTime) / float(totalLightOffTime)

	print 'lightOffProbability', lightOffProbability
	optimized_Energy, regular_Energy, sensor_Energy = calculateEnergy(x2 - x1, occurTime, totalTime, lightOffProbability, totalLightOffTime, lightOffTime, avg_td_value)
	print 'the average of time differences(0->1) in this time interval is ', avg_td_value, 'this time interval is from %ss to %ss in absolute seconds' %(int(x1), int(x2))
	print 'the naive energy consumption in this time period is %sWH, whereas our optimized energy consumption is %sWH' %(regular_Energy, optimized_Energy)
	print 'the energy consumption for the sensor mode is %sWH' % sensor_Energy


print 'The testing time of this dataset is from %s to %s in real clock time' %(x_zero_moment[0], x_zero_moment[len(x_zero_moment) - 1])

# Split time intervals with starting, second deriv and ending points
fristFlag = True
for index in range(len(root_points)):
	if x_zero_moment_tosec[0] > root_points[index]:
		pass
	elif x_zero_moment_tosec[len(x_zero_moment_tosec) - 1] < root_points[index]:
		if fristFlag:
			if x_zero_moment_tosec[len(x_zero_moment_tosec) - 1] < root_points[index]:
				pass
			else:
				avg_td(x_zero_moment_tosec[0], root_points[index])
				avg_td(root_points[index], x_zero_moment_tosec[len(x_zero_moment_tosec) - 1])
		else:
			avg_td(root_points[index - 1], x_zero_moment_tosec[len(x_zero_moment_tosec) - 1])
		break
	else:
		if(fristFlag):
			avg_td(x_zero_moment_tosec[0], root_points[index])
			fristFlag = False
		else:
			avg_td(root_points[index-1], root_points[index])
			if index == len(root_points) - 1:
				avg_td(root_points[index], x_zero_moment_tosec[len(x_zero_moment_tosec) - 1])


