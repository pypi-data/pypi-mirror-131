import os
import json
import logging
from collections import defaultdict
from datetime import datetime, date, timedelta
from dateutil import parser as dateparser
import pandas as pd

from enrichsdk import Compute, S3Mixin, CheckpointMixin

logger = logging.getLogger("app")

__all__ = ['FeaturesetExtractorBase',
           'FeatureComputeBase', 'note']

def note(df, title):
    msg = title + "\n"
    msg += "--------" + "\n"
    msg += "Timestamp: " + str(datetime.now()) + "\n"
    msg += "\nShape: "+ str(df.shape) + "\n"
    msg += "\nColumns: " + ", ".join(df.columns) + "\n"
    if len(df) > 0:
        msg += "\nSample:" + "\n"
        msg += df.sample(min(2, len(df))).T.to_string() + "\n" + "\n"
    msg += "\nDtypes" + "\n"
    msg += df.dtypes.to_string() + "\n"
    msg += "------" + "\n"
    return msg


class FeaturesetExtractorBase:
    """
    Base class for a feature set extractor.
    """

    def get_extractors(self):
        return []

    def get_specs(self):
        return []

    def one_record(self, data):
        """
        It is assumed that this will be called arbitrary number of times. 
        """
        allfeatures = []

        extractors = self.get_extractors()
        specs = self.get_specs()
        for spec in specs:

            extractor = spec.get('extractor', 'default')
            extractor = extractors[extractor]

            if isinstance(spec['keys'], list):
                for key in spec['keys']:
                    if key not in data:
                        continue
                    features = extractor.extract(key, data)
                    allfeatures.extend(features)
            elif isinstance(spec['keys'], dict):
                for name, key in spec['keys'].items():
                    features = extractor.extract(name, data, key)
                    allfeatures.extend(features)

        return allfeatures

    def collate(self, features):
        """
        Combine a list of dictionaries into a dataframe
        """
        return pd.DataFrame(features)
    
    def clean(self, df):
        """
        All the records are combined into a dataframe. Clean 
        that dataframe.
        """
        return df

    def finalize(self, df, computed):
        """
        Take this dataframe along with others and generate a 
        """
        return df

    def document(self, df):
        """
        Document the profile
        """
        return note(df, getattr(self, 'name', self.__class__.__name__))
                    
class FeatureComputeBase(Compute):
    """
    A built-in transform baseclass to handle standard feature 
    computation and reduce the duplication of code.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "FeatureComputeBase"
        self._environ = os.environ.copy()

    @classmethod
    def instantiable(cls):
        return False

    def get_featureset_extractors(self):
        raise Exception("Implement in subclass")
        
    def process(self, state):
        """
        Run the computation and update the state
        """
        logger.debug("Start execution",
                     extra=self.config.get_extra({
                         'transform': self.name
                     }))

        self.state = state

        # What
        featureset_extractors = self.get_featureset_extractors()
        
        featuresets = defaultdict(list)

        # Go through all the available files
        root = self.args['root']
        files = os.listdir(root)
        counts = defaultdict(int)
        for f in files:
            try:
                counts['files_total'] += 1
                try:
                    filename = os.path.join(root, f)
                    data = json.load(open(filename))
                    if isinstance(data, dict):
                        data = [data]
                except:
                    counts['files_error'] += 1
                    continue

                for index, d in enumerate(data):
                    try:
                        counts['records_total'] += 1
                        if ((not isinstance(d, dict)) or (len(d) == 0)):
                            logger.error("Empty or invalid data",
                                         extra={
                                             'transform': self.name,
                                             'data': str(d)[:100]
                                         })
                            counts['records_error_invalid'] += 1
                            continue

                        if (('data' not in d) or not isinstance(d['data'], str)):
                            logger.error("Invalid 'data' element",
                                         extra={
                                             'transform': self.name,
                                             'data': str(d['data'])[:100]
                                         })
                            counts['records_error_missing'] += 1
                            continue

                        data = eval(d['data'])

                        # Compute various feature sets for each patient
                        for detail in featureset_extractors:
                            try:
                                extractor = detail['extractor']
                                name       = detail['name']
                                
                                features = extractor.one_record(data)

                                # Skip if no features are being generated
                                if features is None:
                                    continue 
                                
                                if isinstance(features, dict):
                                    features = [features]
                                featuresets[name].extend(features)
                            except:
                                counts[f'extractor_{name}_exception'] += 1
                                if counts[f'extractor_{name}_exception'] == 1:
                                    logger.exception("Unable to process:{name}",
                                                     extra={
                                                         'transform': self.name
                                                     })
                    except:
                        # Handle exceptions in individual records
                        counts['records_error_exception'] += 1
                        logger.exception(f"Error in processing {index}",
                                         extra={
                                             'transform': self.name,
                                             'data': str(d)[:200]
                                         })

                counts['files_valid'] += 1
            except:
                # Handle exceptions in individual records
                counts['files_error_exception'] += 1
                logger.exception(f"Error in processing file",
                                         extra={
                                             'transform': self.name,
                                             'data': f
                                         })

        logger.debug("Completed reading files",
                     extra={
                         'transform': self.name,
                         'data': json.dumps(counts, indent=4)
                     })

        # Now collect all features of all patient
        computed = {}
        for detail in featureset_extractors:

            name = detail['name']
            extractor = detail['extractor']
    
            if ((name not in featuresets) or
                (featuresets[name] is None)):
                logger.warning(f"Features missing: {name}",
                             extra={
                                 'transform': self.name
                             })
                continue

            # Collect all the features into a dataframe..
            df = extractor.collate(featuresets[name])

            # Clean the dataframe generated.
            df = extractor.clean(df)

            computed[name] = df

        # Now we have individual dataframes. May be the extractor
        # wants to compute some more. 
        final = {}
        for detail in featureset_extractors:
            name = detail['name']
            extractor = detail['extractor']
            df = computed.get(name, None)
            df = extractor.finalize(df, computed)
            final[name] = df
            
        # note them
        for detail in featureset_extractors:
            name = detail['name']        
            extractor = detail['extractor']
            df = final[name]
            logger.debug(f"Featureset: {name}_features",
                         extra={
                             'transform': self.name,
                             "data": extractor.document(df)
                         })

            self.update_frame(name + "_features",
                              "Features of patient across all encounters",
                              df, files[0])

        logger.debug("Complete execution",
                     extra=self.config.get_extra({
                         'transform': self.name
                     }))

        ###########################################
        # => Return
        ###########################################
        return state

    def validate_results(self, what, state):
        """
        Check to make sure that the execution completed correctly
        """
        pass
