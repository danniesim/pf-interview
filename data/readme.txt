Version 5.0 Produced 2017-07-19

National Student Survey 2017

Notes on the use of the data

Following a major review, the National Student Survey was substantially revised in 2017. These are the first major changes to the survey since its establishment in 2005.

The 2017 survey therefore used a different main questionnaire from that used in 2016 and previous years.  The 2017 questionnaire can be downloaded from /www.hefce.ac.uk/pubs/Year/2016/CL,302016/

The main changes to the survey in 2017 were:

•	Inclusion of 9 new questions on student engagement 
•	Amendment of questions on Learning Resources and on Assessment and Feedback
•	Removal of largely duplicative questions
•	Transfer of personal development questions to optional banks.

While some questions within the survey have remained the same, including the final question on overall satisfaction (previously Q 22, now Q 27), the following caveats applying to the data and its use should be noted.

•	Time series: As the questionnaire has changed, it is no longer statistically robust to create time series data at question level including 2017 data and data from previous years.

•	Question level aggregation: Question level responses from data from 2017 should not be directly aggregated with (compiled together with) data from 2016 or previous years with no statistical adjustment made for the differences in the dataset.

•	Comparison of data:  It is not valid to compare question level responses from 2017 with data from 2016 or previous years and such comparisons should not be undertaken.

•	We do not endorse any presentations of the data which compare or aggregate question level data in this way without statistical adjustments as noted.

How will data be presented on Unistats?

As a result of the questionnaire changes, where 2017 NSS data on the Unistats web-site does not meet customary publication response thresholds (50% of the sample responding and at least 10 students), data is aggregated only on the basis of a higher level subject grouping (JACs level), and not aggregated using data from 2016.

Where there is insufficient data from 2017 to meet publication thresholds, the following message will appear on the Unistats web-site. This message will link to a fact sheet providing students with straightforward information about the changes to the survey:

“There is not enough National Student Survey (NSS) data available to publish for this course. This does not reflect on the quality of the course.
 
It may be because:
 
•	The course is new
•	The course is small
•	We have not received enough survey responses
 
The 2017 NSS is a new survey so it is not valid for us to group data over years to allow us to publish it.  Find out more.”

The kis .csv files have been included in this folder to enable users to load .csv versions of the kis.xml file entities into their databases for analysis.

The .csv file structure is based on that created for the Unistats output .xml file with some exceptions (see paragraph below). 

This documentation includes details of the parent entity, field description, field type, min/max occurrence, field length and additional notes.  Field information for the three .csv lookup tables (ACCREDITATIONTABLE.csv, KISAIM.csv and LOCATION.csv), plus the two additional .csv entities (UCASCOURSEID.csv and SBJ.csv (created to hold the COURSELOCATION UCASCOURSEID and KISCourse SBJ repeating fields)), can be found in the 'Unistats dataset file structure and description' 

https://www.hesa.ac.uk/collection/c17061/unistats_dataset_file_structure/

The .csv file name, the entity name, the entity description, how to join to other files and additional notes, if applicable, are listed below:

ACCREDITATION.csv, 
Accreditation entity, 
Contains information about course accreditation, 
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

ACCREDITATIONTABLE.csv, 
Accreditation lookup table,
Contains the accrediting body text and accreditation url for each ACCTYPE,
Lookup table
(This lookup table may be linked to the ACCREDITATION entity using ACCTYPE)

COMMON.csv, 
Common job types entity, 
Contains information relating to common job types obtained by students taking the course, 
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE,
Linked to JOBLIST entity using PUBUKPRN, KISCOURSEID, KISMODE and COMSBJ,
(Note COMSBJ may contain nulls)

CONTINUATION.csv,
Continuation entity,
Contains continuation information for students on the course,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

COURSELOCATION.csv,
Course location entity,
Contains details of the KIS course location,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE
Linked to UCASCOURSEID entity using PUBUKPRN, KISCOURSEID, KISMODE and LOCID
(Note LOCID may contain nulls)

DEGREECLASS.csv,
Degree classification entity,
Contains information relating to the degree classifications obtained by students,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

EMPLOYMENT.csv,
Employment statistics entity,
Contains information relating to student employment outcomes,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

ENTRY.csv
Entry qualifications entity,
Contains information relating to the entry qualifications of students,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

INSTITUTION.csv,
Institution table,
This entity describes the reporting institution
Linked to KISCOURSE entity using PUBUKPRN

JOBLIST.csv,
Job list entity,
Contains information about common job types obtained by students,
Linked to COMMON entity using PUBUKPRN, KISCOURSEID, KISMODE and COMSBJ,
(Note COMSBJ may contain nulls)

JOBTYPE.csv,
Job type entity,
Contains information relating to the types of profession entered by students,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

KISAIM.csv, 
KIS Aim lookup table,
Contains the code and label for each KISAIM,
Lookup table,
(This lookup table may be linked to the KISCOURSE entity using KISAIMCODE)

KISCOURSE.csv,
KIS course entity,
This entity records details of KIS courses,
Linked to INSTITUTION entity using PUBUKPRN and
Linked to child entities using PUBUKPRN, KISCOURSEID and KISMODE

LOCATION.csv,
Location lookup table,
Contains details for each teaching location,
Lookup table,
(This lookup table may be linked to the LOCID entity using UKPRN and LOCID)

NHSNSS.csv,
NHS NSS entity,
Contains the results for the questions on the NSS for students on NHS funded courses,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

NSS.csv,
NSS entity,
Contains the National Student Survey (NSS) results,

Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE


SALARY.csv,
Salary entity,
Contains salary information of students,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

SBJ.csv,
Subject entity,
Contains JACS level subject codes for each KISCourse,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

TARIFF.csv,
Tariff entity,
Contains information relating to the entry tariff points of students,
Linked to KISCOURSE entity using PUBUKPRN, KISCOURSEID and KISMODE

UCASCOURSEID.csv,
UCASCOURSEID entity,
Contains UCAS course identifiers for each COURSELOCATION,
Linked to COURSELOCATION entity using PUBUKPRN, KISCOURSEID, KISMODE and LOCID


ACCREDITATIONBYHEP.csv,
Table showing usage of accreditation types by Higher Education Provider. This file enables Accrediting Bodies to determine which HE providers are using which accreditation types, to support their quality assurance and audit functions.
