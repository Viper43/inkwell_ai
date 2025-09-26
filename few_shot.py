import json
import pandas as pd

class FewShotPost:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)
        
    def load_posts(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            posts = json.load(f)
            df= pd.json_normalize(posts)
            self.df = df

        self.df['length_category'] = pd.cut(self.df['line_count'], bins=[1,5,10,20,float('inf')], labels=['short', 'medium', 'long', 'very long'])
        all_tags = self.df['tags'].sum()
        self.unique_tags = list(set(all_tags))
        
    def get_filtered_posts(self, length_category=None, tag=None, language=None):
        filtered_df = self.df[
            (self.df['language'] == language) &
            (self.df['length_category'] == length_category) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]
        
        return filtered_df.to_dict(orient='records')
    
    def get_unique_tags(self):
        return self.unique_tags

if __name__ == "__main__":
    fs = FewShotPost()
    posts = fs.get_filtered_posts(length_category='long', tag='Motivation', language='English')
    print(posts)

