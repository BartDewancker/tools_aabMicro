import numpy as np
import pandas as pd 

def computeMetrics(gt, pred):

    out = dict()
    out['tp'] = sum(np.logical_and(gt, pred))
    out['tn'] = sum(np.logical_and(np.logical_not(gt), np.logical_not(pred)))
    out['fp'] = sum(np.logical_and(np.logical_not(gt), pred))
    out['fn'] = sum(np.logical_and(gt, np.logical_not(pred)))

    out['total_true'] = sum(gt)
    out['total_false'] = sum(gt == False)
    out['total_positive'] = sum(pred)
    out['total_negative'] = sum(pred == False)
    
    out['precision'] = np.NaN
    if out['total_positive'] > 0:
        out['precision'] = float(out['tp']) / out['total_positive']

    out['recall'] = np.NaN
    if out['total_true'] > 0:
        out['recall'] = float(out['tp']) / out['total_true']

    out['tpr'] = out['recall'] 

    out['fpr'] = np.NaN
    if out['total_false'] > 0:
        out['fpr'] = float(out['fp']) / out['total_false']

    out['accuracy'] = np.NaN
    if (out['total_true'] + out['total_false']) > 0:
        out['accuracy'] = float(out['tp'] + out['tn']) / (out['total_true'] + out['total_false'])
   
    return out

def computeMetricsPerCategory(df, gtColumn, predColumn, categoryColumn):
    rows = []
    
    # Metrics for category == 'allCategories'
    row = {}
    row['category'] = 'allCategories'
    row['category_gt'] = False
    gt = df[gtColumn] 
    pred = df[predColumn] > 0 # column 'FlameAlarm' or 'SmokeAlarm'
    row = {**row, **computeMetrics(gt, pred)}
    rows.append(row)

    # metrics per category
    for cat, data in df.groupby(categoryColumn):
        row = {}
        row['category'] = cat
        row['category_gt'] =  data[gtColumn].max() 
        gt = data[gtColumn] # column 'flame' or column 'smoke'
        pred = data[predColumn] > 0 # column 'FlameAlarm' or 'SmokeAlarm'
        row = {**row, **computeMetrics(gt, pred)}
        rows.append(row)
    
    return pd.DataFrame(rows)
