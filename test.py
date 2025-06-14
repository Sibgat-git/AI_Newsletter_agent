from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_perplexity import ChatPerplexity


load_dotenv()



model = ChatPerplexity(
    model="llama-3.1-sonar-small-128k-online",
    temperature=0.7
    
)




newsletter_file_path = "/home/sibgat/Desktop/Newsletter/langchain-crash-course/newsletters.txt"

loader = TextLoader(newsletter_file_path)
documents = loader.load()

document_content = "\n".join([doc.page_content for doc in documents])

# HTML Newsletter Prompt
html_messages = [
    ("system", """You are an expert AI news editor and content strategist. 
Your task is to take multiple email newsletters about AI news (which I will provide) and compile them into a single, comprehensive, and engaging compound newsletter. 
This newsletter should go beyond simple aggregation to provide analysis, context, and actionable insights.

Newsletter Structure & Requirements:

1. Compelling Opening & Key Highlights

- **Greeting & Hook**: Start with an engaging, enthusiastic greeting that captures the current AI zeitgeist
- **Weekly Power Highlights**: Present 4-6 high-impact bullet points covering the absolute must-know developments, written with compelling headlines that:
    - Grab attention and evoke curiosity
    - Explain why each development matters (the \"so wh...

Ensure the output is valid and well-formed HTML."""),
    ("human", "Based on this given prompt create a compound newsletter in HTML format from this {document}. Make sure that there are lots of emojis and the output is clean, well-formatted HTML.")
]

# Text Newsletter Prompt
text_messages = [
    ("system", """Your task is to act as an expert AI newsletter generator. Given the raw content from various AI newsletters, your goal is to synthesize this information into a single, cohesive, plain-text compound newsletter. 

Key Principles for Generation:

- **Comprehensive**: Cover all significant developments
- **Contextual**: Provide background and significance and implications
- **Forward-Looking**: Connect current developments to future trends
- **Practical**: Include actionable insights where possible
- **Diverse Perspectives**: Cover technical, business, ethical, and societal angles

The final output MUST be clean, well-formatted, plain text, with ample emojis."""),
    ("human", "Based on this given prompt create a compound newsletter in plain text format from this {document}. Make sure that there are lots of emojis and the output is clean, well-formatted text.")
]

# Create prompt templates
html_prompt = ChatPromptTemplate.from_messages(html_messages)
text_prompt = ChatPromptTemplate.from_messages(text_messages)

# Create chains
html_chain = html_prompt | model | StrOutputParser()
text_chain = text_prompt | model | StrOutputParser()

# Prepare document content


print("Generating HTML newsletter...")
html_output = html_chain.invoke({"document": document_content})

print("Generating text newsletter...")
text_output = text_chain.invoke({"document": document_content})

# Save HTML version
with open("compound_newsletter_perplexity.html", "w", encoding="utf-8") as f:
    f.write(html_output)

# Save text version
with open("compound_newsletter_perplexity.txt", "w", encoding="utf-8") as f:
    f.write(text_output)

print("\n✅ Newsletter generation complete!")
print("📄 HTML version saved to: compound_newsletter.html")
print("📝 Text version saved to: compound_newsletter.txt")