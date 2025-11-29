import os
import logging
import base64
from typing import Any
from PIL import Image
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

logger = logging.getLogger(__name__)

# Helper function to encode images to base64 required by structured inputs
def pil_to_base64(image: Image.Image) -> str:
    import io
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG") # Use JPEG format during encoding
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode("utf-8")


class GoogleGenerativeAIAdapter:
    # Using gemini-2.5-flash which is a powerful multimodal model
    def __init__(self, model: str = "gemini-2.5-flash", **kwargs):
        self.llm = ChatGoogleGenerativeAI(
            model=model, 
            api_key=os.getenv("GEMINI_API_KEY"),
            **kwargs
        )
        self.model = model

    def generate_and_parse(self, prompt: str, image: Image.Image, pydantic_model: Any):
        """Generate and return parsed dict matching `pydantic_model`."""

        # 1. Configure the LLM to return a structured Pydantic object directly
        # This enforce the Google Gemini model to return structured output as per the provided Pydantic schema
        structured_llm = self.llm.with_structured_output(pydantic_model)

        # 2. Prepare the multimodal input content in LangChain HumanMessage format
        base64_image_str = pil_to_base64(image)

        image_url_content = {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image_str}"},
        }
        text_content = {"type": "text", "text": prompt}

        # Combine all parts into a standard HumanMessage
        multimodal_message = HumanMessage(
            content=[
                text_content, 
                image_url_content
            ]
        )

        try:
            # 3. Invoke the structured model
            # The result here is automatically a Pydantic object, not raw text
            pydantic_object = structured_llm.invoke([multimodal_message])

            # 4. Return as a dictionary
            return pydantic_object.model_dump()

        except Exception as e:
            logger.error("Structured LLM invocation failed: %s", e)

        raise RuntimeError("Could not produce a parsed response.")

