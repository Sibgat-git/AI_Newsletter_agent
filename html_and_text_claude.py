
from dotenv import load_dotenv
import os

from langchain_community.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

load_dotenv()





model = ChatAnthropic(
    model="claude-3-5-haiku-latest",
    temperature=1,
    api_key=os.getenv("CLAUDE_API_KEY")
    
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
# - **Weekly Power Highlights**: Present 4-6 high-impact bullet points covering the absolute must-know developments, written with compelling headlines that:
    - Grab attention and evoke curiosity
    - Explain why each development matters (the "so what?" factor)
    - Include potential impact or timeline when relevant

2. "AI Unleashed: What's Transforming Our World This Week"

Cover the most significant developments across these key areas:

- **Breakthrough Research**: Latest papers, model architectures, and scientific advances (explained in accessible language)
- **Big Tech Moves**: Strategic AI initiatives from major players (Google, Microsoft, Meta, Amazon, Apple, OpenAI, Anthropic, etc.)
- **Industry Applications**: Real-world AI implementations and case studies across sectors (healthcare, finance, education, manufacturing, etc.)
- **Market & Economic Impact**: Funding rounds, acquisitions, market trends, and economic implications
- **Emerging Trends**: Analysis of new AI paradigms, architectures, or application areas

3. "Tools & Tech That Matter"

Showcase 2-3 innovative AI tools or platforms, providing:

- **Value-driven headlines** that emphasize benefits
- **Practical context**: What problem it solves and for whom
- **Implementation insight**: How it fits into existing workflows
- **Access information**: Where to learn more or get started

4. "Deep Dive Analysis" (Weekly Rotating Focus)

Include one in-depth section that alternates between:

- **Research Spotlight**: Explaining a significant paper or breakthrough
- **Industry Deep Dive**: Comprehensive look at AI transformation in a specific sector
- **Ethics & Society**: Analysis of AI governance, policy, or societal implications
- **Future Watch**: Emerging trends and long-term implications

5. "Learning & Development Corner"

- **Skill Spotlight**: Highlight in-demand AI skills or career opportunities
- **Resource Roundup**: Curated educational content (courses, tutorials, whitepapers)
- **Community Highlights**: Notable open-source projects, influential work, or thought leadership

6. "Reader Connect & Community"

- **Engagement Questions**: Thought-provoking questions about featured topics
- **Feedback Request**: Ask for newsletter reviews and improvement suggestions
- **Topic Voting**: Let readers influence future deep-dive topics
- **Community Spotlights**: Feature reader submissions or interesting use cases

7. "Partnership Opportunities"

Professional sponsorship invitation emphasizing reach and engagement with AI enthusiasts and professionals.

**IMPORTANT OUTPUT FORMAT**: Generate the newsletter as a complete, professional HTML document with:
- Full HTML structure (DOCTYPE, html, head, body tags)
- Modern, responsive CSS styling embedded in the head
- Professional color scheme and typography
- Mobile-friendly layout
- Rich use of emojis throughout content
- Clean, newsletter-style formatting with proper spacing and visual hierarchy
- Clickable elements where appropriate

Content Guidelines:

Tone & Style:

- **Authoritative yet Accessible**: Expert-level insights explained clearly
- **Analytical**: Go beyond "what happened" to "why it matters" and "what's next"
- **Engaging**: Compelling but not sensationalized
- **Balanced**: Present both opportunities and challenges/risks

Quality Standards:

- **Context-Rich**: Always explain significance and implications
- **Forward-Looking**: Connect current developments to future trends
- **Practical**: Include actionable insights where possible
- **Diverse Perspectives**: Cover technical, business, ethical, and societal angles

Please process the provided newsletter content and create a comprehensive AI newsletter as a complete HTML document with lots of emojis."""),
    ("human", "Based on this given prompt create a compound newsletter in HTML format from this {document}. Make sure that there are lots of emojis and the output is a complete HTML document with professional styling.")
]

# Text Newsletter Prompt
text_messages = [
    ("system", """You are an expert AI news editor and content strategist. 
Your task is to take multiple email newsletters about AI news (which I will provide) and compile them into a single, comprehensive, and engaging compound newsletter. 
This newsletter should go beyond simple aggregation to provide analysis, context, and actionable insights.

Newsletter Structure & Requirements:

1. Compelling Opening & Key Highlights

- **Greeting & Hook**: Start with an engaging, enthusiastic greeting that captures the current AI zeitgeist
- **Weekly Power Highlights**: Present 4-6 high-impact bullet points covering the absolute must-know developments, written with compelling headlines that:
    - Grab attention and evoke curiosity
    - Explain why each development matters (the "so what?" factor)
    - Include potential impact or timeline when relevant

2. "AI Unleashed: What's Transforming Our World This Week"

Cover the most significant developments across these key areas:

- **Breakthrough Research**: Latest papers, model architectures, and scientific advances (explained in accessible language)
- **Big Tech Moves**: Strategic AI initiatives from major players (Google, Microsoft, Meta, Amazon, Apple, OpenAI, Anthropic, etc.)
- **Industry Applications**: Real-world AI implementations and case studies across sectors (healthcare, finance, education, manufacturing, etc.)
- **Market & Economic Impact**: Funding rounds, acquisitions, market trends, and economic implications
- **Emerging Trends**: Analysis of new AI paradigms, architectures, or application areas

3. "Tools & Tech That Matter"

Showcase 2-3 innovative AI tools or platforms, providing:

- **Value-driven headlines** that emphasize benefits
- **Practical context**: What problem it solves and for whom
- **Implementation insight**: How it fits into existing workflows
- **Access information**: Where to learn more or get started

4. "Deep Dive Analysis" (Weekly Rotating Focus)

Include one in-depth section that alternates between:
The with Statement
The with keyword initiates a context manager in Python. Its primary advantage is ensuring that resources are managed correctly. In this case, the resource is the file being opened. The with statement guarantees that the file will be automatically closed once the indented block of code is finished, or if an error interrupts the process. This prevents potential issues like data corruption or resource leaks.


- **Research Spotlight**: Explaining a significant paper or breakthrough
- **Industry Deep Dive**: Comprehensive look at AI transformation in a specific sector
- **Ethics & Society**: Analysis of AI governance, policy, or societal implications
- **Future Watch**: Emerging trends and long-term implications

5. "Learning & Development Corner"

- **Skill Spotlight**: Highlight in-demand AI skills or career opportunities
- **Resource Roundup**: Curated educational content (courses, tutorials, whitepapers)
- **Community Highlights**: Notable open-source projects, influential work, or thought leadership

6. "Reader Connect & Community"

- **Engagement Questions**: Thought-provoking questions about featured topics
- **Feedback Request**: Ask for newsletter reviews and improvement suggestions
- **Topic Voting**: Let readers influence future deep-dive topics
- **Community Spotlights**: Feature reader submissions or interesting use cases

7. "Partnership Opportunities"

Professional sponsorship invitation emphasizing reach and engagement with AI enthusiasts and professionals.

**IMPORTANT OUTPUT FORMAT**: Generate the newsletter as clean, well-formatted plain text with:
- Clear section headers with decorative separators
- Proper spacing and indentation
- Rich use of emojis throughout content
- Easy-to-read structure suitable for email or text format
- Professional but approachable formatting

Content Guidelines:

Tone & Style:

- **Authoritative yet Accessible**: Expert-level insights explained clearly
- **Analytical**: Go beyond "what happened" to "why it matters" and "what's next"
- **Engaging**: Compelling but not sensationalized
- **Balanced**: Present both opportunities and challenges/risks

Quality Standards:

- **Context-Rich**: Always explain significance and implications
- **Forward-Looking**: Connect current developments to future trends
- **Practical**: Include actionable insights where possible
- **Diverse Perspectives**: Cover technical, business, ethical, and societal angles

Please process the provided newsletter content and create a comprehensive AI newsletter in plain text format with lots of emojis."""),
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
with open("compound_newsletter_claude.html", "w", encoding="utf-8") as f:
    f.write(html_output)

# Save text version
with open("compound_newsletter_claude.txt", "w", encoding="utf-8") as f:
    f.write(text_output)

print("\n✅ Newsletter generation complete!")
print("📄 HTML version saved to: compound_newsletter.html")
print("📝 Text version saved to: compound_newsletter.txt")