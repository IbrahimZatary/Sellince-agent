# Sellince Chat UI

Frontend application for Sellince, built with React 19, Vite, Tailwind CSS, and shadcn/ui.

## Features

- **Landing Page (`/`)**: Hero section and navigation with a floating "Chat with Us" button.
- **Floating Chatbot**: Popup assistant with message history, typing indicator, and responsive design.
- **Authentication (`/login`, `/signup`)**:
  - Sign up with name, email, password, company name, and sector dropdown.
  - Login with email and password (includes show/hide password toggle).
  - Client-side validation and accessible error alerts.
- **Onboarding (`/onboarding`)**: Setup flow to select workspace products.
- **Dashboard (`/dashboard`)**: Full workspace with inbox list, conversation view, and customer details sidebar.

## Routes & Navigation

| Route         | Page             | Description                                            | How to Navigate                                                      |
| ------------- | ---------------- | ------------------------------------------------------ | -------------------------------------------------------------------- |
| `/`           | **Landing Page** | Marketing homepage with floating chatbot               | Visit root URL or click the Sellince logo                            |
| `/login`      | **Login**        | Sign in with email and password                        | Click **Log in** in the top navigation or on the homepage            |
| `/signup`     | **Sign Up**      | Register account, company, and sector                  | Click **Get started** in the header or **Sign up** on the Login page |
| `/onboarding` | **Onboarding**   | Workspace setup and product selection                  | Proceed after sign up, or open `/onboarding`                         |
| `/dashboard`  | **Dashboard**    | Workspace inbox, chat transcript, and customer details | Click **Continue to workspace** on Onboarding, or open `/dashboard`  |

## Tech Stack

- React 19
- Vite
- React Router
- Tailwind CSS
- shadcn/ui (Radix primitives)
- Lucide React
- Axios
- Vitest + React Testing Library

## Getting Started

### 1. Clone & Install

```bash
git clone https://github.com/ghaithmubaidin/Sellince-Chat-UI.git
cd Sellince-Chat-UI
npm install
```

### 2. Environment Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Set `VITE_API_BASE_URL` to your backend URL when available.

### 3. Run Locally

```bash
npm run dev
```

Open `http://localhost:5173` in your browser.

## Scripts

- `npm run dev` – Start development server
- `npm run build` – Build for production
- `npm run preview` – Preview production build
- `npm test` – Run test suite
- `npm run lint` – Run ESLint
- `npm run format` – Format code with Prettier

## Project Structure

```text
src/
├── api/              # Axios client and API calls
├── assets/           # Images and illustrations
├── components/
│   ├── auth/         # Login, SignUp, and form fields
│   ├── chat/         # Chatbot popup, button, and messages
│   ├── dashboard/    # Workspace dashboard components
│   ├── home/         # Landing page header and hero
│   ├── onboarding/   # Onboarding cards and progress
│   └── ui/           # shadcn UI components
├── data/             # Demo data
├── pages/            # Home, Onboarding, Dashboard
├── App.jsx           # Route setup
└── main.jsx          # React entry point
```
