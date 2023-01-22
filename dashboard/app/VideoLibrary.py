# %%
import pandas as pd
from typing import List

class VideoLibrary:
    def __init__(self, excelFile):
        self.excelFile = excelFile
        self.df = pd.read_excel(self.excelFile)

        assert('videoPath' in self.df.columns)
        assert('library' in self.df.columns)

        self.df = self.df.set_index('videoPath', drop=True)

    def data(self, version=None, library=None, category=None) -> pd.DataFrame:
        subset = self.df
        if (version is not None):
            print("version: {version}")
            subset = subset[subset[version]]
        if (library is not None) and (not subset.empty):
            subset = subset[subset['library']==library]
        if (category is not None) and (not subset.empty):
            subset = subset[subset['category']==category]
        return subset

    def videos(self, version=None, library=None, category=None) -> List[str]:
        return list(self.data(version, library, category).index)

    def categories(self, version=None, library=None) -> List[str]:
         return list(self.data(version, library)['category'].unique())

    def libraries(self) -> List[str]:
        return list(self.df['library'].unique())

    def benchmarkVersions(self) -> List[str]:
        benchmarkVersions = list(
            filter(
                lambda c: 
                    (c[0].lower()=='v') and 
                    (c[1] in [str(num) for num in range(10)]), 
                list(self.df.columns)
            )
        )
        return benchmarkVersions
    
    def __str__(self):
        return f"VideoLibrary with columns {self.columns} containing {self.size} videos"
        
    @property
    def columns(self) -> List[str]:
        return list(self.df.columns)

    @property
    def size(self) -> int:
        return len(self.df)

# %%
# import os
# VIDEOLIBDIR = os.path.realpath(os.getenv("AAB_VIDEOLIBRARY", r"D:/VideoLibrary"))
# videoLibrary = VideoLibrary(os.path.join(VIDEOLIBDIR, "videoLibrary.xlsx")) 
# print(videoLibrary)

# %%
