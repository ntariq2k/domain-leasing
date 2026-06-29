"""
build_sites.py — generates complete professional business websites for all 9 lease domains.
Run: python build_sites.py
Outputs: sites/<domain>/index.html for each domain
"""
import os, json, re, urllib.request, urllib.parse, datetime

FORMSPREE_ID = "mykqjzoq"
CONTACT_EMAIL = "omegaincomeclub@gmail.com"
CONTACT_PHONE = "(646) 555-0148"

DOMAINS = {
    "nycreagent.com": {
        "theme": "realestate",
        "biz_name": "NYC Real Estate Agent",
        "tagline": "Expert Real Estate Representation in New York City",
        "hero_headline": "Sell Faster. Buy Smarter. Win the NYC Market.",
        "hero_sub": "Top-rated real estate agents serving Manhattan, Brooklyn, Queens, The Bronx & Staten Island. Millions sold. Results guaranteed.",
        "cta": "Get a Free Consultation",
        "niche": "real estate agent",
        "schema_type": "RealEstateAgent",
        "geo": ("New York", "US-NY"),
        "stats": [
            ("500+", "Properties Sold"),
            ("$2B+", "In Transactions"),
            ("98%", "Client Satisfaction"),
            ("15+", "Years Experience"),
        ],
        "services": [
            ("Buyer Representation", "Exclusive advocacy when purchasing — from search to close. We negotiate hard so you don't overpay."),
            ("Seller Representation", "Strategic pricing, marketing, staging guidance, and negotiation to maximize your sale price."),
            ("Investment Properties", "Cap-rate analysis, off-market deals, and portfolio-building strategy across all NYC boroughs."),
            ("Luxury Condos & Co-ops", "Specialist knowledge of board packages, flip taxes, and high-end Manhattan market dynamics."),
            ("Rental Placement", "Find qualified tenants fast with professional listing, screening, and lease preparation."),
            ("Market Analysis & CMAs", "Detailed comparable market analyses to help you price right and time the market."),
        ],
        "areas": ["Manhattan", "Brooklyn", "Queens", "The Bronx", "Staten Island", "Long Island City", "Astoria", "Flushing", "Harlem", "Upper East Side"],
        "testimonials": [
            ("Sarah M.", "Manhattan Buyer", "Incredible experience — found my dream apartment in 3 weeks under asking price. These agents are the real deal."),
            ("James R.", "Brooklyn Seller", "Listed on a Friday, had 7 offers by Monday. Sold $85K over asking. Could not be happier."),
            ("Linda K.", "Queens Investor", "They helped me build a 4-property portfolio in 18 months. Brilliant investment insight."),
        ],
        "about": "NYC Real Estate Agent is your premier partner for all real estate transactions in New York City. Whether you are buying your first home in Queens, selling a luxury condo in Manhattan, or growing an investment portfolio across the five boroughs, our licensed agents bring deep market expertise and relentless client advocacy. We combine hyper-local knowledge with cutting-edge market data to deliver results that consistently exceed expectations.",
        "keywords": "NYC real estate agent, New York City realtor, Manhattan homes for sale, Brooklyn real estate, Queens property agent, NYC home buying, NYC home selling",
        "faq": [
            ("How much does a real estate agent cost in NYC?", "In NYC, the seller typically pays the full commission (5–6% of sale price), split between buyer and seller agents. Buyers pay nothing out of pocket."),
            ("How long does it take to sell a home in NYC?", "Well-priced NYC properties typically go under contract in 30–90 days. Luxury or unique properties may take longer."),
            ("Do I need a buyer's agent in NYC?", "Absolutely. NYC's market is complex with co-ops, condos, and bidding wars. A buyer's agent protects your interests at no cost to you."),
        ],
    },
    "webuyqueens.com": {
        "theme": "realestate",
        "biz_name": "We Buy Queens Homes",
        "tagline": "Fast Cash Home Buyers in Queens, NY",
        "hero_headline": "Sell Your Queens Home Fast — Cash Offer in 24 Hours.",
        "hero_sub": "No repairs, no agents, no fees. We buy houses in any condition across all Queens neighborhoods. Close in as little as 7 days.",
        "cta": "Get My Cash Offer",
        "niche": "cash home buyer",
        "schema_type": "RealEstateAgent",
        "geo": ("Queens, New York", "US-NY"),
        "stats": [
            ("300+", "Homes Purchased"),
            ("24hr", "Cash Offer Turnaround"),
            ("7 Days", "Fastest Close"),
            ("0%", "Commission or Fees"),
        ],
        "services": [
            ("Cash Home Purchases", "We buy your Queens home as-is with a guaranteed cash offer — no contingencies, no delays."),
            ("Any Condition Buying", "Hoarder homes, fire damage, flood damage, code violations — we buy it all without repairs."),
            ("Foreclosure Prevention", "Facing foreclosure? We can close before the bank does, protecting your credit and equity."),
            ("Probate & Estate Sales", "Simplify inherited property sales with a fast, hassle-free cash transaction."),
            ("Divorce Property Sales", "Quick, fair sales during divorce proceedings to help both parties move forward."),
            ("Landlord Exit Strategy", "Done being a landlord? We buy tenant-occupied properties without eviction hassles."),
        ],
        "areas": ["Jamaica", "Flushing", "Astoria", "Jackson Heights", "Forest Hills", "Jamaica Estates", "Bayside", "Richmond Hill", "Ozone Park", "Far Rockaway"],
        "testimonials": [
            ("Marcus T.", "Jamaica Homeowner", "Got a cash offer in 4 hours and closed in 8 days. Saved my credit from foreclosure. Absolute lifesavers."),
            ("Diana L.", "Flushing Seller", "Inherited a property I couldn't afford to fix up. They bought it as-is and the process was incredibly smooth."),
            ("Robert P.", "Astoria Landlord", "Problem tenant situation — they bought the house with the tenant still in it. Problem solved!"),
        ],
        "about": "We Buy Queens specializes in fast, fair, all-cash home purchases across every Queens neighborhood. We eliminate the traditional headaches of selling — no agent commissions, no repair demands, no open houses, no financing contingencies. Whether you are dealing with foreclosure, an inherited home, a difficult tenant, or simply need to sell fast, we provide a straightforward solution with guaranteed cash and flexible closing dates.",
        "keywords": "we buy houses Queens NY, cash home buyers Queens, sell my house fast Queens, sell house as-is Queens NY, cash offer Queens home",
        "faq": [
            ("How fast can you close on my Queens home?", "We can close in as little as 7 days once you accept our cash offer, or we can wait up to 60 days — your timeline, your choice."),
            ("Will you really buy my house in any condition?", "Yes. Fire damage, water damage, code violations, hoarder cleanup needed — we buy it all. You pay for nothing."),
            ("Is the cash offer really free?", "100% free with zero obligation. We make an offer; if you like it, great. If not, you walk away owing nothing."),
        ],
    },
    "webuynycbuilding.com": {
        "theme": "realestate",
        "biz_name": "We Buy NYC Buildings",
        "tagline": "Commercial & Multifamily Building Buyers in New York City",
        "hero_headline": "Sell Your NYC Building — Cash Closing, No Hassles.",
        "hero_sub": "We purchase commercial buildings, multifamily properties, and mixed-use assets across all five boroughs. Discreet, fast, and all-cash.",
        "cta": "Request a Building Valuation",
        "niche": "commercial building buyer",
        "schema_type": "RealEstateAgent",
        "geo": ("New York City", "US-NY"),
        "stats": [
            ("150+", "Buildings Acquired"),
            ("$500M+", "In Building Purchases"),
            ("30 Days", "Average Close Time"),
            ("5 Boroughs", "Coverage Area"),
        ],
        "services": [
            ("Multifamily Building Purchases", "We buy 2–50+ unit apartment buildings across all NYC boroughs, any condition, any occupancy situation."),
            ("Commercial Property Acquisition", "Office buildings, retail, warehouse — we evaluate and close on commercial assets quickly."),
            ("Mixed-Use Building Buys", "Retail-plus-residential mixed-use properties are our specialty. We understand the NYC zoning landscape."),
            ("Distressed Asset Purchasing", "Buildings with violations, deferred maintenance, or difficult tenants? We price fairly and close fast."),
            ("Off-Market Transactions", "Prefer a discreet sale? We handle transactions with complete confidentiality — no public listings required."),
            ("1031 Exchange Facilitation", "Our team can structure transactions to accommodate your 1031 exchange timeline and requirements."),
        ],
        "areas": ["Manhattan", "Brooklyn", "Queens", "The Bronx", "Staten Island", "Long Island City", "Bushwick", "Crown Heights", "Washington Heights", "Mott Haven"],
        "testimonials": [
            ("Anthony G.", "Bronx Building Owner", "Owned a 12-unit building with 3 problem tenants and roof issues. They valued it fairly and closed in 22 days. Outstanding."),
            ("Grace W.", "Brooklyn Investor", "Needed to complete a 1031 exchange fast. They structured the deal perfectly and closed in time. Professional and reliable."),
            ("Frank S.", "Manhattan Seller", "Inherited a commercial building with no desire to manage it. They handled everything discreetly. Highly recommend."),
        ],
        "about": "We Buy NYC Building is a direct buyer of commercial real estate, multifamily properties, and mixed-use buildings throughout New York City. Our principals have decades of experience in NYC real estate, giving us the ability to value complex properties accurately and close quickly without traditional lender delays. We buy in any condition, any occupancy situation, and handle all paperwork — you simply show up at closing.",
        "keywords": "we buy NYC buildings, sell commercial building NYC, sell apartment building New York, multifamily building buyers NYC, cash buyer commercial real estate NYC",
        "faq": [
            ("What types of buildings do you buy in NYC?", "We buy multifamily (2–100+ units), commercial, mixed-use, industrial, and specialty buildings across all five boroughs."),
            ("Do you buy buildings with violations or liens?", "Yes. We work with our title team to resolve violations and liens at closing — you don't need to fix anything first."),
            ("How do you determine a fair offer for my building?", "We analyze current rents, occupancy, building condition, recent comparable sales, and local market trends to arrive at a fair offer within 48 hours."),
        ],
    },
    "webuynycbuildings.com": {
        "theme": "realestate",
        "biz_name": "We Buy NYC Buildings Group",
        "tagline": "NYC's Premier Institutional Building Acquisition Group",
        "hero_headline": "Portfolio Acquisitions & Single Asset Building Purchases in NYC.",
        "hero_sub": "Institutional-quality buyers for NYC's multifamily, commercial, and mixed-use real estate. Discretion. Speed. Certainty of close.",
        "cta": "Submit a Building for Review",
        "niche": "building acquisition group",
        "schema_type": "RealEstateAgent",
        "geo": ("New York City", "US-NY"),
        "stats": [
            ("200+", "Buildings Acquired"),
            ("$800M+", "Total Portfolio Value"),
            ("21 Days", "Average Close"),
            ("All Classes", "A, B & C Assets"),
        ],
        "services": [
            ("Portfolio Acquisitions", "We acquire 3–20+ building portfolios in a single transaction, simplifying complex multi-asset dispositions."),
            ("Multifamily Acquisitions", "Class A, B, and C multifamily properties — stabilized, transitional, or value-add — all welcomed."),
            ("Retail & Office Buildings", "Single-tenant, multi-tenant, and ground-floor retail buildings with residential above acquired city-wide."),
            ("Value-Add Assets", "We specialize in buildings requiring capital investment — deferred maintenance, vacancy, or repositioning."),
            ("Distressed & REO Properties", "Bank-owned or distressed commercial real estate acquired with all-cash, no-contingency offers."),
            ("Development Site Purchases", "Vacant land, air rights acquisitions, and buildings with significant development upside."),
        ],
        "areas": ["Midtown Manhattan", "Lower Manhattan", "Harlem", "Brooklyn Heights", "Williamsburg", "Bushwick", "Long Island City", "South Bronx", "Flushing", "Staten Island"],
        "testimonials": [
            ("Patricia H.", "Estate Trustee", "We needed to liquidate a 7-building estate portfolio. They valued each property fairly and closed all 7 simultaneously. Extraordinary capability."),
            ("Michael B.", "REIT Asset Manager", "Off-loaded 4 underperforming assets in a single transaction. Clean, fast, and professionally executed."),
            ("Donna C.", "Family Office Rep", "Discreet, fair, and incredibly efficient. Best large-transaction buyer we have ever worked with in NYC."),
        ],
        "about": "We Buy NYC Buildings Group is an institutional direct buyer specializing in the acquisition of commercial and multifamily real estate portfolios across New York City. With hundreds of buildings acquired and deep relationships throughout the NYC lending and title community, we provide unmatched speed and certainty. Our team includes experienced underwriters, attorneys, and property managers who can evaluate, close, and absorb complex transactions that other buyers cannot handle.",
        "keywords": "we buy NYC buildings portfolio, commercial real estate buyers NYC, multifamily portfolio sale New York, institutional buyer NYC real estate, sell apartment building portfolio NYC",
        "faq": [
            ("Do you buy single buildings or only portfolios?", "Both. We handle single assets from $1M and portfolios from 2 to 20+ buildings in a single close."),
            ("How discreet is your acquisition process?", "Fully confidential. We sign NDAs before any building details are shared and never list properties publicly without explicit seller consent."),
            ("What is your minimum building size?", "We typically acquire buildings from 4 units or 3,000 sq ft commercial, with no maximum size restriction."),
        ],
    },
    "njsellersagent.com": {
        "theme": "realestate",
        "biz_name": "NJ Sellers Agent",
        "tagline": "New Jersey's Top Listing Agent — Maximum Sale Price Guaranteed",
        "hero_headline": "Sell Your NJ Home for More. Expert Listing Agent, Proven Results.",
        "hero_sub": "Dedicated seller-side representation across New Jersey. Strategic pricing, aggressive marketing, and expert negotiation to net you the highest possible sale price.",
        "cta": "Get Your Free Home Valuation",
        "niche": "sellers agent",
        "schema_type": "RealEstateAgent",
        "geo": ("New Jersey", "US-NJ"),
        "stats": [
            ("450+", "NJ Homes Sold"),
            ("102%", "Avg List-to-Sale Ratio"),
            ("28 Days", "Avg Days on Market"),
            ("5-Star", "Client Rating"),
        ],
        "services": [
            ("Strategic Home Pricing", "Data-driven comparative market analysis to price your home optimally — not too high to sit, not too low to leave money behind."),
            ("Professional Marketing", "Professional photography, 3D tours, video walkthroughs, MLS listing, Zillow/Realtor.com syndication, and targeted social advertising."),
            ("Staging Consultation", "Expert staging advice (and vetted staging vendors) to make your home show its absolute best."),
            ("Offer Evaluation & Negotiation", "We analyze every offer detail — price, contingencies, closing timeline — and negotiate hard to maximize your net proceeds."),
            ("Transaction Management", "Full coordination with attorneys, inspectors, appraisers, and the buyer's agent from accepted offer through closing."),
            ("Relocation Selling", "Moving out of state? We handle everything remotely so you can focus on your new location."),
        ],
        "areas": ["Newark", "Jersey City", "Hoboken", "Edison", "Teaneck", "Montclair", "Princeton", "Cherry Hill", "Parsippany", "Fort Lee"],
        "testimonials": [
            ("Catherine B.", "Montclair Seller", "We were nervous about pricing in a shifting market. They nailed it — sold in 11 days for $22K over asking."),
            ("Steven W.", "Hoboken Seller", "Professional photography, incredible marketing, and relentless follow-up. Best agent experience I've ever had."),
            ("Angela D.", "Edison Seller", "Handled our relocation sale entirely remotely. Closed without us ever flying back. Absolutely seamless."),
        ],
        "about": "NJ Sellers Agent is a dedicated listing-side specialist serving homeowners across New Jersey who want to achieve the highest possible sale price with minimum hassle. Unlike generalist agents who split attention between buyers and sellers, we focus exclusively on seller representation — which means every strategy, every marketing dollar, and every negotiation tactic is deployed solely in your interest. Our average list-to-sale ratio of 102% consistently outperforms the NJ market average.",
        "keywords": "NJ sellers agent, New Jersey listing agent, sell my home New Jersey, NJ real estate agent seller, top listing agent NJ, New Jersey home selling agent",
        "faq": [
            ("What makes a dedicated sellers agent different from a regular agent?", "A dedicated sellers agent works exclusively for you — no split loyalties. Every strategy is optimized to maximize your sale price and protect your interests."),
            ("How do you determine the right listing price for my NJ home?", "We run a detailed CMA using recent comparable sales, active listings, market trends, and your home's unique features to find the sweet spot that attracts buyers and maximizes your net."),
            ("What does your marketing package include?", "Professional photography, 3D Matterport tour, video walkthrough, MLS listing, Zillow/Realtor.com Premier placement, Facebook/Instagram advertising, and email campaigns to our buyer database."),
        ],
    },
    "nycroofexperts.com": {
        "theme": "trades",
        "biz_name": "NYC Roof Experts",
        "tagline": "New York City's Trusted Roofing Contractors",
        "hero_headline": "NYC's Top Roofing Contractors — Repairs, Replacements & Inspections.",
        "hero_sub": "Licensed and insured roofing professionals serving all five boroughs. Flat roofs, pitched roofs, commercial roofing — we do it all with a 10-year workmanship warranty.",
        "cta": "Get a Free Roof Inspection",
        "niche": "roofing contractor",
        "schema_type": "HomeAndConstructionBusiness",
        "geo": ("New York City", "US-NY"),
        "stats": [
            ("2,000+", "Roofs Completed"),
            ("10 Year", "Workmanship Warranty"),
            ("Licensed", "& Fully Insured"),
            ("24hr", "Emergency Response"),
        ],
        "services": [
            ("Flat Roof Installation & Repair", "EPDM, TPO, and modified bitumen flat roof systems for NYC residential and commercial buildings."),
            ("Pitched Roof Replacement", "Asphalt shingle, slate, and metal roofing for Brooklyn brownstones, Queens homes, and Staten Island residences."),
            ("Commercial Roofing", "Large-scale commercial roof installation, maintenance contracts, and emergency repair for NYC businesses."),
            ("Emergency Roof Repair", "24/7 emergency tarping and repair service. Storm damage, leaks, and blow-offs handled same day."),
            ("Roof Inspection & Certification", "NYC-required roof certifications, pre-purchase inspections, and annual maintenance assessments."),
            ("Skylights & Roof Hatches", "Installation and repair of skylights, roof hatches, and roof access systems for commercial buildings."),
        ],
        "areas": ["Manhattan", "Brooklyn", "Queens", "The Bronx", "Staten Island", "Long Island City", "Astoria", "Flushing", "Harlem", "Williamsburg"],
        "testimonials": [
            ("Tom A.", "Brooklyn Homeowner", "Had a serious leak during a storm. They were on my roof within 4 hours and fixed it completely. Exceptional service."),
            ("Maria C.", "Queens Building Owner", "Replaced the flat roof on my 6-unit building. Clean, professional, and done ahead of schedule. Highly recommend."),
            ("Derek F.", "Manhattan Co-op Board", "Our building's roof certification was overdue. They handled the inspection and paperwork quickly and professionally."),
        ],
        "about": "NYC Roof Experts is a fully licensed and insured roofing contractor serving residential and commercial property owners across New York City. With over 2,000 roofing projects completed in the five boroughs, our team brings unmatched expertise in flat roof systems, brownstone pitched roofs, and large-scale commercial roofing. We are NYC DOB compliant, carry $2M in general liability, and back every installation with a 10-year workmanship warranty.",
        "keywords": "NYC roofing contractor, New York City roofer, flat roof repair NYC, roof replacement Brooklyn, commercial roofing NYC, emergency roof repair New York",
        "faq": [
            ("How much does a flat roof replacement cost in NYC?", "NYC flat roof replacement typically costs $8–$20 per square foot depending on the membrane type and roof condition. We provide free detailed estimates."),
            ("Do you handle emergency roof repairs?", "Yes. We have a 24/7 emergency line and can typically respond within 4 hours for active leaks or storm damage."),
            ("Are you licensed to work in NYC?", "Yes. We are fully licensed with the NYC Department of Buildings, carry $2M general liability, and are fully workers' compensation insured."),
        ],
    },
    "nycpaintexperts.com": {
        "theme": "trades",
        "biz_name": "NYC Paint Experts",
        "tagline": "Commercial & Residential Painting Contractors in New York City",
        "hero_headline": "NYC's Premier Painting Contractors — Flawless Finish, Every Time.",
        "hero_sub": "Professional interior and exterior painting for residential homes, apartments, and commercial spaces across all five boroughs. Licensed, insured, and EPA Lead-Safe Certified.",
        "cta": "Get a Free Painting Estimate",
        "niche": "painting contractor",
        "schema_type": "HomeAndConstructionBusiness",
        "geo": ("New York City", "US-NY"),
        "stats": [
            ("5,000+", "Spaces Painted"),
            ("EPA", "Lead-Safe Certified"),
            ("Licensed", "& Fully Insured"),
            ("5-Star", "Google Rating"),
        ],
        "services": [
            ("Interior Residential Painting", "Apartments, condos, brownstones, and houses — walls, ceilings, trim, and millwork painted to perfection."),
            ("Exterior Building Painting", "Full exterior painting for NYC brownstones, wood-frame homes, and masonry buildings with weather-resistant coatings."),
            ("Commercial Office Painting", "Minimal-disruption commercial painting with evening and weekend scheduling to keep your business running."),
            ("Apartment Turnover Painting", "Fast, high-quality apartment turnover painting for landlords and property managers. Unit ready in 48 hours."),
            ("Lead Paint Removal & Encapsulation", "EPA Lead RRP certified removal and encapsulation for pre-1978 NYC buildings. Fully compliant with NYC Local Law 1."),
            ("Wallpaper Installation & Removal", "Precision wallpaper installation, feature walls, and complete wallpaper removal and skim coating."),
        ],
        "areas": ["Manhattan", "Brooklyn", "Queens", "The Bronx", "Staten Island", "Hoboken", "Jersey City", "Long Island City", "Astoria", "Williamsburg"],
        "testimonials": [
            ("Nina S.", "Upper West Side Tenant", "They painted my entire apartment in 2 days with zero mess. The finish is absolutely beautiful. I'm beyond impressed."),
            ("Paul R.", "Brooklyn Landlord", "I use them for all my apartment turnovers. Fast, clean, consistent quality. My go-to painters for 3 years running."),
            ("Tanya M.", "Midtown Office Manager", "Painted our 10,000 sq ft office over a weekend. Monday morning it looked brand new. Zero disruption to business."),
        ],
        "about": "NYC Paint Experts is New York City's leading professional painting contractor, specializing in residential, commercial, and apartment turnover painting across all five boroughs. Our painters are trained craftsmen who take pride in preparation, clean lines, and lasting finishes. We are EPA Lead-Safe RRP certified for pre-1978 buildings, fully licensed with NYC DOB, and carry comprehensive insurance. Whether you need a single room refreshed or a 20-floor commercial building repainted, we deliver on time and on budget.",
        "keywords": "NYC painting contractor, New York City painters, commercial painting NYC, apartment painting New York, lead paint removal NYC, exterior painting contractor NYC",
        "faq": [
            ("How much does interior painting cost in NYC?", "NYC interior painting typically runs $3–$7 per square foot depending on prep needed, ceiling height, and finish quality. We provide free detailed estimates."),
            ("Are you certified for lead paint work in NYC?", "Yes. We are EPA Lead RRP certified and fully compliant with NYC Local Law 1 for pre-1978 buildings. Safe for families with children."),
            ("How long does apartment painting take?", "A standard 1-bedroom apartment takes 1–2 days. We offer 48-hour turnaround for landlord turnover projects."),
        ],
    },
    "nycreconsultant.com": {
        "theme": "consulting",
        "biz_name": "NYC Real Estate Consultant",
        "tagline": "Independent Real Estate Consulting for NYC Investors & Developers",
        "hero_headline": "Data-Driven NYC Real Estate Consulting for Smarter Investments.",
        "hero_sub": "Independent advisory services for investors, developers, and institutions navigating New York City real estate. Unbiased analysis. Actionable strategy.",
        "cta": "Schedule a Consulting Call",
        "niche": "real estate consultant",
        "schema_type": "ProfessionalService",
        "geo": ("New York City", "US-NY"),
        "stats": [
            ("$1B+", "Assets Advised"),
            ("200+", "Consulting Engagements"),
            ("Independent", "No Brokerage Bias"),
            ("NYC Only", "Deep Local Focus"),
        ],
        "services": [
            ("Investment Property Analysis", "Detailed underwriting of NYC multifamily and commercial acquisitions — cash-on-cash, IRR, cap rate, and stress-testing."),
            ("Market Feasibility Studies", "Independent feasibility analysis for ground-up development, conversions, and adaptive reuse projects in NYC."),
            ("Portfolio Strategy", "Strategic review of existing real estate holdings with recommendations for optimization, disposition, or expansion."),
            ("Due Diligence Support", "Physical, financial, and regulatory due diligence coordination for NYC acquisitions and development projects."),
            ("Zoning & Entitlement Advisory", "Navigate NYC zoning regulations, variance applications, and air rights with expert guidance."),
            ("Landlord-Tenant Strategy", "Legal and strategic guidance for rent-stabilized building owners navigating HSTPA and NYC housing regulations."),
        ],
        "areas": ["Manhattan", "Brooklyn", "Queens", "The Bronx", "Staten Island", "Long Island City", "Greenpoint", "Bushwick", "Crown Heights", "Astoria"],
        "testimonials": [
            ("Jeffrey L.", "Private Investor", "Their underwriting saved me from a bad deal that looked great on the surface. Exceptional analytical depth. Worth every dollar."),
            ("Carmen V.", "Developer", "The feasibility study they produced for our Bronx project was the most thorough analysis I've seen. Lenders were impressed."),
            ("Harold N.", "Family Office", "We needed an independent view of our NYC portfolio. Their strategic recommendations added real value immediately."),
        ],
        "about": "NYC Real Estate Consultant provides independent, unbiased advisory services to real estate investors, developers, family offices, and institutions operating in the New York City market. Unlike brokers or developers who have transactional conflicts of interest, we operate on a pure fee-for-service model — our only incentive is to give you the most accurate, actionable analysis possible. Our principals have underwritten over $1 billion in NYC real estate transactions and bring deep expertise in multifamily, commercial, development, and regulatory environments.",
        "keywords": "NYC real estate consultant, New York City real estate advisory, investment property analysis NYC, real estate feasibility study New York, independent real estate consultant NYC",
        "faq": [
            ("What makes an independent consultant different from a real estate broker?", "An independent consultant has no transaction-based income — we earn a flat fee for advice, so our recommendations are never influenced by commission incentives."),
            ("What types of clients do you work with?", "We work with individual investors, family offices, institutional funds, and real estate developers of all sizes operating in the NYC market."),
            ("How are your consulting fees structured?", "We offer project-based flat fees, hourly advisory, and monthly retainer arrangements depending on the scope and duration of the engagement."),
        ],
    },
    "nycreconsultants.com": {
        "theme": "consulting",
        "biz_name": "NYC Real Estate Consultants",
        "tagline": "Full-Service Real Estate Consulting Firm for NYC Market",
        "hero_headline": "NYC Real Estate Consulting Firm — Strategy, Analysis & Advisory.",
        "hero_sub": "A full-service consulting practice dedicated to New York City real estate. Market intelligence, development advisory, investment strategy, and regulatory navigation.",
        "cta": "Request a Consultation",
        "niche": "real estate consulting firm",
        "schema_type": "ProfessionalService",
        "geo": ("New York City", "US-NY"),
        "stats": [
            ("$2B+", "In Assets Advised"),
            ("300+", "Client Engagements"),
            ("15+", "Years NYC Focus"),
            ("Full-Service", "A to Z Advisory"),
        ],
        "services": [
            ("Acquisition Advisory", "Source, underwrite, and structure NYC real estate acquisitions with institutional-grade analysis and local market expertise."),
            ("Development Consulting", "From site selection through lease-up — feasibility, programming, design review, and go-to-market strategy for NYC developments."),
            ("Asset Management Advisory", "Operational and financial performance optimization for existing NYC real estate portfolios."),
            ("Capital Markets Advisory", "Debt and equity structuring, lender identification, and capital stack optimization for NYC transactions."),
            ("Market Research & Intelligence", "Custom market research reports, submarket analyses, and competitive studies for NYC neighborhoods."),
            ("Regulatory & Compliance Consulting", "HPD, DOB, DHCR, and Landmarks compliance strategy for NYC property owners and developers."),
        ],
        "areas": ["Midtown Manhattan", "Downtown Manhattan", "Upper Manhattan", "Brooklyn", "Queens", "The Bronx", "Staten Island", "Long Island City", "Jersey City", "Hoboken"],
        "testimonials": [
            ("Sandra K.", "Real Estate Fund Manager", "They provided market research that was deeper and more actionable than what we get from major brokerage firms. Exceptional team."),
            ("Victor P.", "Developer", "Our entire Bronx development project was guided by their consulting from day one. Delivered on time and at budget — largely because of their advisory."),
            ("Rachel T.", "Institutional Investor", "Best real estate consulting firm in NYC, full stop. Deep expertise, responsive team, and always objective."),
        ],
        "about": "NYC Real Estate Consultants is a full-service real estate advisory firm specializing exclusively in the New York City market. Our multidisciplinary team combines deep transactional experience, development expertise, regulatory knowledge, and market research capabilities to deliver comprehensive consulting solutions across the real estate lifecycle. We serve as trusted advisors to investors, developers, lenders, and public sector clients seeking independent, data-driven guidance in one of the world's most complex real estate markets.",
        "keywords": "NYC real estate consultants, New York City real estate consulting firm, real estate advisory NYC, development consulting New York, market research real estate NYC",
        "faq": [
            ("What services does your consulting firm offer?", "We offer acquisition advisory, development consulting, asset management, capital markets advisory, market research, and regulatory compliance consulting — full lifecycle coverage."),
            ("Do you work with first-time investors?", "Absolutely. We tailor our engagement model to clients at every experience level, from first-time investors to institutional funds managing billions."),
            ("Can you help with NYC regulatory issues?", "Yes. We have deep expertise in NYC DOB, HPD, DHCR, and Landmarks regulations and can guide property owners through compliance challenges and enforcement actions."),
        ],
    },
}

THEMES = {
    "realestate": {
        "primary": "#0d1b4b",
        "accent": "#c9a84c",
        "accent_light": "#f0dfa0",
        "bg": "#f8f9fc",
        "card_bg": "#ffffff",
        "text": "#1a1a2e",
        "muted": "#6b7280",
        "gradient": "linear-gradient(135deg, #0d1b4b 0%, #1a3a7a 100%)",
    },
    "trades": {
        "primary": "#1e293b",
        "accent": "#f97316",
        "accent_light": "#fed7aa",
        "bg": "#f8fafc",
        "card_bg": "#ffffff",
        "text": "#0f172a",
        "muted": "#64748b",
        "gradient": "linear-gradient(135deg, #1e293b 0%, #334155 100%)",
    },
    "consulting": {
        "primary": "#111827",
        "accent": "#ca8a04",
        "accent_light": "#fde68a",
        "bg": "#f9fafb",
        "card_bg": "#ffffff",
        "text": "#111827",
        "muted": "#6b7280",
        "gradient": "linear-gradient(135deg, #111827 0%, #1f2937 100%)",
    },
}


def fetch_rss(query: str) -> bytes:
    url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query) + "&hl=en-US&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except Exception:
        return b""


def parse_rss(xml_bytes: bytes) -> list:
    articles = []
    text = xml_bytes.decode("utf-8", errors="replace")
    items = re.findall(r"<item>(.*?)</item>", text, re.S)
    for item in items[:20]:
        title_m = re.search(r"<title><!\[CDATA\[(.*?)\]\]></title>", item, re.S)
        link_m  = re.search(r"<link>(.*?)</link>", item, re.S)
        desc_m  = re.search(r"<description><!\[CDATA\[(.*?)\]\]></description>", item, re.S)
        pub_m   = re.search(r"<pubDate>(.*?)</pubDate>", item, re.S)
        source_m= re.search(r"<source[^>]*>(.*?)</source>", item, re.S)
        if not title_m:
            continue
        title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip()
        link  = link_m.group(1).strip() if link_m else "#"
        desc  = re.sub(r"<[^>]+>", "", desc_m.group(1)).strip() if desc_m else ""
        pub   = pub_m.group(1).strip() if pub_m else ""
        src   = source_m.group(1).strip() if source_m else "News"
        articles.append({"title": title, "link": link, "desc": desc, "pub": pub, "source": src})
    return articles


def fetch_articles(domain: str, cfg: dict) -> list:
    queries = {
        "nycreagent.com":        "NYC real estate agent when:30d",
        "webuyqueens.com":       "Queens NY home sale real estate when:30d",
        "webuynycbuilding.com":  "NYC commercial building investment when:30d",
        "webuynycbuildings.com": "New York City building sale investment when:30d",
        "njsellersagent.com":    "New Jersey home selling real estate when:30d",
        "nycroofexperts.com":    "NYC roofing contractor repair cost when:90d",
        "nycpaintexperts.com":   "NYC painting contractor commercial when:90d",
        "nycreconsultant.com":   "NYC real estate consulting market when:30d",
        "nycreconsultants.com":  "New York real estate market trends when:30d",
    }
    query = queries.get(domain, cfg["niche"] + " New York when:30d")
    articles = parse_rss(fetch_rss(query))
    if len(articles) < 8:
        broad = re.sub(r"\s+when:\S+", "", query).strip()
        if broad != query:
            articles = parse_rss(fetch_rss(broad))
    return articles[:20]


def escape_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_articles(articles: list, theme: dict) -> str:
    if not articles:
        return "<p style='color:#6b7280;'>Latest industry news loading...</p>"
    cards = []
    for a in articles:
        title = escape_html(a["title"])
        desc  = escape_html(a["desc"][:200] + ("..." if len(a["desc"]) > 200 else ""))
        source= escape_html(a["source"])
        pub   = escape_html(a["pub"][:16]) if a["pub"] else ""
        link  = a["link"]
        cards.append(f"""
      <a href="{link}" target="_blank" rel="noopener" class="news-card">
        <div class="news-meta"><span class="news-source">{source}</span><span class="news-date">{pub}</span></div>
        <h3 class="news-title">{title}</h3>
        <p class="news-desc">{desc}</p>
        <span class="news-read">Read article →</span>
      </a>""")
    return "\n".join(cards)


def generate_html(domain: str, cfg: dict, articles: list) -> str:
    t = THEMES[cfg["theme"]]
    today = datetime.date.today().isoformat()
    biz = escape_html(cfg["biz_name"])
    tagline = escape_html(cfg["tagline"])
    hero_h = escape_html(cfg["hero_headline"])
    hero_s = escape_html(cfg["hero_sub"])
    cta = escape_html(cfg["cta"])
    about = escape_html(cfg["about"])
    geo_place, geo_region = cfg["geo"]

    # Stats strip
    stats_html = "".join(f"""
      <div class="stat-item">
        <div class="stat-number">{s[0]}</div>
        <div class="stat-label">{escape_html(s[1])}</div>
      </div>""" for s in cfg["stats"])

    # Services
    svcs_html = "".join(f"""
      <div class="service-card">
        <div class="service-icon">✦</div>
        <h3>{escape_html(s[0])}</h3>
        <p>{escape_html(s[1])}</p>
      </div>""" for s in cfg["services"])

    # Service areas
    areas_html = "".join(f'<span class="area-tag">{escape_html(a)}</span>' for a in cfg["areas"])

    # Testimonials
    testi_html = "".join(f"""
      <div class="testimonial-card">
        <div class="stars">★★★★★</div>
        <p class="testi-text">"{escape_html(t[2])}"</p>
        <div class="testi-author">
          <strong>{escape_html(t[0])}</strong>
          <span>{escape_html(t[1])}</span>
        </div>
      </div>""" for t in cfg["testimonials"])

    # FAQ schema
    faq_schema_items = ",\n".join(
        json.dumps({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        for q, a in cfg["faq"]
    )

    # News
    news_html = render_articles(articles, t)

    # Nav links
    nav_links = ["#home", "#services", "#areas", "#about", "#news", "#contact"]
    nav_labels = ["Home", "Services", "Areas", "About", "News", "Contact"]
    nav_html = "".join(f'<a href="{l}">{n}</a>' for l, n in zip(nav_links, nav_labels))

    # FAQ section
    faq_html = "".join(f"""
      <div class="faq-item">
        <button class="faq-q" onclick="this.nextElementSibling.classList.toggle('open');this.classList.toggle('active')">
          {escape_html(q[0])}
          <span class="faq-arrow">▼</span>
        </button>
        <div class="faq-a"><p>{escape_html(q[1])}</p></div>
      </div>""" for q in cfg["faq"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{biz} | {tagline}</title>
  <meta name="description" content="{escape_html(cfg['hero_sub'][:160])}">
  <meta name="keywords" content="{escape_html(cfg['keywords'])}">
  <meta name="robots" content="index, follow">
  <meta name="geo.region" content="{escape_html(geo_region)}">
  <meta name="geo.placename" content="{escape_html(geo_place)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://{domain}/">
  <meta property="og:title" content="{biz} | {tagline}">
  <meta property="og:description" content="{escape_html(cfg['hero_sub'][:160])}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{biz} | {tagline}">
  <meta name="twitter:description" content="{escape_html(cfg['hero_sub'][:160])}">
  <link rel="canonical" href="https://{domain}/">
  <link rel="sitemap" type="application/xml" href="/sitemap.xml">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebPage",
        "@id": "https://{domain}/#webpage",
        "url": "https://{domain}/",
        "name": "{biz}",
        "description": "{escape_html(cfg['hero_sub'][:160])}",
        "inLanguage": "en-US"
      }},
      {{
        "@type": "{cfg['schema_type']}",
        "@id": "https://{domain}/#organization",
        "name": "{biz}",
        "description": "{escape_html(cfg['about'][:300])}",
        "url": "https://{domain}/",
        "telephone": "{CONTACT_PHONE}",
        "email": "{CONTACT_EMAIL}",
        "areaServed": {{
          "@type": "State",
          "name": "{geo_place}"
        }},
        "priceRange": "$$"
      }}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {faq_schema_items}
    ]
  }}
  </script>
  <style>
    :root {{
      --primary: {t['primary']};
      --accent: {t['accent']};
      --accent-light: {t['accent_light']};
      --bg: {t['bg']};
      --card: {t['card_bg']};
      --text: {t['text']};
      --muted: {t['muted']};
      --gradient: {t['gradient']};
      --radius: 10px;
      --shadow: 0 4px 24px rgba(0,0,0,0.08);
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}

    /* NAV */
    .nav {{ position: sticky; top: 0; z-index: 100; background: var(--primary); box-shadow: 0 2px 12px rgba(0,0,0,0.3); }}
    .nav-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; height: 64px; }}
    .nav-logo {{ color: #fff; font-size: 1.1rem; font-weight: 700; text-decoration: none; letter-spacing: -0.02em; }}
    .nav-logo span {{ color: var(--accent); }}
    .nav-links {{ display: flex; gap: 24px; }}
    .nav-links a {{ color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: color 0.2s; }}
    .nav-links a:hover {{ color: var(--accent); }}
    .nav-cta {{ background: var(--accent); color: var(--primary); padding: 10px 20px; border-radius: 6px; font-weight: 700; font-size: 0.85rem; text-decoration: none; transition: opacity 0.2s; }}
    .nav-cta:hover {{ opacity: 0.88; }}
    @media (max-width: 768px) {{
      .nav-links {{ display: none; }}
    }}

    /* HERO */
    .hero {{ background: var(--gradient); color: #fff; padding: 96px 24px 80px; text-align: center; }}
    .hero-inner {{ max-width: 900px; margin: 0 auto; }}
    .hero-badge {{ display: inline-block; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); color: rgba(255,255,255,0.9); padding: 6px 16px; border-radius: 999px; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 24px; }}
    .hero h1 {{ font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 800; line-height: 1.15; margin-bottom: 20px; letter-spacing: -0.03em; }}
    .hero h1 em {{ font-style: normal; color: var(--accent); }}
    .hero-sub {{ font-size: 1.15rem; color: rgba(255,255,255,0.82); max-width: 700px; margin: 0 auto 40px; }}
    .hero-btns {{ display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }}
    .btn-primary {{ background: var(--accent); color: var(--primary); padding: 16px 32px; border-radius: 8px; font-weight: 700; font-size: 1rem; text-decoration: none; transition: transform 0.2s, box-shadow 0.2s; }}
    .btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }}
    .btn-ghost {{ background: transparent; color: #fff; border: 2px solid rgba(255,255,255,0.5); padding: 14px 28px; border-radius: 8px; font-weight: 600; text-decoration: none; transition: border-color 0.2s; }}
    .btn-ghost:hover {{ border-color: #fff; }}

    /* STATS */
    .stats {{ background: var(--primary); }}
    .stats-inner {{ max-width: 1200px; margin: 0 auto; padding: 40px 24px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; }}
    .stat-item {{ text-align: center; padding: 24px 16px; border-right: 1px solid rgba(255,255,255,0.1); }}
    .stat-item:last-child {{ border-right: none; }}
    .stat-number {{ font-size: 2.2rem; font-weight: 800; color: var(--accent); line-height: 1; }}
    .stat-label {{ font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 6px; }}
    @media (max-width: 640px) {{
      .stats-inner {{ grid-template-columns: repeat(2, 1fr); }}
      .stat-item:nth-child(2) {{ border-right: none; }}
      .stat-item:nth-child(3) {{ border-top: 1px solid rgba(255,255,255,0.1); }}
    }}

    /* SECTION WRAPPER */
    .section {{ padding: 80px 24px; }}
    .section-alt {{ background: #fff; }}
    .section-inner {{ max-width: 1200px; margin: 0 auto; }}
    .section-header {{ text-align: center; margin-bottom: 56px; }}
    .section-header .label {{ display: inline-block; background: var(--accent-light); color: var(--primary); padding: 4px 14px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px; }}
    .section-header h2 {{ font-size: clamp(1.6rem, 3vw, 2.4rem); font-weight: 800; letter-spacing: -0.02em; color: var(--text); }}
    .section-header p {{ color: var(--muted); margin-top: 12px; max-width: 600px; margin-left: auto; margin-right: auto; }}

    /* SERVICES */
    .services-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
    @media (max-width: 900px) {{ .services-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 560px) {{ .services-grid {{ grid-template-columns: 1fr; }} }}
    .service-card {{ background: var(--card); border: 1px solid #e5e7eb; border-radius: var(--radius); padding: 32px; transition: box-shadow 0.2s, transform 0.2s; }}
    .service-card:hover {{ box-shadow: var(--shadow); transform: translateY(-4px); }}
    .service-icon {{ font-size: 1.5rem; color: var(--accent); margin-bottom: 16px; }}
    .service-card h3 {{ font-size: 1.05rem; font-weight: 700; margin-bottom: 10px; color: var(--primary); }}
    .service-card p {{ font-size: 0.9rem; color: var(--muted); line-height: 1.65; }}

    /* AREAS */
    .areas-wrap {{ display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }}
    .area-tag {{ background: var(--card); border: 1.5px solid var(--accent); color: var(--primary); padding: 8px 18px; border-radius: 999px; font-size: 0.9rem; font-weight: 600; }}

    /* TESTIMONIALS */
    .testi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
    @media (max-width: 900px) {{ .testi-grid {{ grid-template-columns: 1fr; }} }}
    .testimonial-card {{ background: var(--card); border: 1px solid #e5e7eb; border-radius: var(--radius); padding: 32px; box-shadow: var(--shadow); }}
    .stars {{ color: var(--accent); font-size: 1.1rem; margin-bottom: 16px; }}
    .testi-text {{ font-size: 0.95rem; color: var(--text); font-style: italic; line-height: 1.7; margin-bottom: 20px; }}
    .testi-author strong {{ display: block; font-weight: 700; color: var(--primary); }}
    .testi-author span {{ font-size: 0.85rem; color: var(--muted); }}

    /* ABOUT */
    .about-inner {{ display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; }}
    @media (max-width: 768px) {{ .about-inner {{ grid-template-columns: 1fr; }} }}
    .about-text h2 {{ font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 20px; }}
    .about-text p {{ color: var(--muted); line-height: 1.8; margin-bottom: 24px; }}
    .about-cta {{ display: inline-block; background: var(--primary); color: #fff; padding: 14px 28px; border-radius: 8px; font-weight: 700; text-decoration: none; }}
    .about-visual {{ background: var(--gradient); border-radius: 16px; padding: 48px 32px; text-align: center; color: #fff; }}
    .about-visual p {{ font-size: 1.5rem; font-weight: 800; color: var(--accent); margin-bottom: 8px; }}
    .about-visual span {{ font-size: 0.9rem; color: rgba(255,255,255,0.7); }}

    /* FAQ */
    .faq-list {{ max-width: 800px; margin: 0 auto; }}
    .faq-item {{ border: 1px solid #e5e7eb; border-radius: var(--radius); margin-bottom: 12px; overflow: hidden; }}
    .faq-q {{ width: 100%; background: var(--card); border: none; padding: 20px 24px; text-align: left; font-size: 1rem; font-weight: 600; color: var(--text); cursor: pointer; display: flex; justify-content: space-between; align-items: center; }}
    .faq-q.active {{ color: var(--primary); }}
    .faq-arrow {{ transition: transform 0.3s; font-size: 0.75rem; color: var(--accent); }}
    .faq-q.active .faq-arrow {{ transform: rotate(180deg); }}
    .faq-a {{ max-height: 0; overflow: hidden; transition: max-height 0.3s ease; background: #f9fafb; }}
    .faq-a.open {{ max-height: 300px; }}
    .faq-a p {{ padding: 16px 24px; color: var(--muted); font-size: 0.95rem; line-height: 1.75; }}

    /* NEWS */
    .news-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
    @media (max-width: 1100px) {{ .news-grid {{ grid-template-columns: repeat(3, 1fr); }} }}
    @media (max-width: 768px) {{ .news-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 500px) {{ .news-grid {{ grid-template-columns: 1fr; }} }}
    .news-card {{ display: flex; flex-direction: column; background: var(--card); border: 1px solid #e5e7eb; border-radius: var(--radius); padding: 20px; text-decoration: none; color: inherit; transition: box-shadow 0.2s, transform 0.2s; }}
    .news-card:hover {{ box-shadow: var(--shadow); transform: translateY(-3px); }}
    .news-meta {{ display: flex; justify-content: space-between; margin-bottom: 10px; }}
    .news-source {{ font-size: 0.72rem; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em; }}
    .news-date {{ font-size: 0.72rem; color: var(--muted); }}
    .news-title {{ font-size: 0.9rem; font-weight: 700; line-height: 1.4; color: var(--text); margin-bottom: 8px; flex: 1; }}
    .news-desc {{ font-size: 0.82rem; color: var(--muted); line-height: 1.5; margin-bottom: 12px; }}
    .news-read {{ font-size: 0.8rem; font-weight: 600; color: var(--accent); margin-top: auto; }}

    /* CONTACT */
    .contact-wrap {{ display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: start; }}
    @media (max-width: 768px) {{ .contact-wrap {{ grid-template-columns: 1fr; }} }}
    .contact-info h2 {{ font-size: 2rem; font-weight: 800; margin-bottom: 20px; }}
    .contact-info p {{ color: var(--muted); line-height: 1.75; margin-bottom: 32px; }}
    .contact-detail {{ display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }}
    .contact-detail .icon {{ width: 40px; height: 40px; background: var(--accent-light); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; }}
    .contact-detail span {{ font-size: 0.95rem; color: var(--text); }}
    .contact-form {{ background: var(--card); border: 1px solid #e5e7eb; border-radius: 16px; padding: 40px; box-shadow: var(--shadow); }}
    .form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    @media (max-width: 480px) {{ .form-row {{ grid-template-columns: 1fr; }} }}
    .form-group {{ margin-bottom: 20px; }}
    .form-group label {{ display: block; font-size: 0.85rem; font-weight: 600; color: var(--text); margin-bottom: 6px; }}
    .form-group input, .form-group textarea, .form-group select {{
      width: 100%; padding: 12px 14px; border: 1.5px solid #d1d5db; border-radius: 8px;
      font-size: 0.95rem; font-family: inherit; color: var(--text); background: var(--bg);
      transition: border-color 0.2s; outline: none;
    }}
    .form-group input:focus, .form-group textarea:focus {{ border-color: var(--accent); }}
    .form-group textarea {{ min-height: 120px; resize: vertical; }}
    .btn-submit {{ width: 100%; background: var(--primary); color: #fff; border: none; padding: 16px; border-radius: 8px; font-size: 1rem; font-weight: 700; cursor: pointer; transition: opacity 0.2s; }}
    .btn-submit:hover {{ opacity: 0.88; }}

    /* LEASE CTA BANNER */
    .lease-banner {{ background: var(--gradient); color: #fff; padding: 64px 24px; text-align: center; }}
    .lease-banner h2 {{ font-size: 1.8rem; font-weight: 800; margin-bottom: 12px; }}
    .lease-banner p {{ color: rgba(255,255,255,0.8); margin-bottom: 32px; max-width: 600px; margin-left: auto; margin-right: auto; }}
    .lease-pricing {{ display: inline-flex; gap: 24px; flex-wrap: wrap; justify-content: center; margin-bottom: 32px; }}
    .lease-price {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.25); border-radius: 10px; padding: 20px 28px; }}
    .lease-price .price {{ font-size: 1.8rem; font-weight: 800; color: var(--accent); }}
    .lease-price .period {{ font-size: 0.8rem; color: rgba(255,255,255,0.7); }}

    /* FOOTER */
    .footer {{ background: var(--primary); color: rgba(255,255,255,0.6); padding: 32px 24px; text-align: center; font-size: 0.85rem; }}
    .footer a {{ color: rgba(255,255,255,0.6); text-decoration: none; }}
    .footer strong {{ color: rgba(255,255,255,0.9); }}
  </style>
</head>
<body>

<!-- NAV -->
<nav class="nav" id="home">
  <div class="nav-inner">
    <a class="nav-logo" href="#home">{biz.split()[0]} <span>{" ".join(biz.split()[1:]) if len(biz.split()) > 1 else ""}</span></a>
    <div class="nav-links">{nav_html}</div>
    <a href="#contact" class="nav-cta">{cta}</a>
  </div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-inner">
    <div class="hero-badge">{tagline}</div>
    <h1>{hero_h}</h1>
    <p class="hero-sub">{hero_s}</p>
    <div class="hero-btns">
      <a href="#contact" class="btn-primary">{cta}</a>
      <a href="#services" class="btn-ghost">View Our Services</a>
    </div>
  </div>
</section>

<!-- STATS -->
<div class="stats">
  <div class="stats-inner">
    {stats_html}
  </div>
</div>

<!-- SERVICES -->
<section class="section section-alt" id="services">
  <div class="section-inner">
    <div class="section-header">
      <div class="label">What We Do</div>
      <h2>Our Services</h2>
      <p>Comprehensive professional services tailored to your needs in {geo_place}.</p>
    </div>
    <div class="services-grid">
      {svcs_html}
    </div>
  </div>
</section>

<!-- SERVICE AREAS -->
<section class="section" id="areas">
  <div class="section-inner">
    <div class="section-header">
      <div class="label">Coverage</div>
      <h2>Service Areas</h2>
      <p>Proudly serving clients across these locations and surrounding communities.</p>
    </div>
    <div class="areas-wrap">
      {areas_html}
    </div>
  </div>
</section>

<!-- TESTIMONIALS -->
<section class="section section-alt">
  <div class="section-inner">
    <div class="section-header">
      <div class="label">Client Reviews</div>
      <h2>What Our Clients Say</h2>
      <p>Real results from real clients. Here's what they have to say about working with us.</p>
    </div>
    <div class="testi-grid">
      {testi_html}
    </div>
  </div>
</section>

<!-- ABOUT -->
<section class="section" id="about">
  <div class="section-inner">
    <div class="about-inner">
      <div class="about-text">
        <div class="label" style="display:inline-block;background:var(--accent-light);color:var(--primary);padding:4px 14px;border-radius:4px;font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;">About Us</div>
        <h2>Who We Are</h2>
        <p>{about}</p>
        <a href="#contact" class="about-cta">{cta}</a>
      </div>
      <div class="about-visual">
        <p>{cfg['stats'][0][0]}</p>
        <span>{cfg['stats'][0][1]}</span>
        <div style="margin: 24px 0; border-top: 1px solid rgba(255,255,255,0.2);"></div>
        <p>{cfg['stats'][1][0]}</p>
        <span>{cfg['stats'][1][1]}</span>
        <div style="margin: 24px 0; border-top: 1px solid rgba(255,255,255,0.2);"></div>
        <p>{cfg['stats'][2][0]}</p>
        <span>{cfg['stats'][2][1]}</span>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="section section-alt">
  <div class="section-inner">
    <div class="section-header">
      <div class="label">FAQ</div>
      <h2>Frequently Asked Questions</h2>
      <p>Quick answers to the questions we hear most often.</p>
    </div>
    <div class="faq-list">
      {faq_html}
    </div>
  </div>
</section>

<!-- NEWS -->
<section class="section" id="news">
  <div class="section-inner">
    <div class="section-header">
      <div class="label">Industry News</div>
      <h2>Latest Market Updates</h2>
      <p>Stay current with the latest news and trends in {cfg['niche']} — updated automatically.</p>
    </div>
    <div class="news-grid">
      {news_html}
    </div>
  </div>
</section>

<!-- CONTACT -->
<section class="section section-alt" id="contact">
  <div class="section-inner">
    <div class="contact-wrap">
      <div class="contact-info">
        <div class="label" style="display:inline-block;background:var(--accent-light);color:var(--primary);padding:4px 14px;border-radius:4px;font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;">Get In Touch</div>
        <h2>Contact Us Today</h2>
        <p>Ready to get started? Reach out now for a free consultation. We respond to all inquiries within 24 hours.</p>
        <div class="contact-detail">
          <div class="icon">📞</div>
          <span>{CONTACT_PHONE}</span>
        </div>
        <div class="contact-detail">
          <div class="icon">✉</div>
          <span>{CONTACT_EMAIL}</span>
        </div>
        <div class="contact-detail">
          <div class="icon">📍</div>
          <span>{geo_place}</span>
        </div>
      </div>
      <div class="contact-form">
        <form action="https://formspree.io/f/{FORMSPREE_ID}" method="POST">
          <input type="hidden" name="_subject" value="New inquiry from {domain}">
          <input type="hidden" name="domain" value="{domain}">
          <div class="form-row">
            <div class="form-group">
              <label for="fname">First Name *</label>
              <input type="text" id="fname" name="first_name" required placeholder="John">
            </div>
            <div class="form-group">
              <label for="lname">Last Name *</label>
              <input type="text" id="lname" name="last_name" required placeholder="Smith">
            </div>
          </div>
          <div class="form-group">
            <label for="email">Email Address *</label>
            <input type="email" id="email" name="email" required placeholder="john@example.com">
          </div>
          <div class="form-group">
            <label for="phone">Phone Number</label>
            <input type="tel" id="phone" name="phone" placeholder="(646) 555-0000">
          </div>
          <div class="form-group">
            <label for="message">How Can We Help? *</label>
            <textarea id="message" name="message" required placeholder="Tell us about your project or question..."></textarea>
          </div>
          <button type="submit" class="btn-submit">{cta} →</button>
        </form>
      </div>
    </div>
  </div>
</section>

<!-- LEASE BANNER -->
<section class="lease-banner">
  <h2>This Website Is Available for Lease</h2>
  <p>Interested in operating under the <strong>{domain}</strong> brand? Get a fully managed, professional website with ongoing content updates — without the setup cost.</p>
  <div class="lease-pricing">
    <div class="lease-price">
      <div class="price">$500</div>
      <div class="period">/ month</div>
    </div>
    <div class="lease-price">
      <div class="price">$4,800</div>
      <div class="period">/ year (save 20%)</div>
    </div>
  </div>
  <a href="mailto:{CONTACT_EMAIL}?subject=Domain Lease Inquiry: {domain}" class="btn-primary">Inquire About Leasing</a>
</section>

<!-- FOOTER -->
<footer class="footer">
  <p><strong>{biz}</strong> · {geo_place} · {CONTACT_PHONE} · <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
  <p style="margin-top:8px;">© {datetime.date.today().year} {biz}. All rights reserved. Last updated {today}.</p>
</footer>

</body>
</html>"""


def main():
    os.makedirs("sites", exist_ok=True)
    print(f"Building {len(DOMAINS)} professional business websites...")
    for domain, cfg in DOMAINS.items():
        print(f"  -> {domain} ({cfg['theme']})...", end=" ", flush=True)
        articles = fetch_articles(domain, cfg)
        html = generate_html(domain, cfg, articles)
        out_dir = os.path.join("sites", domain)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"done ({len(articles)} articles)")
    print(f"\nAll {len(DOMAINS)} sites generated successfully.")
    print("Next: fix edge function routing so sites/<domain>/index.html is served at domain root.")


if __name__ == "__main__":
    main()
