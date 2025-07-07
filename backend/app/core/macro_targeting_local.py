"""
Macro Targeting Service using Local RAG Pipeline

Sentence-Transformers + Chroma to generate target macro recommendations 
based on user context and stores them in the database.

Uses metadata-based filtering for exact matches and local embeddings for fallback.
"""

import os
import json
import yaml
from typing import Dict, Optional, Tuple, Any, List
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.db.models import UserInput, MacroTarget
from app.db.session import get_db

load_dotenv()

class MacroTargetingServiceLocal:
    def __init__(self, rag_store_path: str = "../rag_store"):
        """
        Initialize the macro targeting service with local RAG capabilities.
        
        Args:
            rag_store_path: Path to store Chroma vector database
        """
        self.rag_store_path = rag_store_path
        
        # Initialize local embeddings
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize vector store
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize the vector store with nutrition guidelines."""
        try:
            # Try to load existing vector store
            self.vectorstore = Chroma(
                persist_directory=self.rag_store_path,
                embedding_function=self._get_embedding_function()
            )
        except:
            # If it doesn't exist, create it from documents
            self._create_vectorstore()
    
    def _get_embedding_function(self):
        """Create a LangChain-compatible embedding function from sentence-transformers."""
        from langchain.embeddings.base import Embeddings
        
        class SentenceTransformerEmbeddings(Embeddings):
            def __init__(self, model):
                self.model = model
            
            def embed_documents(self, texts):
                embeddings = self.model.encode(texts)
                return embeddings.tolist()
            
            def embed_query(self, text):
                embedding = self.model.encode([text])
                return embedding.tolist()[0]
        
        return SentenceTransformerEmbeddings(self.embeddings)
    
    def _load_documents(self):
        """Load nutrition guideline documents with enhanced metadata."""
        documents = []
        guidelines_dir = "nutrition_guidelines"
        
        # Age groups and their corresponding directories
        age_groups = ["age6-11", "age12-18", "age19-59"]
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        
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
                            # Load and parse frontmatter
                            frontmatter, content = self._parse_markdown_with_frontmatter(filepath)
                            
                            # Create document with enhanced metadata
                            doc_metadata = {
                                'age_group': age_group,
                                'filename': filename,
                                'filepath': filepath,
                                'content': content,  # Store full content for exact retrieval
                                **frontmatter  # Include all frontmatter fields
                            }
                            
                            # Create a single document per file (no chunking for exact matches)
                            from langchain.schema import Document
                            doc = Document(
                                page_content=content,
                                metadata=doc_metadata
                            )
                            documents.append(doc)
                            print(f"Loaded: {filepath} (metadata: {frontmatter})")
                            
                        except Exception as e:
                            print(f"Warning: Could not load {filepath}: {e}")
            except Exception as e:
                print(f"Warning: Could not access directory {age_group_path}: {e}")
        
        print(f"Total documents loaded: {len(documents)}")
        for i, doc in enumerate(documents):
            print(f"  Doc {i}: metadata={doc.metadata}")
        return documents

    def _create_vectorstore(self):
        """Create vector store from nutrition guideline documents."""
        # Load documents from guidelines directory
        documents = self._load_documents()
        
        # Create and persist vector store
        self.vectorstore = Chroma.from_documents(
            documents, 
            embedding=self._get_embedding_function(), 
            persist_directory=self.rag_store_path
        )
        self.vectorstore.persist()
        # Debug: Check what is in the vector store after creation
        try:
            all_results = self.vectorstore.get(include=["documents", "metadatas"])
            print(f"[After creation] Total documents in vector store: {len(all_results['documents'])}")
            print("[After creation] Available metadata:")
            for i, metadata in enumerate(all_results['metadatas']):
                print(f"  Doc {i}: {metadata}")
        except Exception as e:
            print(f"Error getting all documents after creation: {e}")
    
    def _parse_markdown_with_frontmatter(self, filepath: str) -> Tuple[Dict[str, Any], str]:
        """Parse markdown file with YAML frontmatter."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1].strip()
                markdown_content = parts[2].strip()
                
                # Parse YAML frontmatter
                try:
                    frontmatter = yaml.safe_load(frontmatter_text) or {}
                except yaml.YAMLError as e:
                    print(f"Warning: Could not parse frontmatter in {filepath}: {e}")
                    frontmatter = {}
            else:
                frontmatter = {}
                markdown_content = content
        else:
            frontmatter = {}
            markdown_content = content
        
        return frontmatter, markdown_content
    
    def _get_age_group_from_age(self, age: int) -> str:
        """Map user age to age group directory."""
        if age <= 11:
            return "age6-11"
        elif age <= 18:
            return "age12-18"
        else:
            return "age19-59"
    
    def _get_duration_type(self, duration_minutes: int) -> str:
        """Map exercise duration to duration type."""
        return "short" if duration_minutes < 60 else "long"
    
    def _get_exercise_type(self, exercise_type: str) -> str:
        """Normalize exercise type."""
        exercise_type_lower = exercise_type.lower()
        if any(word in exercise_type_lower for word in ['cardio', 'running', 'cycling', 'swimming', 'soccer', 'basketball']):
            return "cardio"
        elif any(word in exercise_type_lower for word in ['strength', 'weight', 'lifting', 'resistance']):
            return "strength"
        else:
            return exercise_type_lower
    
    def retrieve_context_by_metadata(self, user_input: UserInput) -> str:
        """Retrieve context using metadata-based filtering."""
        # Extract metadata from user input
        age_group = self._get_age_group_from_age(user_input.age) if user_input.age else None
        exercise_type = self._get_exercise_type(user_input.exercise_type) if user_input.exercise_type else None
        duration_type = self._get_duration_type(user_input.exercise_duration_minutes) if user_input.exercise_duration_minutes else None
        
        print(f"Looking for: age_group={age_group}, exercise_type={exercise_type}, duration={duration_type}")
        
        # Build metadata filter
        where_clause = {}
        if age_group:
            where_clause["age_group"] = age_group
        if exercise_type:
            where_clause["type_of_activity"] = exercise_type
        if duration_type:
            where_clause["duration"] = duration_type
        
        # Try exact metadata match first
        if where_clause:
            # Debug: Check what's in the vector store
            try:
                all_results = self.vectorstore.get(include=["documents", "metadatas"])
                print(f"Total documents in vector store: {len(all_results['documents'])}")
                print("Available metadata:")
                for i, metadata in enumerate(all_results['metadatas']):
                    print(f"  Doc {i}: {metadata}")
            except Exception as e:
                print(f"Error getting all documents: {e}")
            
            try:
                # Chroma metadata filtering syntax
                if len(where_clause) > 1:
                    # Multiple conditions - use $and
                    chroma_where = {"$and": [{k: {"$eq": v}} for k, v in where_clause.items()]}
                else:
                    # Single condition
                    key, value = list(where_clause.items())[0]
                    chroma_where = {key: {"$eq": value}}
                
                print(f"Chroma where clause: {chroma_where}")
                
                results = self.vectorstore.get(
                    where=chroma_where,
                    include=["documents", "metadatas"]
                )
                
                if results['documents']:
                    print(f"Found {len(results['documents'])} exact metadata matches")
                    # Return the full content of the first match
                    return results['documents'][0]
            except Exception as e:
                print(f"Error in metadata-based retrieval: {e}")
        
        # Fallback to vector search if no exact match
        print("No exact metadata match found, falling back to vector search")
        return self.retrieve_context_fallback(user_input)
    
    def retrieve_context_fallback(self, user_input: UserInput) -> str:
        """Fallback to vector search when metadata matching fails."""
        # Build a query for vector search
        query_parts = []
        if user_input.age:
            age_group = self._get_age_group_from_age(user_input.age)
            query_parts.append(f"{age_group} nutrition guidelines")
        
        if user_input.exercise_type:
            exercise_type = self._get_exercise_type(user_input.exercise_type)
            query_parts.append(f"{exercise_type} exercise")
        
        if user_input.exercise_duration_minutes:
            duration_type = self._get_duration_type(user_input.exercise_duration_minutes)
            query_parts.append(f"{duration_type} session")
        
        query = " ".join(query_parts) if query_parts else user_input.user_query
        
        # Use vector search
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 1})
        results = retriever.get_relevant_documents(query)
        
        if results:
            return results[0].page_content
        else:
            return "No relevant nutrition guidelines found."
    
    def retrieve_context(self, user_query: str, k: int = 3) -> str:
        """Legacy method for backward compatibility."""
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        results = retriever.invoke(user_query)
        
        # Format results with metadata information
        formatted_results = []
        for doc in results:
            metadata_info = f"[Source: {doc.metadata.get('age_group', 'Unknown')} - {doc.metadata.get('filename', 'Unknown')}]"
            formatted_results.append(f"{metadata_info}\n{doc.page_content}")
        
        return "\n\n".join(formatted_results)
    
    def _extract_macro_values_from_context(self, context: str, user_input: UserInput) -> Dict[str, Any]:
        """Extract macro values from context using rule-based approach."""
        macro_values = {
            'target_calories': 500.0,  # Default values
            'target_protein': 25.0,
            'target_carbs': 75.0,
            'target_fat': 15.0,
            'target_electrolytes': 1.0,
            'pre_workout_macros': {
                'carbs': 30.0,
                'protein': 10.0,
                'fat': 5.0,
                'calories': 200.0
            },
            'during_workout_macros': {
                'carbs': 20.0,
                'protein': 0.0,
                'electrolytes': 0.5
            },
            'post_workout_macros': {
                'carbs': 25.0,
                'protein': 15.0,
                'fat': 10.0,
                'calories': 300.0
            }
        }
        
        # Adjust based on exercise duration
        duration_factor = user_input.exercise_duration_minutes / 60.0 if user_input.exercise_duration_minutes else 1.0
        
        # Adjust based on exercise type
        if user_input.exercise_type and 'cardio' in user_input.exercise_type.lower():
            macro_values['target_carbs'] *= 1.2  # More carbs for cardio
            macro_values['target_protein'] *= 0.8  # Less protein for cardio
        elif user_input.exercise_type and 'strength' in user_input.exercise_type.lower():
            macro_values['target_protein'] *= 1.3  # More protein for strength
            macro_values['target_carbs'] *= 0.9  # Slightly fewer carbs for strength
        
        # Adjust based on age
        if user_input.age:
            if user_input.age <= 11:  # Children
                macro_values['target_calories'] *= 0.7
                macro_values['target_protein'] *= 0.8
                macro_values['target_carbs'] *= 0.8
                macro_values['target_fat'] *= 0.8
            elif user_input.age <= 18:  # Adolescents
                macro_values['target_calories'] *= 1.1
                macro_values['target_protein'] *= 1.1
                macro_values['target_carbs'] *= 1.1
                macro_values['target_fat'] *= 1.1
            # Adults (19-59) use default values
        
        # Apply duration factor to all values
        for key in ['target_calories', 'target_protein', 'target_carbs', 'target_fat', 'target_electrolytes']:
            macro_values[key] *= duration_factor
        
        # Update timing breakdowns
        macro_values['pre_workout_macros']['carbs'] *= duration_factor
        macro_values['pre_workout_macros']['protein'] *= duration_factor
        macro_values['pre_workout_macros']['fat'] *= duration_factor
        macro_values['pre_workout_macros']['calories'] *= duration_factor
        
        macro_values['during_workout_macros']['carbs'] *= duration_factor
        macro_values['during_workout_macros']['electrolytes'] *= duration_factor
        
        macro_values['post_workout_macros']['carbs'] *= duration_factor
        macro_values['post_workout_macros']['protein'] *= duration_factor
        macro_values['post_workout_macros']['fat'] *= duration_factor
        macro_values['post_workout_macros']['calories'] *= duration_factor
        
        return macro_values
    
    def generate_macro_targets(self, user_input: UserInput) -> MacroTarget:
        """
        Generate macro targets for a user input using local RAG pipeline.
        
        Args:
            user_input: UserInput object with user context
            
        Returns:
            MacroTarget object with generated recommendations
        """
        # Retrieve relevant context using metadata-based filtering
        context = self.retrieve_context_by_metadata(user_input)
        
        # Extract macro recommendations from context using rule-based approach
        macro_values = self._extract_macro_values_from_context(context, user_input)
        
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
            reasoning=f"Generated from local RAG context: {context[:200]}..."
        )
        
        return macro_target
    
    def _build_user_query(self, user_input: UserInput) -> str:
        """Build a natural language query from user input context."""
        query_parts = []
        
        # Add age-specific information
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
        
        # Add exercise type and duration
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
        # Retrieve relevant context using metadata-based filtering
        context = self.retrieve_context_by_metadata(user_input)
        # Generate macro targets
        macro_target = self.generate_macro_targets(user_input)
        return context, macro_target 