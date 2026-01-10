"""
Chanakya Orchestrator
=====================

LangGraph-based orchestrator that handles context, understands queries,
and routes to appropriate tools.
"""

import json
import time
import uuid
from typing import Optional, Dict, Any, TypedDict, Annotated, Sequence
from google import genai
from google.genai import types

from .schemas import (
    OrchestratorInput,
    OrchestratorOutput,
    ActivityOutput,
    ConversationContext,
    ConversationMessage,
)
from .tools import ActivityGeneratorTool


# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


# =============================================================================
# State Definition
# =============================================================================

class OrchestratorState(TypedDict):
    """State that flows through the orchestrator graph."""
    
    # Input
    query: str
    context: Optional[dict]
    session_id: str
    
    # Processing state
    messages: Annotated[Sequence[dict], add_messages]
    intent: Optional[str]
    selected_tool: Optional[str]
    tool_reasoning: Optional[str]
    
    # Output
    tool_result: Optional[dict]
    error: Optional[str]


# =============================================================================
# Router Prompt
# =============================================================================

ROUTER_PROMPT = """You are Chanakya's intelligent router for a classroom support system.

Your job is to understand the teacher's query and decide which tool to use.

AVAILABLE TOOLS:
1. "activity_generator" - Use when the teacher wants a hands-on activity, demonstration, or interactive exercise to help students understand a concept. This tool generates simple classroom activities using basic materials.

FUTURE TOOLS (not yet available, do NOT select these):
- "content_explainer" - For explaining concepts
- "assessment_creator" - For creating quizzes/tests
- "classroom_management" - For behavior/attention issues

ANALYZE THE QUERY AND RESPOND WITH JSON:
{
    "selected_tool": "activity_generator",
    "reasoning": "Brief explanation of why this tool was selected",
    "extracted_topic": "The main topic/concept the teacher wants to address",
    "confidence": 0.95
}

EXAMPLES:

Query: "How can I teach fractions in a fun way?"
Response: {"selected_tool": "activity_generator", "reasoning": "Teacher wants an engaging method to teach fractions - activity would help", "extracted_topic": "fractions", "confidence": 0.95}

Query: "Students are not understanding photosynthesis"
Response: {"selected_tool": "activity_generator", "reasoning": "Teacher needs help making photosynthesis understandable - a hands-on activity would demonstrate the concept", "extracted_topic": "photosynthesis", "confidence": 0.90}

Query: "Give me an activity for teaching addition with carry"
Response: {"selected_tool": "activity_generator", "reasoning": "Teacher explicitly asked for an activity", "extracted_topic": "addition with carry", "confidence": 0.98}

Query: "बच्चों को गुणा समझाने का कोई तरीका बताओ"
Response: {"selected_tool": "activity_generator", "reasoning": "Teacher wants a way to teach multiplication - activity tool can help", "extracted_topic": "multiplication", "confidence": 0.92}

RULES:
- Return ONLY valid JSON
- For now, always select "activity_generator" as it's the only available tool
- Extract the topic/concept clearly
- Set confidence based on how clearly the query matches the tool's purpose"""


# =============================================================================
# Orchestrator Class
# =============================================================================

class ChanakyaOrchestrator:
    """
    LangGraph-based orchestrator for Chanakya classroom support system.
    
    Handles:
    - Context management across conversations
    - Query understanding and intent classification
    - Tool selection and execution
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the orchestrator.
        
        Args:
            api_key: Google AI API key for Gemini
        """
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
        # Initialize tools
        self.tools = {
            "activity_generator": ActivityGeneratorTool(api_key=api_key)
        }
        
        # Conversation contexts (in production, use a proper store)
        self.contexts: Dict[str, ConversationContext] = {}
        
        # Build the LangGraph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Create the graph
        workflow = StateGraph(OrchestratorState)
        
        # Add nodes
        workflow.add_node("understand_query", self._understand_query_node)
        workflow.add_node("select_tool", self._select_tool_node)
        workflow.add_node("execute_tool", self._execute_tool_node)
        
        # Define edges
        workflow.set_entry_point("understand_query")
        workflow.add_edge("understand_query", "select_tool")
        workflow.add_edge("select_tool", "execute_tool")
        workflow.add_edge("execute_tool", END)
        
        # Compile
        return workflow.compile()
    
    async def _understand_query_node(self, state: OrchestratorState) -> dict:
        """
        Node: Understand and enrich the query with context.
        """
        query = state["query"]
        session_id = state["session_id"]
        
        # Get or create conversation context
        if session_id not in self.contexts:
            self.contexts[session_id] = ConversationContext(session_id=session_id)
        
        ctx = self.contexts[session_id]
        
        # Add user message to context
        ctx.add_message("user", query)
        
        # For now, just pass through (future: context enrichment)
        return {
            "messages": [{"role": "user", "content": query}],
            "intent": None,  # Will be set by router
        }
    
    async def _select_tool_node(self, state: OrchestratorState) -> dict:
        """
        Node: Select the appropriate tool based on the query.
        """
        query = state["query"]
        
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part(text=f"Route this teacher query: {query}")]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=ROUTER_PROMPT,
                    temperature=0.1,
                    max_output_tokens=256,
                    response_mime_type="application/json"
                )
            )
            
            # Parse response
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            parsed = json.loads(text.strip())
            
            return {
                "selected_tool": parsed.get("selected_tool", "activity_generator"),
                "tool_reasoning": parsed.get("reasoning", "Default selection"),
                "intent": parsed.get("extracted_topic", query),
            }
            
        except Exception as e:
            # Default to activity generator on error
            return {
                "selected_tool": "activity_generator",
                "tool_reasoning": f"Default selection (router error: {str(e)})",
                "intent": query,
            }
    
    async def _execute_tool_node(self, state: OrchestratorState) -> dict:
        """
        Node: Execute the selected tool.
        """
        tool_name = state["selected_tool"]
        topic = state["intent"] or state["query"]
        context = state.get("context")
        
        if tool_name not in self.tools:
            return {
                "tool_result": None,
                "error": f"Unknown tool: {tool_name}"
            }
        
        try:
            tool = self.tools[tool_name]
            result = await tool.run(topic, context)
            
            # Convert to dict for storage
            return {
                "tool_result": result.model_dump(),
                "error": None
            }
            
        except Exception as e:
            return {
                "tool_result": None,
                "error": str(e)
            }
    
    async def process(self, input_data: OrchestratorInput) -> OrchestratorOutput:
        """
        Process a query through the orchestrator.
        
        Args:
            input_data: The orchestrator input
        
        Returns:
            OrchestratorOutput with the tool result
        """
        start_time = time.time()
        
        # Create session ID if not provided
        session_id = input_data.session_id or str(uuid.uuid4())
        
        # Initial state
        initial_state: OrchestratorState = {
            "query": input_data.query,
            "context": input_data.context,
            "session_id": session_id,
            "messages": [],
            "intent": None,
            "selected_tool": None,
            "tool_reasoning": None,
            "tool_result": None,
            "error": None,
        }
        
        try:
            # Run the graph
            final_state = await self.graph.ainvoke(initial_state)
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            # Build output
            if final_state.get("error"):
                return OrchestratorOutput(
                    tool_used=final_state.get("selected_tool", "none"),
                    reasoning=final_state.get("tool_reasoning", ""),
                    result={},
                    confidence=0.0,
                    processing_time_ms=processing_time_ms,
                    error=final_state["error"]
                )
            
            # Parse result based on tool
            result = final_state.get("tool_result", {})
            if final_state.get("selected_tool") == "activity_generator":
                result = ActivityOutput(**result)
            
            # Update conversation context
            if session_id in self.contexts:
                self.contexts[session_id].add_message(
                    "assistant",
                    f"Generated activity: {result.activity_name if isinstance(result, ActivityOutput) else 'Response'}"
                )
            
            return OrchestratorOutput(
                tool_used=final_state.get("selected_tool", "activity_generator"),
                reasoning=final_state.get("tool_reasoning", ""),
                result=result,
                confidence=0.9,
                processing_time_ms=processing_time_ms,
                error=None
            )
            
        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000
            
            return OrchestratorOutput(
                tool_used="none",
                reasoning="Error occurred during processing",
                result={},
                confidence=0.0,
                processing_time_ms=processing_time_ms,
                error=str(e)
            )
    
    def process_sync(self, input_data: OrchestratorInput) -> OrchestratorOutput:
        """Synchronous version of process()."""
        import asyncio
        return asyncio.run(self.process(input_data))
    
    def get_context(self, session_id: str) -> Optional[ConversationContext]:
        """Get conversation context for a session."""
        return self.contexts.get(session_id)
    
    def clear_context(self, session_id: str) -> bool:
        """Clear conversation context for a session."""
        if session_id in self.contexts:
            del self.contexts[session_id]
            return True
        return False
