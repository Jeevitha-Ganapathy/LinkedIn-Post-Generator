import json
import re
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def clean_text(text):
    """
    Removes characters that cannot be encoded in UTF-8 (like broken emojis or surrogates).
    """
    return text.encode("utf-8", "ignore").decode("utf-8")


def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []

        for post in posts:
            try:
                cleaned_text = clean_text(post['text'])
                metadata = extract_metadata(cleaned_text)
                post_with_metadata = post | metadata
                enriched_posts.append(post_with_metadata)
            except Exception as e:
                print(f"Skipping post due to error: {e}")
                continue

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post.get('tags', [])
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)

    if processed_file_path:
        with open(processed_file_path, mode="w", encoding='utf-8') as outfile:
            json.dump(enriched_posts, outfile, indent=4, ensure_ascii=False)


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)

    Here is the actual post on which you need to perform this task:  
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post})

    match = re.search(r"\{.*\}", response.content, re.DOTALL)
    if not match:
        raise OutputParserException("No JSON found in LLM output.")

    clean_json = match.group()
    try:
        return json.loads(clean_json)
    except json.JSONDecodeError:
        raise OutputParserException("Malformed JSON or context too big.")


def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post.get('tags', []))

    unique_tags_list = ','.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements:
    1. Tags are unified and merged to create a shorter list. 
    2. Each tag should follow title case. 
    3. Output should be a JSON object only, no explanation, no extra text.
    4. Keys are original tags, values are unified tags.

    List of tags:
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": unique_tags_list})

    # Manual JSON extraction (instead of using JsonOutputParser)
    match = re.search(r"\{.*\}", response.content, re.DOTALL)
    if not match:
        raise OutputParserException("No valid JSON found in LLM response for tag unification.")

    json_string = match.group()
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        raise OutputParserException("Malformed JSON in unified tags output.")


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")
