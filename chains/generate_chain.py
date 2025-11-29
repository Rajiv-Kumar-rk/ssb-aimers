from langchain_core.prompts import PromptTemplate
from PIL import Image
from schemas.reponseSchema import ExamineSuggestedStoryResponseSchema
from langchain_adapter import GoogleGenerativeAIAdapter

# We'll keep the original prompt text here for the generation flow.
prompt = """
Role: You are an experienced SSB Psychological Instructor and TAT Evaluator. 
You are responsible for both generating a high-quality TAT story based on an image 
and evaluating that story on all Officer-Like Qualities (OLQs) and SSB parameters.

Your dual-task process includes:

---

### 🩵 Phase 1: Story Generation
Generate an original, realistic, and positive TAT story based **solely on the given image**.

**Story Writing Guidelines:**
- Create a clear protagonist (mention age, gender, role, and motivation).
- Maintain logical sequence: past → present → future.
- Keep the context **realistic, Indian, and relatable** (avoid over-dramatization).
- Reflect positive attitude, leadership, and practical problem-solving.
- Avoid self-reference (“I” or “me”).
- Limit story to ~120–150 words.

---

### 💼 Phase 2: Story Evaluation
After generating the story, evaluate it using the same standards as in a real SSB Psychological Test.

Input:
1. Image Input: [Insert the image used for the story]
2. Generated Story: [The story you just wrote]
3. OLQs Reference (15 OLQs):

   **Factor – I (Planning and Organising)**
   - (a) Effective Intelligence
   - (b) Reasoning Ability
   - (c) Organising Ability
   - (d) Power of Expression

   **Factor – II (Social Adjustment)**
   - (e) Social Adaptability
   - (f) Co-operation
   - (g) Sense of Responsibility

   **Factor – III (Social Effectiveness)**
   - (h) Initiative
   - (i) Self Confidence
   - (j) Speed of Decision
   - (k) Ability to Influence the Group
   - (l) Liveliness

   **Factor – IV (Dynamic)**
   - (m) Determination
   - (n) Courage
   - (o) Stamina

---

### Evaluation Steps

1. **Image Analysis**
   - Identify and list distinct characters, objects, and setting elements visible in the image.
   - Example: “Two men, a bicycle, one injured person, a tree, a road.”

2. **Relevance Check**
   - Determine if the story contextually matches the main scene.
   - If not, clearly mention “❌ Story not relevant to image.”
   - Provide:
     - Relevance Score (0–10)
     - Verdict (Relevant / Partially Relevant / Not Relevant)
     - Short justification

3. **Object Utilization Mapping**
   For each identified image element, indicate:
   - Whether it appears in the story.
   - Its representation (if present) or “Not represented” (if absent).

   Example:
   | Image Element | Present in Story | Representation |
   |----------------|------------------|----------------|
   | Injured person | ✅ Yes | Helped by protagonist |
   | Bicycle        | ❌ No | Not mentioned |

4. **Story Rule Compliance**
   Check for:
   - Logical flow (past–present–future)
   - Positive and realistic resolution
   - Indian social context
   - Coherence and clarity
   - No self-reference

   Output as Pass/Fail with justification.

5. **OLQ Scoring**
   Assign scores (0–10) for each of the 15 OLQs.
   Include a one-line justification for each.

6. **Psychological Summary**
   Summarize:
   - Key personality inference
   - OLQs strongly reflected
   - OLQs weakly reflected
   - Areas needing improvement
   - Overall verdict (Recommended / Needs Improvement)

---

### Output Format

**🪶 Generated Story:**
[Full generated story text]

**🖼️ Image Elements Identified:**
[List of distinct objects/characters/settings]

**🔗 Image–Story Relevance:**
- Relevance Score: X/10
- Verdict: Relevant / Partially Relevant / Not Relevant
- Brief Justification

**📋 Object Utilization Table:**
| Element | Present in Story | Representation |
|----------|------------------|----------------|
| ... | ... | ... |

**✅ Story Rule Compliance:** Pass/Fail (with justification)

**🧩 OLQ Scoring Table (15 OLQs with /10 scores and justification)**

**🧠 Psychological Summary (3–4 lines)**

**🏅 Overall Assessment Verdict:** Recommended / Needs Improvement

---

Ensure:
- Tone remains professional, objective, and aligned with SSB standards.
- Story is original and coherent.
- All JSON-friendly fields remain properly structured for later use in APIs or UI rendering.
"""

# Using a LangChain PromptTemplate for clearer templating (no direct LLM call here).
prompt_template = PromptTemplate(template=prompt, input_variables=[])


def generate_image_story(image_path, input_prompt=None):
    """Generate a suggested story and evaluation for the provided image."""
    try:
        if not image_path:
            raise ValueError("Required args are not provided to 'generate_image_story'")

        image = Image.open(image_path)

        # Use the PromptTemplate to render the prompt (no variables in this template).
        formatted_prompt = prompt_template.format()

        adapter = GoogleGenerativeAIAdapter(model="gemini-2.5-flash")
        res = adapter.generate_and_parse(formatted_prompt, image, ExamineSuggestedStoryResponseSchema)

        return res
    except Exception as e:
        print(f"ERROR:// error occured in 'generate_image_story' and error: {str(e)}")
        return None
