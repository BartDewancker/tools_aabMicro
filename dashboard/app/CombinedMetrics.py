# %%
from Run import Run
from typing import List
import pandas as pd
from pandas.api.types import CategoricalDtype

class CombinedMetrics:
    """
    Join metrics dataframes of all runs into a single dataframe.
    The dataframe is extended with columns:
    'id', 'algo_type', 'version', 'library' and 'benchmark_version'.
    for identifying to what run each row belongs.
    The dataframe is also extended with a column for each algo parameter.
    The column name has the following format: '<subalgo>_param_<parameter>'
    For example 'FlameDetectionSensitivity' of subalgo 'Flame'
    is named 'Flame_param_FlameDetectionSensitivity'.
    """

    separator = '_param_'

    def __init__(self, runs: List[Run]):
        self.algoTypes = self.__getAlgoTypes(runs)
        self.subAlgos = self.__getSubAlgos(runs)
        self.parameters = self.__getAllParameters(runs)
        self.dataframe = self.__combineMetrics(runs)

    @classmethod
    def columnName(cls, parameter, subalgo):
        return subalgo+cls.separator+parameter 

    @classmethod
    def isParameterColumn(cls, columnName):
        return columnName.find(cls.separator) >= 0

    @classmethod
    def parameter(cls, columnName):
        if cls.isParameterColumn(columnName):
            return columnName[columnName.find(cls.separator) + len(cls.separator):]
    
    @classmethod
    def subalgo(cls, columnName):
        if cls.isParameterColumn(columnName):
            return columnName[:columnName.find(cls.separator)]

    def parameterColumns(self):
        parameterColumnNames = list()
        for subAlgo, params in self.parameters.items():
            parameterColumnNames += [self.columnName(p, subAlgo) for p in params]
        return list(set(parameterColumnNames))

    def __getAlgoTypes(self, runs):
        return list(set([run.algo.type for run in runs]))

    def __getSubAlgos(self, runs):
        listOfSubAlgos = []
        for run in runs:
            listOfSubAlgos += list(run.getSettings().keys())
        return list(set(listOfSubAlgos))

    def __getAllParameters(self, runs):
        parameters = {subalgo: list() for subalgo in self.__getSubAlgos(runs)}
        for run in runs:
            for subAlgo, params in run.getSettings().items():
                parameters[subAlgo] += list(params.keys())
        for subAlgo in parameters:
            parameters[subAlgo] = list(set(parameters[subAlgo]))
        return parameters
        
    def __combineMetrics(self, runs):
        # Create Single DataFrame with all metrics from selected runs 
        mDf = list() # Metrics data
        for run in runs:
            metrics = run.getMetrics()
            settings = run.getSettings()
            for benchmarkVersion, benchmark in metrics.items():
                for lib, df in benchmark.items():
                    df['id'] = run.id
                    df['algo_type'] = run.algo.type
                    df['version'] = run.algo.version
                    df['library'] = lib 
                    df['benchmark_version'] = benchmarkVersion
                    # Add algo settings with prefix 'Flame_param_' or 'Smoke_param_'
                    for subAlgo, algoSettings in settings.items():
                        for k,v in algoSettings.items():
                            df[self.columnName(k, subAlgo)] = v 
                    mDf.append(df)
                    del df 
        mDf = pd.concat(mDf, ignore_index=True)

        # Set dtype of algo settings columns to Categorical, so we can have nan as a category
        paramColumns = list(filter(self.isParameterColumn, mDf.columns))
        for paramCol in paramColumns:
            # get all unique values, sort them, convert to string, and add 'nan
            categories = ['nan'] + list(map(str, sorted(set(mDf[paramCol].dropna()))))
            cat_type = CategoricalDtype(categories=categories, ordered=True)
            mDf[paramCol] = mDf[paramCol].astype(str).astype(cat_type)
        return mDf