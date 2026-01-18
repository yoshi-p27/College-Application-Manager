import os
import django
import re
import pandas as pd
import sys


# Clean CEEB codes
# Remove all non-numeric characters
def remove_non_numeric_characters(value):
    if type(value) != str and type(value) != int:
        raise TypeError(f"Value must be a string or integer, got {type(value)} from {value}")
    if type(value) == int:
        value = str(value)
    return re.sub(r'[^0-9]', '', str(value))

# If the CEEB code is not 4 characters long, set it to a blank string
# Always called after remove_non_numeric_characters which always returns a string
def is_valid_ceeb_code(value):
    value = remove_non_numeric_characters(value)
    if len(value) == 4:
        return value
    return ""

# Application result should be cleaned to be any value that is not unknown or no decision, they should be set to a blank string"
def clean_application_result(value):
    if type(value) != str:
        raise TypeError(f"Value must be a string, got {type(value)} from {value}")
    value = value.lower()
    value = value.strip()
    if value not in ["", "unknown", "no decision"]:
        return value
    return ""

    # expand some of the application types into their full words, e.g. "ED" -> "Early Decision"
def expand_application_type(value):
    if type(value) != str:
        raise TypeError(f"Value must be a string, got {type(value)} from {value}")
    value = value.lower()
    value = value.strip()
    if value == "":
        return ""
    if "rolling" in value:
        return "Rolling Decision"
    elif value == "restricted early action" or value == "rea":
        return "Restricted Early Action"
    elif "priority" in value or value == "pri":
        return "Priority Decision"
    elif "early action ii" in value or value == "ea2":
        return "Early Action II"
    elif "early action" in value or value == "ea":
        return "Early Action"
    elif "early decision ii" in value or value == "ed2":
        return "Early Decision II"
    elif "early decision" in value or value == "ed":
        return "Early Decision"
    elif "regular decision" in value or "regular" in value:
        return "Regular Decision"
    else:
        return "Other"

def convert_attending_to_boolean(value):
    value = str(value).lower()
    value = value.strip()
    if value == "yes" or value == "true" or value == "1":
        return True
    elif value == "no" or value == "false" or value == "0":
        return False
    else:
        return None

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()
    from core.models import Student, College, Application
    from django.core.management import call_command
    call_command('makemigrations', 'core', verbosity=0)
    call_command('migrate', verbosity=0)


    try:
        applications_df = pd.read_csv("applications.csv")
    except FileNotFoundError:
        print("Error: applications.csv file not found")
        sys.exit(1)
    applications_df.columns = applications_df.columns.str.strip()
    applications_df.drop_duplicates(inplace=True)


    # Clean student numbers
    # drop any rows with a null or blank student number
    applications_df.dropna(subset=["student_number"], inplace=True)
    applications_df.drop(applications_df[applications_df["student_number"] == ""].index, inplace=True)




    applications_df["ceeb_code"] = applications_df["ceeb_code"].fillna('')
    applications_df["ceeb_code"] = applications_df["ceeb_code"].apply(is_valid_ceeb_code)



    applications_df["application_result"] = applications_df["application_result"].fillna('')
    applications_df["application_result"] = applications_df["application_result"].apply(clean_application_result)


    applications_df["application_type"] = applications_df["application_type"].fillna('')
    applications_df["application_type"] = applications_df["application_type"].apply(expand_application_type)




    applications_df["attending"] = applications_df["attending"].apply(convert_attending_to_boolean)        
    existing_app_ids = set(Application.objects.values_list('id', flat=True) )
    seen_app_ids = set()

    for index, row in applications_df.iterrows():
        student, _ = Student.objects.get_or_create(student_number=row["student_number"])
        if row["ceeb_code"] != "":
            college, _ = College.objects.get_or_create(ceeb_code=row["ceeb_code"], defaults={"name": row["college_name"]})
        else:
            college, _ = College.objects.get_or_create(name=row["college_name"])
        application, _ = Application.objects.update_or_create(student=student, college=college,  defaults={"application_result": row["application_result"], "application_type": row["application_type"], "attending": row["attending"]})
        seen_app_ids.add(application.id)

    apps_to_delete = existing_app_ids - seen_app_ids
    Application.objects.filter(id__in=apps_to_delete).delete()


