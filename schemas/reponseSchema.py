from pydantic import BaseModel, Field
from typing import List, Optional


# Individual OLQ trait (Factor-based)
class OLQTraitResponseSchema(BaseModel):
    name: str = Field(..., description="Name of the Officer Like Quality trait")
    score: int = Field(..., ge=0, le=10, description="Score assigned out of 10")
    justification: str = Field(..., description="Reason for the assigned score")


# Object or character presence mapping from image → story
class ObjectUtilizationSchema(BaseModel):
    element: str = Field(..., description="Distinct object or character from the image")
    present_in_story: bool = Field(..., description="Whether the element appears in the story")
    representation: Optional[str] = Field(None, description="How the element is represented in the story")


# Image-to-story relevance section
class ImageRelevanceSchema(BaseModel):
    identified_elements: List[str] = Field(..., description="List of distinct characters/objects/settings found in the image")
    relevance_score: int = Field(..., ge=0, le=10, description="How closely the story matches the image")
    verdict: str = Field(..., description="Relevance verdict: Relevant / Partially Relevant / Not Relevant")
    justification: str = Field(..., description="Reason behind the relevance verdict")
    object_utilization_table: List[ObjectUtilizationSchema] = Field(..., description="Mapping of each identified element to story usage")


# Story rule compliance result
class StoryComplianceSchema(BaseModel):
    passed: bool = Field(..., description="Whether the story meets SSB writing standards")
    justification: str = Field(..., description="Brief justification for the compliance verdict")


# Final psychological and evaluation summary
class PsychologicalSummarySchema(BaseModel):
    mindset_summary: str = Field(..., description="Short 3–4 line summary of the candidate's mindset and behavior")
    strengths: List[str] = Field(..., description="OLQs strongly reflected")
    weaknesses: List[str] = Field(..., description="OLQs weakly reflected or needing improvement")
    areas_of_improvement: List[str] = Field(..., description="Development areas")
    final_verdict: str = Field(..., description="Overall assessment verdict: Recommended / Needs Improvement")
    key_personality_inference: str = Field(..., description="Summary of key traits and potential")

class GeneratedStorySection(BaseModel):
    title: str = Field(default="Instructor Generated Story")
    story_text: str
    context_reasoning: Optional[str] = None  # why this story fits the image

# 🧠 Master model combining all sections
class ExamineStoryResponseSchema(BaseModel):
    image_analysis: ImageRelevanceSchema
    story_compliance: StoryComplianceSchema
    olq_scores_summary: List[OLQTraitResponseSchema]
    psychological_summary: PsychologicalSummarySchema


# 🧠 Master model combining all sections with generated story
class ExamineSuggestedStoryResponseSchema(BaseModel):
    generated_story: GeneratedStorySection
    image_analysis: ImageRelevanceSchema
    story_compliance: StoryComplianceSchema
    olq_scores_summary: List[OLQTraitResponseSchema]
    psychological_summary: PsychologicalSummarySchema