class AllTMAnalyzer:
    
    def __init__(self, data):
        
        from pandas import to_datetime, DateOffset
        
        self.original_data = data
        self.data = data
        
    def avg_headcount(self, start, end, get_headcounts=False):

        '''
        Calculates the average headcount for the specified period.

        -------------

        Arguments:

        start - a date-like string in any major format, e.g. January 1, 2021; 1/1/2021; 2021/1/1 (required input)
        end - a date-like string in any major format, e.g. January 1, 2021; 1/1/2021; 2021/1/1 (required input)
        get_headcounts - boolean, change to True if you'd like to also receive the starting and ending headcount figures.

        -------------

        Returns:

        average headcount - the average of the two headcount figures.
        **
        starting_headcount - returns if get_headcounts=True.  The headcount for the starting date.
        ending_headcount - returns if get_headcounts=True.  The headcount for the ending date.

        '''

        start = to_datetime(start)
        end = to_datetime(end)

        start_headcount = self.data[(self.data['HD'] <= start) & ((self.data['TD'] > start) | (self.data['Active Status'] == 'Yes'))].shape[0]
        end_headcount = self.data[(self.data['HD'] <= end) & ((self.data['TD'] > end) | (self.data['Active Status'] == 'Yes'))].shape[0]

        if get_headcounts:
            return (start_headcount + end_headcount) / 2, start_headcount, end_headcount

        return (start_headcount + end_headcount) / 2

    def all_terms(self, start, end):

        '''
        Retrieves the number of terminations, regardless of type, for the specified range.

        -------------

        Arguments:

        start - a date-like string in any major format, e.g. January 1, 2021; 1/1/2021; 2021/1/1 (required input)
        end - a date-like string in any major format, e.g. January 1, 2021; 1/1/2021; 2021/1/1 (required input)

        -------------

        Returns:

        terminations - the termination count for the date range

        '''

        start = to_datetime(start)
        end = to_datetime(end)

        terminations = self.data[(self.data['TD'] >= start) & (self.data['TD'] <= end)].shape[0]

        return terminations

    def voluntary_terms(self, start, end):

        '''
        Retrieves the number of voluntary terminations for the specified range.

        -------------

        Arguments:

        start - a date-like string in any major format, e.g. January 1, 2021; 1/1/2021; 2021/1/1 (required input)
        end - a date-like string in any major format, e.g. January 1, 2021; 1/1/2021; 2021/1/1 (required input)

        -------------

        Returns:

        terminations - the termination count for the date range

        '''

        start = to_datetime(start)
        end = to_datetime(end)

        vol_terminations = self.data[(self.data['TD'] >= start) & (self.data['TD'] <= end) & (self.data['Termination Category'].fillna('').str.contains('Voluntary'))].shape[0]

        return vol_terminations

    def involuntary_terms(self, start, end):

        '''
        Retrieves the number of involuntary terminations for the specified range.

        -------------

        Arguments:

        start - a date-like string in any major format, e.g. January 1, 2021; 1/1/2021; 2021/1/1 (required input)
        end - a date-like string in any major format, e.g. January 1, 2021; 1/1/2021; 2021/1/1 (required input)
        get_terms - boolean, change to True if you'd like to also receive the termination figures.

        -------------

        Returns:

        terminations - the termination count for the date range

        '''

        start = to_datetime(start)
        end = to_datetime(end)

        invol_terminations = self.data[(self.data['TD'] >= start) & (self.data['TD'] <= end) & (self.data['Termination Category'].fillna('').str.contains('Involuntary'))].shape[0]

        return invol_terminations  

    def turnover_rate(self, start, end, term_type='all'):

        start = to_datetime(start)
        end = to_datetime(end)    

        hc = self.avg_headcount(start, end)

        if str.lower(term_type) == 'all':
            terms = self.all_terms(start, end)
        elif str.lower(term_type) == 'voluntary':
            terms = self.voluntary_terms(start, end)
        elif str.lower(term_type) == 'involuntary':
            terms = self.involuntary_terms(start, end)
        else:
            raise ValueError('Please specify a valid termination type: All, Voluntary, Involuntary')

        return terms / hc
    
class SurveyAnalyzer:
    
    import numpy as np
    import pandas as pd
    
    def __init__(self, data):
        self.original_data = data
        self.data = data
        
    def create_construct(self, items, group='all', name='Construct'):
        group_items = ['emp_id'] + items
        
        if group == 'tm':
            construct_score = df[group_items].set_index('emp_id').mean(axis=1).reset_index().rename(columns={0:name})
        elif group == 'all':
            construct_score = df[items].mean()
        else:
            raise ValueError("Please supply a valid grouping type - 'tm' for per-TM construct scores, 'all' for aggregate scores for the data.")
            
        return(construct_score)
        
        