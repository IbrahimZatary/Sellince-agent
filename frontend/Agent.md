create this website 
split each staeg with git push      
Yes. What you have here is enough to turn into a proper product/engineering specification, rather than sending the coding agent a huge informal prompt.
I would structure it as a project specification package with AGENTS.md, PRD.md, ARCHITECTURE.md, ROUTES.md, COMPONENTS.md, and TASKS.md.
Below is the version I'd give the agent as the source of truth.
Recommended project structure
sellince-platform/├── AGENTS.md├── README.md├── package.json├── vite.config.js├── src/│   ├── app/│   │   ├── router/│   │   ├── providers/│   │   └── config/│   ││   ├── components/│   │   ├── ui/│   │   ├── layout/│   │   ├── charts/│   │   ├── tables/│   │   ├── conversations/│   │   └── onboarding/│   ││   ├── pages/│   │   ├── auth/│   │   ├── onboarding/│   │   ├── dashboard/│   │   ├── conversations/│   │   ├── settings/│   │   └── demo/│   ││   ├── features/│   │   ├── auth/│   │   ├── company/│   │   ├── agent/│   │   ├── conversations/│   │   ├── analytics/│   │   └── onboarding/│   ││   ├── services/│   │   └── api/│   │       ├── client.js│   │       ├── interceptors.js│   │       ├── auth.api.js│   │       ├── company.api.js│   │       ├── conversations.api.js│   │       ├── analytics.api.js│   │       └── settings.api.js│   ││   ├── hooks/│   ├── utils/│   ├── types/│   └── assets/│├── docs/│   ├── PRD.md│   ├── ARCHITECTURE.md│   ├── ROUTES.md│   ├── COMPONENTS.md│   ├── API.md│   ├── DATA_MODEL.md│   ├── UX_FLOW.md│   └── TASKS.md│└── tests/

1. AGENTS.md

Project
Sellince — AI Agent Management & Customer Engagement Platform
This repository contains the frontend application for a multi-company platform where companies can configure and monitor AI agents that communicate with their end users.
The application must be designed as a production-grade, scalable React application.

1. Engineering Principles
The implementation must prioritize:
Maintainability
Scalability
Reusability
Separation of concerns
Type safety where applicable
Responsive behavior
Accessibility
Performance
Clear component boundaries
API isolation
Do not build the application as a collection of large page components.
Pages must compose reusable components.

2. Technology Stack
Use:
React 19
Vite
React Router DOM
Tailwind CSS
Axios
JavaScript/TypeScript according to the existing project configuration
Do not introduce additional libraries unless there is a clear requirement.
If an additional dependency is genuinely necessary, explain why before introducing it.
-------------------------------------------------------
3. Architecture
Use a layered architecture.
UI components must not directly contain API implementation.
Recommended flow:
Page
↓
Feature/component
↓
Hook/state
↓
API service
↓
Axios client
↓
Backend
Do not place Axios calls directly inside UI components.

4. API Architecture
All API communication must be isolated under:
src/services/api/
Create a centralized Axios client.
The Axios client must support:
Base URL configuration
Request interceptor
Response interceptor
Error normalization
Future JWT authorization
Future token refresh handling
JWT authorization must be architected but MUST NOT be activated or implemented as a working authentication mechanism until backend integration is introduced.
The frontend should therefore be ready for:
Authorization: Bearer
but should not invent authentication behavior or fake backend authentication.
API URLs must be configurable through environment variables.
Never hardcode production API URLs inside components.

5. Authentication
The frontend must support these conceptual states:
Logged out
Login
Signup
Onboarding
Authenticated company user
Current implementation may use mocked/local development data where necessary.
Do not pretend that frontend-only authentication is secure.
Backend authentication will be integrated later.
The architecture must make that integration straightforward.

6. Multi-Company Architecture
The platform is company-based.
A company has:
Company identity
Users
Agents
End users/customers
Conversations
Analytics
Settings
The current primary role is:
SUPER_ADMIN
The architecture should allow future roles such as:
SUPER_ADMIN
ADMIN
SALES_AGENT
CUSTOMER_SUPPORT_AGENT
VIEWER
Do not implement unnecessary permissions now, but do not architect the application in a way that prevents role-based access control later.

7. Component Rules
Components must have one clear responsibility.
Avoid:
Huge page components
Repeated UI
Hardcoded tables
Hardcoded dashboard cards
Hardcoded navigation
Business logic inside presentation components
Prefer reusable components such as:
MetricCard
ChartCard
DataTable
StatusBadge
ConversationList
ConversationItem
MessageBubble
AgentStatus
SearchInput
FilterDropdown
Sidebar
Topbar
Modal
EmptyState
LoadingState
ErrorState
OnboardingStep
ProgressIndicator
Components should receive data through props/configuration whenever practical.

8. Dynamic Data
Dashboard and conversation data must be represented as structured data objects.
Do not hardcode values directly into JSX.
Example:
const metrics = [
{
id: "revenue",
label: "Revenue generated",
value: 184300,
currency: "JOD",
trend: 22.4
}
];
The example values in the product specification are demonstration values only.
They are not production/business requirements.
--------------------------------------
9. Dashboard
The dashboard must be designed to consume backend/API data later.
The dashboard should contain reusable sections for:
Overview metrics
Revenue / ARPU trend
Conversion funnel
Revenue by offer type
Agent autonomy
Recent agent activity
The implementation must not assume that the example numbers supplied in the specification are real.
All values should come from a data layer.

10. Conversations
The conversation interface is a core product area.
Users must be able to:
View AI agent conversations
Search conversations
Filter conversations
Open a conversation
View customer information
View conversation history
Identify whether AI or human is currently handling the conversation
Take over a conversation manually
Respond as a human agent after escalation
Return handling to the AI agent where permitted
Human takeover must be represented as an explicit state transition.
Example:
AI_HANDLING
→ HUMAN_REQUESTED
→ HUMAN_HANDLING
→ RESOLVED
Do not implement real-time/backend behavior before backend integration.
Create clean interfaces that can later consume WebSocket/SSE/API events.

11. Demo / Training
After successful signup and onboarding, the user should enter a guided demo/training experience.
The demo is a product walkthrough.
It is NOT a complete training system.
The walkthrough should introduce major platform sections such as:
Dashboard
Conversations
AI Agent
Analytics
Settings
Each step should explain the purpose of the relevant section.
The walkthrough must be reusable and configurable rather than hardcoded into individual pages.

12. Responsive Design
The entire application must be responsive.
Support:
Desktop
Laptop
Tablet
Mobile
The sidebar, tables, dashboard cards, charts, and conversation UI must adapt appropriately.
Do not simply shrink desktop layouts.
Use appropriate responsive layouts and interaction patterns.

13. Design
Visual direction:
Clean
Modern
Playful geometric
Professional SaaS
Strong visual hierarchy
Clear spacing
Minimal unnecessary decoration
The provided Sellince HTML files are visual/product references.
Use them to understand the intended UI direction, structure, spacing, interaction patterns, and visual language.
Do not copy implementation code blindly.
The new application must be implemented using the specified React architecture.

14. Navigation
Navigation must be configuration-driven where practical.
Do not duplicate sidebar navigation definitions across pages.
The sidebar should support sections such as:
Dashboard
Conversations
AI Agent
Analytics
Settings
Additional sections can be added through configuration as the product expands.

15. Error / Loading / Empty States
Every data-driven page should have appropriate:
Loading state
Error state
Empty state
Do not leave blank screens when data is unavailable.

16. Backend Independence
The frontend must not depend on mocked data being embedded throughout components.
Mock data should live in a dedicated development/mock layer.
When backend APIs become available, replacing mock services should not require rewriting page components.

17. Scope Control
Do not invent product functionality.
Do not add:
Billing
Payments
WhatsApp integration
CRM integrations
Real-time infrastructure
Advanced permissions
Backend implementation
unless explicitly requested.
Build the frontend architecture so these can be added later.

18. Quality Gate
Before declaring a task complete:
Verify the application builds.
Verify routes work.
Verify responsive behavior.
Verify affected components.
Verify no unnecessary duplication.
Verify API calls remain isolated.
Verify no secrets are committed.
Verify no unrelated files were changed.
Verify the implementation follows this document.
Never claim a test/build passed unless it was actually executed.

2. PRD.md
PRD — Sellince Platform
1. Product
Sellince is a SaaS platform that allows companies to deploy, monitor, and manage AI agents that communicate with their customers.
The first frontend version focuses on:
Company registration
Company onboarding
Company dashboard
AI agent conversations
Human takeover
Search
Settings
Guided demo/training

2. User Journey
The primary user journey is:
porfolio page : 
present the idea 
flow 
the ROI as you a company you will take 
plans to take 
{
    Make the plans empty
    as 3 plans basic , advance , elite {contact sales }
    dont add content make it ready to add th content in the future  

}
New Company
→ Signup
→ Company Information
→ Agent Behavior Configuration
→ Onboarding Complete
→ Product Demo / Guided Tour
→ Dashboard
→ Conversations
→ Settings
Returning Company:
Login
→ Dashboard

3. Authentication
Login
Fields:
Company email
Password
Actions:
Login
Navigate to application after successful authentication
Forgot password may be represented in the UI architecture but does not need backend functionality at this stage.

4. Signup
Signup consists of multiple stages.
Page 1 — Company Information
Fields:
Company Name
Email
Password
Re-enter Password
Validation:
Required fields
Valid email format
Password required
Password confirmation must match

Page 2 — Agent Behavior
The company selects the initial business behavior/context for its AI agent.
Options:
Telecommunications
The AI agent is configured conceptually for a telecommunications company.
Banking
The AI agent is configured conceptually for a banking environment.
The architecture must allow additional industries to be added later without rewriting the onboarding flow.

5. Onboarding Completion
After signup is completed:
Create the company onboarding state.
Show a product walkthrough.
Introduce the main application sections.
Allow the user to navigate through the guided experience.
After the walkthrough, enter the main dashboard.
The walkthrough should be skippable if product requirements later allow it.

6. Main Application
Sidebar
The primary navigation should include:
Dashboard
Conversations
AI Agent
Analytics
Settings
The exact enabled sections can evolve as the product expands.

7. Dashboard
The dashboard is the company Super Admin's primary overview.
Purpose:
Give the company an immediate understanding of AI agent performance and business impact.

Overview
Display configurable metrics such as:
Conversations
Revenue generated
Revenue trend
ARPU uplift
Conversion rate
Churn prevented
The values provided in the original specification are examples only.
The frontend must use structured dynamic data.

Revenue & ARPU Trend
Display a chart representing historical performance.
Possible dimensions:
Revenue
ARPU
Volume
Baseline
The chart must be reusable and accept dynamic datasets.

Conversion Funnel
Display stages such as:
Engaged proactively
↓
Customer replied
↓
Offer presented
↓
Accepted & closed
Each stage should support:
Label
Count
Percentage
Optional comparison

Revenue by Offer Type
Display revenue grouped by configurable offer categories.
Examples:
Data upgrades
Device upsell
Add-ons & roaming
Retention saves
These are examples and must not be treated as fixed business categories.

Agent Autonomy
Show how conversations are currently handled.
Example categories:
Auto-resolved
Handed to human
Follow-up queued
The categories must be data-driven.

Recent Agent Activity
Display recent AI agent activity.
Suggested fields:
Customer
Customer identifier
Signal detected
Offer/action
Status
Value
Timestamp
Example statuses:
Won
In progress
Handed to human
Follow-up
Closed

8. Conversations
Conversations are a primary operational interface.
The page should have a layout similar to modern customer-support inbox products.
Suggested structure:
┌─────────────────────────────────────────────┐
│ Search / Filters │
├──────────────┬──────────────────────────────┤
│ Conversations│ Conversation │
│ │ │
│ Customer │ Customer header │
│ Preview │ │
│ Status │ Message history │
│ Time │ │
│ │ │
│ │ Composer │
└──────────────┴──────────────────────────────┘

Conversation List
Each item may contain:
Customer name
Customer identifier
Last message
Timestamp
Status
Handling mode
Unread state

Conversation Search
Users must be able to search conversations.
Search should eventually support:
Customer name
Customer identifier
Conversation content
Conversation ID
The frontend should expose a search interface that can later connect to backend search.

9. AI / Human Handling
Every conversation has a handling mode.
Possible states:
AI
Human
Escalated
Resolved
Example flow:
AI handling
→ Customer requests human
→ Escalation
→ Human takes over
→ Human responds
→ Conversation resolved
The UI must clearly communicate who currently controls the conversation.

10. Human Takeover
A Sales Agent or Customer Support Agent should be able to take control of a conversation.
Possible actions:
Take Over
Transfers conversation handling from AI to human.
Respond
Allows the human agent to send a response.
Release to AI
Returns the conversation to AI handling where business rules allow it.
These actions must be represented through service interfaces so backend behavior can be connected later.

11. Settings
Settings must appear in the sidebar.
The Settings architecture should be extensible.
Potential sections:
Company
Profile
AI Agent
Notifications
Team
Integrations
Security
Only the required frontend screens should be implemented initially.

12. Demo / Training
The first-time company experience should include a guided walkthrough.
Example:
Step 1
Dashboard
"See your company's overall AI performance."
Step 2
Conversations
"Review customer conversations and take over when needed."
Step 3
AI Agent
"Configure and understand your agent behavior."
Step 4
Analytics
"Measure business impact."
Step 5
Settings
"Manage company and platform configuration."
The walkthrough should use a reusable step configuration.

13. Non-Goals
This frontend phase does not include:
Backend implementation
Real JWT authentication
Real customer messaging
WhatsApp integration
Real-time WebSocket implementation
Payment processing
Billing
Production AI inference
Production database
The architecture must support these capabilities later.

3. ARCHITECTURE.md
ARCHITECTURE.md
1. Architecture Goal
Build Sellince as a modular frontend application where UI, business logic, data access, and infrastructure concerns are separated.
The application must remain easy to modify when backend services are introduced.

2. Application Layers
┌──────────────────────────────┐│            Pages             │├──────────────────────────────┤│       Feature Components     │├──────────────────────────────┤│       Hooks / State          │├──────────────────────────────┤│        API Services          │├──────────────────────────────┤│       Axios Client           │├──────────────────────────────┤│          Backend             │└──────────────────────────────┘

3. Pages
Pages represent routes.
Examples:
/pages/auth/Login/pages/auth/Signup/pages/onboarding/CompanyInfo/pages/onboarding/AgentBehavior/pages/dashboard/Dashboard/pages/conversations/Conversations/pages/settings/Settings/pages/demo/ProductTour
Pages should compose components rather than implement complex reusable UI themselves.

4. Components
Reusable UI should live under:
src/components/
Suggested categories:
components/├── ui/├── layout/├── charts/├── tables/├── conversations/└── onboarding/

5. Feature Modules
Business-specific logic should live under:
src/features/
Examples:
features/├── auth/├── company/├── agent/├── conversations/├── analytics/└── onboarding/
A feature can contain:
hooks
utilities
state
types
feature-specific components

6. API Layer
All backend interaction belongs under:
src/services/api/
Example:
api/├── client.js├── interceptors.js├── auth.api.js├── company.api.js├── agent.api.js├── conversations.api.js├── analytics.api.js└── settings.api.js

7. Axios
Create a single configured Axios client.
Responsibilities:
Base URL
Default headers
Request interceptor
Response interceptor
Error normalization
Future JWT injection
Components must never import Axios directly.
Bad:
import axios from "axios";
inside a component.
Preferred:
import { getConversations } from "@/services/api/conversations.api";

8. JWT Preparation
JWT support should be architected but not activated before backend integration.
The Axios interceptor should have a clear extension point for:
Authorization: Bearer <token>
Do not fabricate token generation or pretend frontend-only JWT is secure.

9. Environment Configuration
API configuration must use environment variables.
Example conceptual configuration:
VITE_API_BASE_URL
Do not hardcode backend URLs.

10. Data Flow
Example dashboard:
Dashboard Page      ↓useDashboard()      ↓analytics.api.js      ↓Axios client      ↓Backend      ↓Dashboard data      ↓MetricCard / Chart / Funnel / Table

11. Mock Data
During frontend development, mock data may be used.
Mock data must be isolated.
Example:
src/└── mocks/    ├── dashboard.mock.js    ├── conversations.mock.js    └── company.mock.js
Components should not contain mock datasets.

12. State
Use local component state where appropriate.
Do not introduce global state management unless the application actually requires it.
Authentication/company/session state should have a clear abstraction so a state-management solution can be introduced later without rewriting the UI.

13. Routing
Use React Router DOM.
Routes must be centrally defined.
The application should distinguish between:
Public routes:
/login/signup
Onboarding routes:
/onboarding/company/onboarding/agent
Application routes:
/dashboard/conversations/agent/analytics/settings
Demo:
/demo

14. Layout
Authenticated pages should use a shared application layout:
AppLayout├── Sidebar├── Topbar└── MainContent
Do not duplicate sidebar/topbar markup across pages.

15. Conversation Architecture
The conversation UI should be divided into reusable units:
ConversationPage├── ConversationToolbar├── ConversationList│   └── ConversationItem└── ConversationPanel    ├── CustomerHeader    ├── MessageList    │   └── MessageBubble    ├── AgentStatus    └── MessageComposer
Human takeover should be exposed through a service abstraction.
Example conceptual API:
takeOverConversation()releaseConversationToAI()sendMessage()
The actual backend contract will be defined later.

16. Dashboard Architecture
The dashboard should be composed from independent sections:
Dashboard├── DashboardHeader├── MetricsGrid│   └── MetricCard├── RevenueTrendCard├── ConversionFunnelCard├── RevenueByOfferCard├── AgentAutonomyCard└── RecentActivityTable
Each component should accept structured data.

17. Design System
Reusable design primitives should be centralized.
Examples:
ButtonInputSelectBadgeCardModalTabsTooltipDropdownAvatarSkeletonEmptyState
Avoid creating slightly different versions of the same component.

18. Scalability
Future requirements may include:
More industries
More user roles
More agents
More channels
More analytics
Team management
Integrations
Real-time conversations
The current architecture should make these additions incremental rather than requiring a rewrite.

4. ROUTES.md
ROUTES.md
Public
Route
Page
/login
Login
/signup
Signup
Onboarding
Route
Page
/onboarding/company
Company Information
/onboarding/agent
Agent Behavior
/onboarding/complete
Completion / Demo Entry
Application
Route
Page
/dashboard
Company Dashboard
/conversations
AI/Human Conversations
/agent
AI Agent
/analytics
Analytics
/settings
Settings
Demo
Route
Page
/demo
Product Guided Tour

Route Behavior
Unauthenticated users attempting to access application routes should eventually be redirected to /login.
Do not implement production authentication guards before backend authentication exists.
The route structure should nevertheless be prepared for authentication guards.

Onboarding Flow
/signup   ↓/onboarding/company   ↓/onboarding/agent   ↓/onboarding/complete   ↓/demo   ↓/dashboard
Returning users:
/login   ↓/dashboard

5. COMPONENTS.md
COMPONENTS.md
Layout
AppLayout
Responsible for authenticated application structure.
Contains:
Sidebar
Topbar
Main content
Sidebar
Navigation configuration should be data-driven.
Topbar
Responsible for:
Page context
Company context
User menu
Notifications where applicable

Dashboard Components
MetricCard
Props conceptually:
titlevaluesubtitletrendtrendDirectioniconformat
ChartCard
Reusable container for analytics visualizations.
RevenueTrendChart
Receives dynamic time-series data.
ConversionFunnel
Receives configurable stages.
RevenueByOffer
Receives category/value pairs.
AgentAutonomy
Receives handling distribution.
RecentActivityTable
Receives dynamic activity records.

Conversation Components
ConversationToolbar
Contains:
Search
Filters
Actions
ConversationList
Displays conversation records.
ConversationItem
Displays:
Customer
Last message
Timestamp
Status
Handling mode
Unread state
ConversationPanel
Displays the selected conversation.
CustomerHeader
Displays customer context.
MessageList
Displays messages in chronological order.
MessageBubble
Represents one message.
Message types should be extensible.
Examples:
customer
ai
human
system
AgentStatus
Clearly displays current handling mode.
MessageComposer
Used by human agents when they have control.

Onboarding Components
OnboardingLayout
Shared layout for onboarding.
StepIndicator
Displays current onboarding progress.
CompanyForm
Company registration fields.
AgentBehaviorSelector
Industry/behavior selection.
CompletionScreen
Transitions user into demo/training.

Demo Components
ProductTour
Controls walkthrough state.
TourStep
Represents an individual step.
Tour content should be configuration-driven.

Shared UI
Create reusable primitives for:
Button
Input
PasswordInput
Select
Checkbox
Card
Modal
Dropdown
Badge
Avatar
Tooltip
Tabs
Skeleton
Spinner
EmptyState
ErrorState
Pagination
Avoid one-off implementations when an existing primitive can be reused.

6. TASKS.md
TASKS.md
Phase 0 — Repository Investigation
Inspect existing repository.
Inspect current Sellince HTML references.
Identify reusable visual patterns.
Identify existing dependencies.
Identify existing routing.
Identify existing styling system.
Identify existing API patterns.
Do not rewrite existing functionality without justification.

Phase 1 — Foundation
Configure React 19.
Configure Vite.
Configure Tailwind CSS.
Configure React Router DOM.
Configure Axios.
Create application structure.
Create shared layout.
Create shared UI primitives.
Create environment configuration.
Create API client.
Create Axios interceptors.
Prepare JWT integration point.

Phase 2 — Authentication UI
Login page.
Signup page.
Form validation.
Password confirmation.
Authentication service abstraction.
Route structure.
Do not implement real backend authentication.

Phase 3 — Onboarding
Company information page.
Agent behavior page.
Industry selection.
Onboarding progress.
Completion state.
Reusable onboarding components.

Phase 4 — Application Layout
Sidebar.
Topbar.
Responsive navigation.
Application layout.
Route configuration.
Mobile navigation behavior.

Phase 5 — Dashboard
Dashboard header.
Metrics grid.
Revenue/ARPU chart.
Conversion funnel.
Revenue by offer.
Agent autonomy.
Recent activity.
Loading states.
Empty states.
Error states.
Responsive behavior.
Use dynamic structured data.
Do not hardcode example business numbers into components.

Phase 6 — Conversations
Conversation list.
Conversation search.
Filters.
Conversation detail.
Customer header.
Message list.
Message bubbles.
AI/human status.
Human takeover UI.
Human response composer.
Release to AI UI.
Empty state.
Loading state.
Error state.
Responsive conversation layout.

Phase 7 — AI Agent
Agent overview page.
Agent status.
Agent behavior presentation.
Configuration-ready architecture.
Do not implement actual AI inference.

Phase 8 — Analytics
Analytics page.
Reusable chart components.
Dynamic dataset interfaces.
Loading/error/empty states.

Phase 9 — Settings
Settings page.
Company settings.
Profile settings.
Agent settings structure.
Extensible settings navigation.

Phase 10 — Demo
Product tour.
Tour configuration.
Dashboard walkthrough.
Conversations walkthrough.
AI Agent walkthrough.
Analytics walkthrough.
Settings walkthrough.
Completion state.

Phase 11 — Quality
Build application.
Verify all routes.
Verify desktop layout.
Verify tablet layout.
Verify mobile layout.
Verify navigation.
Verify forms.
Verify conversation interactions.
Verify mock/API boundaries.
Review component duplication.
Review unnecessary dependencies.
Review final diff.

Definition of Done
The frontend is considered complete when:
All required routes exist.
Signup/onboarding flow works on the frontend.
Demo flow works.
Dashboard is fully componentized.
Conversations interface is functional using mock data.
Search/filter UI works against the mock data layer.
Human takeover interaction is represented correctly.
Settings exists in the sidebar.
Axios/API architecture is isolated.
JWT integration point exists without pretending to authenticate.
Responsive layouts work.
The project builds successfully.
Components are reusable and understandable.
No major functionality is implemented directly inside page components.
Backend integration can be introduced without restructuring the application.

One important thing I'd change from your original request
You mentioned:
file:///C:/Users/yazan/Downloads/sellince-conversations.html
and
file:///C:/Users/yazan/Downloads/sellince-dashboard.html
Don't put those file:/// paths into the agent specification and expect the agent to access them.
Instead, if those HTML files are the actual design references, give the files to the agent/repository and state:
Reference UI files:/references/sellince-dashboard.html/references/sellince-conversations.html
Then explicitly tell the agent:
Treat these files as visual/product references. Inspect their structure and appearance before implementing the React version. Do not copy their implementation architecture. Recreate the UI using the project's React component architecture.
That is much cleaner.
And your actual agent prompt can now be extremely small
Once these files exist, I would start the coding agent with:
Read the project specification before making any implementation changes.
Start with:
AGENTS.md
docs/PRD.md
docs/ARCHITECTURE.md
docs/ROUTES.md
docs/COMPONENTS.md
docs/TASKS.md
Also inspect the existing repository and the UI reference files under /references.
Do not start coding immediately.
First produce an implementation assessment containing:
Current repository structure
Existing architecture
Relevant existing components/code that can be reused
Gaps against the specification
Proposed implementation architecture
Required files/components
API boundaries
Routing plan
Risks or ambiguities
Recommended implementation order
Do not modify application code during this assessment.
After the assessment, wait for implementation approval.
This is the important shift: you're no longer asking the agent to figure out the product from your prompt. You're giving it a mini engineering spec + architecture contract + acceptance criteria and asking it to reason against the actual repository.
That is the direction I'd recommend for a senior/SWE workflow.
---------------------------------
UI/UX : 
Here is the complete color palette extracted directly from the dashboard interface, organized by functional UI/UX design categories:
🟧 Primary Brand & Accent Colors
Used for active navigation states, call-to-actions, and primary visualizations like the conversion funnel bars and line chart trends.


Brand Orange: #F27A22 (Main active indicators, filled funnel charts, and line graphs)
Light Orange Tint / Hover State: #FFF3EB (Background tint for active buttons or selected tabs)

⬛ Layout & Background Colors
Used to establish visual hierarchy, grouping, and container depth.


Dark Sidebar Background: #1A1613 (Deep off-black/warm charcoal used for the left workspace menu)
Main App Background: #F9F8F6 (Very light, warm gray/off-white canvas background)
Card & Container Background: #FFFFFF (Pure white used for dashboard widgets and metric cards)
Borders & Dividers: #EAE7E4 (Soft gray used to separate layout sections and card outlines)

🟩 Semantic & Status Colors
Used to convey quantitative performance, system status, and micro-copy changes.


Success / Growth Green: #2BB673 (Used for positive trend indicators like ^ 22.4%, active agent badges, and online statuses)
Light Green Tint: #EAF8F1 (Background badge container color for positive trends)

🔤 Typography & Text Colors
Used to control readability and content hierarchy across headlines and body elements.


Primary Headers & Data Values: #110F0E (Near-black used for main titles, metrics, and high-emphasis numbers)
Secondary / Body Text: #615E5B (Medium neutral gray used for sub-labels and supporting descriptions)
Muted / Disabled Text: #9A9692 (Light neutral gray used for secondary insights like "vs last month" or placeholder text)

----------------------------------------------------------------------------------