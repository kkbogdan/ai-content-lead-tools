"""
AI Lead Research Tool for Home Services Businesses
Uses the Claude API to identify and profile potential customer segments
and generate outreach strategies based on location and service type.
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


def research_customer_segments(city: str, service_type: str) -> list[dict]:
    """
    Identify potential customer segments for a home services business
    in a given city and service category.
    """
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=700,
        messages=[
            {
                "role": "user",
                "content": (
                    f"You are helping a home services company find leads in {city} "
                    f"for the service type: '{service_type}'. "
                    f"Identify 4 realistic customer segments they should target. "
                    f"For each segment include: 'segment' (name), 'why_they_need_us' (1 sentence), "
                    f"and 'where_to_find_them' (1-2 online or local channels). "
                    f"Respond ONLY with a JSON array of 4 objects. No preamble or markdown."
                ),
            }
        ],
    )

    raw = response.content[0].text.strip()
    return json.loads(raw)


def generate_outreach_message(segment: dict, business_name: str, service_type: str) -> str:
    """
    Generate a short, personalized outreach message for a specific customer segment.
    """
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Write a short, genuine outreach message from {business_name} "
                    f"to the following customer segment: '{segment['segment']}'. "
                    f"Service being offered: '{service_type}'. "
                    f"Reason they need it: '{segment['why_they_need_us']}'. "
                    f"Keep it under 5 sentences, conversational, and not pushy. "
                    f"No subject line needed — just the message body."
                ),
            }
        ],
    )

    return response.content[0].text.strip()


def generate_lead_summary(city: str, service_type: str, segments: list[dict]) -> str:
    """
    Summarize the lead landscape and suggest a prioritization strategy.
    """
    segment_names = [s["segment"] for s in segments]

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": (
                    f"A handyman company is targeting '{service_type}' customers in {city}. "
                    f"They have identified these segments: {', '.join(segment_names)}. "
                    f"Write a short paragraph (4-5 sentences) recommending which segment to prioritize first "
                    f"and why, based on ease of reach and likely conversion. Keep it practical and direct."
                ),
            }
        ],
    )

    return response.content[0].text.strip()


def run_lead_research(
    city: str,
    service_type: str,
    business_name: str = "Odd Job Handyman Services",
):
    """
    Full lead research pipeline: identifies customer segments, generates
    outreach messages, and produces a prioritization summary.
    """
    print(f"\n{'='*60}")
    print(f"  Lead Research — Service: '{service_type}' in {city}")
    print(f"  Business: {business_name}")
    print(f"{'='*60}\n")

    # Step 1: Research customer segments
    print("Researching customer segments...")
    segments = research_customer_segments(city, service_type)

    print("\nCustomer Segments Identified:")
    for i, seg in enumerate(segments, 1):
        print(f"\n  {i}. {seg['segment']}")
        print(f"     Why they need us: {seg['why_they_need_us']}")
        print(f"     Where to find them: {seg['where_to_find_them']}")

    # Step 2: Generate outreach message for top segment
    top_segment = segments[0]
    print(f"\nGenerating outreach message for: '{top_segment['segment']}'...")
    message = generate_outreach_message(top_segment, business_name, service_type)
    print("\nSample Outreach Message:")
    print(message)

    # Step 3: Generate prioritization summary
    print("\nGenerating lead prioritization summary...")
    summary = generate_lead_summary(city, service_type, segments)
    print("\nPrioritization Summary:")
    print(summary)

    print(f"\n{'='*60}\n")

    return {
        "city": city,
        "service_type": service_type,
        "segments": segments,
        "sample_outreach": message,
        "prioritization_summary": summary,
    }


if __name__ == "__main__":
    # Example runs relevant to a handyman/home maintenance business
    run_lead_research(
        city="Mississauga, Ontario",
        service_type="recurring home maintenance subscriptions",
    )

    run_lead_research(
        city="Mississauga, Ontario",
        service_type="seasonal HVAC and plumbing inspections",
    )
