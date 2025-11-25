# PartSelect Chat Agent - Instalily AI Case Study

LOOM LINK: https://www.loom.com/share/5a187da5f73d4ea29a12524781fc30fb

This is my submission for the Instalily AI case study. I built an intelligent chat agent for PartSelect that helps customers find and install refrigerator and dishwasher parts. The agent uses React for the frontend, Node.js/Express for the backend, and integrates with Deepseek's LLM to understand what users are asking for.

## What It Does

The chat agent can handle several types of queries:

- **Installation help** - Ask about installing a specific part number and get step-by-step instructions
- **Compatibility checks** - Find out if a part works with your appliance model
- **Troubleshooting** - Describe a problem (like "ice maker not working") and get part recommendations
- **Product search** - Look for parts by name, type, or brand

I focused on creating a clean, intuitive interface that matches PartSelect's branding, with visual product cards and easy-to-follow installation steps. The agent is smart enough to stay on topic - if you ask about something unrelated to appliance parts, it'll politely redirect you back.

The product data is real - I scraped 19 actual parts from PartSelect.com with their actual prices (ranging from $22.42 to $218.18).

## How It Works

I designed the system to work like a pipeline:

1. **User asks a question** → Deepseek figures out what they're really asking about
2. **Intent classification** → The system determines if they want installation help, compatibility info, troubleshooting, or product search
3. **Tool execution** → Based on the intent, the appropriate tool runs (search the parts database, check compatibility, get installation steps, etc.)
4. **Response generation** → Deepseek takes the results and writes a natural, helpful response

The key insight here was separating the "understanding" phase from the "doing" phase. Deepseek is great at understanding what users mean, even when they phrase things awkwardly. Then I have specific tools that do the actual work of finding parts, checking compatibility, etc. Finally, Deepseek takes those results and explains them in plain English.

I built four main tools:
- **search_parts** - Finds parts by name, type, brand, or the symptoms they fix
- **check_compatibility** - Checks if a part works with a specific model number
- **get_installation_steps** - Pulls up installation instructions for a part
- **troubleshoot_symptoms** - Recommends parts based on what's broken

## Tech Stack

**Frontend**
- React - I went with Create React App to get up and running quickly
- Axios for API calls
- Marked library to render markdown responses nicely
- RSuite CSS for some base styling

**Backend**
- Node.js with Express - simple, straightforward REST API
- Deepseek API (deepseek-chat model) - honestly impressed with how well it handles structured outputs
- JSON file for the product database (would use a real database in production)

**Data Collection**
- Python with BeautifulSoup to scrape PartSelect.com
- Got 19 real parts (11 refrigerator, 8 dishwasher) from Whirlpool and GE
- All prices are real from their website

## Installation

### Prerequisites
- Node.js v18+ 
- npm or yarn

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd case-study
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
```bash
cd backend
cp .env.example .env
# Edit .env and add your Deepseek API key
DEEPSEEK_API_KEY=your_api_key_here
```

4. **Start the backend server**
```bash
cd backend
node server.js
# Server runs on http://localhost:3001
```

5. **Start the frontend (in a new terminal)**
```bash
npm start
# App opens at http://localhost:3000
```

## Usage

### Example Queries (from case study requirements)

1. **Installation Query**
   ```
   "How can I install part number PS11752778?"
   ```
   Returns: Step-by-step installation instructions with part details

2. **Compatibility Query**
   ```
   "Is this part compatible with my WDT780SAEM1 model?"
   ```
   Returns: Compatibility confirmation with compatible parts list

3. **Troubleshooting Query**
   ```
   "The ice maker on my Whirlpool fridge is not working"
   ```
   Returns: Recommended parts that fix ice maker issues

### Additional Query Types

- Search by part type: *"Show me dishwasher pump parts"*
- Search by brand: *"I need GE refrigerator parts"*
- General search: *"water filter for refrigerator"*

## How I Got the Real Product Data

I wanted to use actual PartSelect products rather than making up fake data, so I built a Python scraper to pull real information from their website.

**The Approach:**
First, I researched popular parts on PartSelect and identified about 20 common part numbers (things like ice makers, water valves, dishwasher pumps, etc.). I noticed their URL pattern was predictable: `partselect.com/{PartNumber}-{Brand}-{ManufacturerNumber}.htm`

**The Scraper:**
I used Python with BeautifulSoup and Requests to:
- Hit each product page
- Extract the part number, manufacturer number, name, and most importantly the actual price
- Pull descriptions and what symptoms each part fixes
- Grab the product URLs so users can go directly to PartSelect

**The Challenge:**
PartSelect has anti-scraping measures (as they should), so I had to be respectful - proper user agent headers, rate limiting between requests, etc. I successfully scraped 19 parts before hitting their rate limits, which was enough for this demo.

**The Enhancement:**
The scraper got most of the data, but I manually added some realistic compatible model numbers (like WDT780SAEM1, WRS325SDHZ) based on typical compatibility for those part types. In a production system, this would come from PartSelect's API or a more comprehensive scraping setup.

**Result:** All 19 parts in the database are real - real part numbers, real prices, real product pages you can visit on PartSelect.com

## 🧪 Testing

### Test All Example Queries

Open the chat interface at `http://localhost:3000` and test:

- Installation: "How can I install part number PS11752778?"
- Compatibility: "Is part PS11752778 compatible with my WDT780SAEM1 model?"
- Troubleshooting: "The ice maker on my Whirlpool fridge is not working"

### Test Out-of-Scope

Try: "What's the weather today?" or "How do I fix my car?"  
Expected: Polite message redirecting to PartSelect-related questions

## Project Structure

```
case-study/
├── backend/
│   ├── server.js              # Express server
│   ├── .env                   # Deepseek API key
│   ├── routes/
│   │   └── chat.js            # Chat API endpoint
│   ├── services/
│   │   ├── chatService.js     # Main chat pipeline orchestration
│   │   ├── deepseekService.js # Deepseek API integration
│   │   └── toolExecutor.js    # Tool execution logic
│   └── data/
│       └── seedParts.json     # 19 real products from PartSelect
├── src/
│   ├── App.js                 # Main React app
│   ├── components/
│   │   ├── ChatWindow.js      # Chat interface
│   │   ├── ProductCard.js     # Product display component
│   │   └── InstallationSteps.js # Installation steps component
│   └── api/
│       └── api.js             # Frontend API client
└── public/
    └── index.html
```

## UI Features

- **Product Cards**: Display part details with images, prices, compatible models, and symptoms fixed
- **Installation Steps**: Numbered step visualization for installation instructions
- **Loading States**: Animated typing indicator during API calls
- **Quick Actions**: Pre-configured query buttons for common use cases
- **Message History**: Full conversation context preserved
- **Responsive Design**: Works on desktop and mobile
- **PartSelect Branding**: Blue gradient theme matching PartSelect's brand colors

## Extending the System

I designed this to be easy to extend. Here's how you'd add new capabilities:

**Adding a New Type of Query:**
Say you want to add "price comparison" functionality:
1. Update the intent classification prompt in `deepseekService.js` to recognize "price_comparison" as an intent
2. Write a new tool function in `toolExecutor.js` that compares prices
3. Make sure the response generation knows how to present price comparison data

**Adding a New Tool:**
```javascript
// Just add to toolExecutor.js
function compare_prices(params) {
  const parts = findSimilarParts(params.part_type);
  return parts.sort((a, b) => a.price - b.price);
}
```

**Adding More Products:**
The simplest way is to edit `backend/data/seedParts.json` directly. Each part needs:
- `part_number`: The PartSelect PS number
- `name`: What it's called
- `type`: "refrigerator" or "dishwasher"
- `brand`: Manufacturer
- `price`: Actual price
- `compatible_models`: Array of model numbers
- `symptoms_fixed`: What problems it solves

In production, you'd probably want a proper database and an admin interface for managing this.

## Why I Chose Deepseek

The case study required using Deepseek, but honestly, I was pleasantly surprised by how well it worked. I'm using the `deepseek-chat` model for two different purposes:

**1. Understanding What Users Want (Intent Classification)**
I send the user's message to Deepseek with a prompt that says "figure out what this person is asking for and give me back JSON." I set the temperature to 0.3 to keep it deterministic - I need reliable JSON structure here, not creativity. It returns something like:
```json
{ "intent": "installation", "part_number": "PS11752778" }
```

**2. Writing the Response**
After my tools do their thing and find the relevant parts or info, I send that data back to Deepseek and ask it to write a helpful, conversational response. Here I bump the temperature to 0.7 so it sounds natural and not robotic.

**Why it works well:**
- Really fast response times (important for chat)
- Surprisingly good at structured JSON output - I tested GPT-4 too and Deepseek was more consistent
- Actually understands the appliance repair domain without much prompting
- Cost-effective if this were going to production

## Data Statistics

- **Total Parts:** 19
- **Refrigerator Parts:** 11
- **Dishwasher Parts:** 8
- **Whirlpool Parts:** 12
- **GE Parts:** 7
- **Price Range:** $22.42 - $218.18
- **Average Price:** $108.51

## Known Limitations & What I'd Do Next

**Current Limitations:**
- Only 19 parts in the database (limited by scraping time/rate limits)
- Installation instructions are pretty basic - would be great to add diagrams or videos
- No actual shopping cart or checkout (this is a demo, not a full e-commerce integration)
- Compatible models are curated rather than comprehensive

**If I Had More Time:**
- Scrape way more products (or ideally, get access to PartSelect's actual API)
- Add order tracking - "where's my part?"
- Include installation videos embedded in the responses
- Support Spanish - lots of PartSelect customers would benefit
- Add voice input for hands-free use during repairs
- Build admin tools to easily add/update parts without touching the JSON file

## License

This project is submitted as part of the Instalily AI case study interview process.

## Author

Kosta Karathanasopoulos  
Case Study Submission for Instalily AI  
November 25, 2025

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
