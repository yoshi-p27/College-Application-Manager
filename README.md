# College Application Manager

Lightweight college application manager using Django and Pandas

## Task 1: Django Data Model Design

### Overview
I began by considering what analytics it would be valuable for a student to have as well as what features may be used by admissions officers at colleges. Here is a prospective list of some I considered. 

1. Student sat or act scores and where they end up as a percentile of the accepted students to a college or from their district
2. Student gpa scores and where they end up as a percentile of the accepted students to a college or from their district
3. Student demographics 
4. course rigor -- what percentage of college students got into a particular college who took that course or number of ap/ib courses taken
5. extracurriculars -- what percentage of students participating in that org were accepted to college 

I then designed my models to enable analytics like these as best as possible


### Models

#### District:
The district model contains information relevant to various districts. 
- Geographic information: information about the state, county, and zip code it pertains to. 
- It also contains a few fields prefaced with "external_" these correspond to average SAT, ACT, and GPA scores associated with a district that may be provided from external sources, i.e. those not calculated from internal student data by Schoolinks. They can be empty in case internal metrics are the only ones that exist or can be prioritized.
- These internal metrics are prefaced with "internal_"

#### HighSchool:
The high school model contains information relevant to particular high schools. 
- district (foreign key)
- name
- a few fields prefaced with "external_" see explanation in District model section above
- A few fields are prefaced with "internal_" see explanation in District model section above

#### Student:
Student model contains information associated with individual students
 - student number 
 - high school (foreign key)
 - Student demographic information (race, gender, cultural/economic background)
 - Quantifiable academic background (SAT/ACT score, GPA)
 - Student's intended major

#### College:
College model contains information associated with individual colleges
- name 
- ceeb_code, given, college's identification number
- A few fields prefaced with "external_" see explanation in District model section above.

#### Application:
Application model contains information associated with each individual application with both college and student as foreign keys
- Student foreign key
- College foreign key
- Application result
- Application type (ED, EA, RD, etc)
- Attending, whether student decided to attend the college
- Legacy_status, whether student is a legacy to a particular university

#### Course:
Course model to store information associated with high school courses that a student may take
- SCED_code, a semi-standardized code for a particular class which is assigned by National Center for Education Statistics. It contains information about the subject area, the course number, course level, Carnegie units and sequence of courses. It also has unique codes for AP and IB courses. The aim here is to be able to compare the kinds of courses students across the nation took and the outcomes associated with them. Here is a link where you may read more: https://nces.ed.gov/forum/pdf/sced_faq_508.pdf
- course_name in case SCED code is not available
- course_description is a short description of the course
- AP_Course - whether it is an AP Course
- IB_course - whether it is an IB Course
- student - a student associated with the course. It will make use of the forthcoming enrollment table as an intermediary, so it functions through it.

#### Enrollment:
Intermediate model to store information associated with a particular student's enrollment and performance in a course
- student - foreign key to the student model
- course - foreign key to the course model
- grade - grade in the course
- semester - semester it was taken in 
- year - the year it was taken in 


### Design Decisions

#### Assumptions:
I assumed that some information would be available through the district and the college, such as average GPA and standardized test scores, but I also understand that this isn't universally the case. As such I aimed to account for it by including fields to be populated by these external sources, but I left them optional so that similar analytics may be generated using Schoolinks' internal data. 

I also assumed that extracurricular data would be too unstructured to make a reliable model for, making it a notable exclusion. If I were to design a more complex system, I would treat it like a dropdown menu with a list of predefined extracurriculars (DECA, Speech and Debate, Model UN), but that also could be added to if a particular extracurricular wasn't present. We could then analyze how each extracurricular affected a student's chances of being accepted into a particular college. 

#### Design decisions
First I aimed to prioritize Normalization, as per the spec, it seems like a priority that the data is as consistent as possible. True normalization would allow for more efficient deletions and the like. 

I included an intermediary table, enrollment so that we could store information associated with a particular student in a particular course instead of exclusively a manytomany field which would only allow an association of the courses. I also made the present manytomany field "through" enrollment meaning that there won't have to be a join for more efficient lookups. 

To this end, I also eliminated the district foreign key from the student model, replacing it instead with a high school foreign key. This carries the assumption that students will have a high school, but it also allows for normalization instead of redundant keys which may require extra computation to keep consistent.

I also set db_index to true for a few fields to ensure faster lookups. These include: names of districts, college CEEB codes, and SCED codes. 

---

## Task 2: Data Ingestion with Pandas

### Overview
Here I spent some time doing some exploratory data analysis. Getting value_counts and null_counts for each column to understand what the values looked like. I took note of values which could be consolidated and others that needed to be replaced with blank or null values, as well as replacing existing null values with data more appropriate to our django schema.


### Assumptions and Transformations

Since we are reading from CSVs I assumed that all data was either a string, or integer. 

First I noticed that there were extra spaces in some of the column names so I stripped them. 

EDA showed that there were some rows which were duplicated so I dropped duplicates in place. Our manner of loading data into our django models would automatically account for this but for legibility and redundancy and to minimize database calls.

There were no null or blank student_numbers but in the event future datasets had such values I opted to drop the entire row. This is because a blank or null student_number seems rare as I assume most counselor's systems require this identifying information, meaning much data is not lost. 

Many ceeb codes had letters in them. At first I assumed they were mostly valid except for additional errors, as in the case of Harvard. After only selecting the numbers, some CEEB codes were of a different size than 4. Instead of dropping the whole row, I only replaced the CEEBs of incorrect size with a blank string. I did not drop the row because there is likely another system elsewhere with a list of names of valid universities and the name could be looked up for verification purposes and the CEEB filled in retroactively.
As such the lookup logic is (if ceeb exists and is valid) -> lookup by CEEB; (else if ceeb_code is blank ->lookup by college_name)

Assumed that any answer that wasn't "unknown" or "no decision" which is functionally the same as unknown is maintained, others were replaced with a blank string. This was to account for conditional acceptances and january admits which carries more important information than the three "accepted, denied, withdrawn" and as such should not be reduced to them. They can be treated as accepted if need be in other analytics but the information should be preserved in its present state as a student's January admission, for example, is a unique and useful bit of information for prospective students to know as acceptance rates often differ for late admission. 

Decision type seems to be well reported with no null values and seems to be collected rather robustly, I opted to make results which do not fall within the standard ones (Early Decision, Rolling Decision, Early Decision II, Early Action, Early Action II, Priority Decision) to be "Other" if they are not blank, as the application must necessarily exist in some form. Also assumed PRI corresponds to priority decision based on some rudimentary research. I also expanded all abbreviations into title case.

Attending has a lot of unknown values which I will transform to None as our django model has that as a default. I will then convert 1 and 0, as well as a few other common phrases ("yes/no", the strings "true/false") to booleans True and False. 

### How It Works
First the data is cleaned in accordance with the assumptions and transformations described above, column by column. More comments are available in the college_applications.py file

Next it is loaded into the django models in a manner which allows it to be updated based on new CSVs (archiving logic). This occurs in the following way:

1. A set of existing_app_ids is created from the records in the db for quick lookups later. 
Another set of ids to track the ids which are seen on the new pass through the csv is created, called seen_app_ids.

2. I iterate through each row of the cleaned dataframe from the csv. Since our application model has two foreign keys, student and college, we have to populate them with student numbers for students and colleges by their ceeb code if it exists, or its college_name. These students and colleges are created if they don't exist. 

3. I update_or_create the application objects indexed by their student id and college and populate the rest of our fields with the relevant fields from the csv. Students are only created with a student_number since other data isn't available. This is made possible since other fields in the student model are nullable.

4. I then take the .id of each application and add it to the seen_app_ids set. 

5. I subtractively create a new set: apps_to_delete, which is constituted by old data which are then filtered and deleted from the db.


---

## Task 3: Unit Tests

### Overview
I isolated the functions I use for transformation before the __name__ == "__main__" block of the function so that pytest can run and test them without running the entire django script. I then tested the functions' behavior as well as its ability to catch errors. 

### Test Cases
#### remove_non_numeric_characters()
Here I wrote two functions. First testing the ability to remove non-numeric characters. I wrote a series of strings which included excluded characters like letters and punctuation

Second I wrote a test for type checking. remove_non_numeric_characters converts every input value to a string, but it only takes integers as strings as inputs, so I made sure that python raises a type error for every kind of excluded type like booleans, lists, sets, nonetypes and tuples. 

#### is_valid_ceeb_code()
This function calls remove_non_numeric_characters - so some of the redundant cases are excluded. I mainly checked to ensure it accurately converts invalid values into blank spaces.
I did not need to check if it raises type errors accurately that type checking is handled by remove_non_numeric_characters

#### clean_application_result()
The first function makes sure that applications are being transformed correctly. It ensures that unknown and no decision are transformed into "" and accounts for various odd kinds of capitalization.

The second function ensures that type checking is occurring correctly. The logic is the same as for the type checking function for remove_non_numeric_characters(), but includes a check for integers since this function does not take integers. Other type checking test functions will be identical to this one

#### test_expand_application_type()
The first function ensures that various kinds of abbreviations for application types are updated to their full expansion, while also ensuring that expanded types are also returned correctly.

The second function is identical to the last type checking function

#### convert_attending_to_boolean()
Ensure that all variations of booleans will be converted to the True and False boolean or None for missing data. No type checking function since all inputs are converted to strings

#### test_handles_whitespace_in_values()
Test to ensure that most variations of entry value are stripping spaces correctly when performing their matches and conversions.



---

## Task 4: College Classification

### Data Points
I outlined some of the student data points that I would use in Task 1 (GPA, test scores, course rigor, and demographics). I also mentioned some of the external college-specific data there (SAT/ACT/GPA averages and distributions, demographics and acceptance rates). This would be categorized into both historical data and year by year data. I would also aggregate user information and stats so an individual student can be compared with their peers. 
<!-- varying weights for historical data depending on how much data we have. -->


### Classification Approach

The goal is to calculate the probability a student with a particular profile will get into a school. I will then split up these probabilities into three ranges 70 - 100% is Likely, 30 - 70% is Target and 0 - 30% is a Reach. 

The guaranteed section will require additional data about the colleges and to categorize as a certainty, which I do not have the necessary experience with to describe. One example I can think of is the UC system which guarantees admission to at least one of its colleges (usually Merced) if the student has a certain score on a proprietary scoring system. This would be quite difficult to model and may be beyond the scope of this assignment. 

There are two classification approaches I would like to discuss to accomplish this. The first is a logistic regression which would be able to account for the wide range of kinds of features we have, both categorical (race, low-income) and continuous (GPA, ACT/SAT scores). We would do some feature engineering to determine which features have a significant impact on the scores then run a regression with the features we have decided upon and return a probability the student will get in. This would require historical data that would be accumulated from both external and internal data sets. 

The second classification approach is to use a simple rule based system to return a weighted average of each percentile score based on continuous data. Then fit each percentile within our categories This would be based primarily on things like internal and external GPA and SAT/ACT scores. This would allow for more transparency and actionable insights for students who can now know where they may have fallen short.

### Edge Cases & Trade-offs
#### Logistic Regression:
This data is more opaque meaning it would be difficult to understand what specific areas a student may need to improve. Further, it relies on historical data which may not be available for certain schools because they may not have been applied to very much by SchooLinks users or there may not be published data from external sources. The college may be new, for example. 

#### Rule-base classifier:
This method would not easily be able to account for categorical data as it too would likely run into problems with a lack of data (there may not be many low-income students applying to a particular school so percentiles may not be descriptive for that school). Also it is difficult to determine how to weight the different features when computing the average.

Students with incomplete data would also be a problem for both forms of classification.

---

## Known Limitations
College name matching is not fuzzy -- it relies on exact matching. This is because it is a fallback option if the CEEB is not available. The assumption is that the CEEB usually is available. However the solution would be improved by more fuzzy matching, but that is impractical for such wide ranges of variations for colleges. This could be resolved by a data set of variations, or with use of a lightweight semantic model like from HuggingFace. There is also no validation of college_names against known colleges but this is difficult to resolve without a more comprehensive data set or use of a larger model with a lot of context.

The students model is created with limited information only, as it is all that is available in the given dataset. 

The logic for updating the database deletes the old records which have since been updated, instead of archiving them elsewhere. This may be an issue if one would like to look at archived data, or revert to an old version of the data. I chose to do it this way for simplicity as archiving data would require a substantially more complex data model. Additionally, it is unlikely that one would like to view a record whose application result has been updated from "unknown" to "accepted", for example.  

## Areas for Improvement
I would try to use more bulk operations for more efficient computation instead of iterating through records with iterrows. I am not super well versed in django but I have read that this has significant performance benefits especially for a table which is substantially larger. Since this table had only 500 rows, I opted for the simpler iterrows approach.

I would like to include extracurriculars in the future. I outlined a potential approach in the Design Decisions:Assumptions section of this document. 

I think I would also aim to have a more robust set of application decision types that I could draw from to make my expand_application_type() function more comprehensive. I think I would also try to make matches with well-formed regex patterns instead of matching so literally.

I could likely have a more robust database design which does not require so much repetition of the external and internal data fields in each class. I could likely use some kind of external abstract class to handle this. This would require a more in depth understanding of django to accomplish, which would require more time.

## Setup & Usage
### Prerequisites
- Python 3.11+

Install dependencies:
```pip install -r requirements.txt```

Run the Ingestion Script:
```python college_applications.py```

Run the tests:
```python -m pytest test_college_applications.py```

