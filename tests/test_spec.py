from udi_grammar_py import Chart, Op
from udi_grammar_py.spec import transfer_kwargs

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


def test_transfer_kwargs_empty():
    state = {}
    kwargs = {}
    transfer_kwargs({'field', 'type'}, state, kwargs)
    assert state == {}

def test_transfer_kwargs_valid_args():
    state = {}
    kwargs = {'field': 'age', 'type': 'quantitative'}
    transfer_kwargs({'field', 'type'}, state, kwargs)
    assert state == {'field': 'age', 'type': 'quantitative'}

def test_transfer_kwargs_invalid_args():
    state = {}
    kwargs = {'field': 'age', 'invalid_arg': 'value'}
    transfer_kwargs({'field', 'type'}, state, kwargs)
    assert state == {'field': 'age'}

def test_transfer_kwargs_in_name():
    state = {}
    kwargs = {'in_name': 'input_field'}
    transfer_kwargs({'in'}, state, kwargs)
    assert state == {'in': 'input_field'}
    
def test_transfer_kwargs_out_name():
    state = {}
    kwargs = {'out_name': 'input_field'}
    transfer_kwargs({'out'}, state, kwargs)
    assert state == {'out': 'input_field'}

# Tests charts originally from examples page.

# Bar Charts
def test_total_record_count():
    chart = Chart()
    chart.source('donors', './data/example_donors.csv') \
        .transformation() \
        .rollup({'count': Op.count()})
    
    chart.representation().mark('bar') \
         .map(encoding='x', field='count', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "donors", "source": "./data/example_donors.csv"},
        "transformation": [
            {"rollup": {"count": {"op": "count"}}},
        ],
        "representation": {
            "mark": "bar",
            "mapping": {"encoding": "x", "field": "count", "type": "quantitative"},
        },
    }

def test_count_by_category():
    chart = Chart()
    chart.source('donors', './data/example_donors.csv') \
        .transformation() \
        .groupby('sex') \
        .rollup({'count': Op.count()})
    
    chart.representation().mark('bar') \
         .map(encoding='x', field='sex', type='nominal') \
         .map(encoding='y', field='count', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "donors", "source": "./data/example_donors.csv"},
        "transformation": [
            {"groupby": "sex"},
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

def test_aggregate_by_category():
    chart = Chart()
    chart.source('donors', './data/example_donors.csv') \
        .transformation() \
        .groupby('sex') \
        .rollup({'average weight': Op.mean('weight')})
    
    chart.representation().mark('bar') \
         .map(encoding='x', field='sex', type='nominal') \
         .map(encoding='y', field='average weight', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "donors", "source": "./data/example_donors.csv"},
        "transformation": [
            {"groupby": "sex"},
            {"rollup": {"average weight": {"op": "mean", "field": "weight"}}},
        ],
        "representation": {
            "mark": "bar",
            "mapping": [
                {"encoding": "x", "field": "sex", "type": "nominal"},
                {"encoding": "y", "field": "average weight", "type": "quantitative"},
            ],
        },
    }

def test_combining_data_sources():
    chart = Chart()
    chart.source('donors', './data/example_donors.csv') \
        .source('samples', './data/example_samples.csv') \
        .transformation() \
        .join(on=['id', 'donor_id'], in_name=['donors', 'samples'], out_name='donor_sample_combined') \
        .groupby('sex') \
        .rollup({'sample count': Op.count()})
    
    chart.representation().mark('bar') \
         .map(encoding='x', field='sex', type='nominal') \
         .map(encoding='y', field='sample count', type='quantitative')

    assert chart.to_dict() == {
        "source": [
            {"name": "donors", "source": "./data/example_donors.csv"},
            {"name": "samples", "source": "./data/example_samples.csv"},
        ],
        "transformation": [
            {
                "in": ["donors", "samples"],
                "join": {"on": ["id", "donor_id"]},
                "out": "donor_sample_combined"
            },
            {"groupby": "sex"},
            {"rollup": {"sample count": {"op": "count"}}},
        ],
        "representation": {
            "mark": "bar",
            "mapping": [
                {"encoding": "x", "field": "sex", "type": "nominal"},
                {"encoding": "y", "field": "sample count", "type": "quantitative"},
            ],
        },
    }

def test_single_stacked_bar_chart():
    chart = Chart()
    chart.source('samples', './data/example_samples.csv') \
        .transformation() \
        .groupby('organ') \
        .rollup({'count': Op.count()})
    
    chart.representation().mark('bar') \
         .map(encoding='x', field='count', type='quantitative') \
         .map(encoding='color', field='organ', type='nominal')

    assert chart.to_dict() == {
        "source": {"name": "samples", "source": "./data/example_samples.csv"},
        "transformation": [
            {"groupby": "organ"},
            {"rollup": {"count": {"op": "count"}}},
        ],
        "representation": {
            "mark": "bar",
            "mapping": [
                {"encoding": "x", "field": "count", "type": "quantitative"},
                {"encoding": "color", "field": "organ", "type": "nominal"},
            ],
        },
    }

def test_single_stacked_bar_chart_relative():
    chart = Chart()
    chart.source('samples', './data/example_samples.csv') \
        .transformation() \
        .groupby('organ') \
        .rollup({'frequency': Op.frequency()})
    
    chart.representation().mark('bar') \
         .map(encoding='x', field='frequency', type='quantitative') \
         .map(encoding='color', field='organ', type='nominal')

    assert chart.to_dict() == {
        "source": {"name": "samples", "source": "./data/example_samples.csv"},
        "transformation": [
            {"groupby": "organ"},
            {"rollup": {"frequency": {"op": "frequency"}}},
        ],
        "representation": {
            "mark": "bar",
            "mapping": [
                {"encoding": "x", "field": "frequency", "type": "quantitative"},
                {"encoding": "color", "field": "organ", "type": "nominal"},
            ],
        },
    }

def test_multiple_stacked_bar_charts():
    chart = Chart()
    chart.source('samples', './data/example_samples.csv') \
        .transformation() \
        .groupby(['organ', 'organ_condition']) \
        .rollup({'count': Op.count()})
    
    chart.representation().mark('bar') \
         .map(encoding='x', field='count', type='quantitative') \
         .map(encoding='y', field='organ', type='nominal') \
         .map(encoding='color', field='organ_condition', type='nominal')

    assert chart.to_dict() == {
        "source": {"name": "samples", "source": "./data/example_samples.csv"},
        "transformation": [
            {"groupby": ["organ", "organ_condition"]},
            {"rollup": {"count": {"op": "count"}}},
        ],
        "representation": {
            "mark": "bar",
            "mapping": [
                {"encoding": "x", "field": "count", "type": "quantitative"},
                {"encoding": "y", "field": "organ", "type": "nominal"},
                {"encoding": "color", "field": "organ_condition", "type": "nominal"},
            ],
        },
    }

def test_multiple_stacked_bar_charts_relative():
    chart = Chart()
    chart.source('samples', './data/example_samples.csv') \
        .transformation() \
        .groupby('organ', out_name='groupCounts') \
        .rollup({'organ_count': Op.count()}) \
        .groupby(['organ', 'organ_condition']) \
        .rollup({'organ_and_condition_count': Op.count()}) \
        .join(on='organ', in_name=['samples', 'groupCounts'], out_name='datasets') \
        .derive({'frequency': 'd.organ_and_condition_count / d.organ_count'})
    
    chart.representation().mark('bar') \
         .map(encoding='x', field='frequency', type='quantitative') \
         .map(encoding='y', field='organ', type='nominal') \
         .map(encoding='color', field='organ_condition', type='nominal')

    assert chart.to_dict() == {
        "source": {"name": "samples", "source": "./data/example_samples.csv"},
        "transformation": [
            {"groupby": "organ", "out": "groupCounts"},
            {"rollup": {"organ_count": {"op": "count"}}},
            {"groupby": ["organ", "organ_condition"]},
            {"rollup": {"organ_and_condition_count": {"op": "count"}}},
            {
                "in": ["samples", "groupCounts"],
                "join": {"on": "organ"},
                "out": "datasets"
            },
            {"derive": {"frequency": "d.organ_and_condition_count / d.organ_count"}},
        ],
        "representation": {
            "mark": "bar",
            "mapping": [
                {"encoding": "x", "field": "frequency", "type": "quantitative"},
                {"encoding": "y", "field": "organ", "type": "nominal"},
                {"encoding": "color", "field": "organ_condition", "type": "nominal"},
            ],
        },
    }

# Circular Charts
def test_pie_chart():
    chart = Chart()
    chart.source('samples', './data/example_samples.csv') \
        .transformation() \
        .groupby('organ') \
        .rollup({'frequency': Op.frequency()})
    
    chart.representation().mark('arc') \
         .map(encoding='color', field='organ', type='nominal') \
         .map(encoding='theta', field='frequency', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "samples", "source": "./data/example_samples.csv"},
        "transformation": [
            {"groupby": "organ"},
            {"rollup": {"frequency": {"op": "frequency"}}},
        ],
        "representation": {
            "mark": "arc",
            "mapping": [
                {"encoding": "color", "field": "organ", "type": "nominal"},
                {"encoding": "theta", "field": "frequency", "type": "quantitative"},
            ],
        },
    }

def test_donut_chart():
    chart = Chart()
    chart.source('samples', './data/example_samples.csv') \
        .transformation() \
        .groupby('organ') \
        .rollup({'frequency': Op.frequency()})
    
    chart.representation().mark('arc') \
         .map(encoding='color', field='organ', type='nominal') \
         .map(encoding='theta', field='frequency', type='quantitative') \
         .map(encoding='radius2', value=60)

    assert chart.to_dict() == {
        "source": {"name": "samples", "source": "./data/example_samples.csv"},
        "transformation": [
            {"groupby": "organ"},
            {"rollup": {"frequency": {"op": "frequency"}}},
        ],
        "representation": {
            "mark": "arc",
            "mapping": [
                {"encoding": "color", "field": "organ", "type": "nominal"},
                {"encoding": "theta", "field": "frequency", "type": "quantitative"},
                {"encoding": "radius2", "value": 60},
            ],
        },
    }

# scatterplots
def test_basic_scatter_plot():
    chart = Chart()
    chart.source('donors', './data/example_donors.csv') \
        .representation() \
        .mark('point') \
        .map(encoding='y', field='height', type='quantitative') \
        .map(encoding='x', field='weight', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "donors", "source": "./data/example_donors.csv"},
        "representation": {
            "mark": "point",
            "mapping": [
                {"encoding": "y", "field": "height", "type": "quantitative"},
                {"encoding": "x", "field": "weight", "type": "quantitative"},
            ],
        },
    }

def test_scatter_plot_with_categories():
    chart = Chart()
    chart.source('donors', './data/example_donors.csv') \
        .representation() \
        .mark('point') \
        .map(encoding='y', field='height', type='quantitative') \
        .map(encoding='x', field='weight', type='quantitative') \
        .map(encoding='color', field='sex', type='nominal') \
        .map(encoding='shape', field='sex', type='nominal')

    assert chart.to_dict() == {
        "source": {"name": "donors", "source": "./data/example_donors.csv"},
        "representation": {
            "mark": "point",
            "mapping": [
                {"encoding": "y", "field": "height", "type": "quantitative"},
                {"encoding": "x", "field": "weight", "type": "quantitative"},
                {"encoding": "color", "field": "sex", "type": "nominal"},
                {"encoding": "shape", "field": "sex", "type": "nominal"},
            ],
        },
    }

def test_bubble_plot():
    chart = Chart()
    chart.source('donors', './data/example_donors.csv') \
        .representation() \
        .mark('point') \
        .map(encoding='y', field='height', type='quantitative') \
        .map(encoding='x', field='weight', type='quantitative') \
        .map(encoding='size', field='age', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "donors", "source": "./data/example_donors.csv"},
        "representation": {
            "mark": "point",
            "mapping": [
                {"encoding": "y", "field": "height", "type": "quantitative"},
                {"encoding": "x", "field": "weight", "type": "quantitative"},
                {"encoding": "size", "field": "age", "type": "quantitative"},
            ],
        },
    }
    
# heatmaps

# Heatmaps
def test_heatmap_of_categories():
    chart = Chart()
    chart.source('samples', './data/example_samples.csv') \
        .transformation() \
        .groupby(['organ', 'organ_condition']) \
        .rollup({'count': Op.count()})
    
    chart.representation().mark('rect') \
         .map(encoding='x', field='organ_condition', type='nominal') \
         .map(encoding='y', field='organ', type='nominal') \
         .map(encoding='color', field='count', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "samples", "source": "./data/example_samples.csv"},
        "transformation": [
            {"groupby": ["organ", "organ_condition"]},
            {"rollup": {"count": {"op": "count"}}},
        ],
        "representation": {
            "mark": "rect",
            "mapping": [
                {"encoding": "x", "field": "organ_condition", "type": "nominal"},
                {"encoding": "y", "field": "organ", "type": "nominal"},
                {"encoding": "color", "field": "count", "type": "quantitative"},
            ],
        },
    }

def test_heatmap_with_aggregation():
    chart = Chart()
    chart.source('samples', './data/example_samples.csv') \
        .transformation() \
        .groupby(['organ', 'organ_condition']) \
        .rollup({'average_weight': Op.mean('weight')})
    
    chart.representation().mark('rect') \
         .map(encoding='x', field='organ_condition', type='nominal') \
         .map(encoding='y', field='organ', type='nominal') \
         .map(encoding='color', field='average_weight', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "samples", "source": "./data/example_samples.csv"},
        "transformation": [
            {"groupby": ["organ", "organ_condition"]},
            {"rollup": {"average_weight": {"op": "mean", "field": "weight"}}},
        ],
        "representation": {
            "mark": "rect",
            "mapping": [
                {"encoding": "x", "field": "organ_condition", "type": "nominal"},
                {"encoding": "y", "field": "organ", "type": "nominal"},
                {"encoding": "color", "field": "average_weight", "type": "quantitative"},
            ],
        },
    }

def test_heatmap_with_multiple_aggregations():
    chart = Chart()
    chart.source('samples', './data/example_samples.csv') \
        .transformation() \
        .groupby(['organ', 'organ_condition']) \
        .rollup({'average_weight': Op.mean('weight'), 'count': Op.count()})
    
    chart.representation().mark('rect') \
         .map(encoding='x', field='organ_condition', type='nominal') \
         .map(encoding='y', field='organ', type='nominal') \
         .map(encoding='color', field='average_weight', type='quantitative') \
         .map(encoding='size', field='count', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "samples", "source": "./data/example_samples.csv"},
        "transformation": [
            {"groupby": ["organ", "organ_condition"]},
            {"rollup": {"average_weight": {"op": "mean", "field": "weight"}, "count": {"op": "count"}}},
        ],
        "representation": {
            "mark": "rect",
            "mapping": [
                {"encoding": "x", "field": "organ_condition", "type": "nominal"},
                {"encoding": "y", "field": "organ", "type": "nominal"},
                {"encoding": "color", "field": "average_weight", "type": "quantitative"},
                {"encoding": "size", "field": "count", "type": "quantitative"},
            ],
        },
    }

# distribution plots

def test_histogram():
    chart = Chart()
    chart.source('penguins', './data/penguins.csv') \
        .transformation() \
        .binby(field='bill_length_mm', bins=10, nice=True, output={'bin_start': 'start', 'bin_end': 'end'}) \
        .rollup({'count': Op.count()})
    
    chart.representation().mark('rect') \
         .map(encoding='x', field='start', type='quantitative') \
         .map(encoding='x2', field='end', type='quantitative') \
         .map(encoding='y', field='count', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "penguins", "source": "./data/penguins.csv"},
        "transformation": [
            {"binby": {"field": "bill_length_mm", "bins": 10, "nice": True, "output": {"bin_start": "start", "bin_end": "end"}}},
            {"rollup": {"count": {"op": "count"}}},
        ],
        "representation": {
            "mark": "rect",
            "mapping": [
                {"encoding": "x", "field": "start", "type": "quantitative"},
                {"encoding": "x2", "field": "end", "type": "quantitative"},
                {"encoding": "y", "field": "count", "type": "quantitative"},
            ],
        },
    }

def test_kde_density_plot():
    chart = Chart()
    chart.source('penguins', './data/penguins.csv') \
        .transformation() \
        .kde(field='bill_length_mm', samples=100, output={'sample': 'bill_length_mm', 'density': 'density'})
    
    chart.representation().mark('area') \
         .map(encoding='x', field='bill_length_mm', type='quantitative') \
         .map(encoding='y', field='density', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "penguins", "source": "./data/penguins.csv"},
        "transformation": [
            {"kde": {"field": "bill_length_mm", "samples": 100, "output": {"sample": "bill_length_mm", "density": "density"}}},
        ],
        "representation": {
            "mark": "area",
            "mapping": [
                {"encoding": "x", "field": "bill_length_mm", "type": "quantitative"},
                {"encoding": "y", "field": "density", "type": "quantitative"},
            ],
        },
    }

def test_kde_density_plot_grouped():
    chart = Chart()
    chart.source('penguins', './data/penguins.csv') \
        .transformation() \
        .groupby('species') \
        .kde(field='bill_length_mm', samples=100, output={'sample': 'bill_length_mm', 'density': 'density'})
    
    chart.representation().mark('area') \
         .map(encoding='x', field='bill_length_mm', type='quantitative') \
         .map(encoding='y', field='density', type='quantitative') \
         .map(encoding='color', field='species', type='nominal') \
         .map(encoding='opacity', value=0.25)
    
    chart.representation().mark('line') \
         .map(encoding='x', field='bill_length_mm', type='quantitative') \
         .map(encoding='y', field='density', type='quantitative') \
         .map(encoding='color', field='species', type='nominal')

    assert chart.to_dict() == {
        "source": {"name": "penguins", "source": "./data/penguins.csv"},
        "transformation": [
            {"groupby": "species"},
            {"kde": {"field": "bill_length_mm", "samples": 100, "output": {"sample": "bill_length_mm", "density": "density"}}},
        ],
        "representation": [
            {
                "mark": "area",
                "mapping": [
                    {"encoding": "x", "field": "bill_length_mm", "type": "quantitative"},
                    {"encoding": "y", "field": "density", "type": "quantitative"},
                    {"encoding": "color", "field": "species", "type": "nominal"},
                    {"encoding": "opacity", "value": 0.25},
                ],
            },
            {
                "mark": "line",
                "mapping": [
                    {"encoding": "x", "field": "bill_length_mm", "type": "quantitative"},
                    {"encoding": "y", "field": "density", "type": "quantitative"},
                    {"encoding": "color", "field": "species", "type": "nominal"},
                ],
            },
        ],
    }

def test_empirical_cdf():
    chart = Chart()
    chart.source('penguins', './data/penguins.csv') \
        .transformation() \
        .orderby('bill_length_mm') \
        .derive({'total': 'count()'}) \
        .derive({'percentile': {'rolling': {'expression': 'count() / d.total'}}})
    
    chart.representation().mark('line') \
         .map(encoding='x', field='bill_length_mm', type='quantitative') \
         .map(encoding='y', field='percentile', type='quantitative')

    assert chart.to_dict() == {
        "source": {"name": "penguins", "source": "./data/penguins.csv"},
        "transformation": [
            {"orderby": "bill_length_mm"},
            {"derive": {"total": "count()"}},
            {"derive": {"percentile": {"rolling": {"expression": "count() / d.total"}}}},
        ],
        "representation": {
            "mark": "line",
            "mapping": [
                {"encoding": "x", "field": "bill_length_mm", "type": "quantitative"},
                {"encoding": "y", "field": "percentile", "type": "quantitative"},
            ],
        },
    }

def test_empirical_cdf_grouped():
    chart = Chart()
    chart.source('penguins', './data/penguins.csv') \
        .transformation() \
        .orderby('bill_length_mm') \
        .groupby('species') \
        .derive({'total': 'count()'}) \
        .derive({'percentile': {'rolling': {'expression': 'count() / d.total'}}})
    
    chart.representation().mark('line') \
         .map(encoding='x', field='bill_length_mm', type='quantitative') \
         .map(encoding='y', field='percentile', type='quantitative') \
         .map(encoding='color', field='species', type='nominal')

    assert chart.to_dict() == {
        "source": {"name": "penguins", "source": "./data/penguins.csv"},
        "transformation": [
            {"orderby": "bill_length_mm"},
            {"groupby": "species"},
            {"derive": {"total": "count()"}},
            {"derive": {"percentile": {"rolling": {"expression": "count() / d.total"}}}},
        ],
        "representation": {
            "mark": "line",
            "mapping": [
                {"encoding": "x", "field": "bill_length_mm", "type": "quantitative"},
                {"encoding": "y", "field": "percentile", "type": "quantitative"},
                {"encoding": "color", "field": "species", "type": "nominal"},
            ],
        },
    }

# Table Tests
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