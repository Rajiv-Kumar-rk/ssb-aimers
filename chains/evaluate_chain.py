from langchain_core.prompts import PromptTemplate
from PIL import Image
from schemas.reponseSchema import ExamineStoryResponseSchema
from langchain_adapter import GoogleGenerativeAIAdapter

prompt = """
Role: You are an experienced SSB Psychological Instructor responsible for assessing candidates’ Thematic Apperception Test (TAT) stories.

Your evaluation must not only assess Officer-Like Qualities (OLQs) but also ensure that the candidate’s story is contextually relevant to the given image.

Input:
1. Image Input: [Insert the image used for the story]
2. Candidate Story:
{candidate_story}
3. Available OLQs Reference:
   Officer Like Qualities (15 OLQs) Factors
   Factor – I (Planning and Organising)
     (a) Effective Intelligence
     (b) Reasoning Ability
     (c) Organising Ability
     (d) Power of Expression
   Factor – II (Social Adjustment)
     (e) Social Adaptability
     (f) Co-operation
     (g) Sense of Responsibility
   Factor – III (Social Effectiveness)
     (h) Initiative
     (i) Self Confidence
     (j) Speed of Decision
     (k) Ability to Influence the Group
     (l) Liveliness
   Factor – IV (Dynamic)
     (m) Determination
     (n) Courage
     (o) Stamina

Your Task:
Analyze the given image and candidate story to assess:
1. Story relevance to the image — how well the story aligns with the situation, theme, and objects seen in the picture.
2. The use of image elements — whether the distinct people, actions, and objects from the image are represented meaningfully in the story.
3. Adherence to SSB story-writing guidelines:
   - Logical sequence (past → present → future)
   - Positive, realistic, and Indian-context-based
   - No self-reference (“I”, “me”)
   - Clear protagonist (age, gender, motivation, and actions)
4. Reflection of OLQs through the main character’s behavior and thought process.
5. Grammar, coherence, and expression quality.

Evaluation Steps:
1. **Image Analysis** – Identify and list all distinct characters, objects, and key visual elements visible in the image (e.g., “two men, one bicycle, one injured person, a street, an ambulance”).
   
2. **Relevance Check** – Determine:
   - Whether the story contextually matches the main scene shown in the image.
   - If the main characters or setting of the image are represented.
   - Assign a Relevance Score (0–10) based on closeness of match.
   - If the story is not relevant, clearly mention: “❌ Story not relevant to image.”

3. **Object Utilization Mapping** – For each identified object/character/visual element, specify:
   - Whether it is represented or referenced in the story.
   - If missing, mention “not represented”.

   Example Table:
   | Image Element | Present in Story | Representation |
   |----------------|------------------|----------------|
   | Injured woman  | ✅ Yes | Helped by protagonist |
   | Bicycle        | ❌ No | Not mentioned |
   | Crowd          | ✅ Yes | Volunteers gathered |

4. **Story Rule Compliance Check** – Assess standard SSB parameters:
   - Logical structure (past–present–future)
   - Positive and realistic outcome
   - Clarity and coherence
   - Indian context maintained
   - Self-reference avoided

5. **Psychological and OLQ Analysis** – Examine protagonist’s traits and assign scores for all 15 OLQs (0–10 each) with a one-line justification.

6. **Narrative Feedback Summary** – Provide:
   - Key personality inference
   - OLQs strongly reflected
   - OLQs weakly reflected
   - Areas of improvement
   - Overall recommendation (Recommended / Needs Improvement)

Output Format:
- 🖼️ **Image Elements Identified:** [List of distinct objects/characters/settings]
- 🔗 **Image–Story Relevance:** 
  - Relevance Score: X/10
  - Verdict: Relevant / Partially Relevant / Not Relevant
  - Brief Justification
- 📋 **Object Utilization Table:**
  | Element | Present in Story | Representation |
  |----------|------------------|----------------|
- ✅ **Story Rule Compliance:** Pass/Fail (with short justification)
- 🧩 **OLQ Scoring Table (15 OLQs, each rated /10 with reason)**
- 🧠 **Psychological Summary (3–4 lines)**
- 🏅 **Overall Assessment Verdict:** Recommended / Needs Improvement

Ensure tone is professional, objective, and aligned with SSB Psychological Testing standards.
If the story is irrelevant to the image, highlight that clearly before proceeding with OLQ analysis.
"""

prompt_template = PromptTemplate(template=prompt, input_variables=["candidate_story"])


def examine_candidate_written_story(image_path, story_content=None):
    try:
        if  not image_path or not story_content:
            raise ValueError("Required args are not provided to 'examine_candidate_written_story'")

        formatted_prompt = prompt_template.format(candidate_story=story_content)

        image = Image.open(image_path)
        adapter = GoogleGenerativeAIAdapter(model="gemini-2.5-flash")
        res = adapter.generate_and_parse(formatted_prompt, image, ExamineStoryResponseSchema)

        return res
    except Exception as e:
        print(f"ERROR:// error occured in 'examine_candidate_written_story' and error: {str(e)}")
        return None
