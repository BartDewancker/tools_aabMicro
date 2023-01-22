
# %%
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
import uuid
import os
import glob
import json
import uuid
import xml.etree.ElementTree as ET 
import pandas as pd
from AraaniProtocol import getStateMessageCount
import inspect

def generateUUID():
    return str(uuid.uuid1())

@dataclass
class Algo():
    name: str
    build_type: str
    version: str
    type = None

    @classmethod
    def from_dict(cls, env):      
        return cls(**{
            k: v for k, v in env.items() 
            if k in inspect.signature(cls).parameters
        })

    def __post_init__(self):
        self.type = f"{self.name}_{self.build_type}"

@dataclass
class Run():
    algo: Algo
    dataDir: str # path to VideoLibrary directory
    xmlSettings: Optional[str]=None # settings as xml-formatted string 
    id: Optional[str] = field(default_factory=generateUUID) # automatically generated if not supplied
    stateMessages = ['Flame Alarm', 'Smoke Alarm', 'Fire Alarm', 'Fault Signal', 'Supervisory Signal', 'Operational Signal']

    _settings: Union[Dict, None] = None
    _avpaTaskSettings: Union[Dict, None] = None
    _stateCounts: Union[pd.DataFrame, None] = None
    _metrics: Union[Dict, None] = None

    def __post_init__(self):
        self.__loadSettings()
        self.__loadStateCounts()

    @classmethod
    def fromConfigFile(cls, configFile: str):      
        parentDir = os.path.dirname(configFile)
        dataDir = os.path.join(parentDir, 'VideoLibrary')
        if not os.path.exists(dataDir):
            raise ValueError("Directory of configFile does not contain a VideoLibrary directory.")
        
        with open(configFile) as f:
            content = json.load(f)

            # create Algo object from content
            algo = Algo.from_dict(content['algo'])

            # create id if there isn't one yet
            if 'id' in content:
                id = content['id']
            else:
                id = generateUUID()

            # load settings if present
            if ('settings' in content['algo']) and len(content['algo']['settings']):
                xmlSettings = content['algo']['settings']
            else: 
                xmlSettings = None
        
        # update configFile with 'id'
        with open(configFile, 'w') as f:
            content['id'] = id
            json.dump(content, f)

        # create Run object
        return cls(
            algo=algo, 
            dataDir=dataDir, 
            id=id, 
            xmlSettings=xmlSettings)

    def getSettings(self) -> Dict:
        return self._settings

    def getStateCounts(self, videos: List[str]=None) -> pd.DataFrame:
        if videos is None:
            return self._stateCounts
        else: 
            return self._stateCounts.loc[videos]

    def getProtocolFiles(self) -> List:
        return glob.glob(
            os.path.join(self.dataDir, "**/*.xml"), 
            recursive=True)

    def getAVPAFiles(self) -> List:
        return glob.glob(
            os.path.join(self.dataDir,"**/*-avpa_task_settings.json"), 
            recursive=True)

    def getVideoRoot(self, protocolFile) -> str:
        """
        Get video root of a protocol file.
        The video root  is relative to dataDir without extension.
        So that "PathToVideoLibrary + video + .mp4" is the absolute path to the video.
        
        For example:  
        the video root of protocol file  
        ```
        'D:\\aabData\\aal_flame_standard_E4.0.10_flame_default\\VideoLibrary\\02. Flame\\01. Flame\\1__F_20170927_132504_4eb2-1-1-11-57\\1__F_20170927_132504_4eb2-1-1-11-57.xml'
        ``` 
        is 
        ```
        '02. Flame/01. Flame/1__F_20170927_132504_4eb2-1-1-11-57'
        ```.

        """
        relPath = os.path.relpath(protocolFile, self.dataDir)
        noExtPath = os.path.splitext(relPath)[0]
        dir, filename = os.path.split(noExtPath)
        # directory name same as filename?
        if os.path.split(dir)[1] == filename:
            videoRoot = dir
        else:
            videoRoot = os.path.join(dir, filename)
        videoRoot = videoRoot.replace(os.sep, "/")
        return videoRoot

    def getProcessedVideos(self) -> List:
        """ 
        Get all videos for which a protocol file is available.
        """
        return [self.getVideoRoot(protocolFile)+'.mp4' for protocolFile in self.getProtocolFiles()]

    def getMetrics(self):
        return self._metrics 

    def setMetrics(self, metrics):
        self._metrics = metrics

    @staticmethod
    def findConfigFiles(directory, configFilename="aab_config.json") -> List:
        return glob.glob(directory + f"/*/{configFilename}", recursive=True)

    def __xmlSettingsToDict(self, xmlSettings):
        settings = {}
        configElement = ET.fromstring(xmlSettings).find('Configuration')
        for algo in list(configElement):
            settings[algo.tag] = algo.attrib
        return settings
    
    def __sameSettingsInAllAvpaFiles(self, avpaFiles):
        """
        Check all avpa files have the same algo settings.
        """
        settings = list()
        for avpaFile in avpaFiles:
            with open(avpaFile) as f:
                avpaData = json.load(f)
            configElement = ET.fromstring(avpaData['task']['settingsFileContent']).find('Configuration')
            setting = {}
            for subAlgo in list(configElement):
                algoSettings = {subAlgo.tag+k:v for k,v in subAlgo.attrib.items()}
                setting = {**setting, **algoSettings}
            settings.append(setting)

        allTheSame = settings.count(settings[0]) == len(settings)
        return allTheSame

    def __loadSettings(self) -> None:
        self._settings = None
        if self.xmlSettings is not None:
            # load settings from supplies xmlSettings string
            self._settings = self.__xmlSettingsToDict(self.xmlSettings)
        else:
            # Load settings from avpa files
            # check all avpa files contain the same settings
            avpaFiles = self.getAVPAFiles()
            if len(avpaFiles) and self.__sameSettingsInAllAvpaFiles(avpaFiles):
                # pick the first
                with open(avpaFiles[0]) as f:
                    avpaData = json.load(f)
                self._avpaTaskSettings = avpaData
                self._settings = self.__xmlSettingsToDict(avpaData['task']['settingsFileContent'])
        
        if self._settings is not None:
            # replace "Flame" and "Smoke" by "FlameAlarm" and "SmokeAlarm" in settings
            if 'Flame' in self._settings:
                self._settings['FlameAlarm'] = self._settings.pop('Flame')
            if 'Smoke' in self._settings:
                self._settings['SmokeAlarm'] = self._settings.pop('Smoke')

    def __loadStateCounts(self):
        """
        Read the protocol files and count the state messages.
        Store the result as a dataframe, indexed by videoPath.
        """
        rows = []
        for protocolFile in self.getProtocolFiles():
            video = self.getVideoRoot(protocolFile) + '.mp4'
            row = {'videoPath': video}
            
            # add state message count
            for state in self.stateMessages:
                # remove white space in state message string
                row[state.replace(" ","")] = getStateMessageCount(protocolFile, state)
            
            rows.append(row)
        df = pd.DataFrame(rows)
        df = df.set_index('videoPath', drop=True)
        self._stateCounts = df


#%%
# run = Run.fromConfigFile(r"D:\aabData\aal_flame_standard_E4.0.10_flame_default\aab_config.json")
# run.getStateCounts().head()

# # %%
# run.getSettings()
# algo = Algo(name="aal_fire", build_type="standard", version="v3.3.2")
# r = Run(algo=algo, dataDir=r"D:\aabData\aal_flame_standard_E4.0.10_flame_default\VideoLibrary")

# # %%
# algo = Algo(name="aal_fire", build_type="standard", version="v3.3.2")
# r = Run(id="some-id", algo=algo, dataDir=r"D:\aabData\aal_flame_standard_E4.0.10_flame_default\VideoLibrary")

# configFile = r"D:\aabData\aal_flame_standard_E4.0.10_flame_default\aab_config.json"
# with open(configFile) as f:
#     content = json.load(f)

# r.getSettings()
# %%

# env = {"name":"aal_flame", "build_type":"standard", "version":"E4.0.1", "type": "something"}
# algo = Algo.from_dict(env)
# print(algo)
# %%
