"""
Chanakya NLP Layer - Test Runner
================================

Simple test runner to validate NLP pipeline with example cases.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from nlp.pipeline import NLPPipeline, PipelineConfig
from nlp.schemas import TeacherUtterance, ClassroomContext, NLPOutput
from nlp.governance import GovernanceValidator, ExplainabilityGenerator
from nlp.examples import ALL_EXAMPLES, HINDI_EXAMPLES


def run_single_test(
    pipeline: NLPPipeline,
    example: Dict[str, Any],
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run a single test case.
    
    Returns:
        Dict with test results
    """
    utterance = TeacherUtterance(
        text=example["input"]["text"],
        timestamp=datetime.utcnow()
    )
    
    # Run pipeline
    try:
        output = pipeline.process_sync(utterance)
        
        result = {
            "id": example["id"],
            "description": example["description"],
            "success": True,
            "input": example["input"]["text"],
            "output": {
                "classroom_state": output.classroom_state.value,
                "teacher_intent": output.teacher_intent.value,
                "urgency": output.urgency.value,
                "topic": output.topic.value,
                "detected_language": output.detected_language.value,
                "confidence": output.confidence,
                "english_translation": output.english_translation
            },
            "expected": example.get("expected_output", {}),
            "processing_time_ms": output.processing_time_ms
        }
        
        # Check matches
        expected = example.get("expected_output", {})
        matches = {
            "classroom_state": output.classroom_state.value == expected.get("classroom_state"),
            "teacher_intent": output.teacher_intent.value == expected.get("teacher_intent"),
            "urgency": output.urgency.value == expected.get("urgency"),
            "topic": output.topic.value == expected.get("topic"),
            "detected_language": output.detected_language.value == expected.get("detected_language")
        }
        result["matches"] = matches
        result["all_matched"] = all(matches.values())
        
    except Exception as e:
        result = {
            "id": example["id"],
            "description": example["description"],
            "success": False,
            "error": str(e),
            "input": example["input"]["text"]
        }
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Test: {example['id']} - {example['description']}")
        print(f"Input: {example['input']['text']}")
        if result.get("success"):
            print(f"State: {result['output']['classroom_state']} (expected: {example.get('expected_output', {}).get('classroom_state')})")
            print(f"Intent: {result['output']['teacher_intent']} (expected: {example.get('expected_output', {}).get('teacher_intent')})")
            print(f"Urgency: {result['output']['urgency']}")
            print(f"Language: {result['output']['detected_language']}")
            print(f"Confidence: {result['output']['confidence']:.2f}")
            print(f"Translation: {result['output']['english_translation']}")
            print(f"Time: {result['processing_time_ms']:.0f}ms")
            print(f"All Matched: {'✅' if result.get('all_matched') else '❌'}")
        else:
            print(f"Error: {result.get('error')}")
    
    return result


def run_all_tests(api_key: str, examples: List[Dict] = None) -> Dict[str, Any]:
    """
    Run all test cases.
    
    Args:
        api_key: Gemini API key
        examples: List of examples to test (defaults to ALL_EXAMPLES)
        
    Returns:
        Summary of test results
    """
    if examples is None:
        examples = ALL_EXAMPLES
    
    # Create pipeline
    config = PipelineConfig(
        enable_audit_logging=True,
        strict_validation=False
    )
    pipeline = NLPPipeline(
        gemini_api_key=api_key,
        config=config
    )
    
    results = []
    for example in examples:
        result = run_single_test(pipeline, example)
        results.append(result)
    
    # Summary
    total = len(results)
    successful = sum(1 for r in results if r.get("success"))
    matched = sum(1 for r in results if r.get("all_matched"))
    
    summary = {
        "total_tests": total,
        "successful": successful,
        "failed": total - successful,
        "all_matched": matched,
        "accuracy": matched / total if total > 0 else 0,
        "results": results
    }
    
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"All classifications matched: {matched}/{total} ({summary['accuracy']*100:.1f}%)")
    
    return summary


def demo_governance_validation(api_key: str):
    """Demonstrate governance validation."""
    
    print("\n" + "="*60)
    print("GOVERNANCE VALIDATION DEMO")
    print("="*60)
    
    config = PipelineConfig()
    pipeline = NLPPipeline(gemini_api_key=api_key, config=config)
    
    validator = GovernanceValidator(min_confidence=0.3)
    explainer = ExplainabilityGenerator()
    
    # Test input
    utterance = TeacherUtterance(
        text="Bachche sun nahi rahe, kya karu?",
        timestamp=datetime.utcnow()
    )
    
    output = pipeline.process_sync(utterance)
    
    # Validate
    violations = validator.validate(output)
    is_valid = validator.is_valid(output)
    
    print(f"\nInput: {utterance.text}")
    print(f"Valid: {is_valid}")
    print(f"Violations: {len(violations)}")
    for v in violations:
        print(f"  - [{v.severity}] {v.rule.value}: {v.message}")
    
    # Generate explanation
    explanation = explainer.generate_explanation(output, for_audience="crp")
    print(f"\nExplanation for CRP:")
    print(f"  Summary (Hindi): {explanation['summary_hi']}")
    print(f"  Teacher need: {explanation['teacher_need_hi']}")
    print(f"  Confidence: {explanation['confidence_level']}")
    print(f"  Urgency: {explanation['urgency_hi']}")


def interactive_demo(api_key: str):
    """Interactive demo for testing custom inputs."""
    
    print("\n" + "="*60)
    print("INTERACTIVE DEMO")
    print("="*60)
    print("Enter teacher utterances to test (type 'quit' to exit)\n")
    
    config = PipelineConfig()
    pipeline = NLPPipeline(gemini_api_key=api_key, config=config)
    explainer = ExplainabilityGenerator()
    
    while True:
        text = input("\nTeacher says: ").strip()
        if text.lower() == 'quit':
            break
        
        if not text:
            continue
        
        utterance = TeacherUtterance(
            text=text,
            timestamp=datetime.utcnow()
        )
        
        try:
            output = pipeline.process_sync(utterance)
            
            print(f"\n--- NLP Output ---")
            print(f"Language: {output.detected_language.value}")
            print(f"Classroom State: {output.classroom_state.value}")
            print(f"Teacher Intent: {output.teacher_intent.value}")
            print(f"Urgency: {output.urgency.value}")
            print(f"Topic: {output.topic.value}")
            print(f"Confidence: {output.confidence:.2f}")
            print(f"Translation: {output.english_translation}")
            
            if output.specific_concept:
                print(f"Specific Concept: {output.specific_concept}")
            if output.student_count_mentioned:
                print(f"Students Mentioned: {output.student_count_mentioned}")
            
            print(f"\nProcessing time: {output.processing_time_ms:.0f}ms")
            
            # CRP explanation
            explanation = explainer.generate_explanation(output, "crp")
            print(f"\n--- For CRP ---")
            print(f"{explanation['summary_hi']}")
            print(f"{explanation['teacher_need_hi']}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    import sys
    
    # Get API key from environment or argument
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable or pass as argument")
        print("Usage: python test_nlp.py <api_key>")
        sys.exit(1)
    
    # Run tests
    print("Chanakya NLP Layer Test Suite")
    print("="*60)
    
    # Run limited tests first (Hindi only for quick validation)
    print("\nRunning Hindi examples...")
    run_all_tests(api_key, HINDI_EXAMPLES[:3])
    
    # Governance demo
    demo_governance_validation(api_key)
    
    # Interactive demo
    interactive_demo(api_key)
