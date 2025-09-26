from llm_helper import llm
from few_shot import FewShotPost

few_shot_generation = FewShotPost()

def get_length_of_post(length_category):
    if length_category == 'short':
        return "1 to 5 lines"
    if length_category == 'medium':
        return "5 to 10 lines"
    if length_category == 'long':
        return "10 to 30 lines"
    if length_category == 'very long':
        return "more than 30 lines"
    
def generate_post(length_category, tag, language):
    prompt = get_prompt(length_category, tag, language)
    response = llm.invoke(prompt)
    return response.content

def get_prompt(length_category, tag, language):
    str_length = get_length_of_post(length_category)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {str_length}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

    examples = few_shot_generation.get_filtered_posts(length_category, tag, language)

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f"\n\nExample {i+1}: \n\n{post_text}\n"

    return prompt


if __name__ == "__main__":
    print(generate_post('long', 'Motivation', 'English'))