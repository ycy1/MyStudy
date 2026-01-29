import sys
import langchain
import openai

def main():
    print("Hello from langchain!")
    print(langchain.__version__)
    print(openai.__version__)
    
    print(sys.version)


if __name__ == "__main__":
    main()
