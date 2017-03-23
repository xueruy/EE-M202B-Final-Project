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

**Future Work**


#



**Conclusion**

#


**Reference** 

#
