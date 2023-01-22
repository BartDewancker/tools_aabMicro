import os
import pickle
from Run import Run
from typing import List, Dict

class DataBase:
    def __init__(self, dbFile):
        self.dbFile = dbFile
        self.runs = []

        if os.path.exists(self.dbFile):
            with open(self.dbFile, 'rb') as f:
                self.runs = pickle.load(f)
        else:
            os.makedirs(os.path.dirname(self.dbFile), exist_ok=True)
            with open(self.dbFile, 'wb') as f:  
                pickle.dump(self.runs, f)

    def __str__(self):
        return f"DataBase with {len(self.runs)} runs"

    def dump(self):
        with open(self.dbFile, "wb") as f:
            pickle.dump(self.runs, f)
    
    def clear(self):
        self.runs = []

    def getIds(self):
        return [r.id for r in self.runs]

    def getRun(self, id):
        return list(filter(lambda r: r.id == id, self.runs))[0]

    def add(self, run: Run):
        if run.id not in self.getIds():
            self.runs.append(run)
        else:
            raise ValueError(f"Database already contains a run with id {run.id}.")

    def remove(self, id: str):
        if id in self.getIds():
            self.runs = list(filter(lambda r: r.id != id, self.runs))
        else:
            raise ValueError(f"There is no run with id {id} in database.")

    def find(self, algoTypes: List[str], versions: List[str], library: str, specifiers: Dict[str,List]):
        """ 
        Return the id of the runs with
        - algo.type in algoTypes, and 
        - algo.version in versions, and
        - library available in metrics, and
        - settings in specifiers

        specifiers is a dict with algo settings internal name and a list with their values:
        eg. specifiers = {'Flame_param_FlameDetectionSensitivity':['60','90']}
        to get id from runs that have 'FlameDetectionSensitivity' equal to '60' or '90'.
        """
        selection = []

        for run in self.runs:

            if ((run.algo.type in algoTypes) and
                (run.algo.version in versions)):
                
                evaluatedLibraries = []
                for benchmark in run.getMetrics().values():
                    evaluatedLibraries += list(benchmark.keys())

                if library.lower() in evaluatedLibraries:

                    settings = run.getSettings()
                    allMatching = True
                    for k,specifiedValues in specifiers.items():
                        if k == 'version':
                            allMatching &= specifiedValues.count(run.algo.version) > 0 
                        elif k == 'algo_type' or k == 'algo':
                            allMatching &= specifiedValues.count(run.algo.type) > 0 
                        else:
                            subalgo, paramName = k.split('_param_')
                            # are the setting of this run in the specifiedValues (if the subalgo and paramName exist for this run)?
                            if subalgo in settings:
                                if paramName in settings[subalgo]:
                                    allMatching &= specifiedValues.count(settings[subalgo][paramName]) > 0 
                    if allMatching:
                        selection.append(run.id)
        return selection
