import os
import json
import dataUtils as utils 
import pandas as pd
from typing import Dict
from Run import Run
from DataBase import DataBase
from VideoLibrary import VideoLibrary

DATADIR = os.path.realpath(os.getenv("AAB_DATADIR", r"D:/aabData"))
APPDATADIR = os.path.join(DATADIR, "appData") 
VIDEOLIBDIR = os.path.realpath(os.getenv("AAB_VIDEOLIBRARY", r"D:/VideoLibrary"))
print(f"DATADIR {DATADIR}\nAPPDATADIR {APPDATADIR}\nVIDEOLIBDIR {VIDEOLIBDIR}")


def computeMetricsOnBenchmarks(run: Run, videoLibrary: VideoLibrary) -> Dict:

    # for every benchmark version, and Smoke and Flame
    metrics = dict()

    processedVideos = run.getProcessedVideos()
    
    for version in videoLibrary.benchmarkVersions():
        metrics[version] = dict()

        for library in videoLibrary.libraries():

            # videos in benchmark for this library
            benchmark = videoLibrary.data(version=version, library=library)
            
            gotAllFilesForBenchmark = all([video in processedVideos for video in benchmark.index])
            if gotAllFilesForBenchmark:

                # get ground truth for the benchmark videos
                gtColumn = 'gt'+library.capitalize()
                gt = benchmark[gtColumn]

                # get predictions for benchmark videos   
                predColumn = library.capitalize()+'Alarm'           
                if 'aal_fire' in run.algo.name:
                    predColumn = 'FireAlarm' 
                predictions = run.getStateCounts(benchmark.index)[predColumn]
                
                # get category of the benchmark videos 
                categoryColumn = 'category'
                categories = benchmark[categoryColumn]

                # compute metrics per category
                df = pd.concat([gt, predictions, categories], axis=1, ignore_index=False)
                metrics[version][library.lower()] = utils.computeMetricsPerCategory(df, gtColumn, predColumn, categoryColumn)
    
    return metrics

def loadDatabase():

    videoLibrary = VideoLibrary(os.path.join(VIDEOLIBDIR, "videoLibrary.xlsx")) 
    print(f"Imported videolibrary: {videoLibrary}")

    db = DataBase(os.path.join(APPDATADIR, "aab_data.pkl"))

    # Look for runs in DATADIR
    # Check which runs are new
    # and add them to database

    configFiles = Run.findConfigFiles(DATADIR)

    newRunIds = []
    for configFile in configFiles:
        with open(configFile, "r") as f:
            content = json.load(f)
            addToDataBase = (
                ('id' not in content) or
                (('id' in content) and (content['id'] not in db.getIds()))
            )
        if addToDataBase:
            run = Run.fromConfigFile(configFile)
            db.add(run)
            newRunIds.append(run.id)

    print(f"Found {len(configFiles)} runs in {DATADIR} of which {len(newRunIds)} are new.")

    # get metrics for new runs 

    for i, id in enumerate(newRunIds):
        run = db.getRun(id)

        print(f"Checking run {i+1}/{len(newRunIds)}: {run.dataDir}")
        
        if run.getMetrics() is None:           
            metrics = computeMetricsOnBenchmarks(run, videoLibrary)
            run.setMetrics(metrics)
            
            # print info
            for version, benchmark in metrics.items():
                for library in benchmark.keys():
                    print(f"Benchmarking {library} on version {version} succeeded.")

    print(f"Saving new runs")
    db.dump()
    print("Done!")

    return db

def loadVideoLibrary():
    return VideoLibrary(os.path.join(VIDEOLIBDIR, "videoLibrary.xlsx")) 

