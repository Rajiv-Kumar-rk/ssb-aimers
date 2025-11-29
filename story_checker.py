from chains.evaluate_chain import examine_candidate_written_story as examine_candidate_written_story_chain


# Thin wrapper to keep API backward-compatible with existing imports
def examine_candidate_written_story(client, image_path, story_content=None):
	return examine_candidate_written_story_chain(client, image_path, story_content)

