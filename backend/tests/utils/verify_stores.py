#!/usr/bin/env python3
"""
Verification script to check RAG store and Product vector store contents.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_rag_store():
    """Verify RAG store contents."""
    print("=" * 50)
    print("VERIFYING RAG STORE")
    print("=" * 50)
    
    try:
        from app.core.macro_targeting_local import MacroTargetingServiceLocal
        
        # Initialize service (this will load the RAG store)
        service = MacroTargetingServiceLocal()
        
        # Check if store is loaded
        if hasattr(service, '_store') and service._store:
            # Get all documents
            try:
                all_docs = service._store.get(include=["documents", "metadatas"])
                print(f"✅ RAG Store loaded successfully")
                print(f"📊 Total documents: {len(all_docs['documents'])}")
                
                print("\n📋 Document metadata:")
                for i, metadata in enumerate(all_docs['metadatas']):
                    print(f"  Doc {i+1}: {metadata}")
                
                # Test a simple query
                print(f"\n🔍 Testing sample query...")
                test_query = "strength training protein needs"
                results = service._store.similarity_search(test_query, k=1)
                if results:
                    print(f"✅ Query successful - found {len(results)} result(s)")
                    print(f"📄 Sample result: {results[0].page_content[:200]}...")
                else:
                    print("❌ No results found for test query")
                    
            except Exception as e:
                print(f"❌ Error checking RAG store contents: {e}")
        else:
            print("❌ RAG store not loaded")
            
    except Exception as e:
        print(f"❌ Error loading RAG store: {e}")
        import traceback
        traceback.print_exc()

def verify_product_store():
    """Verify Product vector store contents."""
    print("\n" + "=" * 50)
    print("VERIFYING PRODUCT VECTOR STORE")
    print("=" * 50)
    
    try:
        from app.db.vector_store import get_product_vector_store
        
        # Get product vector store
        vector_store = get_product_vector_store()
        
        if hasattr(vector_store, 'vectorstore') and vector_store.vectorstore:
            try:
                # Get all documents
                all_docs = vector_store.vectorstore.get(include=["documents", "metadatas"])
                print(f"✅ Product Store loaded successfully")
                print(f"📊 Total products: {len(all_docs['documents'])}")
                
                # Sample some product metadata
                print(f"\n📋 Sample product metadata:")
                for i in range(min(5, len(all_docs['metadatas']))):
                    metadata = all_docs['metadatas'][i]
                    print(f"  Product {i+1}: {metadata.get('name', 'Unknown')} - {metadata.get('brand', 'Unknown Brand')}")
                
                # Test a query
                print(f"\n🔍 Testing sample query...")
                results = vector_store.vectorstore.similarity_search(
                    "chocolate protein bar", 
                    k=3,
                    filter=None
                )
                if results:
                    print(f"✅ Query successful - found {len(results)} result(s)")
                    for i, result in enumerate(results):
                        metadata = result.metadata
                        print(f"  Result {i+1}: {metadata.get('name', 'Unknown')} - {metadata.get('brand', 'Unknown Brand')}")
                else:
                    print("❌ No results found for test query")
                    
            except Exception as e:
                print(f"❌ Error checking product store contents: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ Product store not loaded")
            
    except Exception as e:
        print(f"❌ Error loading product store: {e}")
        import traceback
        traceback.print_exc()

def verify_database():
    """Verify the SQLite database has products."""
    print("\n" + "=" * 50)
    print("VERIFYING SQLITE DATABASE")
    print("=" * 50)
    
    try:
        from app.db.session import SessionLocal
        from app.db.models import Product
        
        db = SessionLocal()
        try:
            # Count total products
            total_products = db.query(Product).count()
            print(f"✅ Database connected successfully")
            print(f"📊 Total products in database: {total_products}")
            
            # Sample some products
            if total_products > 0:
                sample_products = db.query(Product).limit(5).all()
                print(f"\n📋 Sample products:")
                for i, product in enumerate(sample_products):
                    print(f"  Product {i+1}: {product.name} - {product.brand}")
            else:
                print("❌ No products found in database")
                
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 VERIFYING VECTOR STORES AND DATABASE")
    print("=" * 60)
    
    verify_rag_store()
    verify_product_store() 
    verify_database()
    
    print("\n" + "=" * 60)
    print("✅ VERIFICATION COMPLETE")
