#!/usr/bin/env python3
"""Build and generate the full research report for the Bloomberg Next Africa video."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from html_report import generate_html_report, save_report
from tts_script_generator import generate_tts_script, save_script
from audio_generator import generate_audio_sync
from email_sender import send_report_email

# ============================================================
# REPORT DATA — Bloomberg Next Africa: 25 African Startups to Watch 2026
# ============================================================

report_data = {
    "video_title": "25 African Startups to Watch; Fintech Unicorn Moniepoint in Focus | Bloomberg Next Africa",
    "video_url": "https://www.youtube.com/watch?v=XB3ciz4_lrE",
    "video_duration": "~26 min",
    
    # ---- SECTION 1: Executive Summary ----
    "executive_summary": (
        "Bloomberg Next Africa's May 2026 edition spotlights the 2026 African Startups to Watch list — "
        "the second annual compilation featuring 25 companies tackling urgent infrastructure and social "
        "challenges across the continent. The theme this year is 'urgency,' reflecting how startups from "
        "Chad to Madagascar are solving real-world problems rather than pursuing AI hype like their Western "
        "counterparts. Fintech dominates both the list and investor interest, with Nigerian unicorn Moniepoint "
        "as the featured success story — processing $250 billion annually across 14 billion+ transactions. "
        "Key shifts in the funding landscape include rising debt financing over equity, growing dominance of "
        "African domestic investors (45% of funding), and a renewed focus on operational discipline and unit "
        "economics over growth-at-all-costs. The episode also explores Terra Industries, a Nigerian drone "
        "startup that raised $34M in seed funding and is expanding manufacturing to Accra, Ghana."
    ),
    
    # ---- SECTION 2: Key Takeaways ----
    "key_takeaways": [
        {
            "point": "African startups are solving urgent, real-world problems — not chasing AI hype",
            "explanation": "Unlike the US startup ecosystem where AI dominates, African startups focus on basic needs: telemedicine kiosks in Chad, clean water in Tanzania, climate-resilient agriculture in Madagascar, and solar hearing aids in Botswana."
        },
        {
            "point": "Moniepoint processes $250B annually across 14B+ transactions",
            "explanation": "Verified from Moniepoint's website: the Nigerian fintech unicorn serves 20M+ bank accounts, powers 100M+ unique card users on terminals annually, and has maintained profitability even before its banking license. Co-founder Felix Ike confirms they are evaluating IPO options within the next few years."
        },
        {
            "point": "African investors now account for 45% of startup funding, US investors 26%",
            "explanation": "Tokunboh Ishmael of Alitheia Capital notes this shift reflects domestic investors moving from 'armchair investing' (treasuries) into private equity as pension funds balloon and traditional products can't meet yield demands. US investors are focused on domestic AI opportunities."
        },
        {
            "point": "Debt financing is replacing equity for African startups",
            "explanation": "Founders report investors now demand proof of operational discipline and unit economics before deploying capital. Debt financing gives investors downside protection in an uncertain global environment shaped by geopolitical tensions."
        },
        {
            "point": "Terra Industries raises $34M seed to build drones in Nigeria, expand to Ghana",
            "explanation": "The Nigerian drone startup (founded by Nathan Nwachuku with co-founder Maxwell Maduka), backed by Palantir's Joe Lonsdale and Lux Capital, is opening its first international factory in Accra. Plans include scaling from hundreds to 50,000 drones and counter-drone systems within 2 years, addressing asymmetric warfare needs across West Africa."
        },
        {
            "point": "Africa's VC market is recovering — from $5B peak to $3B dip, now growing sustainably",
            "explanation": "Tokunboh Ishmael notes the market has moved from 'blitzscaling' to fundamentally-driven growth. Partech Africa data shows startup funding rose 25% to over $4B in 2025, with fintech, cleantech, and healthtech leading."
        },
        {
            "point": "Startups are spreading beyond the big 4 hubs (Kenya, Nigeria, Egypt, South Africa)",
            "explanation": "The 2026 list features companies from Chad (first-ever entry), Somalia (biochar from weed), Ivory Coast, Madagascar, and Tanzania — signaling ecosystem maturation across the continent."
        },
        {
            "point": "Jem (Cape Town) and Deaftronics (Botswana) represent the ' WhatsApp-native' and 'social enterprise' models",
            "explanation": "Jem built an HR platform for deskless workers entirely on WhatsApp — employees get payslips and leave requests in seconds. Deaftronics manufactures solar-powered hearing aids made by hearing-impaired people in Botswana, addressing a market where 90% of the 40M Africans with hearing impairment can't afford devices (WHO data)."
        },
    ],
    
    # ---- SECTION 3: Detailed Analysis ----
    "detailed_analysis": [
        {
            "heading": "The 'Urgency' Theme and What It Signals",
            "content": (
                "Bloomberg Managing Editor for Africa Arijit Ghosh explains that the 2026 list's "
                "'urgency' theme emerged from observing that African startups are fundamentally different "
                "from their Western counterparts. While US startups chase AI capabilities, African "
                "entrepreneurs are solving critical infrastructure gaps: lack of healthcare access, "
                "clean water scarcity, food insecurity from climate change, and financial exclusion. "
                "This framing is significant because it positions African innovation as complementary "
                "to — not derivative of — global tech trends. The theme also serves as a pitch to "
                "investors: these aren't 'nice-to-have' solutions, but essential services where demand "
                "is guaranteed and pricing power is strong. The implication for the investment thesis "
                "is that African startups addressing urgent needs may actually carry lower business "
                "risk than US startups building discretionary AI tools, a point Kaleo Ventures' "
                "Andrew Firman explicitly makes in the episode."
            )
        },
        {
            "heading": "Moniepoint: Inside Africa's Fintech Flagship",
            "content": (
                "Felix Ike, co-founder and CTO of Moniepoint, provides rare transparency about one of "
                "Africa's most valuable tech companies. The key numbers from Moniepoint's own website "
                "and the interview: $250 billion processed annually (approximately $20.8B monthly), "
                "14 billion+ transactions per year, 20 million+ bank accounts, and 100 million unique "
                "card users on terminals annually. The company operates in Nigeria and Kenya. On the "
                "unicorn status, Ike is characteristically grounded — calling it 'nice' and a 'validation' "
                "but emphasizing that Moniepoint is driven by customer value, not valuation. Critically, "
                "he confirms profitability: 'The truth is we've always been profitable, even before we "
                "went into building a banking solution.' This is unusual among unicorns and signals "
                "genunit economics. Regarding the $200 million raise that pushed them past the billion-dollar "
                "valuation, Ike clarifies they were already profitable before the raise. On IPO, he says "
                "all options are on the table — IPO, acquisition, or staying private — but expects the "
                "direction to become clear 'within the next couple of years.' TechCrunch previously "
                "reported Moniepoint's $110M round from Google and Development Partners International "
                "(DPI) in October 2024, and a January 2025 Visa investment that brought contactless "
                "payments capabilities."
            )
        },
        {
            "heading": "Terra Industries and the Drone Warfare Thesis",
            "content": (
                "Perhaps the most strategically significant segment covers Terra Industries, a Nigerian "
                "startup building both drones and counter-drone systems. CEO Nathan Nwachuku frames the "
                "opportunity around asymmetric warfare — the kind of conflict Africa and emerging markets "
                "actually face, as opposed to the conventional warfare Western defense contractors design "
                "for. His argument is compelling: Western drone systems are too expensive and not built "
                "for African terrain, while non-state armed groups are using cheap off-the-shelf components "
                "to devastating effect. The ACLED conflict monitoring group reports that Africa now accounts "
                "for the majority of Islamic State-linked activity, with over two-thirds recorded there in "
                "H1 2025. Terra Industries' $34M seed round — remarkable for an African hardware startup — "
                "came from high-profile backers including Palantir's Joe Lonsdale (who brings defense "
                "technology credibility) and Lux Capital. The Accra, Ghana factory represents a strategic "
                "expansion: it will serve as the regional manufacturing hub with plans to scale production "
                "to 50,000 drones and counter-drone systems within 2 years. The company is also exploring "
                "Latin American and Middle Eastern markets, noting that asymmetric security threats are "
                "transferable across emerging markets. A larger funding round is planned for the coming months."
            )
        },
        {
            "heading": "The Funding Landscape: Resilience, Retooling, and Rebalancing",
            "content": (
                "Investment data paints a picture of resilience. According to AVCA (Africa Venture Capital "
                "Association), over $5 billion was invested in African startups in 2025 despite tightening "
                "global conditions. Partech Africa's data shows a 25% rise to just over $4 billion in "
                "tech startup funding alone. Two major shifts define the current moment. First, the "
                "investor base is rebalancing: African investors now account for 45% of funding (up from "
                "a minority share), while US investors represent 26%. Tokunboh Ishmael of Alitheia Capital "
                "attributes this to structural forces — African pension funds are ballooning and can no "
                "longer be served by traditional treasury products, forcing them into alternative assets "
                "like private equity. Second, the nature of financing is changing. Founders report that "
                "investors are increasingly pushing debt financing instead of equity, demanding proof of "
                "unit economics and operational discipline before deploying capital. Andrew Firman of Kaleo "
                "Ventures urges international investors to take a 'nuanced view' of risk: solving essential "
                "problems in Africa can be less risky than building discretionary solutions in the US, "
                "especially when valuations are adjusted for the opportunity."
            )
        },
        {
            "heading": "The Broader Ecosystem: From HR Tech to Social Enterprise",
            "content": (
                "The episode spotlights two startups that represent important trends. Jem from Cape Town "
                "has built an HR platform for deskless workers — a massive underserved market in Africa "
                "where most workers don't have corporate email or apps. CEO Simon Ellis's insight was to "
                "build on WhatsApp, which every worker already uses. Employees receive payslips, leave "
                "requests, time sheets, and increment letters through familiar chat interfaces. This "
                "'WhatsApp-native' approach eliminates adoption friction entirely. Deaftronics from "
                "Botswana represents the social enterprise model: they manufacture solar-powered hearing "
                "aid devices, crucially employing hearing-impaired people in the manufacturing process. "
                "The market opportunity is enormous — WHO estimates 40 million people in Africa have "
                "hearing impairment, but only 10% can afford conventional hearing aids. Both companies "
                "demonstrate that African startups are building category-defining products for "
                "specifically African contexts — HR for deskless workers, affordable hearing aids for "
                "the deaf — rather than copying Silicon Valley playbooks."
            )
        },
    ],
    
    # ---- SECTION 4: External Research ----
    "external_research": [
        {
            "topic": "Moniepoint Financial Performance (2024-2026)",
            "findings": (
                "Moniepoint processes $250 billion in digital payments transaction value annually "
                "across 14+ billion transactions, with 20 million+ bank accounts and 100 million "
                "unique card users on terminals annually (source: moniepoint.com/about). The company "
                "achieved unicorn status through a $200 million raise. Prior funding includes a "
                "$110M round backed by Google and Development Partners International (DPI) in October "
                "2024, and a Visa investment announced January 2025 that added contactless payments "
                "capabilities. African VC firm Oui Capital successfully returned its first fund through "
                "the Moniepoint exit. Moniepoint is confirmed profitable both before and after "
                "obtaining its banking license — a rarity among unicorns."
            ),
            "source": "https://www.moniepoint.com/about"
        },
        {
            "topic": "Moniepoint: Visa and Google Investment Details",
            "findings": (
                "TechCrunch reported in January 2025 that Moniepoint received Visa backing and "
                "planned to work on contactless payments. In October 2024, Google and Development "
                "Partners International (DPI) backed Moniepoint in a $110M funding round. By April "
                "2025, TechCrunch was reporting on Moniepoint's expansion into remittances — "
                "questioning whether the company was late to that particular game given competition "
                "from Wave, Chipper Cash, and others. The Visa partnership positions Moniepoint to "
                "compete in the $500B+ global remittances market, with Africa receiving approximately "
                "$100B in remittances annually."
            ),
            "source": "https://techcrunch.com/tag/moniepoint/"
        },
        {
            "topic": "Africa Startup Funding Trends 2025-2026",
            "findings": (
                "Partech Africa data shows African startup funding rose 25% year-over-year to over "
                "$4 billion in 2025, driven by fintech, cleantech, and healthtech. AVCA reports "
                "over $5 billion total invested across all African startups in 2025 despite global "
                "funding tightening. The VC market peaked at $5 billion three years ago, dipped to "
                "under $3 billion, and is now recovering — but with a fundamentally different "
                "character. Investors now prioritize operational discipline, unit economics, and "
                "resilient growth over blitzscaling. Tokunboh Ishmael of Alitheia Capital has been "
                "focusing on impact-driven, fundamentally resilient businesses since before the "
                "recent geopolitical conflicts reshaped investor risk calculations."
            ),
            "source": "https://techcrunch.com/tag/africa/"
        },
        {
            "topic": "Terra Industries: Nigeria's Drone Manufacturing Ambition",
            "findings": (
                "Terra Industries is a Nigerian defense tech startup founded by Nathan Nwachuku "
                "with co-founder Maxwell Maduka. The company raised $34 million in seed funding "
                "from notable investors including Joe Lonsdale (co-founder of Palantir) and Lux Capital — "
                "an unusually large seed round for African hardware. The company develops both drones "
                "and counter-drone systems (jammers, radars) specifically designed for African terrain "
                "and asymmetric warfare. Opening its first international factory in Accra, Ghana as the "
                "regional manufacturing hub. Production target: scale from hundreds to 50,000 drones "
                "and counter-drone systems within 24 months. ACLED conflict monitoring data shows Africa "
                "accounts for the majority of Islamic State-linked activity globally, with over two-thirds "
                "of incidents in H1 2025. The cheaper threat (off-the-shelf components for non-state "
                "groups) vs. costly defense solutions creates the market gap Terra Industries fills."
            ),
            "source": "https://www.youtube.com/watch?v=XB3ciz4_lrE"
        },
        {
            "topic": "Alitheia Capital and Africa's Domestic Investment Shift",
            "findings": (
                "Alitheia Capital is a co-managed Gender-Lens Fund with N54.6 billion (~$35M) "
                "AUM focused on investments in Nigeria and francophone Africa. Co-founder and Managing "
                "Director Tokunboh Ishmael has been a leading voice in African impact investing. "
                "The firm's thesis centers on fundamentally-driven businesses that deliver both impact "
                "and returns. Key market insight from Ishmael: African pension funds are ballooning "
                "and traditional 'armchair' investments (treasuries) can no longer meet their yield "
                "requirements, creating a structural forcing function that pushes domestic capital "
                "into private equity and venture. This helps explain why African investors now account "
                "for 45% of startup funding despite global risk-off sentiment."
            ),
            "source": "https://www.alitheiacapital.com/"
        },
        {
            "topic": "WHO Hearing Impairment Data & Deaftronics Market Opportunity",
            "findings": (
                "According to the World Health Organization, approximately 40 million people in "
                "Africa have some form of hearing impairment. Only 10% of those who need hearing "
                "aids can afford conventional devices — creating a market gap for 36 million "
                "people. Deaftronics, based in Botswana, addresses this with solar-powered hearing "
                "aids at accessible price points. Their social enterprise model — manufacturing by "
                "hearing-impaired people — represents both an employment and accessibility solution. "
                "The WHO estimates that unaddressed hearing loss costs the global economy $980 billion "
                "annually, with a significant portion burdening developing nations where financial "
                "infrastructure for hearing healthcare is minimal."
            ),
            "source": "https://www.youtube.com/watch?v=XB3ciz4_lrE"
        },
        {
            "topic": "ACLED Conflict Data and Emerging Market Security",
            "findings": (
                "ACLED (Armed Conflict Location & Event Data Project) reports that Africa now accounts "
                "for the majority of Islamic State-linked activity globally, with over two-thirds of "
                "incidents recorded on the continent in the first half of 2025. This marks a "
                "significant shift in global terrorism patterns and validates the market thesis for "
                "defense technology startups like Terra Industries. The asymmetric nature of these "
                "conflicts — where non-state actors use cheap, widely available technology — creates "
                "demand for cost-effective counter-measures that Western defense contractors are not "
                "optimized to provide. The cost asymmetry is stark: thousands of dollars for defense "
                "systems vs. hundreds for the threat technology."
            ),
            "source": "https://www.youtube.com/watch?v=XB3ciz4_lrE"
        },
    ],
    
    # ---- SECTION 5: Sources ----
    "sources": [
        {"title": "Bloomberg Next Africa: 25 African Startups to Watch (YouTube, May 2026)", "url": "https://www.youtube.com/watch?v=XB3ciz4_lrE"},
        {"title": "Moniepoint — About Us / Company Data", "url": "https://www.moniepoint.com/about"},
        {"title": "TechCrunch — Moniepoint Tag (Visa, Google/DPI, Oui Capital coverage)", "url": "https://techcrunch.com/tag/moniepoint/"},
        {"title": "TechCrunch — Google and DPI back African fintech Moniepoint in $110M round (Oct 2024)", "url": "https://techcrunch.com/2024/10/29/google-and-dpi-back-african-fintech-moniepoint-in-110m-round/"},
        {"title": "CNBC Africa — Latest News & Market Data", "url": "https://www.cnbcafrica.com/"},
        {"title": "ACLED — Conflict Monitoring Data (Africa ISIS Activity)", "url": "https://acleddata.com/"},
        {"title": "Alitheia Capital — Investment Thesis & Fund Information", "url": "https://www.alitheiacapital.com/"},
        {"title": "Partech Africa — Startup Funding Report 2025", "url": "https://partechpartners.com/"},
        {"title": "World Health Organization — Hearing Impairment Statistics", "url": "https://www.who.int/news-room/fact-sheets/detail/deafness-and-hearing-loss"},
    ],
}


# ============================================================
# GENERATE ALL OUTPUTS
# ============================================================

print("Building HTML report...")
html = generate_html_report(report_data)
report_path = save_report(html, report_data["video_title"])
print(f"  Report: {report_path} ({len(html)} chars)")

print("Generating TTS script...")
tts_script = generate_tts_script(report_data)
wc = len(tts_script.split())
mins = wc / 150
script_path = save_script(tts_script, report_data["video_title"])
print(f"  Script: {wc} words (~{mins:.1f} min)")
print(f"  Saved:  {script_path}")

print("Generating audio...")
audio_path = generate_audio_sync(tts_script)
audio_size = os.path.getsize(audio_path) / (1024*1024)
print(f"  Audio:  {audio_path} ({audio_size:.1f} MB)")

print("Sending email...")
success = send_report_email(
    html_report=html,
    tts_script=tts_script,
    audio_path=audio_path,
    to_email="cryptosi@protonmail.com",
    from_email="lisakimvirtuals@gmail.com",
)

if success:
    print("✅ Email sent to cryptosi@protonmail.com")
else:
    print("❌ Email failed — files saved locally")

# Save report data as JSON for reference
json_path = "/workspace/youtube-research-tool/output/report_data.json"
with open(json_path, "w") as f:
    json.dump(report_data, f, indent=2, ensure_ascii=False)
print(f"Report data: {json_path}")
