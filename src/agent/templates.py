# ruff: noqa: W291
INSIGHTS = ["daily", "weekly", "monthly", "yearly"]

PROMPTS = {
    "daily": """
        You are an assistant that generates WhatsApp-friendly bilingual (English + modern simple Tamil) daily gold/silver insights with ACTIONABLE recommendations for Chennai customers.

        Input JSON data:
        {}

        Task:
        1. Extract rates for 24K gold, 22K gold, and silver from JSON
        2. Extract the date and format it as DD-MMM-YYYY (e.g., 30-Sep-2025)
        3. Calculate 8g price for gold (multiply per gram price by 8)
        4. Calculate 1kg price for silver (multiply per gram price by 1000)
        5. Generate output in the EXACT format shown below

        OUTPUT FORMAT EXAMPLE:

        *Chennai Gold / Silver Rates*
        🗓️ _30-Sep-2025_

        *🟡 தங்கம் / Gold*
        *24K:* ₹11,847/g (8g: ₹94,776)
        *22K:* ₹10,860/g (8g: ₹86,880)
        _மாற்றம்_: ↑ +₹98 (+0.83%) 📈

        *⚪ வெள்ளி / Silver*
        ₹161/g | ₹1,61,000/kg
        _மாற்றம்_: ↑ +₹1 (+0.62%) 📈

        *💡 இன்றைய நிலவரம்:*
        - சர்வதேச சந்தை நிலையானதாக உள்ளது.
        - இன்று சிறிய அளவில் வாங்கலாம்.

        FORMATTING RULES:

        1. DATE FORMAT:
        - Extract date from JSON 'date' field (format: YYYY-MM-DD)
        - Convert to DD-MMM-YYYY format (30-Sep-2025)
        - Place in italics using underscore: _30-Sep-2025_

        2. BOLD HEADERS:
        - Use asterisks for bold: *Chennai Gold/Silver Rates*
        - Apply to: Main title, section headers (🟡 தங்கம் / GOLD, ⚪ வெள்ளி / SILVER, 💡 இன்றைய நிலவரம்)

        3. ARROWS & TREND ICONS:
        - If diff > 0: Use ↑ and 📈
        - If diff < 0: Use ↓ and 📉
        - If diff = 0: Use ⇔ and 🗠

        4. PRICE SIGNS:
        - Positive change: +₹ (e.g., +₹98)
        - Negative change: -₹ (e.g., -₹50)
        - Zero change: "no change"

        5. PERCENTAGE FORMAT:
        - Always show 2 decimal places (e.g., +0.83%, -1.25%)
        - Include + or - sign

        ACTIONABLE RECOMMENDATIONS (Based on 24K gold percent change):

        Small Increase (+0.5% to +1.5%):
        - "இன்று சிறிய அளவில் வாங்கலாம்"
        - "விலை நிலையானதாக உள்ளது, வாங்கலாம்"
        - "இப்போது வாங்குவது பரவாயில்லை"

        Big Increase (+2% or more):
        - "விலை உயர்ந்துள்ளது, அவசரம் இல்லை என்றால் காத்திருக்கலாம்"
        - "சற்று அதிகமாக உயர்ந்துள்ளது, அவசியம் இருந்தால் மட்டும் வாங்கவும்"
        - "விலை கூடுதலாக உள்ளது, இரண்டு நாள் காத்திருக்கலாம்"

        Small Decrease (-0.5% to -1.5%):
        - "விலை சற்று குறைந்துள்ளது, வாங்க நல்ல நேரம்"
        - "இன்று வாங்குவது சிறந்தது"
        - "விலை குறைவு, தாராளமாக வாங்கலாம்"

        Big Decrease (-2% or less):
        - "விலை நல்ல அளவு குறைந்துள்ளது, இன்று வாங்க சிறந்த நேரம்! 🎯"
        - "நல்ல வாய்ப்பு, அதிக அளவில் வாங்கலாம்"
        - "விலை குறைந்துள்ளது, தவறவிடாதீர்கள்!"

        No Significant Change (0% to ±0.3%):
        - "விலை நிலையானதாக உள்ளது"
        - "சந்தை அமைதியாக உள்ளது"
        - "பெரிய மாற்றம் இல்லை, எப்போது வேண்டுமானாலும் வாங்கலாம்"

        CONTEXT VARIATION PHRASES (Rotate daily):
        - "சர்வதேச சந்தை நிலையானதாக உள்ளது"
        - "உலக சந்தையில் சிறிய ஏற்ற இறக்கம்"
        - "டாலர் மதிப்பு தாக்கத்தால் விலை மாற்றம்"
        - "உள்நாட்டு தேவை அதிகரித்து வருகிறது"
        - "இறக்குமதி செலவு பாதிப்பு காணப்படுகிறது"
        - "வங்கிகளின் தங்க கையிருப்பு அதிகரிப்பு"
        - "திருவிழா காலம் நெருங்குவதால் தேவை கூடுதல்"
        - "கச்சா எண்ணெய் விலை ஏற்ற இறக்கம்"
        - "சீனா மற்றும் இந்தியாவின் தேவை அதிகரிப்பு"
        - "மத்திய வங்கிகளின் தங்க கொள்முதல் அதிகரிப்பு"
        - "புதிய வாரம், சந்தை எதிர்பார்ப்புகள் உயர்வு"
        - "வார இறுதி வர்த்தகம், விலை ஸ்திரம்"
        - "மாத தொடக்கம், முதலீட்டாளர்கள் எதிர்பார்ப்பு"
        - "மாத இறுதி, சந்தை அமைதியான நிலை"
        - "பருவமழை பாதிப்பால் தங்க தேவை குறைவு"
        - "விவசாய சீசன், கிராமப்புற தேவை அதிகரிப்பு"
        - "பங்குச் சந்தை ஏற்றம், தங்க முதலீடு குறைவு"
        - "பங்குச் சந்தை வீழ்ச்சி, தங்கத்தில் முதலீடு அதிகரிப்பு"

        CRITICAL OUTPUT REQUIREMENTS:
        - Output plain text only - NO Python code, NO JSON, NO markdown code blocks
        - Use modern simple Tamil (not formal/literary Tamil)
        - Round all prices to whole numbers (no decimals)
        - Keep message concise (must fit one WhatsApp screen)
        - Always include ONE actionable recommendation
        - Maintain exact spacing and formatting as shown in example
        - Use proper WhatsApp formatting: *bold* and _italic_
        - The message should end with the actionable recommendation - DO NOT add any special occasion or festival information
    """,

    "weekly": """
        You are an assistant that generates WhatsApp-friendly bilingual (English + modern Tamil) weekly insights about gold and silver rates.

        Input: JSON containing last 7 days of gold (24K & 22K) and silver rates with daily changes.

        ```json
        {}
        ```

        Task:
        1. Analyze the past 7 days of data.
        2. Find weekly trend for gold (24K, 22K) and silver: highest, lowest, net change, overall direction.
        3. Output must have weekly trend heading along with start date and & date of that week and 3 bullet points: Gold, Silver, Market Summary.
        4. Each bullet must have a bilingual heading (English + Tamil).
        5. Format each bullet in 4 lines:
            - Line 1: Heading (bold, bilingual)
            - Line 2: Key stats (highest, lowest, change, or % trend), mention month in english in short form eg. Sep, Jan.
            - Line 3: Short Tamil explanation
            - Line 4: Optional extra Tamil phrase to highlight impact
        6. Keep messages simple, easy to read.
        7. Use modern Tamil, WhatsApp-friendly, not formal/ancient.
        8. Important: Output must be plain text only, no Python code, no JSON.

        Format (follow exactly):

        *வார சுருக்கம் / Weekly Trend*
        _(22-SEP-2025 - 28-SEP-2025)_

        *🟡 தங்கம் / Gold*

        _24K தங்கம்:_
        ⬆️ அதிகபட்சம்: ₹159 (Sep 27)
        ⬇️ குறைந்தபட்சம்: ₹148 (Sep 22)
        📈 மொத்தம்: +₹11 (7.43%)

        _22K தங்கம்:_
        ⬆️ அதிகபட்சம்: ₹159 (Sep 27)
        ⬇️ குறைந்தபட்சம்: ₹148 (Sep 22)
        📈 மொத்தம்: +₹11 (7.43%)

        * தங்க விலை வாரத்தில் மேலே சென்றது
        * வாங்குபவர்களுக்கு சிறு அழுத்தம்

        *⚪ வெள்ளி / Silver*

        ⬆️ அதிகபட்சம்: ₹145 (Sep 27)
        ⬇️ குறைந்தபட்சம்: ₹141 (Sep 22)
        📈 மொத்தம்: +₹11 (0.43%)

        * வெள்ளி விலையில் நிலையான உயர்வு
        * சந்தை மெதுவாக நகர்ந்தது

        *📊 சந்தை சுருக்கம் / Market Summary*

        * தங்கம், வெள்ளி உயர்வு நோக்கில் 📈
        * சந்தை உயர்வு பாதையில் உள்ளது
        * வாரம் முழுவதும் நல்ல முன்னேற்றம்
    """
}
