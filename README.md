 EE-M202B-Final-Project

**Introduction**





**Methodology**

<p align="center">
  <img src="https://cloud.githubusercontent.com/assets/22850278/24138603/17d2e5e0-0dd6-11e7-9e12-df5e0b3af57c.png" width="550"/>
</p>





**Experimental Setup**

We choose one of the UCLA Boelter Hall 4th floor halls as our data collection place. We choose this place as our test area because this area has good internet service (our Smartthing hub only support LAN port) and this area has both low-density area and high-density area. Therefore, we can verify the model in different circumstance. Since we only have four sensors, we evenly distribute these sensors along the hall. Therefore, we divide the hall into 4 areas. 

Since my partner and I both have classes in the daytime, we are unable to get a complete one-day data. We take the trade off to spilt the one day data into different period within a week and combine the data we took for the whole week as one day. The reason we use this method is because the hall we choose only contains Seas Lab and offices and there is no classroom in the hallway. Therefore, there should be less variation on people volume within each weekday from Monday to Friday. Besides, we divide our data into Weekday group and Weekend group so we can get more accurate data for each day. For weekday, we choose 7:00am to 11:00pm as our time period.  We consider the other time period the same as “night time as this time period should has the same pattern as time around 11pm (and we need to sleep as well). For weekend, we choose 1pm to 8pm as our data time range. 

The sensor we choose is Smartthing motion sensor (2013 edition) powered by Samsung. Since the sensor is the first edition, we are unable to find its range. The average Battery life is around 2080 hrs. 

![sensor](https://cloud.githubusercontent.com/assets/10173940/24233055/c968b11e-0f4c-11e7-8622-b35aa09bf749.png)

We use this sensor to detect the occurrence of people in the different area in the hall. When the sensor detect a heat (a people), it will send the hub a “high” signal using Zigbee network. When the sensor detect no heat, it will send the hub a “low” signal one minute later using Zigbee.  

Beside the sensors, we also need to use the TP-LINK Wi-Fi as a wifi client for Smartthing Hub. The AP client transform the LAN signal of Smartthing Hub into wifi and connect to the Wifi of the campus. 

![1](https://cloud.githubusercontent.com/assets/10173940/24233058/ccc015a0-0f4c-11e7-86d6-3ed3c73514eb.png)

We also get the information of the fluorescent lamp by taking a picture of the lamp. We learned that the working power of the lamp is 26W. So we will use this data to estimate the energy. 


Besides the equipment, we need to develop a way to log our data. We refer a code from online that can log data from smart sensor to the google sheet. The hub will log the data it get from the smart sensor as well as the current time. If the incoming data is “high”, it will log a “1” with the current time in the google sheet. It will log “0” if the incoming data is “low”. After we get the data, we change the time format and convert it to a csv file for python to read. 


**Experimental Results and Evaluation**

Generally, we choose the degree 5 as our result for weekday because degree 5 has a higher score than degree 4 and degree 6. For the weekend, degree 4 has the higher score. 

For the weekday, we got the following graph and score for Area 1-4

![weekday_area1](https://cloud.githubusercontent.com/assets/10173940/24233375/14a513d2-0f4f-11e7-8d8f-2ec9523999aa.png)
![weekday_area2](https://cloud.githubusercontent.com/assets/10173940/24233378/15c3e4fa-0f4f-11e7-88d6-9471910d559a.png)
![weekday_area3](https://cloud.githubusercontent.com/assets/10173940/24233379/16d85fd8-0f4f-11e7-9865-bde5c38be792.png)
![weekday_area4](https://cloud.githubusercontent.com/assets/10173940/24233401/3e87099e-0f4f-11e7-92c7-90060a1da5f3.png)
![weekday](https://cloud.githubusercontent.com/assets/10173940/24233522/0fb5fa16-0f50-11e7-9ba2-18ebbf0e4faf.png)

From the graph we can see that Naive model consumes the highest total energy among three models. We can also see that Sensor mode has more energy saving during the valley time(the 1st and the 4th period) but it has more energy consuming than Naive model because of the setup energy. Same for the DPM, the DPM has the minimum total energy consumption in three model types but it does not perform good in the region where there are higher frequency of people walking by. The Data Precontrol Model has a good energy consumption during the valley time because that it know at this time people terns to show up less frequently. Therefore it choose to turn off the lamp immediately after letting the current people pass by(and after a 1 min delay caused by sensor). 

The weekend data looks similar to weekday data, but with less frequency of people. Here is the weekend data for area 1-4:

![area1-2_weekend](https://cloud.githubusercontent.com/assets/10173940/24233569/5dcd3926-0f50-11e7-8f05-f134f1d2e199.png)
![area3_weekend](https://cloud.githubusercontent.com/assets/10173940/24233570/5eb6a854-0f50-11e7-8a14-83d53f69e2b4.png)
![area4_weekend](https://cloud.githubusercontent.com/assets/10173940/24233573/5ff00d0a-0f50-11e7-9ad6-9a6c68d89d90.png)
![weekend](https://cloud.githubusercontent.com/assets/10173940/24233575/6190e526-0f50-11e7-91b2-c390028dd2d6.png)

The data for weekend has less degree than the data for weekday. However, we notice that the two edges is going down rather than going up. We think the reason could be that the Seasnet is open on 1PM and closed around 8~9. Therefore there are more people coming and on on these two time period. We think that if we have more data, we could get rid of this kind of period. 

**Related Work**

We did a lot of research, but actually there is no really similar research that could provide us some previous experiences and technology. In fact, We use self-piped regressive model in our case, so we did not figure out that other researcher or group that use this machine learning method to analyze the lighting system in large-scale public buildings. The only research paper found that are close to our research paper is the one that provided by Prof. Mani Srivastava. The paper named “Data Predictive Control for Peak Power Reduction”[4], which presents data-driven based methods which are implemented by data predictive control with regression trees (DPCRT) for making receding horizon control-oriented model in order to reduce peak power in buildings and maintain thermal comfort. The work of their research is relatively close to our topic and we get some inspiration from the experimental setup and the way of evaluation from their content of research paper.  

**Conclusion and Future work**

Our experiment shows that the DPM method we use can reduce the energy consumed by the fluorescent lamp by dynamically change the waiting time for the lamp. The data shows that the energy could be decreased by 30% by using the Naive model. Yet there is a lot of improvement we can do, such as using more data as our sample to get a more accurate model for our prediction. We can also add the Office/class schedule into the data so the algorithm can set up a base model before learning the real data. 

This model should be embedded in microcontroller for real time use. We use Smartthing Hub because we want to see whether there is a potential energy drop by using Data Precontrol Mode. Now that we shows that using DPM can reduce the energy consumption, the next step would be using a real microcontroller and measure the energy by a physical meter to see the result. Although DPM method can drop the energy a lot, the hard part comes from the installation and the maintenance. As LED is replacing the fluorescent light in the future, then the combination of LED and DPM may reduce the energy consumption on campus to the lowest level. 


**Reference** 

[1] “Does Turning Fluorescent Lights Off Use More Energy Than Leaving Them On?”. Retrieved from: https://www.scientificamerican.com/article/turn-fluorescent-lights-off-when-you-leave-room/
[2] “Robust linear estimator fitting”. Retrieved from: http://scikit-learn.org/stable/auto_examples/linear_model/plot_robust_fit.html#sphx-glr-auto-examples-linear-model-plot-robust-fit-py 
[3] “Code reference for logging data to google sheet”. Retrieved From: https://community.smartthings.com/t/log-events-to-google-sheets-see-post-154-for-current-github-repo-and-v1-1/36719
[4] “Data Predictive Control for Peak Power Reduction”. A. jain, etc. Retrieved From:
https://dl.acm.org/citation.cfm?id=2993582

**Weekly Update** 

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
