import extension_entry

def test_extension():
    print("--- 🔬 Testing Metis Memory Extension Hooks ---")
    
    # 1. Test Session Start
    print("\n[1] Testing on_session_start()...")
    success = extension_entry.on_session_start()
    if success:
        print("✅ Session start hook executed successfully.")
    else:
        print("❌ Session start hook failed.")

    # 2. Test Context Provider
    print("\n[2] Testing provide_context()...")
    test_query = "What did we discuss about Ippokampos and session indexes?"
    context = extension_entry.provide_context(test_query)
    
    if context and "RELEVANT MEMORIES" in context:
        print("✅ Context injection confirmed.")
        print("\nCaptured Context Snippet:")
        print("-" * 40)
        # Show first 200 chars of the context
        print(context[:400] + "...")
        print("-" * 40)
    else:
        print("❌ Context injection failed or no relevant memories found.")
        print(f"Returned: {context}")

if __name__ == "__main__":
    test_extension()
