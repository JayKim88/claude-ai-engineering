# Technology Stack Guide

## Overview

This guide provides technology stack recommendations for different types of digital products, with focus on pragmatic choices for solo entrepreneurs and small teams. Recommendations prioritize speed of development, cost-effectiveness, and scalability.

---

## 1. SaaS Web Application

### Recommended Stack

**Frontend:** Next.js (React framework)
**Backend:** Next.js API Routes or separate Python/Node.js backend
**Database:** PostgreSQL (Supabase or Railway)
**Authentication:** NextAuth.js or Clerk
**Hosting:** Vercel
**File Storage:** Cloudflare R2 or AWS S3

### Detailed Breakdown

#### Frontend: Next.js 14+ (App Router)

**Why Next.js:**
- Server-side rendering (SSR) for better SEO
- File-based routing (easy to organize)
- API routes (backend in same codebase)
- Great developer experience
- Deploy to Vercel with zero config
- Large community and ecosystem

**Setup:**
```bash
npx create-next-app@latest my-saas-app
cd my-saas-app
npm run dev
```

**Project Structure:**
```
my-saas-app/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── signup/
│   ├── (dashboard)/
│   │   ├── projects/
│   │   ├── settings/
│   │   └── layout.tsx
│   ├── api/
│   │   ├── projects/
│   │   └── users/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   └── shared/
├── lib/
│   ├── db.ts
│   └── auth.ts
└── public/
```

**Key Libraries:**
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwindcss": "^3.3.0",
    "@radix-ui/react-dialog": "^1.0.0",
    "zustand": "^4.4.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0"
  }
}
```

#### Database: PostgreSQL (Supabase)

**Why PostgreSQL:**
- Robust, mature, reliable
- ACID compliant
- Excellent for relational data
- Great ecosystem (pgvector for AI, full-text search)

**Why Supabase:**
- Managed PostgreSQL
- Built-in authentication
- Real-time subscriptions
- Storage included
- Generous free tier (500MB database, 50,000 MAU)
- Auto-generated REST API
- Row-level security

**Setup:**
```bash
npm install @supabase/supabase-js
```

**Configuration (lib/supabase.ts):**
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

**Schema Example:**
```sql
-- Users table (Supabase auth.users)
create table public.profiles (
  id uuid references auth.users on delete cascade primary key,
  email text unique not null,
  full_name text,
  avatar_url text,
  created_at timestamp with time zone default now()
);

-- Projects table
create table public.projects (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references public.profiles on delete cascade not null,
  name text not null,
  description text,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Row Level Security
alter table public.profiles enable row level security;
alter table public.projects enable row level security;

-- Policies
create policy "Users can view own profile"
  on public.profiles for select
  using (auth.uid() = id);

create policy "Users can view own projects"
  on public.projects for select
  using (auth.uid() = user_id);
```

**Alternative: Railway + PostgreSQL**
- Managed PostgreSQL
- Simple deployment
- $5/month for database
- Good for custom backend needs

#### Authentication: Clerk

**Why Clerk:**
- Beautiful pre-built UI components
- Social login (Google, GitHub, etc.)
- Magic link authentication
- Multi-factor authentication built-in
- User management dashboard
- Free tier: 10,000 MAU

**Setup:**
```bash
npm install @clerk/nextjs
```

**Configuration (app/layout.tsx):**
```typescript
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  )
}
```

**Protected Route Example:**
```typescript
import { auth } from '@clerk/nextjs'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const { userId } = auth()

  if (!userId) {
    redirect('/login')
  }

  return <div>Dashboard</div>
}
```

**Alternative: NextAuth.js**
- Free, open-source
- More configuration required
- Good if you want full control

#### Hosting: Vercel

**Why Vercel:**
- Built by Next.js creators
- Zero-config deployment
- Automatic HTTPS
- Preview deployments for PRs
- Edge functions
- Free tier: Unlimited personal projects

**Deployment:**
```bash
# Push to GitHub, then connect repo in Vercel dashboard
# Or use CLI:
npm install -g vercel
vercel
```

**Environment Variables:**
```
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your-clerk-key
CLERK_SECRET_KEY=your-clerk-secret
```

### Cost Estimate (Monthly)

**Free Tier (MVP):**
```
Vercel: $0 (free tier)
Supabase: $0 (up to 500MB, 50k MAU)
Clerk: $0 (up to 10k MAU)
Domain: $12/year (~$1/month)

Total: ~$1/month
```

**Growth Tier (1,000-10,000 users):**
```
Vercel Pro: $20/month (better performance, team features)
Supabase Pro: $25/month (8GB database, 100k MAU)
Clerk Pro: $25/month (10k+ MAU)
Cloudflare R2: $1-5/month (file storage)

Total: ~$70-80/month
```

**Scale Tier (10,000-100,000 users):**
```
Vercel: $20-100/month (depending on traffic)
Supabase: $25-$50/month (scale database)
Clerk: $25-100/month (more MAU)
CDN/Storage: $10-50/month

Total: $80-300/month
```

### Scaling Path

**0-1,000 users:**
- Vercel free tier
- Supabase free tier
- No CDN needed
- Monolithic Next.js app

**1,000-10,000 users:**
- Upgrade Supabase to Pro
- Add CDN for static assets (Cloudflare)
- Consider database read replicas
- Optimize database queries (indexes)

**10,000-100,000 users:**
- Split backend into separate service (if needed)
- Database connection pooling
- Redis for caching (Upstash)
- Move heavy jobs to background workers (Inngest)
- Consider edge functions for global performance

**100,000+ users:**
- Microservices architecture (if needed)
- Database sharding
- Multi-region deployment
- Dedicated DevOps engineer

---

## 2. Mobile Application

### Recommended Stack

**Framework:** React Native with Expo
**Backend:** Firebase or Supabase
**State Management:** Zustand
**Navigation:** React Navigation
**Push Notifications:** Expo Notifications + Firebase Cloud Messaging

### Detailed Breakdown

#### Frontend: Expo (React Native)

**Why Expo:**
- Managed React Native (less configuration)
- Over-the-air updates (update without app store)
- Easy push notifications
- Built-in components for camera, maps, etc.
- EAS (Expo Application Services) for builds
- Can eject if you need native modules

**Setup:**
```bash
npx create-expo-app my-mobile-app
cd my-mobile-app
npx expo start
```

**Project Structure:**
```
my-mobile-app/
├── app/
│   ├── (tabs)/
│   │   ├── home.tsx
│   │   ├── profile.tsx
│   │   └── _layout.tsx
│   ├── _layout.tsx
│   └── index.tsx
├── components/
├── hooks/
├── services/
│   └── api.ts
└── app.json
```

**Key Libraries:**
```json
{
  "dependencies": {
    "expo": "~49.0.0",
    "react-native": "0.72.0",
    "react-navigation": "^6.0.0",
    "zustand": "^4.4.0",
    "@supabase/supabase-js": "^2.38.0",
    "react-native-reanimated": "^3.5.0"
  }
}
```

#### Backend: Firebase

**Why Firebase:**
- All-in-one backend (database, auth, storage, functions)
- Real-time database
- Excellent mobile SDKs
- Push notifications built-in
- Free tier: 10GB storage, 50k reads/day
- Google infrastructure

**Setup:**
```bash
npm install firebase
```

**Configuration:**
```typescript
import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'
import { getAuth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: process.env.EXPO_PUBLIC_FIREBASE_API_KEY,
  authDomain: "your-app.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-app.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-app-id"
}

const app = initializeApp(firebaseConfig)
export const db = getFirestore(app)
export const auth = getAuth(app)
```

**Firestore Example:**
```typescript
import { collection, addDoc, query, where, getDocs } from 'firebase/firestore'
import { db } from './firebase'

// Add document
await addDoc(collection(db, 'projects'), {
  name: 'New Project',
  userId: currentUser.uid,
  createdAt: new Date()
})

// Query documents
const q = query(
  collection(db, 'projects'),
  where('userId', '==', currentUser.uid)
)
const snapshot = await getDocs(q)
const projects = snapshot.docs.map(doc => ({
  id: doc.id,
  ...doc.data()
}))
```

**Alternative: Supabase for Mobile**
- More traditional SQL database
- Better for complex relational data
- Row-level security
- Real-time subscriptions
- Similar pricing to Firebase

#### Navigation: React Navigation

**Setup:**
```bash
npm install @react-navigation/native @react-navigation/native-stack
npx expo install react-native-screens react-native-safe-area-context
```

**Example:**
```typescript
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'

const Stack = createNativeStackNavigator()

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  )
}
```

### Cost Estimate (Monthly)

**Free Tier (MVP):**
```
Expo: $0 (free for development)
Firebase: $0 (Spark plan - 10GB, 50k reads/day)
EAS Build: $0 (limited builds)

Total: $0/month
```

**Growth Tier:**
```
Expo: $29/month (EAS updates, more builds)
Firebase Blaze: Pay-as-you-go (~$25-100/month for 10k users)
App Store: $99/year ($8/month)
Google Play: $25 one-time

Total: ~$70-150/month
```

### Deployment

**iOS:**
```bash
# Configure app.json with bundle identifier
eas build --platform ios
# Submit to App Store
eas submit --platform ios
```

**Android:**
```bash
eas build --platform android
eas submit --platform android
```

**Over-the-Air Updates:**
```bash
eas update --branch production --message "Bug fixes"
# Users get update without app store review
```

---

## 3. Marketplace Platform

### Recommended Stack

**Frontend:** Next.js
**Backend:** Node.js (Express) or Next.js API routes
**Database:** PostgreSQL
**Payment Processing:** Stripe Connect
**Search:** Algolia or Meilisearch
**Image Hosting:** Cloudinary
**Hosting:** Vercel + Railway

### Detailed Breakdown

#### Payment Processing: Stripe Connect

**Why Stripe Connect:**
- Built for marketplaces
- Handle payments between buyers and sellers
- Automatic seller payouts
- Tax handling
- Fraud protection
- Escrow support

**Setup:**
```bash
npm install stripe
```

**Connect Account Creation:**
```typescript
import Stripe from 'stripe'
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

// Create connected account for seller
const account = await stripe.accounts.create({
  type: 'express',
  country: 'US',
  email: seller.email,
  capabilities: {
    card_payments: { requested: true },
    transfers: { requested: true }
  }
})

// Generate onboarding link
const accountLink = await stripe.accountLinks.create({
  account: account.id,
  refresh_url: 'https://yoursite.com/reauth',
  return_url: 'https://yoursite.com/return',
  type: 'account_onboarding'
})
```

**Payment Intent (Marketplace):**
```typescript
// Create payment intent
const paymentIntent = await stripe.paymentIntents.create({
  amount: 10000, // $100.00
  currency: 'usd',
  application_fee_amount: 1500, // $15.00 platform fee (15%)
  transfer_data: {
    destination: sellerStripeAccountId
  },
  metadata: {
    orderId: order.id,
    sellerId: seller.id
  }
})
```

**Platform Fee Models:**
```
Option 1: Fixed percentage
- Take 10-20% of transaction
- Example: $100 sale → $15 fee → $85 to seller

Option 2: Dual fee
- Buyer pays 3% processing fee
- Seller pays 10% platform fee
- Example: $100 sale → Buyer pays $103, seller gets $90

Option 3: Subscription + lower fee
- Sellers pay $29/month
- Platform takes 5% instead of 15%
- Good for high-volume sellers
```

#### Search: Algolia

**Why Algolia:**
- Instant search results (<10ms)
- Typo tolerance
- Faceted filtering
- Relevance tuning
- Geo-search
- Free tier: 10k searches/month

**Setup:**
```bash
npm install algoliasearch
```

**Index Products:**
```typescript
import algoliasearch from 'algoliasearch'

const client = algoliasearch(
  process.env.ALGOLIA_APP_ID!,
  process.env.ALGOLIA_ADMIN_KEY!
)
const index = client.initIndex('products')

// Index products
await index.saveObjects([
  {
    objectID: '1',
    name: 'Vintage Leather Jacket',
    description: 'Authentic 1970s leather jacket',
    price: 250,
    category: 'clothing',
    sellerId: 'seller123',
    location: {
      lat: 40.7128,
      lng: -74.0060
    }
  }
])
```

**Search Frontend:**
```typescript
import { InstantSearch, SearchBox, Hits } from 'react-instantsearch'

export default function SearchPage() {
  return (
    <InstantSearch
      searchClient={searchClient}
      indexName="products"
    >
      <SearchBox />
      <Hits hitComponent={ProductCard} />
    </InstantSearch>
  )
}
```

**Alternative: Meilisearch**
- Open-source
- Self-hosted (cheaper for high volume)
- Similar features to Algolia
- Good for cost-conscious startups

#### Image Hosting: Cloudinary

**Why Cloudinary:**
- Automatic optimization
- On-the-fly transformations (resize, crop, format)
- CDN included
- Free tier: 25GB storage, 25GB bandwidth

**Setup:**
```bash
npm install cloudinary
```

**Upload:**
```typescript
import { v2 as cloudinary } from 'cloudinary'

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET
})

// Upload image
const result = await cloudinary.uploader.upload(file, {
  folder: 'products',
  transformation: [
    { width: 1000, height: 1000, crop: 'limit' },
    { quality: 'auto', fetch_format: 'auto' }
  ]
})

// URL with transformations
const thumbnailUrl = cloudinary.url(result.public_id, {
  width: 300,
  height: 300,
  crop: 'fill',
  gravity: 'auto'
})
```

### Database Schema Example

```sql
-- Users (buyers and sellers)
create table users (
  id uuid primary key default uuid_generate_v4(),
  email text unique not null,
  name text,
  stripe_customer_id text,
  stripe_account_id text, -- For sellers
  created_at timestamptz default now()
);

-- Listings
create table listings (
  id uuid primary key default uuid_generate_v4(),
  seller_id uuid references users(id),
  title text not null,
  description text,
  price decimal(10,2) not null,
  category text,
  images text[], -- Array of Cloudinary URLs
  status text default 'active', -- active, sold, archived
  created_at timestamptz default now()
);

-- Orders
create table orders (
  id uuid primary key default uuid_generate_v4(),
  buyer_id uuid references users(id),
  seller_id uuid references users(id),
  listing_id uuid references listings(id),
  amount decimal(10,2) not null,
  platform_fee decimal(10,2) not null,
  stripe_payment_intent_id text,
  status text default 'pending', -- pending, completed, cancelled
  created_at timestamptz default now()
);

-- Reviews
create table reviews (
  id uuid primary key default uuid_generate_v4(),
  order_id uuid references orders(id),
  reviewer_id uuid references users(id),
  reviewee_id uuid references users(id),
  rating integer check (rating >= 1 and rating <= 5),
  comment text,
  created_at timestamptz default now()
);
```

### Cost Estimate (Monthly)

**MVP (100 transactions/month):**
```
Vercel: $0
Railway (PostgreSQL): $5
Stripe: $0.30 + 2.9% per transaction (~$5)
Algolia: $0 (free tier)
Cloudinary: $0 (free tier)

Total: ~$10/month
```

**Growth (1,000 transactions/month):**
```
Vercel Pro: $20
Railway: $10-20 (database scaling)
Stripe fees: ~$50
Algolia: $0-50 (depending on searches)
Cloudinary: $0-50 (depending on usage)

Total: ~$130-190/month
```

---

## 4. AI-Powered Product

### Recommended Stack

**Frontend:** Next.js (React)
**Backend:** FastAPI (Python)
**AI/ML:** LangChain + OpenAI API
**Vector Database:** Pinecone or Qdrant
**Database:** PostgreSQL (Supabase)
**Hosting:** Vercel (frontend) + Modal or Railway (backend)

### Detailed Breakdown

#### Backend: FastAPI

**Why FastAPI:**
- Fast performance (async support)
- Automatic API documentation (Swagger)
- Python (best for AI/ML libraries)
- Easy to integrate with LangChain, OpenAI

**Setup:**
```bash
pip install fastapi uvicorn python-dotenv
```

**Example API:**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="gpt-4"
    )

    prompt = PromptTemplate(
        input_variables=["message"],
        template="You are a helpful assistant. User: {message}\nAssistant:"
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    response = await chain.arun(message=request.message)

    return {"response": response}
```

#### Vector Database: Pinecone

**Why Pinecone:**
- Managed vector database
- Fast similarity search
- Easy integration with LangChain
- Free tier: 1 index, 1M vectors

**Setup:**
```bash
pip install pinecone-client langchain openai
```

**Embedding and Search:**
```python
import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

# Initialize
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment="us-west1-gcp"
)

embeddings = OpenAIEmbeddings()

# Create index (one-time)
pinecone.create_index("documents", dimension=1536)

# Add documents
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_text(long_text)

vectorstore = Pinecone.from_texts(
    texts=documents,
    embedding=embeddings,
    index_name="documents"
)

# Search
query = "What is the pricing?"
docs = vectorstore.similarity_search(query, k=3)
```

**Alternative: Qdrant**
- Open-source
- Self-hostable
- Free tier available (cloud)
- Good for cost-conscious projects

#### LangChain Integration

**RAG (Retrieval-Augmented Generation) Example:**
```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Create QA chain
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(model_name="gpt-4"),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Query
question = "How do I reset my password?"
answer = qa.run(question)
```

**Streaming Responses:**
```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = OpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    model_name="gpt-4"
)

# Streams response token by token
response = llm("Tell me a story")
```

#### Hosting: Modal

**Why Modal:**
- Serverless Python functions
- GPU support for ML models
- Auto-scaling
- Pay per second
- Great for AI/ML workloads

**Setup:**
```bash
pip install modal-client
modal token new
```

**Deployment:**
```python
import modal

stub = modal.Stub("my-ai-app")

@stub.function()
def generate_text(prompt: str):
    from langchain.llms import OpenAI
    llm = OpenAI(model_name="gpt-4")
    return llm(prompt)

@stub.local_entrypoint()
def main():
    result = generate_text.remote("Hello, AI!")
    print(result)
```

### Cost Estimate (Monthly)

**MVP (1,000 API calls/month):**
```
Vercel: $0
Modal: ~$10-20 (pay per use)
OpenAI API: ~$20-50 (gpt-4 usage)
Pinecone: $0 (free tier)
Supabase: $0

Total: ~$30-70/month
```

**Growth (10,000 API calls/month):**
```
Vercel: $20
Modal: ~$50-100
OpenAI API: ~$200-500
Pinecone: $70 (Standard plan)
Supabase Pro: $25

Total: ~$365-715/month
```

**Optimization Tips:**
- Use gpt-3.5-turbo instead of gpt-4 (10x cheaper)
- Cache common queries
- Limit response token length
- Use cheaper models for simple tasks

---

## 5. E-commerce Store

### Recommended Stack

**Option A: Shopify (No-code/Low-code)**
- Best for: Simple products, fast launch
- Cost: $29-$299/month
- Pros: Everything built-in, easy, reliable
- Cons: Limited customization, transaction fees

**Option B: Custom (Next.js + Shopify API)**
- Best for: Unique UX, full control
- Cost: $5-$100/month + dev time
- Pros: Full customization, lower fees
- Cons: More development required

### Custom E-commerce Stack

**Frontend:** Next.js
**Payment:** Stripe
**Database:** PostgreSQL or MongoDB
**CMS:** Sanity or Contentful
**Hosting:** Vercel
**Email:** Resend or SendGrid

#### Product Schema

```sql
create table products (
  id uuid primary key,
  name text not null,
  description text,
  price decimal(10,2) not null,
  images text[], -- Array of URLs
  inventory integer default 0,
  category text,
  slug text unique,
  created_at timestamptz default now()
);

create table orders (
  id uuid primary key,
  user_id uuid references users(id),
  total decimal(10,2) not null,
  status text default 'pending',
  stripe_payment_intent_id text,
  shipping_address jsonb,
  created_at timestamptz default now()
);

create table order_items (
  id uuid primary key,
  order_id uuid references orders(id),
  product_id uuid references products(id),
  quantity integer not null,
  price_at_purchase decimal(10,2) not null
);
```

#### Stripe Checkout

```typescript
import Stripe from 'stripe'
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

// Create checkout session
const session = await stripe.checkout.sessions.create({
  payment_method_types: ['card'],
  line_items: cartItems.map(item => ({
    price_data: {
      currency: 'usd',
      product_data: {
        name: item.name,
        images: [item.image]
      },
      unit_amount: item.price * 100 // cents
    },
    quantity: item.quantity
  })),
  mode: 'payment',
  success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${process.env.NEXT_PUBLIC_URL}/cart`,
  metadata: {
    orderId: order.id
  }
})

// Redirect to checkout
window.location.href = session.url
```

### Cost Estimate

**Shopify Route:**
```
Shopify Basic: $29/month
Apps: $0-50/month
Transaction fees: 2.9% + 30¢

For $10k/month revenue: ~$320/month
```

**Custom Route:**
```
Vercel: $0-20
Database: $0-10
Stripe: 2.9% + 30¢ (no monthly fee)

For $10k/month revenue: ~$310/month (lower fees at scale)
```

---

## Summary: Stack Selection Matrix

| Product Type | Frontend | Backend | Database | Hosting | Monthly Cost (MVP) |
|--------------|----------|---------|----------|---------|-------------------|
| SaaS Web App | Next.js | Next.js API / Python | PostgreSQL (Supabase) | Vercel | $0-10 |
| Mobile App | React Native (Expo) | Firebase / Supabase | Firestore / PostgreSQL | Expo + Firebase | $0-20 |
| Marketplace | Next.js | Node.js | PostgreSQL | Vercel + Railway | $10-50 |
| AI Product | Next.js | FastAPI (Python) | PostgreSQL + Pinecone | Vercel + Modal | $30-100 |
| E-commerce | Next.js / Shopify | Shopify / Next.js API | PostgreSQL / Shopify | Vercel / Shopify | $29-100 |

**General Recommendations:**
- **Start simple:** Use managed services (Vercel, Supabase, Firebase)
- **Optimize later:** Don't over-engineer early
- **Use TypeScript:** Type safety prevents bugs
- **Monitor from day 1:** Use Sentry for errors, PostHog for analytics
- **Automate deployments:** CI/CD with GitHub Actions

The best stack is the one you can ship quickly with. Perfect is the enemy of done.
