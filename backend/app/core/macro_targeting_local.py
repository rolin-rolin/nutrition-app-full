"""
Macro Targeting Service using Local RAG Pipeline with LLM Field Extraction

Sentence-Transformers + Chroma for document retrieval + OpenAI for field extraction
to generate target macro recommendations based on user context and stores them in the database.

Uses metadata-based filtering for exact matches and local embeddings for fallback.
LLM extracts structured fields from natural language user queries.
"""

import os
import json
import yaml
from typing import Dict, Optional, Tuple, Any, List
import random
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.db.models import UserInput, MacroTarget
from app.db.session import get_db

load_dotenv()

class MacroTargetingServiceLocal:
    def __init__(self, rag_store_path: str = "../rag_store", force_rebuild: bool = False, openai_api_key: Optional[str] = None):
        print(f"[DEBUG] MacroTargetingServiceLocal __init__ called with rag_store_path={rag_store_path}, force_rebuild={force_rebuild}")
        """
        Initialize the macro targeting service with local RAG capabilities and LLM field extraction.
        
        Args:
            rag_store_path: Path to store Chroma vector database
            force_rebuild: Whether to force rebuild the vector store
            openai_api_key: OpenAI API key for field extraction
        """
        self.rag_store_path = rag_store_path
        
        # Initialize OpenAI for field extraction
        if openai_api_key is None:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_api_key = openai_api_key
        
        if self.openai_api_key:
            # Use gpt-4o-mini which is more widely available and cost-effective
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, openai_api_key=self.openai_api_key)
        else:
            print("Warning: No OpenAI API key provided. Field extraction will use fallback parsing.")
            self.llm = None
        
        # Initialize local embeddings
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize vector store
        if force_rebuild:
            print("[DEBUG] Forcing rebuild of vector store...")
            self._create_vectorstore()
        else:
            self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize the vector store with nutrition guidelines."""
        try:
            print("[DEBUG] Attempting to load existing Chroma vector store...")
            # Try to load existing vector store
            self.vectorstore = Chroma(
                persist_directory=self.rag_store_path,
                embedding_function=self._get_embedding_function()
            )
            print("[DEBUG] Loaded existing Chroma vector store.")
        except Exception as e:
            print(f"[DEBUG] Failed to load existing Chroma vector store: {e}")
            print("[DEBUG] Creating new vector store from documents...")
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
        guidelines_dir = "nutrition_guidelines"  # Corrected path
        print(f"[DEBUG] Looking for guidelines in: {os.path.abspath(guidelines_dir)}")
        
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
        print("[DEBUG] _create_vectorstore called. Loading documents and creating Chroma store...")
        # Load documents from guidelines directory
        documents = self._load_documents()
        
        # Create and persist vector store
        self.vectorstore = Chroma.from_documents(
            documents, 
            embedding=self._get_embedding_function(), 
            persist_directory=self.rag_store_path
        )
        # self.vectorstore.persist()  # No longer needed
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
            return "6-11"
        elif age <= 18:
            return "12-18"
        else:
            return "19-59"
    
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
        results = retriever.invoke(query)
        
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
        """
        Calculate macro targets from YAML-structured nutrition guidelines.
        
        Args:
            context: The YAML content from the nutrition guideline document
            user_input: User input with age, weight, duration, etc.
        
        Returns:
            Dict with calculated macro targets
        """
        try:
            # Try to parse the context as YAML, handling custom tags
            # First, remove all custom tags that cause parsing issues
            import re
            cleaned_context = re.sub(r'!!\w+', '', context)
            
            # Parse the original content line by line to extract the correct values
            # This handles the flat YAML structure properly
            lines = context.split('\n')
            pre = {}
            during = {}
            post = {}
            
            current_section = None
            
            # Parse the original content line by line to extract the correct values
            # This handles the flat YAML structure properly
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                if line == 'pre:':
                    current_section = 'pre'
                elif line == 'during:':
                    current_section = 'during'
                elif line == 'post:':
                    current_section = 'post'
                elif ':' in line and current_section:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    try:
                        # Parse the value as a list
                        parsed_value = eval(value)
                        if current_section == 'pre':
                            pre[key] = parsed_value
                        elif current_section == 'during':
                            during[key] = parsed_value
                        elif current_section == 'post':
                            post[key] = parsed_value
                    except:
                        # Skip if we can't parse the value
                        continue
            
            # If we successfully parsed some values with line-by-line parser, use them
            if pre or during or post:
                # Continue with the line-by-line parsing results
                pass
            else:
                # Fallback to YAML parsing
                data = yaml.safe_load(cleaned_context)
                
                # Extract timing data - handle both nested and flat structures
                if 'timing' in data and data['timing'] is not None:
                    # Nested structure
                    timing = data.get('timing', {})
                    pre = timing.get('pre', {})
                    during = timing.get('during', {})
                    post = timing.get('post', {})
                else:
                    # Flat structure - extract pre, during, post from the flat data
                    pre = {}
                    during = {}
                    post = {}
                    
                    # Extract pre-workout data
                    if 'pre' in data and data['pre'] is not None:
                        pre = data['pre']
                    else:
                        # Look for pre-* keys in flat structure
                        pre = {k: v for k, v in data.items() if k.startswith('pre_') or (not k.startswith('during_') and not k.startswith('post_') and k.endswith('_per_kg'))}
                    
                    # Extract during-workout data
                    if 'during' in data and data['during'] is not None:
                        during = data['during']
                    else:
                        # Look for during-* keys in flat structure
                        during = {k: v for k, v in data.items() if k.startswith('during_') or k.endswith('_per_hour')}
                    
                    # Extract post-workout data
                    if 'post' in data and data['post'] is not None:
                        post = data['post']
                    else:
                        # Look for post-* keys in flat structure
                        post = {k: v for k, v in data.items() if k.startswith('post_') or (k.endswith('_per_kg') and not k.startswith('during_') and not k.startswith('pre_'))}
                    
                    # If we still have empty dictionaries, try to extract from the flat structure
                    # based on the actual keys we see in the data
                    if not pre and not during and not post:
                        # The YAML is being parsed as flat structure
                        # We need to map the values correctly based on the knowledge document structure
                        
                        # For strength long session, the flat structure has:
                        # carbs_g_per_kg: [0.8, 1.0] (this is POST workout)
                        # protein_g_per_kg: [0.3, 0.4] (this is POST workout)
                        # fat_g_per_kg: [0.1, 0.2] (this is POST workout)
                        # carbs_g_per_kg_per_hour: [0.3, 0.5] (this is DURING workout)
                        # protein_g_per_kg_per_hour: [0.05, 0.1] (this is DURING workout)
                        # electrolytes_mg_per_kg_per_hour: [21, 32] (this is DURING workout)
                        
                        # We need to extract the PRE workout values from the original YAML content
                        # Let me parse the original content to get the correct values
                        original_lines = context.split('\n')
                        pre_carbs = [0.5, 0.8]  # Default from strength long session
                        pre_protein = [0.1, 0.15]  # Default from strength long session
                        pre_fat = [0.0, 0.1]  # Default from strength long session
                        
                        # Try to extract actual values from the original content
                        for i, line in enumerate(original_lines):
                            if 'pre:' in line:
                                # Look for the next few lines to get pre values
                                for j in range(i+1, min(i+10, len(original_lines))):
                                    if 'carbs_g_per_kg:' in original_lines[j]:
                                        pre_carbs = eval(original_lines[j].split(':')[1].strip())
                                    elif 'protein_g_per_kg:' in original_lines[j]:
                                        pre_protein = eval(original_lines[j].split(':')[1].strip())
                                    elif 'fat_g_per_kg:' in original_lines[j]:
                                        pre_fat = eval(original_lines[j].split(':')[1].strip())
                                    elif original_lines[j].strip() in ['during:', 'post:']:
                                        break
                        
                        pre = {
                            'carbs_g_per_kg': pre_carbs,
                            'protein_g_per_kg': pre_protein,
                            'fat_g_per_kg': pre_fat
                        }
                        during = {
                            'carbs_g_per_kg_per_hour': data.get('carbs_g_per_kg_per_hour', [0, 0]),
                            'protein_g_per_kg_per_hour': data.get('protein_g_per_kg_per_hour', [0, 0]),
                            'electrolytes_mg_per_kg_per_hour': data.get('electrolytes_mg_per_kg_per_hour', [0, 0])
                        }
                        post = {
                            'carbs_g_per_kg': data.get('carbs_g_per_kg', [0, 0]),
                            'protein_g_per_kg': data.get('protein_g_per_kg', [0, 0]),
                            'fat_g_per_kg': data.get('fat_g_per_kg', [0, 0])
                        }
            
            # Get user weight and duration with validation
            weight_kg = user_input.weight_kg
            duration_minutes = user_input.exercise_duration_minutes
            age = user_input.age
            exercise_type = user_input.exercise_type
            
            if weight_kg is None:
                weight_kg = 70.0  # Default weight for calculations
            
            if duration_minutes is None:
                duration_minutes = 60  # Default duration for calculations
            
            if age is None:
                age = 21  # Default age for calculations
            
            if exercise_type is None:
                exercise_type = "cardio"  # Default exercise type for calculations
            
            duration_hours = duration_minutes / 60.0
            
            # Calculate pre-workout macros
            pre_carbs = self._calculate_range(pre.get('carbs_g_per_kg', [0, 0]), weight_kg)
            pre_protein = self._calculate_range(pre.get('protein_g_per_kg', [0, 0]), weight_kg)
            pre_fat = self._calculate_range(pre.get('fat_g_per_kg', [0, 0]), weight_kg)
            
            # Calculate during-workout macros
            during_carbs = self._calculate_range(during.get('carbs_g_per_kg_per_hour', [0, 0]), weight_kg * duration_hours)
            during_protein = self._calculate_range(during.get('protein_g_per_kg_per_hour', [0, 0]), weight_kg * duration_hours)
            during_fat = self._calculate_range(during.get('fat_g_per_kg_per_hour', [0, 0]), weight_kg * duration_hours)
            during_electrolytes = self._calculate_range(during.get('electrolytes_mg_per_kg_per_hour', [0, 0]), weight_kg * duration_hours)
            
            # Calculate post-workout macros
            post_carbs = self._calculate_range(post.get('carbs_g_per_kg', [0, 0]), weight_kg)
            post_protein = self._calculate_range(post.get('protein_g_per_kg', [0, 0]), weight_kg)
            post_fat = self._calculate_range(post.get('fat_g_per_kg', [0, 0]), weight_kg)
            
            # Calculate totals (now including during-workout protein and fat)
            total_carbs = pre_carbs + during_carbs + post_carbs
            total_protein = pre_protein + during_protein + post_protein
            total_fat = pre_fat + during_fat + post_fat
            total_electrolytes = during_electrolytes  # Only during workout
            
            # Estimate calories (4 cal/g for carbs and protein, 9 cal/g for fat)
            total_calories = (total_carbs * 4) + (total_protein * 4) + (total_fat * 9)
            
            return {
                'target_calories': total_calories,
                'target_protein': total_protein,
                'target_carbs': total_carbs,
                'target_fat': total_fat,
                'target_electrolytes': total_electrolytes,
                'pre_workout_macros': {
                    'carbs': pre_carbs,
                    'protein': pre_protein,
                    'fat': pre_fat,
                    'calories': (pre_carbs * 4) + (pre_protein * 4) + (pre_fat * 9)
                },
                'during_workout_macros': {
                    'carbs': during_carbs,
                    'protein': during_protein,
                    'fat': during_fat,
                    'electrolytes': during_electrolytes,
                    'calories': (during_carbs * 4) + (during_protein * 4) + (during_fat * 9)
                },
                'post_workout_macros': {
                    'carbs': post_carbs,
                    'protein': post_protein,
                    'fat': post_fat,
                    'calories': (post_carbs * 4) + (post_protein * 4) + (post_fat * 9)
                }
            }
            
        except Exception as e:
            print(f"Error calculating macros from YAML: {e}")
            # Fallback to default values
            return self._get_default_macro_values(user_input)
    
    def _calculate_range(self, range_values: List[float], multiplier: float) -> float:
        """
        Calculate the average of a range and multiply by the given factor.
        
        Args:
            range_values: List of values representing a range (e.g., [0.5, 0.8])
            multiplier: The factor to multiply the result by (e.g., weight in kg)
        
        Returns:
            float: The calculated value
        """
        if not range_values:
            return 0.0
        if len(range_values) == 1:
            return range_values[0] * multiplier
        # Take the average of the range
        avg = sum(range_values) / len(range_values)
        return avg * multiplier
    
    def _get_default_macro_values(self, user_input: UserInput) -> Dict[str, Any]:
        """
        Fallback method that provides default macro values using the old rule-based approach.
        This is used when YAML parsing fails or when the context doesn't contain structured data.
        
        Args:
            user_input: User input with age, weight, duration, etc.
        
        Returns:
            Dict with default macro targets
        """
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
                'calories': (30.0 * 4) + (10.0 * 4) + (5.0 * 9)  # 120 + 40 + 45 = 205
            },
            'during_workout_macros': {
                'carbs': 20.0,
                'protein': 5.0,  # Added during-workout protein
                'fat': 2.0,      # Added during-workout fat
                'electrolytes': 0.5,
                'calories': (20.0 * 4) + (5.0 * 4) + (2.0 * 9)  # 80 + 20 + 18 = 118
            },
            'post_workout_macros': {
                'carbs': 25.0,
                'protein': 15.0,
                'fat': 10.0,
                'calories': (25.0 * 4) + (15.0 * 4) + (10.0 * 9)  # 100 + 60 + 90 = 250
            }
        }
        
        # Adjust based on exercise duration
        duration_factor = user_input.exercise_duration_minutes / 60.0 if user_input.exercise_duration_minutes else 1.0
        
        # Adjust based on exercise type (default to cardio)
        exercise_type = user_input.exercise_type or "cardio"
        if 'cardio' in exercise_type.lower():
            macro_values['target_carbs'] *= 1.2  # More carbs for cardio
            macro_values['target_protein'] *= 0.8  # Less protein for cardio
        elif 'strength' in exercise_type.lower():
            macro_values['target_protein'] *= 1.3  # More protein for strength
            macro_values['target_carbs'] *= 0.9  # Slightly fewer carbs for strength
        
        # Adjust based on age (default to 21)
        age = user_input.age or 21
        if age <= 11:  # Children
            macro_values['target_calories'] *= 0.7
            macro_values['target_protein'] *= 0.8
            macro_values['target_carbs'] *= 0.8
            macro_values['target_fat'] *= 0.8
        elif age <= 18:  # Adolescents
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
        macro_values['during_workout_macros']['protein'] *= duration_factor
        macro_values['during_workout_macros']['fat'] *= duration_factor
        macro_values['during_workout_macros']['electrolytes'] *= duration_factor
        macro_values['during_workout_macros']['calories'] *= duration_factor
        
        macro_values['post_workout_macros']['carbs'] *= duration_factor
        macro_values['post_workout_macros']['protein'] *= duration_factor
        macro_values['post_workout_macros']['fat'] *= duration_factor
        macro_values['post_workout_macros']['calories'] *= duration_factor
        
        # Recalculate calories based on updated macro values to ensure accuracy
        macro_values['pre_workout_macros']['calories'] = (
            macro_values['pre_workout_macros']['carbs'] * 4 + 
            macro_values['pre_workout_macros']['protein'] * 4 + 
            macro_values['pre_workout_macros']['fat'] * 9
        )
        
        macro_values['during_workout_macros']['calories'] = (
            macro_values['during_workout_macros']['carbs'] * 4 + 
            macro_values['during_workout_macros']['protein'] * 4 + 
            macro_values['during_workout_macros']['fat'] * 9
        )
        
        macro_values['post_workout_macros']['calories'] = (
            macro_values['post_workout_macros']['carbs'] * 4 + 
            macro_values['post_workout_macros']['protein'] * 4 + 
            macro_values['post_workout_macros']['fat'] * 9
        )
        
        # Recalculate total calories
        macro_values['target_calories'] = (
            macro_values['pre_workout_macros']['calories'] + 
            macro_values['during_workout_macros']['calories'] + 
            macro_values['post_workout_macros']['calories']
        )
        
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
        
        # Extract macro recommendations from context using YAML-based calculation
        macro_values = self._extract_macro_values_from_context(context, user_input)
        
        # Build detailed reasoning
        reasoning_parts = []
        
        # Add user context with new defaults
        if user_input.age and user_input.weight_kg:
            reasoning_parts.append(f"Calculated for {user_input.age}-year-old, {user_input.weight_kg}kg individual")
        elif user_input.age:
            reasoning_parts.append(f"Calculated for {user_input.age}-year-old individual (using default 70kg weight)")
        elif user_input.weight_kg:
            reasoning_parts.append(f"Calculated for {user_input.weight_kg}kg individual (using default age 21)")
        else:
            reasoning_parts.append("Calculated using default values (age: 21, weight: 70kg)")
        
        if user_input.exercise_type and user_input.exercise_duration_minutes:
            reasoning_parts.append(f"doing {user_input.exercise_duration_minutes} minutes of {user_input.exercise_type}")
        elif user_input.exercise_type:
            reasoning_parts.append(f"doing {user_input.exercise_type} (using default 60-minute duration)")
        elif user_input.exercise_duration_minutes:
            reasoning_parts.append(f"doing {user_input.exercise_duration_minutes} minutes of cardio (using default exercise type)")
        else:
            reasoning_parts.append("doing cardio (using default 60-minute duration)")
        
        # Add calculation method
        if "timing:" in context and "pre:" in context:
            reasoning_parts.append("using structured nutrition guidelines with YAML-based calculations")
        else:
            reasoning_parts.append("using fallback rule-based calculations")
        
        # Add macro breakdown
        reasoning_parts.append(f"Total targets: {macro_values['target_carbs']:.1f}g carbs, {macro_values['target_protein']:.1f}g protein, {macro_values['target_fat']:.1f}g fat, {macro_values['target_electrolytes']:.0f}mg electrolytes, {macro_values['target_calories']:.0f} calories")
        
        reasoning = " | ".join(reasoning_parts)
        
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
            reasoning=reasoning
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

    def generate_macro_targets_from_query(self, user_query: str, db: Session) -> Tuple[UserInput, MacroTarget]:
        """
        Main integration method: Extract fields from user query and generate macro targets.
        
        Args:
            user_query: Natural language user query
            db: Database session
            
        Returns:
            Tuple of (UserInput, MacroTarget) objects
        """
        # Step 1: Extract structured fields from user query using LLM
        extracted_fields = self.extract_fields_from_query(user_query)
        
        # Step 2: Convert extracted fields to UserInput format
        user_input_data = self._convert_extracted_fields_to_user_input(extracted_fields, user_query)
        
        # Step 3: Create UserInput object and save to database
        user_input = UserInput(**user_input_data)
        db.add(user_input)
        db.commit()
        db.refresh(user_input)
        
        # Step 4: Generate macro targets using the enhanced pipeline
        macro_target = self.generate_macro_targets_enhanced(user_input, extracted_fields)
        macro_target.user_input_id = user_input.id
        db.add(macro_target)
        db.commit()
        db.refresh(macro_target)
        
        return user_input, macro_target
    
    def generate_macro_targets_enhanced(self, user_input: UserInput, extracted_fields: Optional[Dict[str, Any]] = None) -> MacroTarget:
        """
        Enhanced macro target generation that incorporates LLM-extracted preferences.
        
        Args:
            user_input: UserInput object with user context
            extracted_fields: Optional extracted fields from LLM (for enhanced reasoning)
            
        Returns:
            MacroTarget object with generated recommendations
        """
        # Retrieve relevant context using metadata-based filtering (unchanged)
        context = self.retrieve_context_by_metadata(user_input)
        
        # Extract macro recommendations from context using YAML-based calculation (unchanged)
        macro_values = self._extract_macro_values_from_context(context, user_input)
        
        # Build enhanced reasoning that includes LLM-extracted preferences
        reasoning_parts = []
        
        # Add user context with new defaults
        if user_input.age and user_input.weight_kg:
            reasoning_parts.append(f"Calculated for {user_input.age}-year-old, {user_input.weight_kg}kg individual")
        elif user_input.age:
            reasoning_parts.append(f"Calculated for {user_input.age}-year-old individual (using default 70kg weight)")
        elif user_input.weight_kg:
            reasoning_parts.append(f"Calculated for {user_input.weight_kg}kg individual (using default age 21)")
        else:
            reasoning_parts.append("Calculated using default values (age: 21, weight: 70kg)")
        
        if user_input.exercise_type and user_input.exercise_duration_minutes:
            reasoning_parts.append(f"doing {user_input.exercise_duration_minutes} minutes of {user_input.exercise_type}")
        elif user_input.exercise_type:
            reasoning_parts.append(f"doing {user_input.exercise_type} (using default 60-minute duration)")
        elif user_input.exercise_duration_minutes:
            reasoning_parts.append(f"doing {user_input.exercise_duration_minutes} minutes of cardio (using default exercise type)")
        else:
            reasoning_parts.append("doing cardio (using default 60-minute duration)")
        
        # Add LLM-extracted preferences to reasoning if available
        if extracted_fields:
            preferences_info = []
            
            # Add calorie cap if specified
            calorie_cap = extracted_fields.get("calorie_cap")
            if calorie_cap:
                preferences_info.append(f"calorie limit: {calorie_cap}")
            
            # Add soft preferences
            soft_prefs = extracted_fields.get("soft_preferences", {})
            if soft_prefs.get("flavor"):
                preferences_info.append(f"flavor preferences: {', '.join(soft_prefs['flavor'])}")
            if soft_prefs.get("texture"):
                preferences_info.append(f"texture preferences: {', '.join(soft_prefs['texture'])}")
            if soft_prefs.get("price_dollars"):
                preferences_info.append(f"price limit: ${soft_prefs['price_dollars']}")
            
            # Add hard constraints
            hard_filters = extracted_fields.get("hard_filters", {})
            if hard_filters.get("dietary"):
                preferences_info.append(f"dietary requirements: {', '.join(hard_filters['dietary'])}")
            if hard_filters.get("allergens"):
                preferences_info.append(f"allergen restrictions: {', '.join(hard_filters['allergens'])}")
            
            if preferences_info:
                reasoning_parts.append(f"with preferences: {' | '.join(preferences_info)}")
        
        # Add calculation method
        if "timing:" in context and "pre:" in context:
            reasoning_parts.append("using structured nutrition guidelines with YAML-based calculations")
        else:
            reasoning_parts.append("using fallback rule-based calculations")
        
        # Add macro breakdown
        reasoning_parts.append(f"Total targets: {macro_values['target_carbs']:.1f}g carbs, {macro_values['target_protein']:.1f}g protein, {macro_values['target_fat']:.1f}g fat, {macro_values['target_electrolytes']:.0f}mg electrolytes, {macro_values['target_calories']:.0f} calories")
        
        reasoning = " | ".join(reasoning_parts)
        
        # Create MacroTarget object
        macro_target = MacroTarget(
            user_input_id=user_input.id if hasattr(user_input, 'id') else None,
            target_calories=macro_values['target_calories'],
            target_protein=macro_values['target_protein'],
            target_carbs=macro_values['target_carbs'],
            target_fat=macro_values['target_fat'],
            target_electrolytes=macro_values['target_electrolytes'],
            pre_workout_macros=macro_values['pre_workout_macros'],
            during_workout_macros=macro_values['during_workout_macros'],
            post_workout_macros=macro_values['post_workout_macros'],
            rag_context=context,
            reasoning=reasoning
        )
        
        return macro_target

    def get_context_and_macro_targets(self, user_input: UserInput):
        """
        Retrieve the RAG context and compute macro targets for a user input.
        Returns (context, macro_target)
        """
        # Retrieve relevant context using metadata-based filtering
        context, retrieved_metadata = self.retrieve_context_by_metadata_with_metadata(user_input)
        
        # Check if the retrieved context has "strength" in its metadata
        # and add "high-protein" as a soft preference if so
        strength_detected = self._detect_strength_in_retrieved_metadata(retrieved_metadata, user_input)
        if strength_detected:
            # Add high-protein as a soft preference to the user input preferences
            if not hasattr(user_input, 'preferences') or user_input.preferences is None:
                user_input.preferences = {}
            
            # Initialize soft_preferences if it doesn't exist
            if 'soft_preferences' not in user_input.preferences:
                user_input.preferences['soft_preferences'] = {}
            
            # Add high-protein to the soft preferences
            if 'dietary' not in user_input.preferences['soft_preferences']:
                user_input.preferences['soft_preferences']['dietary'] = []
            
            if 'high-protein' not in user_input.preferences['soft_preferences']['dietary']:
                user_input.preferences['soft_preferences']['dietary'].append('high-protein')
                print(f"[DEBUG] Added high-protein soft preference due to strength activity detection")
        
        # Generate macro targets
        macro_target = self.generate_macro_targets(user_input)
        return context, macro_target

    def retrieve_context_by_metadata_with_metadata(self, user_input: UserInput) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Retrieve context using metadata-based filtering and return both context and metadata."""
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
                
                if results['documents'] and results['metadatas']:
                    print(f"Found {len(results['documents'])} exact metadata matches")
                    # Return both the content and metadata of the first match
                    return results['documents'][0], results['metadatas'][0]
            except Exception as e:
                print(f"Error in metadata-based retrieval: {e}")
        
        # Fallback to vector search if no exact match
        print("No exact metadata match found, falling back to vector search")
        return self.retrieve_context_fallback(user_input), None

    def _detect_strength_in_retrieved_metadata(self, retrieved_metadata: Optional[Dict[str, Any]], user_input: UserInput) -> bool:
        """
        Detect if the retrieved knowledge document has "strength" in its metadata.
        
        Args:
            retrieved_metadata: Metadata from the retrieved document (if available)
            user_input: UserInput object with user context
            
        Returns:
            True if strength activity is detected, False otherwise
        """
        # First check the retrieved metadata if available
        if retrieved_metadata:
            if retrieved_metadata.get('type_of_activity') == 'strength':
                print(f"[DEBUG] Detected strength activity in metadata: {retrieved_metadata}")
                return True
        
        # Fallback: check if exercise_type contains "strength" keywords
        if user_input.exercise_type:
            strength_keywords = ['strength', 'weight', 'lift', 'gym', 'resistance', 'plyometric']
            exercise_type_lower = user_input.exercise_type.lower()
            for keyword in strength_keywords:
                if keyword in exercise_type_lower:
                    print(f"[DEBUG] Detected strength activity from exercise_type: {user_input.exercise_type}")
                    return True
        
        return False

    def extract_key_principles(self, context: str, num_principles: int = 2) -> List[str]:
        """
        Extract key principles from the knowledge document context.
        Specifically targets the key_principles: section and returns random principles.
        
        Args:
            context: The knowledge document content
            num_principles: Number of principles to extract (default: 2)
            
        Returns:
            List of key principles as strings
        """
        principles = []
        
        # Split context into lines
        lines = context.split('\n')
        
        # First, try to find the specific "key_principles:" section
        in_key_principles_section = False
        for line in lines:
            line = line.strip()
            
            # Check if we're entering the key_principles section
            if line.lower() == 'key_principles:' or line.lower() == 'key principles:':
                in_key_principles_section = True
                continue
            
            # Check if we're leaving the key_principles section (next section starts)
            if in_key_principles_section and (line.lower() == 'avoid:' or line.lower() == 'timing:' or line.startswith('---')):
                break
            
            # If we're in the key_principles section, look for bullet points
            if in_key_principles_section:
                if (line.startswith('- ') or 
                    line.startswith('-   ') or
                    line.startswith('* ') or 
                    line.startswith('• ')):
                    
                    # Clean up the principle text
                    principle = line.lstrip('- *• ')
                    if principle and len(principle) > 10:  # Ensure it's substantial
                        principles.append(principle)
        
        # Return random selection if we have more than requested
        if len(principles) > num_principles:
            return random.sample(principles, num_principles)
        else:
            return principles[:num_principles]
    
    def extract_fields_from_query(self, user_query: str) -> Dict[str, Any]:
        """
        Extract structured fields from user query using OpenAI LLM.
        
        Args:
            user_query: Natural language user query
            
        Returns:
            Dict with extracted fields in the expected format
        """
        if not self.llm:
            print("No LLM available, using fallback field extraction")
            return self._fallback_field_extraction(user_query)
        
        system_prompt = """You're an API that extracts structured nutrition planning fields from a user query.

Extract and return the following fields:

{
  "age": int or null,
  "weight_lb": int or null,
  "activity_type": "cardio" | "strength" | null,
  "duration_minutes": int or null,
  "calorie_cap": int or null,
  "soft_preferences": {
    "flavor": [string] (can contain multiple flavors),
    "texture": [string] (can contain multiple textures),
    "price_dollars": float or null
  },
  "hard_filters": {
    "dietary": [string] (can contain multiple dietary requirements),
    "allergens": [string] (can contain multiple allergens)
  }
}

If a value is not specified in the user query, return null or an empty list.

Use the vocabularies below as guidance. Interpret user preferences loosely but return standardized values only from the vocab lists when possible. If a preference doesn't match any known item, return null.

**ACTIVITY TYPE GUIDELINES:**

Classify the user's activity into one of the following two groups:

- Cardio: soccer game, volleyball practice, light run, swimming, badminton, HIIT
- Strength: gym workout, weightlifting competition, plyometrics, resistance band training, bodyweight exercises

**SOFT PREFERENCE VOCABULARY:**

- Flavor: sweet, salty, savory, tangy, chocolate, vanilla, fruity, nutty, spicy, umami
- Texture: crunchy, chewy, smooth, creamy, crispy, soft

**HARD CONSTRAINT VOCABULARY:**

- Dietary: gluten-free, vegan, vegetarian, keto, paleo, high-protein, low-sugar, no-sugar, low-carb, high-fiber, dairy-free, soy-free, organic, non-gmo
- Allergens: peanuts, milk, eggs, wheat, soy, tree-nuts, fish, shellfish

---
**Example query:**
"I'm an 18-year-old guy, weigh 160 pounds. I want savory, chewy snacks for my 90-minute soccer match to fuel recovery. I'm lactose intolerant and I'd like to be gluten-free. Keep it under 400 calories"

**Extracted output:**
```json
{
  "age": 18,
  "weight_lb": 160,
  "activity_type": "cardio",
  "duration_minutes": 90,
  "calorie_cap": 400,
  "soft_preferences": {
    "flavor": ["savory"],
    "texture": ["chewy"],
    "price_dollars": null
  },
  "hard_filters": {
    "dietary": ["gluten-free"],
    "allergens": ["milk"]
  }
}
```

Return ONLY valid JSON. No additional text or explanation."""

        human_prompt = f"Extract fields from this query: {user_query}"
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = self.llm.invoke(messages)
            extracted_data = json.loads(response.content)
            
            print(f"[DEBUG] LLM extracted fields: {extracted_data}")
            return extracted_data
            
        except Exception as e:
            print(f"Error in LLM field extraction: {e}")
            return self._fallback_field_extraction(user_query)
    
    def _fallback_field_extraction(self, user_query: str) -> Dict[str, Any]:
        """
        Fallback field extraction using simple rule-based parsing.
        
        Args:
            user_query: Natural language user query
            
        Returns:
            Dict with basic extracted fields
        """
        query_lower = user_query.lower()
        
        # Basic extraction patterns
        age = None
        weight_lb = None
        activity_type = None
        duration_minutes = None
        calorie_cap = None
        
        # Try to extract age
        if "year" in query_lower or "age" in query_lower:
            import re
            age_match = re.search(r'(\d+)[-\s]*year', query_lower)
            if age_match:
                age = int(age_match.group(1))
        
        # Try to extract weight
        if "pound" in query_lower or "lb" in query_lower:
            import re
            weight_match = re.search(r'(\d+)[-\s]*(?:pound|lb)', query_lower)
            if weight_match:
                weight_lb = int(weight_match.group(1))
        
        # Try to extract activity type
        cardio_keywords = ['soccer', 'volleyball', 'run', 'swimming', 'badminton', 'hiit', 'cardio', 'workout']
        strength_keywords = ['gym', 'weight', 'lifting', 'strength', 'resistance', 'bodyweight']
        
        if any(keyword in query_lower for keyword in cardio_keywords):
            activity_type = "cardio"
        elif any(keyword in query_lower for keyword in strength_keywords):
            activity_type = "strength"
        
        # Try to extract duration
        if "minute" in query_lower:
            import re
            duration_match = re.search(r'(\d+)[-\s]*minute', query_lower)
            if duration_match:
                duration_minutes = int(duration_match.group(1))
        
        # Try to extract calorie cap
        if "calorie" in query_lower:
            import re
            calorie_match = re.search(r'(\d+)[-\s]*calorie', query_lower)
            if calorie_match:
                calorie_cap = int(calorie_match.group(1))
        
        return {
            "age": age,
            "weight_lb": weight_lb,
            "activity_type": activity_type,
            "duration_minutes": duration_minutes,
            "calorie_cap": calorie_cap,
            "soft_preferences": {
                "flavor": [],
                "texture": [],
                "price_dollars": None
            },
            "hard_filters": {
                "dietary": [],
                "allergens": []
            }
        }
    
    def _convert_extracted_fields_to_user_input(self, extracted_fields: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """
        Convert LLM-extracted fields to UserInput model format.
        
        Args:
            extracted_fields: Fields extracted by LLM
            original_query: Original user query
            
        Returns:
            Dict suitable for UserInput model creation
        """
        user_input_data = {
            "user_query": original_query,
            "age": extracted_fields.get("age"),
            "exercise_type": extracted_fields.get("activity_type"),
            "exercise_duration_minutes": extracted_fields.get("duration_minutes"),
        }
        
        # Convert weight from pounds to kg
        weight_lb = extracted_fields.get("weight_lb")
        if weight_lb:
            user_input_data["weight_kg"] = round(weight_lb * 0.453592, 1)
        
        # Store additional preferences in the preferences JSON field
        preferences = {
            "calorie_cap": extracted_fields.get("calorie_cap"),
            "soft_preferences": extracted_fields.get("soft_preferences", {}),
            "hard_filters": extracted_fields.get("hard_filters", {})
        }
        
        # Remove null values to keep JSON clean
        preferences = {k: v for k, v in preferences.items() if v is not None}
        if preferences:
            user_input_data["preferences"] = preferences
        
        return user_input_data 