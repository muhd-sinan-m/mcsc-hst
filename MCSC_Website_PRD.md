# Product Requirements Document

## Marian College Students Council (MCSC) — Official Website

**Version:** 1.0
**Prepared for:** Marian College Students Council
**Status:** Draft for development

\---

## 1\. Project Overview

The MCSC website is the official digital presence of the Marian College Students Council. It serves three core purposes:

1. **Inform** — present the council's vision, mission, objectives, membership process, and current representatives.
2. **Engage** — publish news and events to keep students updated.
3. **Empower** — give students a formal, accountable channel to raise grievances directly with the council.

The site is content-driven and form-heavy rather than highly interactive, and is built to be maintained year-over-year by non-technical council members after handover from the current development team.

**pyqportal integration:** `pyqportal` is a separate, already-built deployment (previous year question papers portal) that must be **prominently highlighted as one of the site's core features**, not just tucked into the nav. Technically it remains fully independent — no shared authentication, database, or codebase integration — the MCSC site simply links/redirects to it, but visually and structurally it should be treated as a first-class feature. See Section 5.1 and 5.8.

\---

## 2\. Tech Stack

|Layer|Choice|Reason|
|-|-|-|
|Backend framework|**Django**|Built-in admin panel doubles as the CMS for Representatives/News/Events and the management console for Grievances — council can maintain content without a developer.|
|Database|**PostgreSQL (Supabase)**|Managed Postgres with built-in storage (photos, event posters, news images/files) and auth support.|
|Frontend|**Server-rendered Django templates** (Jinja-style)|Content + form-driven site; no client-heavy state, so React adds unnecessary build/maintenance overhead.|
|Charts (Grievance dashboard)|**Chart.js** (CDN, no build step)|Lightweight stats visualization for admin dashboard.|
|Authentication|**OAuth 2.0**, restricted to `@mariancollege.org` domain only|See Section 6.6.|
|File/Image storage|**Supabase Storage**|Representative photos, news images/attachments, event posters.|
|Hosting|Render / VPS (existing infra under evaluation)|Needs to stay persistently up — not a cold-start use case.|

**Explicitly excluded:** React, FastAPI, anonymous login/guest access, any auth method other than college-domain OAuth.

\---

## 3\. Design System

### 3.1 Color Palette

Derived directly from the MCSC logo (blue/orange swoosh):

|Token|Hex (approx.)|Usage|
|-|-|-|
|Primary Blue|`#2E75B6`|Headings accents, nav, primary tags, "open" status|
|Primary Orange|`#F5A623`|CTAs, highlights, active states, "upcoming" badges|
|Accent Yellow|`#F4C542`|Sparingly — badges, "in-review" status|
|Background|`#F8FAFC` / `#FDFCF8`|Airy off-white base across all pages|
|Heading Text|`#1B3A57` (dark navy)|All serif headings|
|Body Text|`#3A3A3A`|Paragraphs, labels|
|Success/Resolved|Muted green (to be paired with palette)|"Resolved" status tags|

### 3.2 Typography

* **Headings:** Elegant serif (Playfair Display / Cormorant)
* **Accent word per page:** Script font (Playfair Display Italic or similar) — used once per page, sparingly
* **Nav / buttons / labels:** Small-caps, letter-spaced sans-serif (Inter / Jost)
* **Body copy:** Clean sans-serif, no serif in paragraphs

### 3.3 Layout Conventions (applies to every page)

* **Sticky navbar** — pinned on scroll, subtle shadow/border appears once scrolled past hero.
* Navbar: logo (left) → nav links in small-caps (center, **including a "PYQ Portal" link**) → Login + primary pill CTA (right).
* Hero pattern: eyebrow text → large serif institutional heading → script accent line → subtext → pill CTA.
* Pill-shaped buttons throughout.
* Consistent card style: rounded corners, subtle hover lift, blue/orange border accent on hover.
* **Grievance and Dashboard pages** relax to a more utilitarian, data-dense grid — no script fonts here, since these are functional/transactional, not editorial.
* All pages must have clean, uncluttered, professional UI consistent with the above system — no page should visually break from this system without reason.

\---

## 4\. Sitemap

```
Home
About / Vision
  ├─ Overview
  ├─ Vision \& Mission
  ├─ Objectives
  └─ Membership Procedure
Representatives (current year only)
News
  └─ News detail
Events
  └─ Event detail
Grievance
  ├─ Submit Grievance (student)
  ├─ My Grievances (student)
  └─ Admin Dashboard (admin only)
PYQ Portal (external redirect → pyqportal)
Login (OAuth)
Contact
```

\---

## 5\. Feature Specifications

### 5.1 Home Page

* Hero section introducing MCSC with brand-consistent styling.
* **Core features section** (below hero, above/alongside news \& events widgets) — a row of 3 highlighted feature cards giving the site's main functions equal visual weight:

  1. **PYQ Portal** — "Access previous year question papers" → redirects to pyqportal (external link, opens the existing separate deployment)
  2. **Grievance Portal** — "Raise your concerns, get heard" → links to Submit Grievance
  3. **Representatives** — "Meet your council" → links to Representatives page
  * Each card: icon + short label + one-line description + pill CTA, styled consistently with the rest of the design system (blue/orange accents, hover lift). PYQ Portal card should look and feel as prominent as the other two — not smaller or secondary.
* Quick links / widgets: latest 3–4 news items, next 2–3 upcoming events.
* Primary CTA: likely "Submit a Grievance" or "Student Login" — final copy TBD.

### 5.2 About / Vision Page

Content is year-independent unless noted:

* **Overview** — introductory paragraph about MCSC's role. *Contains year-specific phrasing (e.g. "MCSC 2026–'27 is...")* → store as an editable field tied to `academic\_year`, not hardcoded in template.
* **Vision:** "To create an inclusive, vibrant and empowering campus community," with supporting line on fostering a student-centered environment. Static content.
* **Mission:** Comprehensive programs/services statement + 2 supporting bullet points (safe/welcoming environment; promoting full potential). Static content.
* **Objectives:** 9 objectives (student involvement/leadership, social \& recreational opportunities, community building, representing student interests, resources/services, supporting student entrepreneurship, activism, faculty-student communication, student wellness). Displayed as an **icon grid**, not a plain bullet list. Static content.
* **Membership Procedure:** Displayed as a **numbered step/timeline component** (structure is static, year-specific details like dates/names are data-driven):

  1. Eligibility check per college rules
  2. Election as Class Representative (CR)
  3. CRs convene for council elections
  4. Candidates campaign/speak
  5. Faculty-supervised voting \& counting, witnessed by CRs
  6. Results announced
  * Below the steps: small credit line naming supervising faculty for that year (data-driven, muted styling, not a headline).

### 5.3 Representatives Page

* Shows **current academic year only** — no past-years archive/browse UI (per client decision), though `academic\_year` remains a DB field for future-proofing.
* 18 elected Class Representatives + Technical Coordinator (headcount to be confirmed with council — provided list shows 20 named roles; verify exact official count before final launch).
* **Three-tier card layout:**

  1. **Office Bearers** (Chairperson, Vice Chairperson, General Secretary, Joint Secretary) — larger, featured cards.
  2. **Councilors \& Secretaries** (Student Councilors I/II, Arts Club Secretary/Joint Secretary, Student Editor, Sports Secretary/Joint Secretary, Clubs \& Association Secretary, Technical Coordinator).
  3. **Year \& Category Representatives** (UG 1st/2nd/3rd Year Reps, PG 1st/2nd Year Reps, UG Lady Rep, PG Lady Rep).
* Card contents: photo (circular/rounded), name, position (small-caps, orange tag).
* Photo fallback: initials on a blue/orange gradient circle if photo not yet uploaded.

### 5.4 News Page

* Admin-posted news items; each post may include **images and/or file attachments**.
* List view: newest-first, clean card/list layout (thumbnail if image present, title, short excerpt, date).
* Detail view: full content, rich text formatting, embedded images, downloadable attachments clearly listed.
* Must remain visually clean regardless of whether a post has 0, 1, or multiple attachments — no broken layout for text-only posts.

### 5.5 Events Page

* Shows **both upcoming and finished events on the same page**, sorted by proximity to today:

  * Upcoming events: soonest first.
  * Finished events: most recently completed first.
  * Clear visual separation between the two groups (e.g. section divider or tab), with "upcoming" getting an orange badge.
* "Upcoming vs finished" is computed at query time from `event\_date`, not manually flagged — keeps it always accurate.
* Detail view: date, time, venue, description, poster image, registration link (if applicable).

### 5.6 Grievance System

Redesigned per latest requirements — **no anonymous option; all grievances are official and identity-attached.**

**Student flow:**

1. Log in via OAuth (college email only — see 5.6.1).
2. Submit a grievance: title, category, description, optional attachment.
3. View status of their own submitted grievances ("My Grievances" — open / in-review / resolved).
4. Receive a **notification when admin posts a reply** (see 5.6.3).

**Admin flow:**

1. Log in via OAuth with admin role.
2. View all grievances (no anonymous filtering needed — all identity-attached).
3. Reply to a grievance; reply triggers student notification.
4. Update status (open → in-review → resolved).
5. View aggregate **dashboard** (counts by status/category, via Chart.js).

**Non-negotiables per client:**

* No anonymous submissions.
* No login/signup path outside OAuth with `@mariancollege.org`.
* Admin sees all grievances with full student identity attached (official/accountable system, not anonymous complaint box).
* Notification required when a reply is posted.

#### 5.6.1 Authentication

* **OAuth-only login.** No email/password signup, no other identity providers.
* Restricted strictly to accounts ending in `@mariancollege.org`. Any other domain must be rejected at the OAuth callback/verification step, not just hidden in UI.
* Role assignment (student vs admin) handled via a role field tied to the authenticated user — not a separate signup form.

#### 5.6.2 UI Requirements

* Must be **easy and fast to interact with** — this is the most functionally important page on the site, so UI polish here matters as much as (or more than) the editorial pages.
* Clear status badges (color-coded per palette: blue = open, yellow = in-review, green = resolved).
* Simple, minimal-friction submission form — no unnecessary fields.
* "My Grievances" should read like a clean ticket/status tracker, not a raw table dump.

#### 5.6.3 Notifications

* Trigger: admin posts a reply to a grievance.
* Delivery channel: **TBD — recommend email** (simplest to implement with Supabase/Django, no third-party SMS cost). Confirm with council whether email is sufficient or if in-app notification badge is also wanted.

### 5.7 Login Page

* Single OAuth login button only (`Continue with Marian College Email` or similar) — no alternate login methods shown.
* Minimal centered card, consistent serif heading + pill button styling.

### 5.8 PYQ Portal (Highlighted External Feature)

* **pyqportal is a separate, pre-existing deployment** (previous year question papers) built independently of this site. It is not rebuilt or re-integrated here.
* Treated as a **core feature**, on par with Grievance and Representatives in terms of visibility:

  * Dedicated entry in the main navbar.
  * Dedicated feature card on the Home page (Section 5.1), styled with equal visual weight to other core features — no "smaller/secondary link" treatment.
  * Optionally, a short dedicated landing block/page on the MCSC site (`/pyqportal` route) that briefly describes what the portal offers, with a large clear "Go to PYQ Portal" CTA button that redirects to the external deployment — this gives it a proper on-site presence instead of just being an outbound link buried in the nav.
* **Technical boundary:** no shared authentication, database, or codebase. The MCSC site only links/redirects (`target="\_blank"` or same-tab redirect — confirm preference) to the existing pyqportal URL. No data flows between the two systems.
* Action item: confirm the live pyqportal URL to hardcode into the redirect/CTA links.

\---

## 6\. Data Models

### 6.1 Council Info

```
council\_info
- id
- academic\_year (e.g. "2026-27")
- overview\_text
- membership\_supervisor\_names
- election\_date
```

### 6.2 Representatives

```
representatives
- id
- academic\_year
- name
- position
- category (office\_bearer / councilor\_secretary / year\_representative)
- photo\_url
- display\_order
```

### 6.3 News

```
news\_post
- id
- title
- slug
- content (rich text)
- author\_id (FK -> user)
- is\_published (bool)
- published\_at
- created\_at / updated\_at

news\_attachment
- id
- news\_post\_id (FK)
- file\_url
- file\_type (image / document)
```

### 6.4 Events

```
event
- id
- title
- slug
- description
- event\_date (datetime)
- venue
- poster\_image
- registration\_link (optional)
- is\_published (bool)
- created\_at / updated\_at
```

*Upcoming vs. finished determined at query time via `event\_date >= now()` — not a stored field.*

### 6.5 Grievance

```
user
- id
- name
- email (must end in @mariancollege.org)
- role (student / admin)
- created\_at

grievance
- id
- student\_id (FK -> user)
- category
- title
- description
- attachment\_url (optional)
- status (open / in-review / resolved)
- created\_at / updated\_at

grievance\_reply
- id
- grievance\_id (FK)
- admin\_id (FK -> user)
- reply\_text
- created\_at
```

### 6.6 Notification (new, per latest requirement)

```
notification
- id
- user\_id (FK -> user)
- grievance\_id (FK -> grievance)
- type (reply\_posted / status\_changed)
- is\_read (bool)
- created\_at
```

*Used to drive email notification and optionally an in-app badge.*

\---

## 7\. Non-Functional Requirements

* Consistent, polished UI across **every** page — no page should feel unfinished relative to others.
* Mobile-responsive (students will access grievance/news/events on phones primarily).
* Fast page loads — server-rendered pages, minimal JS, images optimized/served via Supabase storage.
* Maintainability: council members with no coding background must be able to update Representatives, News, and Events via Django Admin without developer involvement.
* Data integrity: OAuth domain restriction must be enforced server-side, not just client-side UI hiding.

\---

## 8\. Open Items / Decisions Needed

|Item|Status|
|-|-|
|Exact official council headcount (18 vs 20 in provided list)|20|
|Notification channel: email only, or also in-app|email|
|Grievance categories list (hostel, academics, facilities, etc.)|academics,general,hostel,facilities,progtsms|
|Whether resolved grievances are ever shown publicly/aggregated (even anonymized) for transparency|**ully private, admin + submitting student only**|
|Home page primary CTA copy|Final wording TBD|
|Founding year for "Est." hero eyebrow text (About page)|Needs council input|
|Live pyqportal URL to hardcode into redirect/CTA links|Needs you to confirm|
|Whether PYQ Portal redirect opens in new tab or same tab|new tab|

## 9\. Explicitly Out of Scope (v1)

* Anonymous grievance submission
* Any login method other than `@mariancollege.org` OAuth
* Past-year Representatives archive/browsing
* Real-time (websocket) dashboard updates
* Deep integration with `pyqportal` (shared login, shared DB, embedded content) — it remains a separate deployment, only prominently *linked/redirected* to, not merged

\---

*This document consolidates all requirements gathered through project discovery discussions and should be treated as the single source of truth for development. Update the Open Items table as decisions are finalized.*

