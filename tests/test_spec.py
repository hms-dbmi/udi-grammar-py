from udi_grammar_py import Chart

def test_sanity():
    assert 1 == 1


def test_chart_initialization():
    chart = Chart()
    assert chart._spec['source'] == []
    assert chart._spec['representation'] == []

def test_chart_add_source():
    chart = Chart()
    chart.source('test_name', 'test_source')
    assert chart._spec['source'] == [{'name': 'test_name', 'source': 'test_source'}]

def test_chart_add_multiple_sources():
    chart = Chart()
    chart.source('test_name_1', 'test_source_2').source('test_name_2', 'test_source_2')
    assert chart._spec['source'] == [{'name': 'test_name_1', 'source': 'test_source_2'}, {'name': 'test_name_2', 'source': 'test_source_2'}]

def test_chart_to_json():
    chart = Chart()
    chart.source('test_name', 'test_source')
    expected_json = '{"source": [{"name": "test_name", "source": "test_source"}], "representation": []}'
    assert chart.to_json() == expected_json