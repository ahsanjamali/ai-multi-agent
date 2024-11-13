import os
from menu_analysis_system import MenuAnalysisSystem
import setup  # This will load your API key

def check_environment():
    """Verify that all required environment variables are set"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please make sure you have:\n"
            "1. Created a .env file in your project directory\n"
            "2. Added your API key to the .env file as OPENAI_API_KEY=your-key-here\n"
            "3. The .env file is in the correct location"
        )

def main():
    try:
        # Check environment setup
        check_environment()
        
        # Initialize the system
        print("Initializing Menu Analysis System...")
        system = MenuAnalysisSystem(use_voice=False)
        
        # Process the sample menu data
        print("Loading sample menu data...")
        system.process_menu(None)
        
        # Interactive query loop
        print("\nMenu Analysis System Ready!")
        print("\nYou can ask questions like:")
        print("- Which dishes contain nuts?")
        print("- What should I avoid if I'm allergic to dairy?")
        print("- What appetizers are available?")
        print("\nType 'exit' to quit")
        
        while True:
            try:
                question = input("\nWhat would you like to know about the menu? ")
                
                if question.lower() == 'exit':
                    break
                    
                response = system.query(question)
                print("\nResponse:", response)
                
            except Exception as e:
                print(f"Error processing query: {str(e)}")
                
    except ValueError as e:
        print(f"\nSetup Error: {str(e)}")
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        
    print("\nThank you for using the Menu Analysis System!")

if __name__ == "__main__":
    main()