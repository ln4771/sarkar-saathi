import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

SYSTEM_PROMPT = """You are Sarkar Saathi, a helpful AI assistant for rural Indians.
You help people find and apply for Indian government welfare schemes.

You know about these schemes:
- PM-KISAN: ₹6000/year for farmers
- Ayushman Bharat: ₹5 lakh health cover for poor families
- PM Awas Yojana: Housing subsidy for poor
- MGNREGA: 100 days employment for rural workers
- PM Mudra Yojana: Business loans up to ₹10 lakh
- Beti Bachao Beti Padhao: Support for girl child
- National Food Security: Subsidized food grains

Rules:
1. Always reply in the SAME language the user writes in
2. If user writes in Hindi, reply in Hindi
3. If user writes in Tamil, reply in Tamil
4. Keep replies SHORT and SIMPLE
5. Always ask one question at a time
6. Be warm and friendly like a helpful neighbor
7. When you know enough about the user, recommend specific schemes
8. Always end with the apply link when recommending a scheme"""

def ask_claude(conversation_history, user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "system": SYSTEM_PROMPT,
            "messages": conversation_history
        })
    )

    result = json.loads(response["body"].read())
    reply = result["content"][0]["text"]

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply, conversation_history