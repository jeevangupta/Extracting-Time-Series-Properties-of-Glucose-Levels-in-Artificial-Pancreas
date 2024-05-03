# Extracting Time Series Properties of Glucose Levels in Artificial Pancreas

**In this project, you will extract several performance metrics of an Artificial Pancreas system from sensor data.**

 - Extract feature data from a data set.
 - Synchronize data from two sensors.
 - Compute and report overall statistical measures from data.

Write a Python script that accepts two CSV files: CGMData.csv and InsulinData.csv, runs the analysis procedure, and outputs the metrics discussed in the metrics section.

## Descriptions:
  - In this project, we are considering the Artificial Pancreas medical control system, specifically the Medtronic 670G system. The Medtronic system consists of a continuous glucose monitor (CGM) and the Guardian Sensor (12), which is used to collect blood glucose measurements every 5 minutes. The sensor is single use and can be used continuously for 7 days after which it has to be replaced. The replacement procedures include a recalibration process that requires the user to obtain blood glucose measurements using a Contour NextLink 2.4 glucose meter ®.
 
  - Note that this process also requires manual intervention. The Guardian Link Transmitter powers the CGM sensor and sends the data to the MiniMed 670G® insulin pump. The insulin pump utilizes the Smart Guard Technology that modulates the insulin delivery based on the CGM data. The SmartGuard Technology uses a Proportional, Integrative, and Derivative controller to derive small bursts of insulin also called Micro bolus to be delivered to the user. During meals, the user uses a BolusWizard to compute the amount of food bolus required to maintain blood glucose levels. The user manually estimates the amount of carbohydrate intake and enters it into the Bolus Wizard.

 - The Bolus Wizard is pre-configured with the correction factor, body weight, and average insulin sensitivity of the subject, and it calculates the bolus insulin to be delivered. The user can then program the MiniMed 670G infusion pump to deliver that amount. In addition to the bolus, the MiniMed 670G insulin pump can also provide a correction bolus. The correction bolus amount is provided only if the CGM reading is above a threshold (typically 120 mg/dL) and is a proportional amount with respect to the difference of the CGM reading and the threshold.

 - The SmartGuard technology has two methods of suspending insulin delivery: a) Suspend on low, where the insulin delivery is stopped when the CGM reading is less than a certain threshold, or b) suspend on predicted low, where the insulin delivery is stopped when the CGM reading is predicted to be less than a certain threshold. Apart from these options, insulin delivery can also be suspended manually by the user or can be suspended when the insulin reservoir is running low.

## Directions

 **Dataset:**
 
 You will be given two datasets:
 
  1. from the Continuous Glucose Sensor (CGMData.csv)
  2. from the insulin pump (InsulinData.csv)

  The output of the CGM sensor consists of three columns:
   
  1. data time stamp (Columns B and C combined)
  2. the 5-minute filtered CGM reading in mg/dL, (Column AE)
  3. the ISIG value which is the raw sensor output every 5 mins.

   The output of the pump has the following information: 
        
        a) data time stamp,
        b) Basal setting,
        c) Micro bolus every 5 mins,
        d) Meal intake amount in terms of grams of carbohydrate,
        e) Meal bolus,
        f) correction bolus,
        g) correction factor,
        h) CGM calibration or insulin reservoir-related alarms, and
        i) auto mode exit events and unique codes representing reasons (Column Q).

   Metrics to be extracted:
   
        a) Percentage time in hyperglycemia (CGM > 180 mg/dL),
        b) percentage of time in hyperglycemia critical (CGM > 250 mg/dL),
        c) percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL),
        d) percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL), 
        e) percentage time in hypoglycemia level 1 (CGM < 70 mg/dL), and
        f) percentage time in hypoglycemia level 2 (CGM < 54 mg/dL).

 - Each of the above-mentioned metrics is extracted in three different time intervals: daytime (6 am to midnight), overnight (midnight to 6 am), and whole day (12 am to 12 am).

 - Percentage is with respect to the total number of CGM data that should be available each day. Assume that the total number of CGM data that should be available is 288. There will be days such that the number of data available is less than 288, but still, consider the percentage to be with respect to 288.

 - You have to extract these metrics for each day and then report the mean value of each metric over all days. Hence there are 18 metrics to be extracted.

 - The metrics will be computed for two cases:
    Case A: Manual mode
    Case B: Auto mode



**Analysis Procedure:**

   The data is in reverse order of time. This means that the first row is the end of the data collection whereas the last row is the beginning of the data collection. The data starts with manual mode. Manual mode continues until you get a message AUTO MODE ACTIVE PLGM OFF in the column “Q” of the InsulinData.csv. From then onwards Auto mode starts. You may get multiple AUTO MODE ACTIVE PLGM OFF in column Q but only use the earliest one to determine when you switch to auto mode. There is no switching back to manual mode. So the first task is to determine the time stamp when Auto mode starts. Remember that the time stamp of the CGM data is not the same as the time stamp of the insulin pump data because these are two different devices that operate asynchronously.

   Once you determine the start of Auto Mode from InsulinData.csv, you have to figure out the time stamp in CGMData.csv where Auto Mode starts. This can be done simply by searching for the time stamp that is nearest to (and later than) the Auto mode start time stamp obtained from InsulinData.csv.

   For each user, CGM data is first parsed and divided into segments, where each segment corresponds to a day worth of data. One day is considered to start at 12 am and end at 11:59 pm. If there is no CGM data loss, then there should be 288 samples in each segment. The segment as a whole is used to compute the metrics for the whole day time period. Each segment is then divided into two sub-segments: the daytime sub-segment and overnight subsegment. For each subsegment, the CGM series is investigated to count the number of samples that belong to the ranges specified in the metrics. To compute the percentage with respect to 24 hours, the total number of samples in the specified range is divided by 288.

   Note that here you have to tackle the “missing data problem”. So a particular may not have all 288 data points. In the data files, those are represented as NaN. You need to devise a strategy to tackle the missing data problem. Popular strategies include deletion of the entire day of data, or interpolation.
