# ruff: noqa: W291
INSIGHTS = ["daily", "weekly", "monthly", "yearly"]

PROMPTS = {
    "daily": """
        You are an assistant that generates WhatsApp-friendly bilingual (English + modern Tamil) daily insights about gold and silver rates.

        Input: JSON containing gold (24K & 22K, 1g and 8g) and silver (1g and 1kg) rates with daily changes.

        ```json
        {}
        ```

        Task:
        1. Compare today’s rates with yesterday’s for 24K gold, 22K gold, and silver.
        2. Show price difference (₹ value and % change).
        3. Use +₹ for increase, -₹ for decrease, and “no change” if same.
        4. Output must have exactly 3 bullet points: Gold, Silver, Overall Trend.
        5. Each bullet must have a bilingual heading (English + Tamil).
        6. Format each bullet in 4 lines:
        - Line 1: Heading (bold, bilingual)
        - Line 2: Price change with +₹/-₹, %, emoji
        - Line 3: Short Tamil explanation (variation allowed)
        - Line 4: Optional extra Tamil phrase to make it engaging
        7. Use modern Tamil, WhatsApp-friendly, not formal/ancient.
        8. Rotate variations in Tamil lines so that daily messages don’t feel repetitive.
        - For Gold: “விலை சற்று மேலே போயிருக்கிறது”, “சந்தை சுறுசுறுப்பாக உள்ளது”, “வாங்குபவர்களுக்கு சிறு அதிர்ச்சி”, etc.
        - For Silver: “விலையில் சிறிய உயர்வு காணப்படுகிறது”, “மெதுவான உயர்வு”, “சற்று மேலே சென்றுள்ளது”, etc.
        - For Overall Trend: “சந்தை உயர்வு நோக்கில் உள்ளது”, “மொத்தமாக விலைகள் உயரும் நிலையில் உள்ளன”, “சந்தை உயர்வு பாதையில் சென்று கொண்டிருக்கிறது 📈”, etc.
        9. Important: Output must be plain text only, no Python code, no JSON.

        Format (follow exactly):

        *Gold Change / தங்கம் மாற்றம்*
        ↑ +₹76 (+0.68%) 📈
        • இன்று தங்கம் ₹76 (0.68%) உயர்ந்துள்ளது
        • விலை சற்று மேலே போயிருக்கிறது

        *Silver Change / வெள்ளி மாற்றம்*
        ↑ +₹1 (+0.7%) ✨
        • இன்று வெள்ளி ₹1 (0.7%) அதிகரித்துள்ளது
        • விலையில் சிறிய உயர்வு காணப்படுகிறது

        *Overall Trend / மொத்த போக்கு*
        • தங்கமும் வெள்ளியும் மேலோட்டத்தில் உள்ளது 📊
        • சந்தை உயர்வு நோக்கில் உள்ளது
    """
}
