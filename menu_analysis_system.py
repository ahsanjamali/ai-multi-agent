import os
from typing import Dict, List, Tuple
from dataclasses import dataclass
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor
import pypdf
from pathlib import Path



# Data structures
@dataclass
class AgentState:
    messages: List[str]
    next_agent: str
    menu_data: Dict
    current_query: str = ""
    extracted_text: str = ""

class PDFReaderAgent:
    def __init__(self):
        super().__init__("pdf_reader")
    
    def process(self, state: AgentState) -> AgentState:
        try:
            # Sample menu data for testing
            sample_text = """
            APPETIZERS
            
            Spicy Peanut Spring Rolls $8.99
            Fresh vegetables and rice noodles wrapped in rice paper, served with spicy peanut sauce.
            Contains: peanuts, soy, gluten
            
            Classic Caesar Salad $12.99
            Crisp romaine, parmesan, garlic croutons, house-made caesar dressing.
            Contains: dairy, eggs, gluten
            
            MAIN COURSES
            
            Grilled Salmon $24.99
            Fresh Atlantic salmon, lemon butter sauce, seasonal vegetables.
            Contains: fish, dairy
            
            Vegetable Stir-Fry $16.99
            Mixed vegetables, tofu, rice noodles in ginger-soy sauce.
            Contains: soy, gluten
            
            DESSERTS
            
            Chocolate Nut Brownie $7.99
            Warm chocolate brownie, vanilla ice cream, candied walnuts.
            Contains: nuts, dairy, eggs, gluten
            """
            
            state.extracted_text = sample_text
            self.add_message(state, "Successfully loaded menu data")
            state.next_agent = "menu_parser"
            
        except Exception as e:
            state.error = f"Menu processing error: {str(e)}"
            state.next_agent = "error_handler"
            
        return state

class MenuParserAgent:
    def __init__(self):
        self.name = "menu_parser"
        self.llm = ChatOpenAI(model="gpt-4")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a menu parsing expert. Extract all dishes and their ingredients from the given text."),
            ("human", "{text}")
        ])
    
    def process(self, state: AgentState) -> AgentState:
        # Parse menu text into structured format
        chain = self.prompt | self.llm
        parsed_menu = chain.invoke({"text": state.extracted_text})
        state.menu_data = self._structure_menu_data(parsed_menu.content)
        state.next_agent = "ingredient_analyzer"
        return state
    
    def _structure_menu_data(self, text: str) -> Dict:
        # Implementation would parse LLM output into structured format
        return {}

class IngredientAnalyzerAgent:
    def __init__(self):
        self.name = "ingredient_analyzer"
        self.llm = ChatOpenAI(model="gpt-4")
    
    def process(self, state: AgentState) -> AgentState:
        # Analyze ingredients and create searchable database
        state.next_agent = "query_handler"
        return state

class QueryHandlerAgent:
    def __init__(self):
        self.name = "query_handler"
        self.llm = ChatOpenAI(model="gpt-4")
        
    def process(self, state: AgentState) -> AgentState:
        # Process user query against menu database
        state.next_agent = "end"
        return state

# Graph construction
def create_menu_analysis_graph() -> Graph:
    # Initialize agents
    pdf_reader = PDFReaderAgent()
    menu_parser = MenuParserAgent()
    ingredient_analyzer = IngredientAnalyzerAgent()
    query_handler = QueryHandlerAgent()
    
    # Create workflow graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("pdf_reader", pdf_reader.process)
    workflow.add_node("menu_parser", menu_parser.process)
    workflow.add_node("ingredient_analyzer", ingredient_analyzer.process)
    workflow.add_node("query_handler", query_handler.process)
    
    # Add edges
    workflow.add_edge("pdf_reader", "menu_parser")
    workflow.add_edge("menu_parser", "ingredient_analyzer")
    workflow.add_edge("ingredient_analyzer", "query_handler")
    
    # Set entry and exit points
    workflow.set_entry_point("pdf_reader")
    workflow.add_terminal_node("end")
    
    return workflow.compile()

# Main interface
class MenuAnalysisSystem:
    def __init__(self):
        self.graph = create_menu_analysis_graph()
    
    def process_menu(self, pdf_path: str) -> None:
        initial_state = AgentState(
            messages=[],
            next_agent="pdf_reader",
            menu_data={},
            extracted_text=""
        )
        self.graph.invoke(initial_state)
    
    def query(self, question: str) -> str:
        # Implementation would process query through agents
        return "Query response would go here"
    

if __name__ == "__main__":
    # Initialize system
    system = MenuAnalysisSystem(use_voice=False)
    
    # Process menu
    system.process_menu("menu.pdf")
    
    # Query examples
    print(system.query("Which dishes contain nuts?"))
    print(system.query("What should I avoid if I'm allergic to dairy?"))