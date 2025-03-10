from udi_grammar_py import Chart, Op

def test_chart_initialization():
    chart = Chart()
    assert chart._spec == {}

def test_chart_add_source():
    chart = Chart()
    chart.source(source='test_source', name='test_name')
    assert chart._spec['source'] == [{'name': 'test_name', 'source': 'test_source'}]

def test_chart_add_multiple_sources():
    chart = Chart()
    chart.source('test_name_1', 'test_source_2').source('test_name_2', 'test_source_2')
    assert chart._spec['source'] == [{'name': 'test_name_1', 'source': 'test_source_2'}, {'name': 'test_name_2', 'source': 'test_source_2'}]

def test_chart_to_json():
    chart = Chart()
    chart.source('test_name', 'test_source')
    expected_json = '{"source": [{"name": "test_name", "source": "test_source"}]}'
    assert chart.to_json() == expected_json

def test_chart_to_dict():
    chart = Chart()
    chart.source('test_name', 'test_source')
    expected_dict = {'source': [{'name': 'test_name', 'source': 'test_source'}]}
    assert chart.to_dict() == expected_dict

def test_scatterplot():
    chart = Chart()
    chart.source('donors', './data/donors.csv') \
        .layer() \
        .mark('point') \
        .map(encoding='x', field='weight', type='quantitative') \
        .map(encoding='y', field='height', type='quantitative')
    assert chart.to_dict() == {
        "source": [{"name": "donors", "source": "./data/donors.csv"}],
        "representation": [
            {
                "mark": "point",
                "mapping": [
                    {"encoding": "x", "field": "weight", "type": "quantitative"},
                    {"encoding": "y", "field": "height", "type": "quantitative"},
                ],
            }
        ],
    }


def test_bar_chart():
    chart = Chart()
    chart.source('donors', './data/donors.csv') \
        .transformation() \
        .groupby('sex') \
        .rollup({'count': Op.count()})
    
    chart.layer().mark('bar') \
         .map(encoding='x', field='sex', type='nominal') \
         .map(encoding='y', field='count', type='quantitative')

    assert chart.to_dict() == {
        "source": [{"name": "donors", "source": "./data/donors.csv"}],
        "transformation": [
            {
                "groupby": "sex",
            },
            {"rollup": {"count": {"op": "count"}}},
        ],
        "representation": [
            {
                "mark": "bar",
                "mapping": [
                    {"encoding": "x", "field": "sex", "type": "nominal"},
                    {"encoding": "y", "field": "count", "type": "quantitative"},
                ],
            }
        ],
    }