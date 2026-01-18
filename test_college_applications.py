import pytest
from college_applications import remove_non_numeric_characters, is_valid_ceeb_code, clean_application_result, expand_application_type, convert_attending_to_boolean

def test_remove_non_numeric_characters():
    assert remove_non_numeric_characters("1234a") == "1234"
    assert remove_non_numeric_characters("1234") == "1234"
    assert remove_non_numeric_characters("(754);AM.]`!@#$%^&*()_+-=[]{}|\\;:'\",.<>/?") == "754"

def test_remove_non_numeric_characters_raises_type_error():
    with pytest.raises(TypeError):
        remove_non_numeric_characters(None)
    with pytest.raises(TypeError):
        remove_non_numeric_characters(True)
    with pytest.raises(TypeError):
        remove_non_numeric_characters(False)
    with pytest.raises(TypeError):
        remove_non_numeric_characters([])
    with pytest.raises(TypeError):
        remove_non_numeric_characters({})
    with pytest.raises(TypeError):
        remove_non_numeric_characters(())

def test_is_valid_ceeb_code():
    assert is_valid_ceeb_code("1234") == "1234"
    assert is_valid_ceeb_code("1234a") == "1234"
    assert is_valid_ceeb_code("") == ""
    assert is_valid_ceeb_code("123") == ""
    assert is_valid_ceeb_code("12345") == ""

def test_clean_application_result():
    assert clean_application_result("") == ""
    assert clean_application_result("DENIED") == "denied"
    assert clean_application_result("accepted") == "accepted"
    assert clean_application_result("UNKNOWN") == ""
    assert clean_application_result("no decision") == ""
    assert clean_application_result("widthDrawn") == "widthdrawn"
    assert clean_application_result("OtHER") == "other"
    assert clean_application_result("cond. acceptance") == "cond. acceptance"
    assert clean_application_result("jan. admit") == "jan. admit"

def test_clean_application_result_raises_type_error():
    with pytest.raises(TypeError):
        clean_application_result(1234)
    with pytest.raises(TypeError):
        clean_application_result(None)
    with pytest.raises(TypeError):
        clean_application_result(True)
    with pytest.raises(TypeError):
        clean_application_result(False)
    with pytest.raises(TypeError):
        clean_application_result([])
    with pytest.raises(TypeError):
        clean_application_result({})
    with pytest.raises(TypeError):
        clean_application_result(())

def test_expand_application_type():
    assert expand_application_type("") == ""
    assert expand_application_type("Rolling") == "Rolling Decision"
    assert expand_application_type("Rolling Decision") == "Rolling Decision"
    assert expand_application_type("Priority") == "Priority Decision"
    assert expand_application_type("Priority Decision") == "Priority Decision"
    assert expand_application_type("Pri") == "Priority Decision"
    assert expand_application_type("Early Action") == "Early Action"
    assert expand_application_type("ea") == "Early Action"
    assert expand_application_type("Early Action II") == "Early Action II"
    assert expand_application_type("ea2") == "Early Action II"
    assert expand_application_type("ed2") == "Early Decision II"
    assert expand_application_type("Early Decision II") == "Early Decision II"
    assert expand_application_type("Early Decision") == "Early Decision"
    assert expand_application_type("ed") == "Early Decision"
    assert expand_application_type("Regular") == "Regular Decision"
    assert expand_application_type("Reglar Decision") == "Other"
    assert expand_application_type("Other") == "Other"
    assert expand_application_type("REA") == "Restricted Early Action"
    assert expand_application_type("restricted early action") == "Restricted Early Action"


def test_expand_application_type_raises_type_error():
    with pytest.raises(TypeError):
        expand_application_type(1234)
    with pytest.raises(TypeError):
        expand_application_type(None)
    with pytest.raises(TypeError):
        expand_application_type(True)
    with pytest.raises(TypeError):
        expand_application_type(False)
    with pytest.raises(TypeError):
        expand_application_type([])
    with pytest.raises(TypeError):
        expand_application_type({})
    with pytest.raises(TypeError):
        expand_application_type(())

def test_convert_attending_to_boolean():
    assert convert_attending_to_boolean("") == None
    assert convert_attending_to_boolean("yes") == True
    assert convert_attending_to_boolean("no") == False
    assert convert_attending_to_boolean("true") == True
    assert convert_attending_to_boolean("FALSE") == False
    assert convert_attending_to_boolean("1") == True
    assert convert_attending_to_boolean("0") == False
    assert convert_attending_to_boolean("10") == None
    assert convert_attending_to_boolean("0.5") == None
    assert convert_attending_to_boolean("2") == None

def test_handles_whitespace_in_values():
    assert remove_non_numeric_characters("  1234  ") == "1234"
    assert clean_application_result("  accepted  ") == "accepted"  
    assert expand_application_type("  ea  ") == "Early Action" 
    assert convert_attending_to_boolean("  yes  ") == True

