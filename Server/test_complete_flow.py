"""
Complete Flow Test - NLP to Orchestrator
=========================================

Tests the entire pipeline:
1. Teacher utterance (any Indian language)
2. NLP processing (translation to English)
3. Orchestrator (tool selection & execution)
4. Final result

Run: python test_complete_flow.py
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from nlp import GeminiProcessor, TeacherUtterance
from orchestrator import ChanakyaOrchestrator, OrchestratorInput


async def test_complete_flow():
    """Test the complete flow from utterance to result."""
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
        return
    
    print("🚀 Initializing Chanakya System...")
    print("=" * 70)
    
    # Initialize NLP processor
    nlp_processor = GeminiProcessor(api_key=api_key)
    print("✅ NLP Processor initialized")
    
    # Initialize orchestrator
    orchestrator = ChanakyaOrchestrator(api_key=api_key)
    print("✅ Orchestrator initialized")
    print()
    
    # Test utterances in different languages
    test_utterances = [
        {
            "text": "Pythagoras theorem kaise sikhaun?",
            "language": "Hindi (mixed with English)",
            "context": {"grade": "Class 8", "subject": "Mathematics"}
        },
        {
            "text": "बच्चे शोर मचा रहे हैं और ध्यान नहीं दे रहे",
            "language": "Hindi",
            "context": {"grade": "Class 6", "class_size": 50}
        },
        {
            "text": "How can I teach negative numbers to my students?",
            "language": "English",
            "context": {"grade": "Class 7", "subject": "Mathematics"}
        },
        {
            "text": "Students are completely out of control, talking and fighting",
            "language": "English",
            "context": {"grade": "Class 5", "class_size": 45}
        },
        {
            "text": "Photosynthesis ka activity chahiye",
            "language": "Hindi (mixed with English)",
            "context": {"grade": "Class 6", "subject": "Science"}
        },
    ]
    
    session_id = "complete-flow-test-001"
    
    for i, test in enumerate(test_utterances, 1):
        print("=" * 70)
        print(f"📢 Test {i}: Teacher Utterance")
        print("=" * 70)
        print(f"🗣️  Original: {test['text']}")
        print(f"🌐 Language: {test['language']}")
        print(f"📚 Context: {test.get('context', {})}")
        print()
        
        # STEP 1: NLP Processing
        print("🔄 STEP 1: NLP Processing...")
        print("-" * 70)
        
        utterance = TeacherUtterance(text=test["text"])
        nlp_result = await nlp_processor.process(utterance)
        
        print(f"✅ English Understanding: {nlp_result.english_understanding}")
        print(f"🔍 Detected Language: {nlp_result.detected_language}")
        print(f"📊 Confidence: {nlp_result.confidence:.2f}")
        print(f"⏱️  Processing Time: {nlp_result.processing_time_ms:.2f}ms")
        
        if nlp_result.error:
            print(f"⚠️  NLP Error: {nlp_result.error}")
            print()
            continue
        
        print()
        
        # STEP 2: Orchestrator Processing
        print("🔄 STEP 2: Orchestrator Processing...")
        print("-" * 70)
        
        # Use the English understanding from NLP as the query
        orchestrator_input = OrchestratorInput(
            query=nlp_result.english_understanding,
            context=test.get("context"),
            session_id=session_id
        )
        
        orchestrator_result = await orchestrator.process(orchestrator_input)
        
        print(f"🔧 Tool Selected: {orchestrator_result.tool_used}")
        print(f"💭 Reasoning: {orchestrator_result.reasoning}")
        print(f"📊 Confidence: {orchestrator_result.confidence:.2f}")
        print(f"⏱️  Processing Time: {orchestrator_result.processing_time_ms:.2f}ms")
        
        if orchestrator_result.error:
            print(f"❌ Error: {orchestrator_result.error}")
            print()
            continue
        
        print()
        
        # STEP 3: Display Final Result
        print("🎯 STEP 3: Final Result")
        print("-" * 70)
        
        activity = orchestrator_result.result
        
        print(f"📌 {activity.activity_name}")
        print(f"📝 {activity.description}")
        print(f"⏰ Duration: {activity.duration_minutes} minutes")
        print()
        
        print("📦 Materials Needed:")
        for material in activity.materials_needed:
            print(f"   • {material}")
        print()
        
        print("📝 Steps:")
        for step in activity.steps:
            print(f"   {step}")
        print()
        
        print(f"🎓 Learning Outcome: {activity.learning_outcome}")
        
        if activity.tips:
            print()
            print("💡 Tips:")
            for tip in activity.tips:
                print(f"   • {tip}")
        
        print()
        print("✅ Complete flow executed successfully!")
        print()
    
    # Show conversation history
    print("=" * 70)
    print("📜 Conversation History (All Interactions)")
    print("=" * 70)
    ctx = orchestrator.get_context(session_id)
    if ctx:
        print(f"Total messages: {len(ctx.messages)}")
        print()
        for msg in ctx.messages:
            role_emoji = "👨‍🏫" if msg.role == "user" else "🤖"
            print(f"{role_emoji} [{msg.role.upper()}] {msg.content[:100]}...")
    
    print()
    print("=" * 70)
    print("🎉 All tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_complete_flow())
