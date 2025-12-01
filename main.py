from dotenv import load_dotenv
from agents.orchestrator_agent import OrchestratorAgent

# Load environment variables (API Key)
load_dotenv()

def main():
    # Initialize the Orchestrator
    orchestrator = OrchestratorAgent()
    
    # Run the interactive loop
    while True:
        try:
            orchestrator.start_session()
        except Exception as e:
            print(f"\n🛑 An unexpected error occurred during the session: {e}")
            
        cont = input("\nStart another session? (y/n): ")
        if cont.lower() != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()