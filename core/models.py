from django.db import models

class District(models.Model):
	"""Model to store school districts and their relevant information."""
	name = models.CharField(max_length=100, db_index=True)
	state = models.CharField(max_length=128, blank=True, default="")
	county = models.CharField(max_length=128, blank=True, default="")
	zip_code = models.CharField(max_length=128, blank=True, default="")
	# external information distinct from values calculated from GPA, ACT, and SAT fields in student model - can be overriden by student GPA/ACT/SAT aggregation
	external_average_gpa = models.FloatField(default=None, null=True, blank=True) # external average GPA
	external_average_act_score = models.FloatField(default=None, null=True, blank=True) # external average ACT score
	external_average_sat_score = models.FloatField(default=None, null=True, blank=True) # external average SAT score
	internal_average_gpa = models.FloatField(default=None, null=True, blank=True) # internal average GPA
	internal_average_act_score = models.FloatField(default=None, null=True, blank=True) # internal average ACT score
	internal_average_sat_score = models.FloatField(default=None, null=True, blank=True) # internal average SAT score

class HighSchool(models.Model):
	"""Model to store high schools and their relevant information."""
	district = models.ForeignKey(District, related_name="high_schools", on_delete=models.CASCADE)
	name = models.CharField(max_length=128, db_index=True)
	external_average_gpa = models.FloatField(default=None, null=True, blank=True) # external average GPA
	external_average_act_score = models.FloatField(default=None, null=True, blank=True) # external average ACT score
	external_average_sat_score = models.FloatField(default=None, null=True, blank=True) # external average SAT score
	internal_average_gpa = models.FloatField(default=None, null=True, blank=True) # internal average GPA
	internal_average_act_score = models.FloatField(default=None, null=True, blank=True) # internal average ACT score
	internal_average_sat_score = models.FloatField(default=None, null=True, blank=True) # internal average SAT score

class Student(models.Model):
	"""Model to store students and their relevant information."""
	student_number = models.CharField(max_length=64, null=True, blank=True, db_index=True)
	# district = models.ForeignKey(District, related_name="students", on_delete=models.CASCADE)
	high_school = models.ForeignKey(HighSchool, related_name="students", on_delete=models.CASCADE, null=True, blank=True)
	gender = models.CharField(max_length=128, blank=True, default="")
	ethnicity = models.CharField(max_length=128, blank=True, default="")
	sexual_orientation = models.CharField(max_length=128, blank=True, default="")
	disability = models.CharField(max_length=128, blank=True, default="")
	low_income = models.BooleanField(default=False)
	gpa = models.FloatField(default=0.0, null=True, blank=True)
	ACT_score = models.IntegerField(null=True, blank=True)
	SAT_score = models.IntegerField(null=True, blank=True)
	first_generation_student = models.BooleanField(default=False)
	intended_major = models.CharField(max_length=128, blank=True, default="")
	grade_level = models.CharField(max_length=128, blank=True, default="")


class College(models.Model):
	"""Model to store colleges and their relevant information."""
	name = models.CharField(max_length=128, default="", blank=True)	
	# A CEEB code is a unique identifier that College Board assigns to colleges, https://blog.collegeboard.org/how-look-ceeb-codes
	# A valid CEEB code is a 4-digit numeric identifier
	ceeb_code = models.CharField(max_length=255, default="", blank=True, db_index=True)
	# external information distinct from values calculated from GPA, ACT, and SAT fields in student model - can be overriden by student GPA/ACT/SAT aggregation
	external_average_gpa = models.FloatField(default=None, null=True, blank=True) # external average GPA
	external_average_act_score = models.IntegerField(default=None, null=True, blank=True) # external average ACT score
	external_average_sat_score = models.IntegerField(default=None, null=True, blank=True) # external average SAT score

class Application(models.Model):
	"""Model to store applications and their relevant information."""
	student = models.ForeignKey(Student, related_name="applications", on_delete=models.CASCADE)
	college = models.ForeignKey(College, related_name="applications", on_delete=models.CASCADE)
	application_result = models.CharField(max_length=128, default="", blank=True)
	application_type = models.CharField(max_length=128, default="", blank=True)
	attending = models.BooleanField(default=None, null=True, blank=True)
	legacy_status = models.BooleanField(default=None, null=True, blank=True)

class Course(models.Model):
	"""Model to store courses and their relevant information."""
	# A SCED code is a unique identifier that the National Center for Education Statistics assigns to courses, https://nces.ed.gov/forum/pdf/sced_faq_508.pdf
	# an SCED code holds information about the subject area, the course number, course level, Carnegie units and sequence of courses
	SCED_code = models.CharField(max_length=12, default="", blank=True, db_index=True)
	# The following fields are important if the SCED code is not available
	course_name = models.CharField(max_length=128, db_index=True)
	course_description = models.TextField(null=True, blank=True)
	subject_area = models.CharField(max_length=128)
	AP_course = models.BooleanField(default=False)
	IB_course = models.BooleanField(default=False)
	student = models.ManyToManyField(Student, through="Enrollment", related_name="courses", blank=True)

class Enrollment(models.Model):
	"""Model to store enrollments and their relevant information. Intermediary model between Student and Course."""
	student = models.ForeignKey(Student, related_name="enrollments", on_delete=models.CASCADE)
	course = models.ForeignKey(Course, related_name="enrollments", on_delete=models.CASCADE)
	grade = models.CharField(max_length=2, default="", blank=True)
	semester = models.CharField(max_length=128, default="", blank=True)
	year = models.IntegerField(default=0, null=True, blank=True)


