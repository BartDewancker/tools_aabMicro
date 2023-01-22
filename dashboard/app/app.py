#%% 
import os
import dash
import pandas as pd

from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import appUtils as utils
from createDataForApp import loadDatabase, loadVideoLibrary
from CombinedMetrics import CombinedMetrics

# -----------------------------------------------------------
# Start App
# ----------------------------------------------

app = dash.Dash(__name__)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

db = loadDatabase()

# create dataframe with combined metrics of runs in database
combinedMetrics = CombinedMetrics(db.runs)
mDf = combinedMetrics.dataframe

# load videolibrary
videoLibrary = loadVideoLibrary()


# labels for parameter names
figLabels = {
    **{'tpr':'True Positive Rate', 
        'fpr':'False Positive Rate',
        'tp':'True Postives',
        'fp':'False Positives'},
    **{col: CombinedMetrics.parameter(col) for col in combinedMetrics.parameterColumns()}
}
figBGColor='#e5e5e5'


# -----------------------------------------------------------
# App Layout
# -----------------------------------------------------------

def createParamTablesTab(tableData):
    headRow = [html.Tr([html.Th('Parameter'), html.Th('Value')])]
    tabs = list()
    for subalgo, params in tableData.items():
        tab = dcc.Tab(label=utils.unCamelCase(subalgo), value=subalgo, children=[
            html.Div(className='table-wrapper', children=[
                html.Div(className='table-scroll', children=[
                    html.Table(headRow+[html.Tr([html.Td([v['label']]), html.Td([dcc.Checklist(id=v['id'], options=v['options'], value=v['value'])])]) for v in params.values()])
                ]),
            ])
        ])
        tabs.append(tab)
    return tabs#dcc.Tabs(id=f'{library.lower()}-tabs', value=f'{library.lower()}-{library.lower()}-tab', children=tabs)

def createVideoListTablesTab(library):
    return dcc.Tabs(value=f'{library.lower()}-tab-detected', children=[
        dcc.Tab(label='Detected', value=f'{library.lower()}-tab-detected', id=f'{library.lower()}-tab-detected', children=[
            html.Div(className='table-wrapper', children=[
                html.Div(className='table-scroll', children=[
                    html.Table(id=f'{library.lower()}-video-table-detected', children=[
                    ]),
                ]),
            ]),
        ]),
        dcc.Tab(label='Not Detected', value=f'{library.lower()}-tab-not-detected', id=f'{library.lower()}-tab-not-detected', children=[
            html.Div(className='table-wrapper', children=[
                html.Div(className='table-scroll', children=[
                    html.Table(id=f'{library.lower()}-video-table-not-detected', children=[
                    ]),
                ]),
            ]),
        ]),
    ])

def createGraphSection(library):
    return [
        dcc.Dropdown(
            id=f'{library.lower()}-color-column',
            placeholder='Select color specifier...',
            style=dict(width=300)
        ),
        dcc.Dropdown(
            id=f'{library.lower()}-symbol-column',
            placeholder='Select symbol specifier...',
            style=dict(width=300)
        ),

        html.Div([
            html.Div([
                dcc.Graph(
                    id=f'{library.lower()}-detection-roc',
                )]
            ),
            html.Div([
                dcc.Graph(
                    id=f'{library.lower()}-tpr-bar',
                )]
            ),
            html.Div([
                dcc.Graph(
                    id=f'{library.lower()}-fp-bar',
                )]
            ),
        ])
    ]

def createAlgoSection(library):
    return [html.H2(children=f'{library} Detection'),

            html.Div(className='row', children=[
                html.Div([
                    html.H3(children=f'{library} Detection Settings'),
                    html.Div(id=f'{library.lower()}-parameter-tables-tab-div', children=[
                        dcc.Tabs(id=f'{library.lower()}-tabs', value=f'{library.lower()}-{library.lower()}-tab')
                    ]),
                    html.Button('Submit', id=f'{library.lower()}-submit-button', n_clicks=0),
                    html.Br(),
                    html.H3(children='Inspect Category'),
                    html.P(children='Click a bar to inspect videos...', id=f'{library.lower()}-video-table-title'),
                    html.Div([
                        createVideoListTablesTab(f'{library.lower()}')
                    ]),
                    html.Br(),
                    html.H3(children='Inspect States'),
                    html.Div(id=f'{library.lower()}-alarm-df-table'),
                ], className='four columns'),
                html.Div([
                    html.H3(children=f'{library} Detection Performance'),
                    html.Div(children=createGraphSection(f'{library.lower()}')),
                ], className='eight columns'),
            ])
        ]

app.layout = html.Div([
    html.H1(children='Araani Analytics Benchmarking'),

    html.Div([
        html.Div([
            html.P('Select Benchmark Version'),
            dcc.Dropdown(
                id='selected-benchmark-version',
                options=[{'label': version, 'value': version} for version in videoLibrary.benchmarkVersions()],
                multi=False,
                placeholder="Select benchmark version...",
                style=dict(width=400)
            ),
            html.P('Select Algorithm'),
            dcc.Dropdown(
                id='selected-algo',
                # options=[{'label': algo, 'value': algo} for algo in listOfAlgoTypes],
                value = [],
                multi=True,
                placeholder="Select algorithm(s)...",
                style=dict(width=400)
            ),
            html.P('Select Version(s)'),
            dcc.Dropdown(
                id='selected-algo-version',
                value = [],
                multi=True,
                placeholder="Select version(s)...",
                style=dict(width=400)
            ),
        ]),
    ]),
    # html.Div(children=createAlgoSection('Smoke')),
    # html.Div(children=createAlgoSection('Flame')),
    html.Br(),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Smoke Detection', children=[
                html.Div(children=createAlgoSection('Smoke'))
            ]),
            dcc.Tab(label='Flame Detection', children=[
                html.Div(children=createAlgoSection('Flame'))
            ]),
        ]),
    ]),
])

# -----------------------------------------------------------
# Callbacks
# -----------------------------------------------------------

# -----------------------------------------------------------
# Common fields: updating dropdown for algorithm and version
# -----------------------------------------------------------

@app.callback(
    Output('selected-algo', 'options'),
    Input('selected-benchmark-version', 'value'))
def set_algo_options(selected_benchmark_version):
    if selected_benchmark_version is None:
        raise PreventUpdate
    algos = list(mDf[mDf['benchmark_version'] == selected_benchmark_version]['algo_type'].unique())
    return [{'label': i, 'value': i} for i in algos]

@app.callback(
    Output('selected-algo-version', 'options'),
    Input('selected-algo', 'value'))
def set_algo_version_options(selected_algos):
    if len(selected_algos) == 0:
        raise PreventUpdate
    versions = mDf[mDf['algo_type'].isin(selected_algos)]['version'].unique()
    return [{'label': i, 'value': i} for i in versions]


# ------------------------------------------------
# Smoke Callbacks
# ------------------------------------------------


@app.callback(
    output=Output('smoke-tabs', 'children'),
    inputs={
        'benchmarkVersion':Input(component_id='selected-benchmark-version', component_property='value'),
        'algos':Input(component_id='selected-algo', component_property='value'),
        'versions':Input(component_id='selected-algo-version', component_property='value')}
)
def set_smoke_algo_settings_options(benchmarkVersion, algos, versions):
    dff = mDf[(mDf['library']=='smoke')]
    if benchmarkVersion is None or len(algos)==0 or len(versions)==0 or dff.empty:
        raise PreventUpdate
    else:
        tableData = utils.getAlgoSettingsTableData(
            mDf, "smoke", 
            benchmarkVersion, algos, versions)
        return createParamTablesTab(tableData)

@app.callback(
    Output(component_id='smoke-color-column', component_property='options'),
    inputs={
        'paramTable':Input(component_id='smoke-tabs', component_property='children'),
        'submitButton':Input(component_id='smoke-submit-button', component_property='n_clicks'),
        'symbolParam':Input(component_id='smoke-symbol-column', component_property='value')},
    state={'settings':State('smoke-tabs','children')}
)
def set_smoke_color_options(paramTable, submitButton, symbolParam, settings):
    """
    Options: "version", "algorithm", or any algo setting for which there are two different values selectable
    Cannot be the same as symbolParam
    """
    colorOptions = utils.get_color_options(symbolParam, settings)
    return colorOptions


@app.callback(
    Output(component_id='smoke-symbol-column', component_property='options'),
    inputs={
        'paramTable':Input(component_id='smoke-tabs', component_property='children'),
        'submitButton':Input(component_id='smoke-submit-button', component_property='n_clicks'),
        'colorParam':Input(component_id='smoke-color-column', component_property='value')},
    state={'settings':State('smoke-tabs','children')}
)
def set_smoke_symbol_options(paramTable, submitButton, colorParam, settings):
    """
    Options: "version" or any algo setting for which there are two different values selectable
    Cannot be the same as colorParam
    """
    symbolOptions = utils.get_symbol_options(colorParam, settings)
    return symbolOptions


@app.callback(
    output=[
        Output(component_id='smoke-detection-roc', component_property='figure'),
        Output(component_id='smoke-tpr-bar', component_property='figure'),
        Output(component_id='smoke-fp-bar', component_property='figure')],
    inputs={
        'benchmarkVersion':Input(component_id='selected-benchmark-version', component_property='value'),
        'algos':Input(component_id='selected-algo', component_property='value'),
        'settings':Input(component_id='smoke-tabs', component_property='children'),
        'versions':Input(component_id='selected-algo-version', component_property='value'),
        'submitButton':Input(component_id='smoke-submit-button', component_property='n_clicks'),
        'colorValue':Input(component_id='smoke-color-column', component_property='value'),
        'symbolValue':Input(component_id='smoke-symbol-column', component_property='value')}
)
def update_smoke_figs(benchmarkVersion, algos, settings, versions, submitButton, colorValue, symbolValue):
    # get data from selected algo and selected version
    dff = mDf[(mDf['library']=='smoke')]
    if benchmarkVersion is None or len(algos)==0 or len(versions)==0 or dff.empty or settings is None:
        raise PreventUpdate
    else:
        dff = dff[
            (dff['benchmark_version'] == benchmarkVersion) & 
            (dff['algo_type'].isin(algos)) &
            (dff['version'].isin(versions))]
        # find smoke parameters that can be selected
        tableData = utils.getTableData(settings)
        for subAlgo, params in tableData.items():
            for param in params.values():
                columnName = CombinedMetrics.columnName(param['label'], subAlgo)
                # not all versions have the same parameters, so it's ok if param value is null
                dff = dff[dff[columnName].isin(param['value']) | (dff[columnName].isnull())]
        # convert the selected parameter names to the corresponding dataframe column name
        colorColumn = utils.internalNameToCombinedMetricsColumn(colorValue, 'smoke')
        symbolColumn = utils.internalNameToCombinedMetricsColumn(symbolValue, 'smoke')
        return [utils.createROCCurve(dff, color=colorColumn, symbol=symbolColumn, figLabels=figLabels, figBGColor=figBGColor), 
                utils.createTPRBarCurve(dff, color=colorColumn, pattern_shape=symbolColumn, figLabels=figLabels, figBGColor=figBGColor),
                utils.createFPBarCurve(dff, color=colorColumn, pattern_shape=symbolColumn, figLabels=figLabels, figBGColor=figBGColor)]


@app.callback(
    output=[
        Output('smoke-video-table-detected', 'children'),
        Output('smoke-video-table-not-detected', 'children'),
        Output('smoke-video-table-title', 'children'),
        Output('smoke-tab-detected', 'label'),
        Output('smoke-tab-not-detected', 'label')],
    inputs={
        'TPRClickData':Input('smoke-tpr-bar', 'clickData'),
        'FPClickData':Input('smoke-fp-bar', 'clickData')},
    state={
        'benchmarkVersion':State('selected-benchmark-version', 'value'),
        'algos':State('selected-algo', 'value'),
        'versions':State('selected-algo-version', 'value'),
        'colorSpecifier':State('smoke-color-column', 'value'),
        'symbolSpecifier':State('smoke-symbol-column', 'value'),
        'TPRFigure':State('smoke-tpr-bar', 'figure'),
        'FPFigure':State('smoke-fp-bar', 'figure'),
        'settings':State('smoke-tabs','children')}
    )
def display_click_smoke_bar_curve(TPRClickData, FPClickData, benchmarkVersion, algos, versions, colorSpecifier, symbolSpecifier, TPRFigure, FPFigure, settings):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
        raise PreventUpdate 
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'smoke-tpr-bar':
            clickData = TPRClickData
            figure = TPRFigure
        elif button_id == 'smoke-fp-bar':
            clickData = FPClickData
            figure = FPFigure
        if clickData is None:
            raise PreventUpdate 
        else:
            library = 'Smoke'
            runIds = utils.getRunIdsFromClick(db, clickData, figure, algos, versions, library, colorSpecifier, symbolSpecifier, settings)
            if len(runIds) == 1:
                run = db.getRun(runIds[0])

                category = utils.getCategory(clickData)
                benchmark = videoLibrary.data(version=benchmarkVersion, library=library, category=category)
                
                gtColumn = f'gt{library.capitalize()}'
                gt = benchmark[gtColumn]

                predictionColumn = 'FireAlarm' if 'aal_fire' in run.algo.type else f'{library.capitalize()}Alarm'
                predictions = run.getStateCounts(benchmark.index)[predictionColumn]

                df = pd.concat([gt, predictions], axis=1, ignore_index=False)

                return utils.getVideoListTableContent(df, gtColumn, predictionColumn, category, library, button_id)
            else:
                raise PreventUpdate 

@app.callback(
    output=[
        Output('smoke-alarm-df-table', 'children')
    ],
    inputs={
        'TPRClickData':Input('smoke-tpr-bar', 'clickData'),
        'FPClickData':Input('smoke-fp-bar', 'clickData')},
    state={
        'benchmarkVersion':State('selected-benchmark-version', 'value'),
        'algos':State('selected-algo', 'value'),
        'versions':State('selected-algo-version', 'value'),
        'colorSpecifier':State('smoke-color-column', 'value'),
        'symbolSpecifier':State('smoke-symbol-column', 'value'),
        'TPRFigure':State('smoke-tpr-bar', 'figure'),
        'FPFigure':State('smoke-fp-bar', 'figure'),
        'settings':State('smoke-tabs','children')}
    )
def display_state_table_on_click_smoke_bar_curve(TPRClickData, FPClickData, benchmarkVersion, algos, versions, colorSpecifier, symbolSpecifier, TPRFigure, FPFigure, settings):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
        raise PreventUpdate 
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'smoke-tpr-bar':
            clickData = TPRClickData
            figure = TPRFigure
        elif button_id == 'smoke-fp-bar':
            clickData = FPClickData
            figure = FPFigure
        if clickData is None:
            raise PreventUpdate 
        else:
            library = 'Smoke'
            runIds = utils.getRunIdsFromClick(db, clickData, figure, algos, versions, library, colorSpecifier, symbolSpecifier, settings)
            if len(runIds) == 1:
                run = db.getRun(runIds[0])
                videos = videoLibrary.videos(version=benchmarkVersion, library=library, category=utils.getCategory(clickData))
                df = run.getStateCounts(videos)
                return utils.createDashTableForStates(df, tableColumns=['FireAlarm', 'FaultSignal', 'FlameAlarm', 'SmokeAlarm'])
            else:
                raise PreventUpdate 


# ------------------------------------------------
# Flame Callbacks
# ------------------------------------------------

@app.callback(
    output=Output('flame-tabs', 'children'),
    inputs={
        'benchmarkVersion':Input(component_id='selected-benchmark-version', component_property='value'),
        'algos':Input(component_id='selected-algo', component_property='value'),
        'versions':Input(component_id='selected-algo-version', component_property='value')}
)
def set_flame_algo_settings_options(benchmarkVersion, algos, versions):
    dff = mDf[(mDf['library']=='flame')]
    if benchmarkVersion is None or len(algos)==0 or len(versions)==0 or dff.empty:
        raise PreventUpdate
    else:
        tableData = utils.getAlgoSettingsTableData(
            mDf, "flame", 
            benchmarkVersion, algos, versions)
        return createParamTablesTab(tableData)

@app.callback(
    Output(component_id='flame-color-column', component_property='options'),
    inputs={
        'paramTable':Input(component_id='flame-tabs', component_property='children'),
        'submitButton':Input(component_id='flame-submit-button', component_property='n_clicks'),
        'symbolParam':Input(component_id='flame-symbol-column', component_property='value')},
    state={'settings':State('flame-tabs','children')}
)
def set_flame_color_options(paramTable, submitButton, symbolParam, settings):
    """
    Options: "version", "algorithm", or any algo setting for which there are two different values selectable
    Cannot be the same as symbolParam
    """
    colorOptions = utils.get_color_options(symbolParam, settings)
    return colorOptions


@app.callback(
    Output(component_id='flame-symbol-column', component_property='options'),
    inputs={
        'paramTable':Input(component_id='flame-tabs', component_property='children'),
        'submitButton':Input(component_id='flame-submit-button', component_property='n_clicks'),
        'colorParam':Input(component_id='flame-color-column', component_property='value')},
    state={'settings':State('flame-tabs','children')}
)
def set_flame_symbol_options(paramTable, submitButton, colorParam, settings):
    """
    Options: "version" or any algo setting for which there are two different values selectable
    Cannot be the same as colorParam
    """
    symbolOptions = utils.get_symbol_options(colorParam, settings)
    return symbolOptions


@app.callback(
    output=[
        Output(component_id='flame-detection-roc', component_property='figure'),
        Output(component_id='flame-tpr-bar', component_property='figure'),
        Output(component_id='flame-fp-bar', component_property='figure')],
    inputs={
        'benchmarkVersion':Input(component_id='selected-benchmark-version', component_property='value'),
        'algos':Input(component_id='selected-algo', component_property='value'),
        'settings':Input(component_id='flame-tabs', component_property='children'),
        'versions':Input(component_id='selected-algo-version', component_property='value'),
        'submitButton':Input(component_id='flame-submit-button', component_property='n_clicks'),
        'colorValue':Input(component_id='flame-color-column', component_property='value'),
        'symbolValue':Input(component_id='flame-symbol-column', component_property='value')}
)
def update_flame_figs(benchmarkVersion, algos, settings, versions, submitButton, colorValue, symbolValue):
    # get data from selected algo and selected version
    dff = mDf[(mDf['library']=='flame')]
    if benchmarkVersion is None or len(algos)==0 or len(versions)==0 or dff.empty or settings is None:
        raise PreventUpdate
    else:
        dff = dff[
            (dff['benchmark_version'] == benchmarkVersion) & 
            (dff['algo_type'].isin(algos)) &
            (dff['version'].isin(versions))]
        # find flame parameters that can be selected
        tableData = utils.getTableData(settings)
        for subAlgo, params in tableData.items():
            for param in params.values():
                columnName = CombinedMetrics.columnName(param['label'], subAlgo)
                # not all versions have the same parameters, so it's ok if param value is null
                dff = dff[dff[columnName].isin(param['value']) | (dff[columnName].isnull())]

        # convert the selected parameter names to the corresponding dataframe column name
        colorColumn = utils.internalNameToCombinedMetricsColumn(colorValue, 'flame')
        symbolColumn = utils.internalNameToCombinedMetricsColumn(symbolValue, 'flame')
        return [utils.createROCCurve(dff, color=colorColumn, symbol=symbolColumn, figLabels=figLabels, figBGColor=figBGColor), 
                utils.createTPRBarCurve(dff, color=colorColumn, pattern_shape=symbolColumn, figLabels=figLabels, figBGColor=figBGColor),
                utils.createFPBarCurve(dff, color=colorColumn, pattern_shape=symbolColumn, figLabels=figLabels, figBGColor=figBGColor)]


@app.callback(
    output=[
        Output('flame-video-table-detected', 'children'),
        Output('flame-video-table-not-detected', 'children'),
        Output('flame-video-table-title', 'children'),
        Output('flame-tab-detected', 'label'),
        Output('flame-tab-not-detected', 'label')],
    inputs={
        'TPRClickData':Input('flame-tpr-bar', 'clickData'),
        'FPClickData':Input('flame-fp-bar', 'clickData')},
    state={
        'benchmarkVersion':State('selected-benchmark-version', 'value'),
        'algos':State('selected-algo', 'value'),
        'versions':State('selected-algo-version', 'value'),
        'colorSpecifier':State('flame-color-column', 'value'),
        'symbolSpecifier':State('flame-symbol-column', 'value'),
        'TPRFigure':State('flame-tpr-bar', 'figure'),
        'FPFigure':State('flame-fp-bar', 'figure'),
        'settings':State('flame-tabs','children')}
    )
def display_click_flame_bar_curve(TPRClickData, FPClickData, benchmarkVersion, algos, versions, colorSpecifier, symbolSpecifier, TPRFigure, FPFigure, settings):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
        raise PreventUpdate 
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'flame-tpr-bar':
            clickData = TPRClickData
            figure = TPRFigure
        elif button_id == 'flame-fp-bar':
            clickData = FPClickData
            figure = FPFigure
        if clickData is None:
            raise PreventUpdate 
        else:
            library = 'Flame'
            runIds = utils.getRunIdsFromClick(db, clickData, figure, algos, versions, library, colorSpecifier, symbolSpecifier, settings)
            if len(runIds) == 1:
                run = db.getRun(runIds[0])

                category = utils.getCategory(clickData)
                benchmark = videoLibrary.data(version=benchmarkVersion, library=library, category=category)
                
                gtColumn = f'gt{library.capitalize()}'
                gt = benchmark[gtColumn]

                predictionColumn = 'FireAlarm' if 'aal_fire' in run.algo.type else f'{library.capitalize()}Alarm'
                predictions = run.getStateCounts(benchmark.index)[predictionColumn]

                df = pd.concat([gt, predictions], axis=1, ignore_index=False)

                return utils.getVideoListTableContent(df, gtColumn, predictionColumn, category, library, button_id)
            else:
                raise PreventUpdate 

@app.callback(
    output=[
        Output('flame-alarm-df-table', 'children')
    ],
    inputs={
        'TPRClickData':Input('flame-tpr-bar', 'clickData'),
        'FPClickData':Input('flame-fp-bar', 'clickData')},
    state={
        'benchmarkVersion':State('selected-benchmark-version', 'value'),
        'algos':State('selected-algo', 'value'),
        'versions':State('selected-algo-version', 'value'),
        'colorSpecifier':State('flame-color-column', 'value'),
        'symbolSpecifier':State('flame-symbol-column', 'value'),
        'TPRFigure':State('flame-tpr-bar', 'figure'),
        'FPFigure':State('flame-fp-bar', 'figure'),
        'settings':State('flame-tabs','children')}
    )
def display_state_table_on_click_flame_bar_curve(TPRClickData, FPClickData, benchmarkVersion, algos, versions, colorSpecifier, symbolSpecifier, TPRFigure, FPFigure, settings):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
        raise PreventUpdate 
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'flame-tpr-bar':
            clickData = TPRClickData
            figure = TPRFigure
        elif button_id == 'flame-fp-bar':
            clickData = FPClickData
            figure = FPFigure
        if clickData is None:
            raise PreventUpdate 
        else:
            library = 'Flame'
            runIds = utils.getRunIdsFromClick(db, clickData, figure, algos, versions, library, colorSpecifier, symbolSpecifier, settings)
            if len(runIds) == 1:
                run = db.getRun(runIds[0])
                videos = videoLibrary.videos(version=benchmarkVersion, library=library, category=utils.getCategory(clickData))
                df = run.getStateCounts(videos)
                return utils.createDashTableForStates(df, tableColumns=['FireAlarm', 'FaultSignal', 'FlameAlarm', 'SmokeAlarm'])
            else:
                raise PreventUpdate 

# Import and start the database connection!
import database as dbNew
dbNew.start_db()

def getAllVideos():
    from videos.repo_video import VideoRepository
    from videos.models import VideoResponse

    res = VideoResponse(message="", error="")

    videos = VideoRepository.get_all(res)

    if res.error != "":
        return res.error
    elif (videos is not None and len(videos) > 0):
        return videos
    else:
        return res.message

if __name__ == '__main__':
    debug = (os.getenv('AAB_DEBUG', 'True') == 'True')
    port = os.getenv('AAB_PORT', 8050)

    print(getAllVideos())
    
    app.run_server(host="0.0.0.0", port=port, debug=debug) # , debug=True ,dev_tools_props_check=False