# Sellince mobile frontend

A mobile-first Orange Max it-inspired UI preview. Authentication, customer data, proactive messages, and chat are not connected. Choose **Continue as a guest** on the welcome screen to preview the app without signing in.

## Run locally

```powershell
npm install
npm run dev
```

Open `http://localhost:5173`. Run `npm run test`, `npm run lint`, and `npm run build` for frontend checks.

## Android preview

The Capacitor Android project bundles the same disconnected frontend and does not require a development server on the phone. Install Node.js 22 or newer, Android Studio and Android SDK Platform 36, plus a compatible JDK (JDK 21 is recommended; the generated Gradle 8.14.3 cannot run on JDK 25). Android Studio normally includes a compatible JDK. See [Capacitor's environment setup](https://capacitorjs.com/docs/getting-started/environment-setup).

```powershell
npm install
npm run android:sync
npm run android:open
```

In Android Studio, let Gradle sync, connect an Android phone with USB debugging enabled and authorized, select it, and press Run. Alternatively, after the Android toolchain is configured, use `npm run android:run`. Run `npm run android:sync` after changing web code so Android receives the latest build. The generated debug APK is `android/app/build/outputs/apk/debug/app-debug.apk` after a successful debug build.

The provisional Android application ID is `com.sellince.mobile`; confirm it with the team before publishing. No live-reload server, production signing keys, or backend credentials are bundled. A phone's `localhost` refers to the phone, not the development computer; when backend integration is ready, agree on an accessible HTTPS API address and CORS configuration with the backend team.

## Backend handoff

The backend team can connect the existing Axios boundary in `src/api/client.js` to its final contracts. It contains request functions for the team's customer login, proactive session, and chat endpoint paths and returns raw response data. No UI currently invokes these functions. Configure `VITE_API_BASE_URL` using `.env.local` when integration is ready; Vite variables are public and must never contain secrets.

The backend team should confirm authentication, customer authorization, conversation history and response contracts before connecting the screens. `src/hooks/useChat.js` owns the local chat state. Its optional `onMessageSend` callback accepts the draft and resolves to a UI message object with a `content` string; the integration should map the confirmed backend response into that shape. When a real proactive message arrives, call `receiveProactiveMessage` with a UI object containing a stable `messageId` and `content`. It places that message in both Home and the conversation; these are UI fields, not assumed backend response fields. Until a message is supplied, Home offers a clearly labeled disconnected chat preview. Dismissal lasts until the preview session ends and leaves the conversation intact.

### Contract snapshot to confirm with the team

The following describes `Manar/agent-unified` at commit `54f1e05d0322fb846fc7986a2a150d86e2749936`; other branches differ, and the team must confirm which branch is authoritative:

- Customer login accepts `phone` and `password`, and returns `access_token`, `token_type`, numeric `customer_id`, and `name`.
- `POST /api/v1/agent/start-session` accepts numeric `customer_id` and returns numeric `conversation_id`, `status`, nullable `response`, and nullable `offer`. The response does not include a message ID. An existing session returns `response: null`.
- `POST /api/v1/chat` accepts numeric `customer_id` and `message`, and returns `response`, nullable `offer`, `action`, and `conversation_stage`. It does not return a message ID.

The UI's `content` and string `messageId` are internal fields, not the API schema. The integration needs a mapping from `response` to `content` and an agreed stable message identity or history contract. The conversation detail route in this branch requires an authenticated operator, so it should not be assumed to be a customer history endpoint. The start-session and chat routes currently take a customer ID without a customer-token dependency; the backend team needs to confirm and enforce customer authorization before connecting customer data. No frontend code currently sends these requests or pretends the contract is finalized.

Reference screenshots are kept separately from this repository.

The Max it illustrations and icons in `src/assets/maxit/` were converted from the installed app for this challenge preview. The Fiber and scholarships campaign images come from Orange Jordan's [Fiber announcement](https://orange.jo/en/corporate/media-center/news/orange-launches-unprecedent-home-internet-experience) and [media center](https://orange.jo/en/corporate/media-center). Promotional content and account data still need the team's live integrations.
