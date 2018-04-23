from biosamples_v4.traverson import Traverson, Utils
from nose.tools import assert_true, assert_equal

__API_TEST = "http://localhost:8081/biosamples"

def base_traverson():
    return Traverson(base_url=__API_TEST)

def test_traverson_get_samples():
    # Verifies traverson is able to get root of the api
    tr = base_traverson()
    response = tr.get()
    assert_true(response.ok)


def test_traverson_can_follow_links():
    tr = base_traverson()
    response = tr.follow('samples').get()
    assert_true(response.ok)


def test_traverson_populate_base_template_url():
    parameterized_url = 'this/is/a/test/url/{id}'
    params = {
        'id': 123456
    }
    expected_url = 'this/is/a/test/url/123456'
    actual_url = Utils.populate_url(parameterized_url, params)
    assert_equal(expected_url, actual_url, "The parameter expantion didnt work'")


def test_traverson_populate_query_parameter():
    parameterized_url = 'this/is/a/test/url{?query1,query2}'
    params = {
        'query1': 'value1',
        'query2': 'value2'
    }

    expected_url = 'this/is/a/test/url?query1=value1&query2=value2'
    actual_url = Utils.populate_url(parameterized_url, params)
    assert_equal(expected_url, actual_url)


def test_traverson_multiple_path_parameters():
    parameterized_url = 'my/name/is/{name}/and/i/love/{love}'
    params = {
        'name': 'Donald',
        'love': 'Daisy'
    }
    expected_url = 'my/name/is/Donald/and/i/love/Daisy'
    assert_equal(expected_url, Utils.populate_url(parameterized_url, params))



