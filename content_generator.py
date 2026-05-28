"""
AI Content Generator for Home Services Businesses
Uses the Claude API to generate YouTube and Instagram content ideas
based on a given topic and target audience.
"""

import anthropic
import json
import os

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError(
        "\n[Setup] ANTHROPIC_API_KEY not set.\n"
        "Get your key at https://console.anthropic.com\n"
        "Then run: export ANTHROPIC_API_KEY='your-key-here'\n"
    )

client = anthropic.Anthropic(api_key=api_key)


def generate_youtube_ideas(topic: str, business_name: str) -> list[str]:
    """Generate YouTube video ideas for a given home services topic."""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": (
                    f"You are a content strategist for a home services company called {business_name}. "
                    f"Generate 5 compelling YouTube video ideas about '{topic}'. "
                    f"Each idea should be practical, helpful to homeowners, and showcase the company's expertise. "
                    f"Respond ONLY with a JSON array of 5 strings, no preamble or markdown."
                ),
            }
        ],
    )

    raw = response.content[0].text.strip()
    return json.loads(raw)


def generate_script_outline(video_title: str, business_name: str) -> str:
    """Generate a short YouTube script outline for a given video title."""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=600,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Write a concise YouTube script outline for a video titled '{video_title}' "
                    f"for a home services company called {business_name}. "
                    f"Include: Hook (first 15 seconds), 3 main points, and a call to action. "
                    f"Keep it practical and conversational — this is a small business, not a corporation."
                ),
            }
        ],
    )

    return response.content[0].text.strip()


def generate_instagram_caption(topic: str, business_name: str) -> str:
    """Generate an Instagram caption for a given home services topic."""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Write an Instagram caption for {business_name}, a home services company, "
                    f"about the topic: '{topic}'. "
                    f"Keep it short, friendly, and end with 2-3 relevant hashtags. "
                    f"The tone should feel like a real person wrote it, not a marketing team."
                ),
            }
        ],
    )

    return response.content[0].text.strip()


def run_pipeline(topic: str, business_name: str = "Odd Job Handyman Services"):
    """
    Full content pipeline: takes a topic and returns YouTube ideas,
    a script outline for the top idea, and an Instagram caption.
    """
    print(f"\n{'='*60}")
    print(f"  Content Pipeline — Topic: '{topic}'")
    print(f"  Business: {business_name}")
    print(f"{'='*60}\n")

    # Step 1: Generate YouTube ideas
    print("Generating YouTube video ideas...")
    ideas = generate_youtube_ideas(topic, business_name)
    print("\nYouTube Video Ideas:")
    for i, idea in enumerate(ideas, 1):
        print(f"  {i}. {idea}")

    # Step 2: Generate script outline for the first idea
    top_idea = ideas[0]
    print(f"\nGenerating script outline for: '{top_idea}'...")
    outline = generate_script_outline(top_idea, business_name)
    print("\nScript Outline:")
    print(outline)

    # Step 3: Generate Instagram caption
    print("\nGenerating Instagram caption...")
    caption = generate_instagram_caption(topic, business_name)
    print("\nInstagram Caption:")
    print(caption)

    print(f"\n{'='*60}\n")

    return {
        "topic": topic,
        "youtube_ideas": ideas,
        "script_outline": outline,
        "instagram_caption": caption,
    }


if __name__ == "__main__":
    # Example topics relevant to a handyman/home services business
    topics = [
        "common home maintenance mistakes homeowners make",
        "when to call a handyman vs DIY",
    ]

    for topic in topics:
        run_pipeline(topic)
