"""
Macro Targeting Service using RAG Pipeline

OpenAI + LangChain + Chroma to generate target macro recommendations 
based on user context and stores them in the database.

Handles document loading, vector store management, and GPT interactions 
"""

import os
import json
from typing import Dict, Optional, Tuple, Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.db.models import UserInput, MacroTarget
from app.db.session import get_db

load_dotenv()

class MacroTargetingService:
    def __init__(self, openai_api_key: Optional[str] = None, rag_store_path: str = "./data/rag_store"):
        """
        Initialize the macro targeting service with RAG capabilities.
        
        Args:
            openai_api_key: OpenAI API key for embeddings and chat
            rag_store_path: Path to store Chroma vector database
        """
        if openai_api_key is None:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_api_key = openai_api_key
        self.rag_store_path = rag_store_path
        
        # Initialize components with explicit API key
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, openai_api_key=self.openai_api_key)
        
        # Initialize vector store
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize the vector store with nutrition guidelines."""
        try:
            # Try to load existing vector store
            self.vectorstore = Chroma(
                persist_directory=self.rag_store_path,
                embedding_function=self.embeddings
            )
        except:
            # If it doesn't exist, create it from documents
            self._create_vectorstore()
    
    def _create_vectorstore(self):
        """Create vector store from nutrition guideline documents."""
        # Load documents from guidelines directory
        documents = self._load_documents()
        
        # Create and persist vector store
        self.vectorstore = Chroma.from_documents(
            documents, 
            embedding=self.embeddings, 
            persist_directory=self.rag_store_path
        )
        self.vectorstore.persist()
    
    def _load_documents(self):
        """Load nutrition guideline documents from the nutrition_guidelines directory."""
        documents = []
        guidelines_dir = "nutrition_guidelines"  # Path to the nutrition guidelines directory
        
        # Age groups and their corresponding directories
        age_groups = ["age6-11", "age12-18", "age19-59"]
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        
        for age_group in age_groups:
            age_group_path = os.path.join(guidelines_dir, age_group)
            if not os.path.exists(age_group_path):
                print(f"Warning: Age group directory {age_group_path} does not exist")
                continue
                
            # Load all .md files in the age group directory
            try:
                for filename in os.listdir(age_group_path):
                    if filename.endswith('.md'):
                        filepath = os.path.join(age_group_path, filename)
                        try:
                            loader = TextLoader(filepath)
                            docs = loader.load()
                            # Add metadata to help with retrieval
                            for doc in docs:
                                doc.metadata.update({
                                    'age_group': age_group,
                                    'filename': filename,
                                    'filepath': filepath
                                })
                            documents.extend(splitter.split_documents(docs))
                            print(f"Loaded: {filepath}")
                        except Exception as e:
                            print(f"Warning: Could not load {filepath}: {e}")
            except Exception as e:
                print(f"Warning: Could not access directory {age_group_path}: {e}")
        
        print(f"Total documents loaded: {len(documents)}")
        return documents
    
    def retrieve_context(self, user_query: str, k: int = 3) -> str:
        """Retrieve relevant context from the vector store."""
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        results = retriever.invoke(user_query)
        
        # Format results with metadata information for better context
        formatted_results = []
        for doc in results:
            # Add metadata information to help with context
            metadata_info = f"[Source: {doc.metadata.get('age_group', 'Unknown')} - {doc.metadata.get('filename', 'Unknown')}]"
            formatted_results.append(f"{metadata_info}\n{doc.page_content}")
        
        return "\n\n".join(formatted_results)
    
    def _extract_macro_values_from_json(self, response_text: str) -> Dict[str, Any]:
        """Extract macro values and timing breakdown from GPT JSON response."""
        macro_values = {
            'target_calories': None,
            'target_protein': None,
            'target_carbs': None,
            'target_fat': None,
            'target_electrolytes': None,
            'pre_workout_macros': None,
            'during_workout_macros': None,
            'post_workout_macros': None
        }
        
        try:
            # Try to find JSON in the response
            # Look for JSON block between ```json and ``` or just parse the whole response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                # Try to parse the entire response as JSON
                json_str = response_text.strip()
            
            # Parse JSON
            parsed_data = json.loads(json_str)
            
            # Extract overall values, handling different possible key names
            macro_values['target_calories'] = parsed_data.get('target_calories') or parsed_data.get('calories')
            macro_values['target_protein'] = parsed_data.get('target_protein') or parsed_data.get('protein')
            macro_values['target_carbs'] = parsed_data.get('target_carbs') or parsed_data.get('carbs') or parsed_data.get('carbohydrates')
            macro_values['target_fat'] = parsed_data.get('target_fat') or parsed_data.get('fat')
            macro_values['target_electrolytes'] = parsed_data.get('target_electrolytes') or parsed_data.get('electrolytes')
            
            # Extract timing breakdown
            macro_values['pre_workout_macros'] = parsed_data.get('pre_workout_macros') or parsed_data.get('pre_workout')
            macro_values['during_workout_macros'] = parsed_data.get('during_workout_macros') or parsed_data.get('during_workout')
            macro_values['post_workout_macros'] = parsed_data.get('post_workout_macros') or parsed_data.get('post_workout')
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not parse JSON from GPT response: {e}")
            print(f"Response text: {response_text[:200]}...")
            # Return None values if parsing fails
            pass
        
        return macro_values
    
    def generate_macro_targets(self, user_input: UserInput) -> MacroTarget:
        """
        Generate macro targets for a user input using RAG pipeline.
        
        Args:
            user_input: UserInput object with user context
            
        Returns:
            MacroTarget object with generated recommendations
        """
        # Build user query from context
        user_query = self._build_user_query(user_input)
        
        # Retrieve relevant context
        context = self.retrieve_context(user_query)
        
        # Build system messages with JSON output requirement
        messages = [
            SystemMessage(content=(
                "You are a certified sports nutrition expert. "
                "Use the retrieved evidence below to recommend how many grams of carbohydrates, protein, fat, and electrolytes a person "
                "should consume for their entire workout session. Also provide total calories and a breakdown by timing (pre-workout, during-workout, post-workout). "
                "Tailor your response to their weight, sex, duration, and exercise type. "
                "IMPORTANT: You must respond with ONLY a valid JSON object containing the following keys:\n"
                "- target_calories (float, total calories for entire session)\n"
                "- target_protein (float, total grams of protein for entire session)\n"
                "- target_carbs (float, total grams of carbohydrates for entire session)\n"
                "- target_fat (float, total grams of fat for entire session)\n"
                "- target_electrolytes (float, total grams of electrolytes for entire session)\n"
                "- pre_workout_macros (object with carbs, protein, fat, calories for pre-workout)\n"
                "- during_workout_macros (object with carbs, protein, electrolytes for during-workout)\n"
                "- post_workout_macros (object with carbs, protein, fat, calories for post-workout)\n"
                "Do not include any explanatory text outside the JSON. Do not make up facts not in the context."
            )),
            SystemMessage(content=f"Retrieved context:\n{context}"),
            HumanMessage(content=user_query)
        ]
        
        # Get response from GPT
        response = self.llm(messages)
        response_text = response.content
        
        # Extract macro values from JSON
        macro_values = self._extract_macro_values_from_json(response_text)
        
        # Create MacroTarget object
        macro_target = MacroTarget(
            user_input_id=user_input.id,
            target_calories=macro_values['target_calories'],
            target_protein=macro_values['target_protein'],
            target_carbs=macro_values['target_carbs'],
            target_fat=macro_values['target_fat'],
            target_electrolytes=macro_values['target_electrolytes'],
            pre_workout_macros=macro_values['pre_workout_macros'],
            during_workout_macros=macro_values['during_workout_macros'],
            post_workout_macros=macro_values['post_workout_macros'],
            rag_context=context,
            reasoning=response_text
        )
        
        return macro_target
    
    def _build_user_query(self, user_input: UserInput) -> str:
        """Build a natural language query from user input context."""
        query_parts = []
        
        # Add age-specific information to help with retrieval
        if user_input.age:
            if user_input.age <= 11:
                age_group = "6-11 years old child"
            elif user_input.age <= 18:
                age_group = "12-18 years old adolescent"
            else:
                age_group = "19-59 years old adult"
            query_parts.append(f"I'm a {age_group}.")
        
        if user_input.weight_kg and user_input.sex:
            query_parts.append(f"I'm a {user_input.sex}, {user_input.weight_kg} kg.")
        
        # Add exercise type and duration with duration classification
        if user_input.exercise_type and user_input.exercise_duration_minutes:
            duration_type = "short session" if user_input.exercise_duration_minutes < 60 else "long session"
            query_parts.append(f"I'm planning to do {user_input.exercise_duration_minutes} minutes of {user_input.exercise_type} ({duration_type}).")
        
        if user_input.exercise_intensity:
            query_parts.append(f"The exercise intensity will be {user_input.exercise_intensity}.")
        
        if user_input.user_query:
            query_parts.append(user_input.user_query)
        
        return " ".join(query_parts) if query_parts else user_input.user_query
    
    def get_macro_targets_for_user(self, user_input_id: int, db: Session) -> Optional[MacroTarget]:
        """Retrieve existing macro targets for a user input."""
        return db.query(MacroTarget).filter(MacroTarget.user_input_id == user_input_id).first()
    
    def create_or_update_macro_targets(self, user_input: UserInput, db: Session) -> MacroTarget:
        """
        Create or update macro targets for a user input.
        
        Args:
            user_input: UserInput object
            db: Database session
            
        Returns:
            MacroTarget object
        """
        # Check if macro targets already exist
        existing_target = self.get_macro_targets_for_user(user_input.id, db)
        
        if existing_target:
            # Update existing target
            new_target = self.generate_macro_targets(user_input)
            existing_target.target_calories = new_target.target_calories
            existing_target.target_protein = new_target.target_protein
            existing_target.target_carbs = new_target.target_carbs
            existing_target.target_fat = new_target.target_fat
            existing_target.target_electrolytes = new_target.target_electrolytes
            existing_target.pre_workout_macros = new_target.pre_workout_macros
            existing_target.during_workout_macros = new_target.during_workout_macros
            existing_target.post_workout_macros = new_target.post_workout_macros
            existing_target.rag_context = new_target.rag_context
            existing_target.reasoning = new_target.reasoning
            db.commit()
            return existing_target
        else:
            # Create new target
            macro_target = self.generate_macro_targets(user_input)
            db.add(macro_target)
            db.commit()
            db.refresh(macro_target)
            return macro_target

    def get_context_and_macro_targets(self, user_input: UserInput):
        """
        Retrieve the RAG context and compute macro targets for a user input.
        Returns (context, macro_target)
        """
        # Build user query from context
        user_query = self._build_user_query(user_input)
        # Retrieve relevant context
        context = self.retrieve_context(user_query)
        # Generate macro targets as before
        macro_target = self.generate_macro_targets(user_input)
        return context, macro_target


# Example usage function
def get_macro_targets(
    user_query: str,
    age: Optional[int] = None,
    weight_kg: Optional[float] = None,
    sex: Optional[str] = None,
    exercise_type: Optional[str] = None,
    exercise_duration_minutes: Optional[int] = None,
    exercise_intensity: Optional[str] = None,
    timing: Optional[str] = None
) -> MacroTarget:
    """
    Convenience function to get macro targets for a user.
    
    Args:
        user_query: Natural language query from user
        age: User's age
        weight_kg: User's weight in kg
        sex: User's sex ('male', 'female', 'other')
        exercise_type: Type of exercise performed
        exercise_duration_minutes: Duration of exercise in minutes
        exercise_intensity: Intensity level ('low', 'medium', 'high')
        timing: Timing context ('pre-workout', 'post-workout', 'general')
        
    Returns:
        MacroTarget object with recommendations
    """
    # Initialize service (you'll need to set your OpenAI API key)
    service = MacroTargetingService(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create user input
    db = next(get_db())
    user_input = UserInput(
        user_query=user_query,
        age=age,
        weight_kg=weight_kg,
        sex=sex,
        exercise_type=exercise_type,
        exercise_duration_minutes=exercise_duration_minutes,
        exercise_intensity=exercise_intensity,
        timing=timing
    )
    db.add(user_input)
    db.commit()
    db.refresh(user_input)
    
    # Generate macro targets
    macro_target = service.create_or_update_macro_targets(user_input, db)
    
    return macro_target 