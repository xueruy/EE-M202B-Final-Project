

# Introduction





# Background of Methodology

## Naive Lighting Control

For the naive lighting control, it is widely used in majority of large-scale public buildings. The Strategy of the naive lighting control is straightforward, which enable the ever-lasting lighting and no matter what kind of and how much environmental changes, the lighting schedules are not affected. This control strategy is almost controlled manually.  

## Sensor-mode Control

The sensor-mode control is the strategy that is commonly used since the sensor-based lighting system becomes more and more popular and universal. Normally, Once the flag raised (“1”) in the sensor, the light will keep ON for a constant time that usually depends on the user settings on the sensor, and then the light would be turned of due to “0” state raised in the sensor.


## Data Precontrol Model (DPM)

We designed the data precontrol model based on the machine learning regression method that predict light OFF waiting time condition in different time intervals during the day in the public building. 

The question might be asked: why machine learning? Our group tests other precontrol model with non-machine learning algorithm including self chose LSE method with exponential and logarithmic models and Polynomial Fit by Numpy, the results are not as well as our machine learning model, because those models are not covering enough parameters to robust the error or outliers in the data. We found our model fits better with polynomial regressive functions, so we decided to build up the polynomial model with machine learning. 

![](https://cloud.githubusercontent.com/assets/22850278/24234325/f042feae-0f54-11e7-8a5b-4177a7d7b066.png)

As for our frame and algorithm of DPM, generally, we mine the prepared (1/0) sensing data sorted in the excel files with csv version, which could include one or more days’ data depends on the requirement of the user. After collecting and preprocessing the data, we put the data into machine learning regression algorithm to train and test data so that we could get the non-linear regression of data. Then we put the trained data to the Numpy ployfit model to output the readable polynomial equation. Once the approximated function from regression is obtained, we could do second derivative and definite integral to set the different time intervals in the testing periods and get the average light OFF waiting time (0->1), respectively. Finally with our energy computing algorithm we could figure out the predicted lighting power consumptions in the assigned time intervals daily. It needs to be noticed that the power consumptions of Naive and Sensing-mode methods in these time intervals can also be calculated with our energy computing algorithm.



### Controllable Parameters in DPM Computation
We set up the following parameters in the DPM in order to get the better and more reasonable model.

*  Changeable data collection area for DPM computing

	The data collection areas sensed by different locationed sensors are changeable, so DPM is able to compute the different testing areas together or separately.  

*  Regression degrees

	We set the degree parameters, so that we could tune and verify our model performance by changing degrees of polynomial regression.

*  Regularization Strength (alpha)

	We set the changeable regularization strength (alpha) in the ridge regression model of DPM, which is a really important parameter for enhancing the performance of the regressive model. We could either tune the alpha manually or use built-in function set_params(**params) with sklearn in python to obtain a range of alpha and gradually shrink that range to specify the best value of regularization strength for the model

*  Normalization 

	We set True value in normalization, so the regressors will be normalized before regression. When the regressors are normalized, which makes the hyperparameters learnt more robust and almost independent of the number of samples. The feature of this parameter thus essential for our model built. 

*  Light OFF waiting threshold time

	The light OFF waiting threshold time is normally depend on the user's’ sensing building, so we set it to be changeable to be feasible for majority sensing setup in different buildings. 

*  Customized light ON wait time

	 This Configurable parameter is provided because in some buildings the user may want to  let the light be ON after the light OFF waiting threshold time for consideration of lighting comfort in the buildings.

### Machine Learning Regression Algorithm in DPM

We choose the PolynomialFeatures to generate polynomial and interaction features for our expected model. It can generate a new feature matrix consisting of all polynomial combinations of the features with degree less than/equal to the required regressive degree. For example, if input data is two dimensional and of the form [a,b], the 2-degree polynomial features are [1, a, b, a^2, ab, b^2].

After deciding to use PolynomialFeatures, we can implement the polynomial regression with linear model, using pipeline to add the polynomialfeatures.

Then we need to figure out what type of the linear model should we choose. At first when choosing the regressor, we tried many regressors of robust linear estimator fitting that could be good fit with our regression model. We tried RANSAC that is known as good for strong outliers in the y direction, TheilSen that is good for small outliers, both in direction X and y, OLS model that is widely used and classic ordinary least squares Linear Regression, and Ridge that solves a regression model where the loss function is the linear least squares function and regularization is given by the l2-norm, with built-in support for multi-variate regression.

The following graphs show the testing result of each linear model mentioned above.

<p align="center">
 <img src="https://cloud.githubusercontent.com/assets/22850278/24234436/8cfb51b0-0f55-11e7-8cbd-bb8bf9096edf.png">
 
 <img src="https://cloud.githubusercontent.com/assets/22850278/24234437/8cfbcd70-0f55-11e7-943e-ecd3dac312ba.png">
 
 <img src="https://cloud.githubusercontent.com/assets/22850278/24234438/8cfcbab4-0f55-11e7-81ba-3fee6c1c69d8.png">
 
 <img src="https://cloud.githubusercontent.com/assets/22850278/24234435/8cfb0ea8-0f55-11e7-8770-0623173db869.png">
</p>




# Experimental Setup

We choose one of the UCLA Boelter Hall 4th floor halls as our data collection place. We choose this place as our test area because this area has good internet service (our Smartthing hub only support LAN port) and this area has both low-density area and high-density area. Therefore, we can verify the model in different circumstance. Since we only have four sensors, we evenly distribute these sensors along the hall. Therefore, we divide the hall into 4 areas. 

Since my partner and I both have classes in the daytime, we are unable to get a complete one-day data. We take the trade off to spilt the one day data into different period within a week and combine the data we took for the whole week as one day. The reason we use this method is because the hall we choose only contains Seas Lab and offices and there is no classroom in the hallway. Therefore, there should be less variation on people volume within each weekday from Monday to Friday. Besides, we divide our data into Weekday group and Weekend group so we can get more accurate data for each day. For weekday, we choose 7:00am to 11:00pm as our time period.  We consider the other time period the same as “night time as this time period should has the same pattern as time around 11pm (and we need to sleep as well). For weekend, we choose 1pm to 8pm as our data time range. 

The sensor we choose is Smartthing motion sensor (2013 edition) powered by Samsung. Since the sensor is the first edition, we are unable to find its range. The average Battery life is around 2080 hrs. 

![sensor](https://cloud.githubusercontent.com/assets/10173940/24233055/c968b11e-0f4c-11e7-8622-b35aa09bf749.png)

We use this sensor to detect the occurrence of people in the different area in the hall. When the sensor detect a heat (a people), it will send the hub a “high” signal using Zigbee network. When the sensor detect no heat, it will send the hub a “low” signal one minute later using Zigbee.  

Beside the sensors, we also need to use the TP-LINK Wi-Fi as a wifi client for Smartthing Hub. The AP client transform the LAN signal of Smartthing Hub into wifi and connect to the Wifi of the campus. 

<p align="center">
 <img src="https://cloud.githubusercontent.com/assets/10173940/24233058/ccc015a0-0f4c-11e7-86d6-3ed3c73514eb.png">
</p>

We also get the information of the fluorescent lamp by taking a picture of the lamp. We learned that the working power of the lamp is 26W. So we will use this data to estimate the energy. 


Besides the equipment, we need to develop a way to log our data. We refer a code from online that can log data from smart sensor to the google sheet. The hub will log the data it get from the smart sensor as well as the current time. If the incoming data is “high”, it will log a “1” with the current time in the google sheet. It will log “0” if the incoming data is “low”. After we get the data, we change the time format and convert it to a csv file for python to read. 


# Experimental Results and Evaluation

Generally, we choose the degree 5 as our result for weekday because degree 5 has a higher score than degree 4 and degree 6. For the weekend, degree 4 has the higher score. 

For the weekday, we got the following graph and score for Area 1-4


<p align="center">

 <img src="https://cloud.githubusercontent.com/assets/10173940/24233375/14a513d2-0f4f-11e7-8d8f-2ec9523999aa.png">
 
 <img src="https://cloud.githubusercontent.com/assets/10173940/24233378/15c3e4fa-0f4f-11e7-88d6-9471910d559a.png">
 
 <img src="https://cloud.githubusercontent.com/assets/10173940/24233379/16d85fd8-0f4f-11e7-9865-bde5c38be792.png">
 
 <img src="https://cloud.githubusercontent.com/assets/10173940/24233401/3e87099e-0f4f-11e7-92c7-90060a1da5f3.png">
 
 <img src="https://cloud.githubusercontent.com/assets/10173940/24233522/0fb5fa16-0f50-11e7-9ba2-18ebbf0e4faf.png">
</p>

From the graph we can see that Naive model consumes the highest total energy among three models. We can also see that Sensor mode has more energy saving during the valley time(the 1st and the 4th period) but it has more energy consuming than Naive model because of the setup energy. Same for the DPM, the DPM has the minimum total energy consumption in three model types but it does not perform good in the region where there are higher frequency of people walking by. The Data Precontrol Model has a good energy consumption during the valley time because that it know at this time people terns to show up less frequently. Therefore it choose to turn off the lamp immediately after letting the current people pass by(and after a 1 min delay caused by sensor). 

The weekend data looks similar to weekday data, but with less frequency of people. Here is the weekend data for area 1-4:

![area1-2_weekend](https://cloud.githubusercontent.com/assets/10173940/24233569/5dcd3926-0f50-11e7-8f05-f134f1d2e199.png)
![area3_weekend](https://cloud.githubusercontent.com/assets/10173940/24233570/5eb6a854-0f50-11e7-8a14-83d53f69e2b4.png)
![area4_weekend](https://cloud.githubusercontent.com/assets/10173940/24233573/5ff00d0a-0f50-11e7-9ad6-9a6c68d89d90.png)
![weekend](https://cloud.githubusercontent.com/assets/10173940/24233575/6190e526-0f50-11e7-91b2-c390028dd2d6.png)

The data for weekend has less degree than the data for weekday. However, we notice that the two edges is going down rather than going up. We think the reason could be that the Seasnet is open on 1PM and closed around 8~9. Therefore there are more people coming and on on these two time period. We think that if we have more data, we could get rid of this kind of period. 

# Related Work

We did a lot of research, but actually there is no really similar research that could provide us some previous experiences and technology. In fact, We use self-piped regressive model in our case, so we did not figure out that other researcher or group that use this machine learning method to analyze the lighting system in large-scale public buildings. The only research paper found that are close to our research paper is the one that provided by Prof. Mani Srivastava. The paper named “Data Predictive Control for Peak Power Reduction”[4], which presents data-driven based methods which are implemented by data predictive control with regression trees (DPCRT) for making receding horizon control-oriented model in order to reduce peak power in buildings and maintain thermal comfort. The work of their research is relatively close to our topic and we get some inspiration from the experimental setup and the way of evaluation from their content of research paper.  

# Conclusion and Future work

Our experiment shows that the DPM method we use can reduce the energy consumed by the fluorescent lamp by dynamically change the waiting time for the lamp. The data shows that the energy could be decreased by 30% by using the Naive model. Yet there is a lot of improvement we can do, such as using more data as our sample to get a more accurate model for our prediction. We can also add the Office/class schedule into the data so the algorithm can set up a base model before learning the real data. 

This model should be embedded in microcontroller for real time use. We use Smartthing Hub because we want to see whether there is a potential energy drop by using Data Precontrol Mode. Now that we shows that using DPM can reduce the energy consumption, the next step would be using a real microcontroller and measure the energy by a physical meter to see the result. Although DPM method can drop the energy a lot, the hard part comes from the installation and the maintenance. As LED is replacing the fluorescent light in the future, then the combination of LED and DPM may reduce the energy consumption on campus to the lowest level. 


# Reference

[1] “Does Turning Fluorescent Lights Off Use More Energy Than Leaving Them On?”. Retrieved from: https://www.scientificamerican.com/article/turn-fluorescent-lights-off-when-you-leave-room/

[2] “Robust linear estimator fitting”. Retrieved from: http://scikit-learn.org/stable/auto_examples/linear_model/plot_robust_fit.html#sphx-glr-auto-examples-linear-model-plot-robust-fit-py 

[3] “Code reference for logging data to google sheet”. Retrieved From: https://community.smartthings.com/t/log-events-to-google-sheets-see-post-154-for-current-github-repo-and-v1-1/36719

[4] “Data Predictive Control for Peak Power Reduction”. A. jain, etc. Retrieved From:
https://dl.acm.org/citation.cfm?id=2993582

# Weekly Update

Week 6:

Get the equipment from the TA and set up the network of Smartthing

Week 7:

Write the code for Smartthing to automatically log sensor info on the online google Sheet. Start taking data. 

Week 8:

Set up the base algorithm, find which part should be learned by machine learning and keep taking data(including the weekend data)

Week 9:

Optimize the algorithm to evaluate the data precisely. Isolate weekend data from weekday data. Write the code for the control side. 

Week 10:

Optimize the algorithm. Set up the presentation. Building website
