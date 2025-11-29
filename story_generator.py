from chains.generate_chain import generate_image_story as generate_image_story_chain

# Thin wrapper to keep API backward-compatible with existing imports
def generate_image_story(image_path, input_prompt=None):
    return generate_image_story_chain(image_path, input_prompt)
    