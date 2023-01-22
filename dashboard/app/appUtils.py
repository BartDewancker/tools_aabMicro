import plotly.express as px
from dash import html
from dash import dash_table
from os.path import basename 
import os

from CombinedMetrics import CombinedMetrics 
from DataBase import DataBase

def internalName(parameter, subalgo, library):
    return f'{library.lower()}_{CombinedMetrics.columnName(parameter, subalgo)}'

def internalNameToCombinedMetricsColumn(internalName, library):
    if internalName is None:
        return 
    if internalName == "version":
        return "version"
    if internalName == "algo":
        return "algo_type"
    identifier = f'{library.lower()}_'
    if internalName.find(identifier) == 0:
        return internalName[len(identifier):]

def unCamelCase(str):
    start_idx = [i for i, e in enumerate(str)
                 if e.isupper()] + [len(str)]
  
    start_idx = [0] + start_idx
    words = [str[x: y] for x, y in zip(start_idx, start_idx[1:])] 
    words = [w for w in words if len(w)>0]
    word = words[0]
    if len(words) > 1:
        for w in words[1:]:
            word += ' '+w
    return word 

# --------------------------------------
# Plotting functions
# --------------------------------------

def createROCCurve(dff, color=None, symbol=None, figLabels=None, figBGColor=None):
    fig = px.scatter(dff[dff['category']=='allCategories'], 
        x='fp', y='tpr', 
        color=color,
        symbol=symbol,
        range_y=(0.,1.1),
        height=400,
        labels=figLabels)
    fig.update_traces(marker=dict(size=10),
        selector=dict(mode='markers'))
    fig.update_layout(plot_bgcolor=figBGColor,
        paper_bgcolor=figBGColor
    )
    return fig

def createTPRBarCurve(dff, color=None, pattern_shape=None, figLabels=None, figBGColor=None):
    fig = px.bar(dff[(dff['category_gt']) & (dff['category'] != 'allCategories')], 
                    x='category', y='tpr', 
                    color=color,
                    pattern_shape=pattern_shape,
                    barmode='group',
                    height=400,
                    labels=figLabels)
    fig.update_layout(plot_bgcolor=figBGColor,
        paper_bgcolor=figBGColor
    )
    return fig

def createFPBarCurve(dff, color=None, pattern_shape=None, figLabels=None, figBGColor=None):
    fig = px.bar(dff[(~dff['category_gt']) & (dff['category'] != 'allCategories')], 
                    x='category', y='fp', 
                    color=color,
                    pattern_shape=pattern_shape,
                    barmode='group',
                    height=400,
                    labels=figLabels)
    fig.update_layout(plot_bgcolor=figBGColor,
        paper_bgcolor=figBGColor
    )
    return fig


# --------------------------------------------
# function to construct table with alarms per video
# --------------------------------------------


def getFalsePositiveVideos(aDf, gtColumn, predColumn):
    return list(aDf[(aDf[predColumn] > 0) & (~aDf[gtColumn])].index)
def getTrueNegativeVideos(aDf, gtColumn, predColumn):
    return list(aDf[(aDf[predColumn] == 0) & (~aDf[gtColumn])].index)
def getFalseNegativeVideos(aDf, gtColumn, predColumn):
    return list(aDf[(aDf[predColumn] == 0) & (aDf[gtColumn])].index)
def getTruePositiveVideos(aDf, gtColumn, predColumn):
    return list(aDf[(aDf[predColumn] > 0) & (aDf[gtColumn])].index)

def getCategory(clickData):
    return clickData['points'][0]['x']

def getBarClickInfo(clickData, figure):
    category = clickData['points'][0]['x']
    curveNumber = clickData['points'][0]['curveNumber']
    curve = figure['data'][curveNumber]
    legendValues = list()
    if len(curve['legendgroup']):
        legendValues = curve['legendgroup'].replace(' ','').split(',')
    return (category, legendValues)

def getTableData(tableTabs):
    """ Get tableData dict from the hmtl tableTabs with algo settings per subalgo."""
    tableData = dict()
    for tab in tableTabs:
        tabLabel = tab['props']['label']
        tabValue = tab['props']['value']
        tableData[tabValue] = dict()
        rows = tab['props']['children'][0]['props']['children'][0]['props']['children'][0]['props']['children']
        for row in rows[1:]:
            label = row['props']['children'][0]['props']['children'][0]
            options = row['props']['children'][1]['props']['children'][0]['props']['options']
            value = row['props']['children'][1]['props']['children'][0]['props']['value']
            id = row['props']['children'][1]['props']['children'][0]['props']['id']
            tableData[tabValue][label] = {'label':label, 'options':options, 'value':value, 'id':id}
    return tableData

# --------------------------------------------
# Callback helper functions
# --------------------------------------------

def getAlgoSettingsTableData(metricsDf, library, benchmarkVersion, algos, versions):
    dff = metricsDf[
        (metricsDf['library']== library.lower()) &
        (metricsDf['benchmark_version'] == benchmarkVersion) &
        (metricsDf['algo_type'].isin(algos)) & 
        (metricsDf['version'].isin(versions))]
    parameterColumns = list(filter(CombinedMetrics.isParameterColumn, dff.columns))
    subAlgos = set()
    settings = set()
    for col in parameterColumns:
        subalgo = CombinedMetrics.subalgo(col)
        parameter = CombinedMetrics.parameter(col)
        subAlgos.add(subalgo)
        settings.add((subalgo,parameter))

    tableData = {subAlgoTab:{} for subAlgoTab in subAlgos}
    for subAlgo, param in settings:
        options = [{'label': val, 'value': val} for val in dff[CombinedMetrics.columnName(param, subAlgo)].unique()]
        tableData[subAlgo][param] = {
            'id':internalName(param, subAlgo, library.lower()),
            'dfColumnName': CombinedMetrics.columnName(param, subAlgo),
            'label':param, 
            'options':options, 
            'value':[opt['value'] for opt in options] # select all options 
        }
    return tableData

def get_color_options(symbolParam, settings):
    colorOptions = []
    if symbolParam != 'version':
        colorOptions.append({'label': 'Version', 'value': 'version'})
    if symbolParam != 'algo':
        colorOptions.append({'label': 'Algorithm', 'value': 'algo'})

    if settings is not None:
        tableData = getTableData(settings)
        for params in tableData.values():
            for param in params.values():
                if param['id'] != symbolParam:
                    if len(param['options']) > 1:
                        colorOptions.append({'label': param['label'], 'value': param['id']})
    return colorOptions

def get_symbol_options(colorParam, settings):
    symbolOptions = []
    if colorParam != 'version':
        symbolOptions.append({'label': 'Version', 'value': 'version'})
    if colorParam != 'algo':
        symbolOptions.append({'label': 'Algorithm', 'value': 'algo'})

    if settings is not None:
        tableData = getTableData(settings)
        for params in tableData.values():
            for param in params.values():
                if param['id'] != colorParam:
                    if len(param['options']) > 1:
                        symbolOptions.append({'label': param['label'], 'value': param['id']})
    return symbolOptions


def getRunIdsFromClick(db: DataBase, clickData, figure, algos, versions, library, colorSpecifier, symbolSpecifier, settings):
    
    # create dict with unique parameter names and allowed values    
    tableData = getTableData(settings)
    specifiers = {}
    for subAlgo, params in tableData.items():
        for param in params.values():
            specifiers[CombinedMetrics.columnName(param['label'], subAlgo)] = param['value']

    # Find out where click occured (what category, and what legend values)
    category, legendValues = getBarClickInfo(clickData, figure)
    
    # Set colorSpecifier and symbolSpecifier to legend values
    colorSpecifier = internalNameToCombinedMetricsColumn(colorSpecifier, library.lower())
    symbolSpecifier = internalNameToCombinedMetricsColumn(symbolSpecifier, library.lower())
        
    if len(legendValues)==2:
        specifiers[colorSpecifier] = [legendValues[0]]
        specifiers[symbolSpecifier] = [legendValues[1]]
    if len(legendValues)==1:
        if (colorSpecifier is None) and (symbolSpecifier is not None):
            specifiers[symbolSpecifier] = [legendValues[0]]
        if (symbolSpecifier is None) and (colorSpecifier is not None):
            specifiers[colorSpecifier] = [legendValues[0]]

    return db.find(algos, versions, library, specifiers)


def getVideoListTableContent(df, gtColumn, predictionColumn, category, library, button_id):
    # default values for output
    tableDataDetected = []
    tableDataNotDetected = []
    tableTitle = 'Could not collect videos with false alarm.\nPlease click single bar...'
    tabDetected = 'Detected'
    tabNotDetected = 'Not detected'

    if df is not None:
        tableTitle = f'Videos from category: {category}.'
        if button_id == f'{library.lower()}-fp-bar':
            tableDataDetected = [html.Tr([html.Td([basename(p)])]) for p in getFalsePositiveVideos(df, gtColumn, predictionColumn)]
            tableDataNotDetected = [html.Tr([html.Td([basename(p)])]) for p in getTrueNegativeVideos(df, gtColumn, predictionColumn)]
        elif button_id == f'{library.lower()}-tpr-bar':
            tableDataDetected = [html.Tr([html.Td([basename(p)])]) for p in getTruePositiveVideos(df, gtColumn, predictionColumn)]
            tableDataNotDetected = [html.Tr([html.Td([basename(p)])]) for p in getFalseNegativeVideos(df, gtColumn, predictionColumn)]
        tabDetected += f' ({len(tableDataDetected)})'
        tabNotDetected += f' ({len(tableDataNotDetected)})'

    return [tableDataDetected, tableDataNotDetected, tableTitle, tabDetected, tabNotDetected]


def createDashTableForStates(df, tableColumns):
    
    for col in tableColumns:
        if col not in df.columns:
            tableColumns.pop(col)
    
    df = df.reset_index()
    df['video'] = df['videoPath'].apply(os.path.basename)
    tableColumns.insert(0, 'video')

    return [dash_table.DataTable(
                data=df.to_dict('records'), 
                columns=[{"name": i, "id": i} for i in tableColumns],
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'video'},
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'width': '40%'
                    },
                ],
                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{FireAlarm} > 0',
                            'column_id': 'FireAlarm'
                        },
                        'backgroundColor': 'tomato',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{FlameAlarm} > 0',
                            'column_id': 'FlameAlarm'
                        },
                        'backgroundColor': 'tomato',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{SmokeAlarm} > 0',
                            'column_id': 'SmokeAlarm'
                        },
                        'backgroundColor': 'tomato',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{FaultSignal} > 0',
                            'column_id': 'FaultSignal'
                        },
                        'backgroundColor': 'mediumpurple',
                        'color': 'white'
                    },
                ],
                tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in df.to_dict('records')
                ],
                tooltip_duration=None)]