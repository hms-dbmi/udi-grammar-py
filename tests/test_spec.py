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
    expected_json = '{"source": {"name": "test_name", "source": "test_source"}}'
    assert chart.to_json() == expected_json

def test_chart_to_dict():
    chart = Chart()
    chart.source('test_name', 'test_source')
    expected_dict = {'source': {'name': 'test_name', 'source': 'test_source'}}
    assert chart.to_dict() == expected_dict

def test_scatterplot():
    chart = Chart()
    chart.source('donors', './data/donors.csv') \
        .representation() \
            .mark('point') \
            .map(encoding='x', field='weight', type='quantitative') \
            .map(encoding='y', field='height', type='quantitative')
    assert chart.to_dict() == {
        "source": {"name": "donors", "source": "./data/donors.csv"},
        "representation": {
            "mark": "point",
            "mapping": [
                {"encoding": "x", "field": "weight", "type": "quantitative"},
                {"encoding": "y", "field": "height", "type": "quantitative"},
            ],
        },
    }

def test_bar_chart():
    chart = Chart()
    chart.source('donors', './data/donors.csv') \
        .transformation() \
        .groupby('sex') \
        .rollup({'count': Op.count()})
    
    chart.representation().mark('bar') \
         .map(encoding='x', field='sex', type='nominal') \
         .map(encoding='y', field='count', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "donors", "source": "./data/donors.csv"},
        "transformation": [
            {
                "groupby": "sex",
            },
            {"rollup": {"count": {"op": "count"}}},
        ],
        "representation": {
            "mark": "bar",
            "mapping": [
                {"encoding": "x", "field": "sex", "type": "nominal"},
                {"encoding": "y", "field": "count", "type": "quantitative"},
            ],
        },
    }

def test_table_default():
    chart = Chart()
    chart.source('donors', './data/donors.csv') \
        .representation() \
        .mark('row') \
        .map(encoding='text', field='*', mark='text')
    assert chart.to_dict() == {
        "source": {"name": "donors", "source": "./data/donors.csv"},
        "representation": {
            "mark": "row",
            "mapping": {"encoding": "text", "field": "*", "mark": "text"},
        },
    }

def test_table_2():
    chart = Chart()
    chart.source('donors', './data/donors.csv') \
        .representation() \
        .mark('row') \
        .map(encoding='color', field='weight_value', mark='rect', type='quantitative') \
        .map(encoding='size', field='height_value', mark='point', type='quantitative') \
        .map(encoding='text', field='*', mark='text')

    assert chart.to_dict() == {
        "source": {
            "name": "donors",
            "source": "./data/donors.csv",
        },
        "representation": {
            "mark": "row",
            "mapping": [
                {
                    "mark": "rect",
                    "field": "weight_value",
                    "encoding": "color",
                    "type": "quantitative",
                },
                {
                    "mark": "point",
                    "field": "height_value",
                    "encoding": "size",
                    "type": "quantitative",
                },
                {"mark": "text", "field": "*", "encoding": "text"},
            ],
        },
    }

def test_layered_table_example_1():
    chart = Chart()
    chart.source('donors', './data/donors.csv') \
        .representation() \
        .mark('row') \
        .map(encoding='color', field='*', mark='rect') \
        .mark('row') \
        .map(encoding='color', field='*', mark='text', value='white')

    assert chart.to_dict() == {
        "source": {
            "name": "donors",
            "source": "./data/donors.csv",
        },
        "representation": [
            {
                "mark": "row",
                "mapping": {"mark": "rect", "field": "*", "encoding": "color"},
            },
            {
                "mark": "row",
                "mapping": {
                    "mark": "text",
                    "field": "*",
                    "value": "white",
                    "encoding": "color",
                },
            },
        ],
    }

def test_layered_table_example_2():
    chart = Chart()
    chart.source('donors', './data/donors.csv') \
        .representation() \
        .mark('row') \
        .map(encoding='size', field='*', mark='point') \
        .map(encoding='color', field='*', mark='point')

    assert chart.to_dict() == {
        "source": {
            "name": "donors",
            "source": "./data/donors.csv",
        },
        "representation": {
            "mark": "row",
            "mapping": [
                {"mark": "point", "field": "*", "encoding": "size"},
                {"mark": "point", "field": "*", "encoding": "color"},
            ],
        },
    }