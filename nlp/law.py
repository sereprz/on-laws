import re
import pandas as pd


class Law:
    '''
        Represents laws from https://www.ontario.ca
    '''
    BASEURL = 'https://www.ontario.ca'

    def __init__(self, name, url, content):

        self.name = name
        self.url = f'{self.BASEURL}{url}'
        self.content_raw = content
        self.table_of_content = self.make_table_of_contents()

    def make_table_of_contents(self):
        '''
            Returns the table of content based on the titles of level 1, 2, and 3
        '''
        
        titles = [(c['id'], c['level1'], c['level2'], c['level3'])
                  for c in self.content_raw]
        
        tbl_of_content = pd.DataFrame(titles,
            columns=['cid', 'level1', 'level2', 'level3']
        ).drop_duplicates(subset=['level1', 'level2', 'level3']
        ).reset_index(drop=True).sort_values(by='cid')

        return tbl_of_content[['level1', 'level2', 'level3']].to_dict('index')
    
    def get_section(self, section_id):
        '''
            Returns the text for section {section_id}

            :param section_id: int, section id
        '''

        try:
            level1, level2, level3 = self.table_of_content[section_id].values()
        except KeyError:
            print(f'Invalid id. The max id is {max(self.table_of_content.keys())}')
        
        text = ' '.join([c['norm'] for c in self.content_raw
                             if c['level1'] == level1 and
                             c['level2'] == level2 and
                             c['level3'] == level3])

        return re.sub(r'Ref\d+\.?', '', text).strip()
        
    def get_all_sections(self):
        '''
            Returns a dictionary with the text of all sections
        '''
        
        return dict([(i, self.get_section(i)) for i in self.table_of_content])
    
    def get_full_text(self):
        '''
            Get the full text of the law
        '''
        sections = self.get_all_sections()
        return ' '.join(sections.values())
        