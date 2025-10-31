import json
import os
from google import genai
from google.genai import types

class QuestionGenerator:
    """Handles AI-powered question generation using Google Gemini API"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        # the newest Gemini model is "gemini-2.5-flash" or "gemini-2.5-pro"
        # do not change this unless explicitly requested by the user
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash"
    
    def generate_questions(self, text_content, question_type="short", num_questions=3):
        """Generate questions from text content based on type"""
        
        if len(text_content.strip()) < 50:
            raise ValueError("Text content is too short to generate meaningful questions")
        
        # Truncate text if too long (to avoid token limits)
        max_chars = 4000
        if len(text_content) > max_chars:
            text_content = text_content[:max_chars] + "..."
        
        try:
            if question_type == "short":
                return self._generate_short_answer_questions(text_content, num_questions)
            elif question_type == "long":
                return self._generate_long_answer_questions(text_content, num_questions)
            elif question_type == "mcq":
                return self._generate_multiple_choice_questions(text_content, num_questions)
            else:
                raise ValueError(f"Unsupported question type: {question_type}")
                
        except Exception as e:
            raise Exception(f"Error generating {question_type} questions: {str(e)}")
    
    def _generate_short_answer_questions(self, text_content, num_questions):
        """Generate short answer questions"""
        
        system_instruction = "You are an expert educator who creates clear, relevant questions from text content."
        
        prompt = f"""
        Based on the following text, generate {num_questions} short answer questions that test comprehension and recall of key facts.
        
        Text: {text_content}
        
        Please respond with a JSON object containing an array of questions. Each question should have:
        - question: the question text
        - answer: a concise answer (1-3 sentences)
        - type: "Short Answer"
        
        Format: {{"questions": [{{"question": "...", "answer": "...", "type": "Short Answer"}}]}}
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                max_output_tokens=4096
            )
        )
        
        result = json.loads(response.text)
        return result.get("questions", [])
    
    def _generate_long_answer_questions(self, text_content, num_questions):
        """Generate long answer questions"""
        
        system_instruction = "You are an expert educator who creates thought-provoking analytical questions from text content."
        
        prompt = f"""
        Based on the following text, generate {num_questions} long answer questions that require analysis, synthesis, and detailed explanation.
        
        Text: {text_content}
        
        Please respond with a JSON object containing an array of questions. Each question should have:
        - question: the question text
        - answer: a detailed answer (paragraph form)
        - type: "Long Answer"
        
        Format: {{"questions": [{{"question": "...", "answer": "...", "type": "Long Answer"}}]}}
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                max_output_tokens=8192
            )
        )
        
        result = json.loads(response.text)
        return result.get("questions", [])
    
    def _generate_multiple_choice_questions(self, text_content, num_questions):
        """Generate multiple choice questions"""
        
        system_instruction = "You are an expert educator who creates clear multiple choice questions with one correct answer and plausible distractors."
        
        prompt = f"""
        Based on the following text, generate {num_questions} multiple choice questions with 4 options each.
        
        Text: {text_content}
        
        Please respond with a JSON object containing an array of questions. Each question should have:
        - question: the question text
        - options: array of 4 answer choices
        - answer: the correct answer (should match one of the options exactly)
        - type: "Multiple Choice"
        
        Make sure the correct answer is clearly identifiable and the distractors are plausible but incorrect.
        
        Format: {{"questions": [{{"question": "...", "options": ["A", "B", "C", "D"], "answer": "A", "type": "Multiple Choice"}}]}}
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                max_output_tokens=8192
            )
        )
        
        result = json.loads(response.text)
        return result.get("questions", [])
