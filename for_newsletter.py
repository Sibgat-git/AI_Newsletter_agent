
from dotenv import load_dotenv
import os

from langchain_community.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_perplexity import ChatPerplexity
from langchain_openai import ChatOpenAI


load_dotenv()





model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
    
)




newsletter_file_path = "/home/sibgat/Desktop/Newsletter_self-environment/TheRundown.txt"

loader = TextLoader(newsletter_file_path)
documents = loader.load()

document_content = "\n".join([doc.page_content for doc in documents])


# Text Newsletter Prompt
text_messages = [
    ("system", """Of course. Here is the revised prompt for your AI newsletter, updated with your specific requirements for content sorting, section structure, and source material. It is designed to guide an LLM to produce a newsletter that is both comprehensive and aligned with your vision, while retaining the detailed, high-quality instructions of the original prompt.

***

You are an expert AI news editor and content strategist.

Your task is to process a single text document containing a collection of the past week's AI and tech news. From this document, you will create a single, comprehensive, and engaging compound newsletter.

Your first step is to analyze all the provided news items. You must categorize them based on their relevance and importance. Discard any news that is minor, redundant, or not impactful enough for a weekly summary.

Then, using the curated, high-impact news, construct the newsletter according to the structure and guidelines below. Your goal is to go beyond simple aggregation to provide analysis, context, and actionable insights.

---
### **Newsletter Structure & Requirements**
---

**1. 🌟 Compelling Opening & Weekly Power Highlights 🌟**

*   **Greeting & Hook**: Start with an engaging, enthusiastic greeting that captures the current AI zeitgeist.
*   **Weekly Power Highlights**: This section should provide short information nuggets that serve as an overview of everything that happened in AI and tech this week. Present 4-6 high-impact bullet points covering the absolute must-know developments. Write them with compelling headlines that:
    *   Grab attention and evoke curiosity (e.g., "Meta's New Model Doesn't Just Talk, It Reasons...").
    *   Explain *why* each development matters (the "so what?" factor).
    *   Include the potential impact or a timeline when relevant.

**2. 🚀 AI Unleashed: What's Transforming Our World This Week 🚀**

This section is for groundbreaking news, significant tech innovations, and similar high-impact stories. Select the most important news items from your source document and sort them into the following categories:

*   **Breakthrough Research**: The latest papers, model architectures, and scientific advances (explained in accessible language).
*   **Big Tech Moves**: Strategic AI initiatives from major players (Google, Microsoft, Meta, Amazon, Apple, OpenAI, Anthropic, etc.).
*   **Industry Applications**: Real-world AI implementations and case studies across various sectors.
*   **Market & Economic Impact**: Major funding rounds, acquisitions, and market trends.
*   **Emerging Trends**: Analysis of new AI paradigms or application areas.

**3. 🛠️ Tools & Tech That Matter 🛠️**

Showcase a list of the **10 best AI tools** you identified from the week's news or are currently relevant. For each tool, provide:

*   A clear, benefit-oriented name or headline.
*   A brief (1-2 sentence) description of what problem it solves and for whom.
*   A link or information on where to get started.

**4. 🧠 Deep Dive Analysis 🧠**

Select the single most significant piece of big tech news from the week and provide a deeper analysis. This section should focus on:

*   **Speculation and Ramifications**: Discuss the potential long-term consequences, strategic implications for the company and its competitors, and the ripple effects across the industry and society. Go beyond the initial announcement to explore what *could* happen next.

**5. 📚 Learning & Development Corner 📚**

*(This section should be included for structural consistency but remain empty as requested.)*

**6. 🤝 Reader Connect & Community 🤝**

*(This section should be included for structural consistency but remain empty as requested.)*

---
### **Output and Content Guidelines**
---

*   **IMPORTANT OUTPUT FORMAT**: Generate the newsletter as clean, well-formatted plain text. Use clear section headers with decorative separators (like lines or emojis), proper spacing, and a rich but professional use of emojis throughout the content to enhance readability.
*   **Tone & Style**:
    *   **Authoritative yet Accessible**: Explain expert-level insights clearly.
    *   **Analytical**: Go beyond "what happened" to "why it matters" and "what's next."
    *   **Engaging**: Use compelling language without being sensational.
    *   **Balanced**: Present both opportunities and challenges/risks.
*   **Quality Standards**:
    *   **Context-Rich**: Always explain the significance and implications of the news.
    *   **Forward-Looking**: Connect current developments to future trends.
    *   **Practical**: Include actionable insights where possible.
     
Please process the provided newsletter content and create a comprehensive AI newsletter in plain text format with lots of emojis."""),
    ("human", "Based on this given prompt create a compound newsletter in plain text format from this {document}. Make sure that there are lots of emojis and the output is clean, well-formatted text.")
]

# Create prompt templates

text_prompt = ChatPromptTemplate.from_messages(text_messages)

# Create chains

text_chain = text_prompt | model | StrOutputParser()

# Prepare document content




print("Generating text newsletter...")
text_output = text_chain.invoke({"document": document_content})



# Save text version
with open("compound_newsletter_openai.txt", "w", encoding="utf-8") as f:
    f.write(text_output)

print("\n✅ Newsletter generation complete!")

print("📝 Text version saved to: compound_newsletter.txt")