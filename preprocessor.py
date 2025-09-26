import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def process_posts(raw_file_path, processed_file_path):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)

        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags_mapping = get_unified_tags(enriched_posts)
    for epost in enriched_posts:
        current_tags = epost['tags']
        new_tags = {unified_tags_mapping[tag] for tag in current_tags}
        epost['tags'] = list(new_tags)

    with open(processed_file_path, 'w', encoding='utf-8') as output:
        json.dump(enriched_posts, output, indent=4)

def get_unified_tags(post_with_metadata):
    unique_tags = set()
    for post in post_with_metadata:
        unique_tags.update(post['tags'])
    
    unique_tag_list = ','.join(unique_tags)
    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tag_list)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except:
        raise OutputParserException("Failed to parse the output as JSON.")  
    return res

def extract_metadata(post):
    template = '''You are given a LinkedIn post. Extract the line Count, Identify the language of the post, Suggest relevant tags based on the content of the post.
    1. Return a valid json object. No preamble.
    2. Json object should have keys: line_count, language, tags.
    3. line_count should be an integer.
    4. language should be a string.
    5. tags should be an array of text tags of size not more than 4.
    6. tags should be relevant to the content of the post.
    7. Language should be English and Hinglish.
    8. Return ONLY a single valid JSON object.
    9. Always return a valid json object. Never return blank or empty response.


    Here ia an actual post on which you need to perform the above task:
    {post}'''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post})
    
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except:
        raise OutputParserException("Failed to parse the output as JSON.")
    return res

if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")