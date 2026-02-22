# UX/UI Design Principles Knowledge Base

## Overview

This guide covers essential UX/UI design principles, frameworks, and best practices for creating user-friendly digital products. These principles apply to websites, web apps, and mobile applications.

---

## 1. Nielsen's 10 Usability Heuristics

### Heuristic 1: Visibility of System Status

**Principle:** Always keep users informed about what is going on through appropriate feedback within reasonable time.

**Why it matters:** Users feel in control when they know what's happening. Uncertainty creates anxiety and abandonment.

**Implementation:**

```
Loading States:
✓ Progress bars for long operations (>2 seconds)
✓ Spinners for indeterminate waits
✓ Skeleton screens while content loads
✗ Blank screen with no feedback

Example:
File upload:
- Show progress bar: "Uploading... 47% complete"
- Show file name and size
- Estimated time remaining
- Allow cancellation

Form submission:
- Disable button immediately: "Submitting..."
- Show success message: "Saved successfully!"
- Or error message: "Error: Email already exists"
```

**Real-world examples:**
- Gmail: Shows "Sending..." then "Sent" confirmation
- Stripe: Real-time validation as you type credit card
- Uber: Live map showing driver location and ETA

**Common mistakes:**
- No feedback after button click (user clicks again)
- Generic "Loading..." without context
- No error messages when something fails

### Heuristic 2: Match Between System and Real World

**Principle:** Speak the users' language. Use familiar words, phrases, and concepts rather than system-oriented terms.

**Why it matters:** Users shouldn't need to translate. Familiar language reduces cognitive load.

**Implementation:**

```
Good Examples:
✓ "Trash" or "Archive" instead of "Delete permanently"
✓ "Shopping Cart" instead of "Transaction buffer"
✓ "Dashboard" instead of "System overview panel"
✓ Icons that match real objects (folder, envelope, magnifying glass)

Bad Examples:
✗ "Null pointer exception" (user sees this error)
✗ "Database connection failed" (technical jargon)
✗ "Select Boolean value" instead of "Yes/No"

Error Messages:
Good: "Your password must be at least 8 characters"
Bad: "Password validation failed: Length < MIN_LENGTH_REQ"

Navigation:
Good: Home > Products > Shoes > Running Shoes
Bad: Root > Category_001 > Subcategory_A > SKU_Group
```

**Industry-specific language:**
```
E-commerce:
✓ "Add to Cart", "Checkout", "Order History"
✗ "Append to transaction queue", "Finalize purchase", "Transaction log"

Project Management:
✓ "Tasks", "Projects", "Team Members"
✗ "Entities", "Collections", "User Objects"

Finance:
✓ "Balance", "Transfer", "Statement"
✗ "Account sum", "Move funds", "Transaction record"
```

### Heuristic 3: User Control and Freedom

**Principle:** Users often perform actions by mistake. Provide clear "emergency exit" to undo actions without going through extended process.

**Why it matters:** Mistakes are inevitable. Users need to feel safe exploring without fear of irreversible consequences.

**Implementation:**

```
Undo/Redo:
✓ Undo text editing (Ctrl+Z)
✓ Undo email send (Gmail's "Undo send")
✓ Restore deleted items (Trash/Archive system)
✓ Cancel in-progress operations

Emergency Exits:
✓ "Cancel" button on every modal
✓ "X" close button that's always visible
✓ ESC key closes modals
✓ Back button works as expected

Confirmation Before Destructive Actions:
✓ "Are you sure you want to delete this?"
✓ "This action cannot be undone"
✓ Soft delete (Archive) instead of permanent delete

Gmail Example:
"Message sent. Undo"
- 5-second window to undo send
- User feels safe, can correct mistakes
```

**Real-world examples:**
- Photoshop: Infinite undo history
- Trello: Restore deleted cards from menu
- Gmail: "Undo send" feature
- Google Docs: Version history and restore

**Common mistakes:**
- No confirmation for destructive actions
- No way to undo accidental deletion
- Modal dialogs without close button
- Forcing users through multi-step process to cancel

### Heuristic 4: Consistency and Standards

**Principle:** Users shouldn't have to wonder if different words, situations, or actions mean the same thing. Follow platform and industry conventions.

**Why it matters:** Consistency reduces learning curve. Users transfer knowledge from other products.

**Implementation:**

```
Visual Consistency:
✓ Same button styles throughout app
✓ Consistent color scheme
✓ Uniform spacing and typography
✓ Icons used consistently

Functional Consistency:
✓ Same interaction patterns (click, hover, swipe)
✓ Consistent placement (logo top-left, search top-right)
✓ Predictable navigation structure

Platform Conventions:
iOS:
- Back button top-left
- Primary action top-right
- Tab bar bottom
- Swipe gestures (swipe right to go back)

Android:
- Back button bottom
- Hamburger menu top-left
- Floating action button bottom-right

Web:
- Logo top-left (links to home)
- Search top-right
- Navigation horizontal top or vertical left
- Footer at bottom (links, copyright, contact)
```

**Consistency Examples:**

| Element | Standard Convention |
|---------|-------------------|
| Primary action | Blue or brand color, prominent |
| Destructive action | Red, less prominent |
| Cancel | Gray or outline, not filled |
| Links | Blue, underlined (or obviously clickable) |
| Required fields | Asterisk (*) or "Required" label |
| Errors | Red text or red border |
| Success | Green text or checkmark |

**Common mistakes:**
- Using different terms for same action ("Submit" vs "Send" vs "Confirm")
- Inconsistent button placement
- Red button that isn't destructive (confusing)
- Breaking platform conventions (back button in wrong place)

### Heuristic 5: Error Prevention

**Principle:** Even better than good error messages is careful design which prevents problems from occurring in the first place.

**Why it matters:** Prevention is better than cure. Helping users avoid errors is better than helping them recover from errors.

**Implementation:**

```
Input Validation:
✓ Email field only accepts valid email format
✓ Phone number field formatted automatically (xxx) xxx-xxxx
✓ Credit card field shows card type icon
✓ Password field shows strength indicator

Constraints:
✓ Date picker instead of free text date
✓ Dropdown instead of free text when options are limited
✓ Disable submit button until all required fields valid
✓ Auto-save (prevent data loss)

Confirmations:
✓ "Are you sure?" for destructive actions
✓ Show summary before final submission
✓ Preview before publishing

Smart Defaults:
✓ Pre-fill known information
✓ Remember user preferences
✓ Suggest common choices

Examples:
Form Design:
- Email field: type="email" (mobile shows @ key)
- Phone field: Auto-format as user types
- Required fields: Clearly marked, validated on blur

File Upload:
- Show allowed file types before upload
- Validate file size before upload
- Show preview before submitting

E-commerce Checkout:
- Show order summary before purchase
- Highlight any errors in form
- Prevent double-submission (disable button)
```

**Preventing Common Errors:**

| Error | Prevention |
|-------|-----------|
| Wrong date format | Date picker |
| Invalid email | Real-time validation |
| Missing required field | Prevent submission, highlight field |
| File too large | Check before upload, show limit |
| Password too weak | Show requirements, strength meter |
| Duplicate submission | Disable button after first click |

### Heuristic 6: Recognition Rather Than Recall

**Principle:** Minimize user's memory load by making elements, actions, and options visible. User shouldn't have to remember information from one part of interface to another.

**Why it matters:** Human short-term memory is limited. Showing options is easier than remembering them.

**Implementation:**

```
Show, Don't Make Users Remember:
✓ Show recently used items
✓ Display available options in dropdowns
✓ Show password requirements near field
✓ Display progress in multi-step process
✓ Show user's previous choices

Examples:
Search:
- Show recent searches
- Show search suggestions as you type
- Display search history

Forms:
- Show password requirements while typing
- Display examples ("e.g., john@example.com")
- Show character count for limited fields

Navigation:
- Highlight current page in menu
- Breadcrumbs show where you are
- Show recently visited pages

E-commerce:
- Show recently viewed products
- Display items in cart
- Show size guide next to size selector
```

**Recognition vs. Recall Examples:**

| Recall (Hard) | Recognition (Easy) |
|---------------|-------------------|
| "What was that feature called?" | Menu showing all features |
| "What format does this accept?" | "Upload JPG, PNG, or PDF" |
| "Am I on step 3 or 4?" | Progress indicator: "Step 3 of 5" |
| "What was my username?" | Email field pre-filled |

### Heuristic 7: Flexibility and Efficiency of Use

**Principle:** Accelerators for expert users—shortcuts that make frequent actions faster—while keeping interface simple for novices.

**Why it matters:** Serve both beginners and power users. Don't force experts through beginner workflows.

**Implementation:**

```
Keyboard Shortcuts:
✓ Cmd/Ctrl + S to save
✓ Cmd/Ctrl + Z to undo
✓ Cmd/Ctrl + F to search
✓ ESC to close modals
✓ Tab to navigate form fields

Power User Features:
✓ Bulk actions (select multiple, act once)
✓ Command palette (Cmd+K)
✓ Keyboard navigation
✓ Customizable views/layouts
✓ Saved filters or searches

Progressive Disclosure:
✓ Show basic options by default
✓ "Advanced options" link for power users
✓ Customize interface based on usage

Examples:
Gmail:
- Basic: Click buttons to archive, delete
- Advanced: Keyboard shortcuts (e to archive, # to delete)
- Power user: Multiple selection, bulk actions

Slack:
- Basic: Click channels, send messages
- Advanced: /slash commands
- Power user: Keyboard shortcuts (Cmd+K to jump anywhere)

Design Tools (Figma):
- Basic: Click and drag
- Advanced: Keyboard shortcuts
- Power user: Plugins, custom shortcuts
```

**Shortcuts by Experience Level:**

| Beginner | Intermediate | Expert |
|----------|--------------|--------|
| Visual buttons | Keyboard shortcuts | Command palette |
| Guided workflows | Skip optional steps | Bulk operations |
| Tooltips everywhere | Tooltips on hover only | No tooltips needed |
| One action at a time | Multiple selection | Custom macros/automation |

### Heuristic 8: Aesthetic and Minimalist Design

**Principle:** Interfaces should not contain information that is irrelevant or rarely needed. Every extra unit of information competes with relevant units and diminishes their visibility.

**Why it matters:** Clutter distracts from important information. Less is more.

**Implementation:**

```
Remove Unnecessary Elements:
✓ Every element should serve a purpose
✓ Remove decorative elements that don't add value
✓ Use white space effectively
✓ Hide advanced options until needed

Progressive Disclosure:
✓ Show most important info first
✓ "Show more" for details
✓ Collapsible sections
✓ Tabs to organize related content

Visual Hierarchy:
✓ Largest/boldest = most important
✓ Use size, color, and spacing to guide attention
✓ Group related items
✓ Use contrast to highlight key actions

Examples:
Google Homepage:
- Just search box and logo
- Everything else hidden until needed
- Minimal, focused, effective

Apple Product Pages:
- Large hero image
- Minimal text (key benefits only)
- Lots of white space
- Clear visual hierarchy

Bad Example (Cluttered):
- Multiple competing CTAs
- Too many colors
- Excessive text
- Too many options visible at once
```

**Before and After Example:**

```
Before (Cluttered):
┌─────────────────────────────────────┐
│ [Logo] [Nav1] [Nav2] [Nav3] [Search]│
├─────────────────────────────────────┤
│ [Ad Banner]                         │
├─────────────────────────────────────┤
│ Welcome! Sign up now for 20% off!  │
│ [Close]                             │
├─────────────────────────────────────┤
│ [Sidebar]  Main Content             │
│ - Link 1   Product Title            │
│ - Link 2   Price: $99               │
│ - Link 3   [Buy] [Add to Cart]      │
│ - Link 4   [Wishlist] [Compare]     │
│ - Link 5   Description: Lorem...    │
│ [Ad]       Reviews: ★★★★☆           │
│            Related: [1][2][3]       │
└─────────────────────────────────────┘

After (Minimalist):
┌─────────────────────────────────────┐
│ [Logo]           [Search] [Cart]    │
├─────────────────────────────────────┤
│                                     │
│        [Product Image]              │
│                                     │
│        Product Title                │
│        $99                          │
│                                     │
│        [Add to Cart]                │
│                                     │
│        Description (collapsible)    │
│        Reviews (collapsible)        │
│                                     │
└─────────────────────────────────────┘
```

### Heuristic 9: Help Users Recognize, Diagnose, and Recover from Errors

**Principle:** Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution.

**Why it matters:** Errors are frustrating. Good error messages turn frustration into resolution.

**Implementation:**

```
Error Message Formula:
1. What went wrong (clear, specific)
2. Why it happened (if helpful)
3. How to fix it (actionable)

Good Error Messages:
✓ "Email address is already registered. Try logging in or use password reset."
✓ "Password must be at least 8 characters with 1 number and 1 special character."
✓ "File size exceeds 10MB limit. Please compress or choose a smaller file."

Bad Error Messages:
✗ "Error 404"
✗ "Invalid input"
✗ "Something went wrong"
✗ "Database connection failed"

Error Styling:
✓ Red text or red border on field
✓ Error icon (⚠️)
✓ Error message near the problem
✓ Stop submission until fixed

Examples by Context:
Form Validation:
✓ "Email must include @"
✓ "Phone number must be 10 digits"
✓ "This field is required"

File Upload:
✓ "Only JPG and PNG files are allowed"
✓ "Maximum file size is 5MB (your file is 8MB)"

Payment:
✓ "Your card was declined. Please try another card or contact your bank."
✓ "Billing ZIP code doesn't match card. Please correct and try again."

Network:
✓ "Unable to connect. Please check your internet connection and try again."
```

**Error Message Template:**

| Component | Example |
|-----------|---------|
| Clear Problem | "Email address is invalid" |
| Specific Reason | "Missing '@' symbol" |
| How to Fix | "Enter a valid email (e.g., name@domain.com)" |
| Visual Indicator | Red border, error icon |

**Recovery Actions:**
```
Make it easy to fix:
✓ Keep form data (don't clear everything)
✓ Highlight exact problem field
✓ Auto-focus on error field
✓ Provide "Try again" button
✓ Offer alternative actions

Example:
Payment failed:
- "Payment could not be processed"
- Reason: "Card was declined"
- Actions:
  [Try Another Card]
  [Contact Support]
  [Update Payment Method]
```

### Heuristic 10: Help and Documentation

**Principle:** Even with best usability, help may be needed. Provide documentation that is easy to search, focused on user's task, and provides concrete steps.

**Why it matters:** Users need help sometimes. Make it findable and useful.

**Implementation:**

```
In-App Help:
✓ Contextual tooltips (on hover or ?)
✓ Onboarding tour for new users
✓ Empty states with guidance
✓ Inline help text

Documentation:
✓ Searchable help center
✓ Task-based articles ("How to...")
✓ Video tutorials for complex tasks
✓ FAQ for common questions

Accessibility:
✓ Help link in navigation
✓ Search in help center
✓ Contact support easily
✓ Community forum

Examples:
Tooltips:
- Hover over icon: Shows explanation
- Question mark icon: Click for more info
- Keyboard shortcut shown in menu

Empty States:
"No projects yet"
[Create Your First Project]
"Projects help you organize tasks..."

Onboarding:
Step 1: "Welcome! Let's create your first project"
Step 2: "Add a task to your project"
Step 3: "Invite team members to collaborate"

Help Center Structure:
- Getting Started
  - Create account
  - First project
  - Invite team
- Features
  - Tasks
  - Calendar
  - Reports
- Troubleshooting
  - Can't log in
  - Payment issues
  - Missing data
```

**Help Types by User Need:**

| User Need | Help Type | Example |
|-----------|-----------|---------|
| I don't understand this | Tooltip | "?" icon shows explanation |
| How do I...? | How-to guide | "How to export data" |
| Something's wrong | Troubleshooting | "Can't log in? Try these steps" |
| I'm new | Onboarding | Welcome tour, getting started |
| I need support | Contact | Chat, email, or ticket system |

---

## 2. Accessibility (WCAG 2.1 AA)

### WCAG Principles: POUR

**Perceivable:** Information must be presentable to users in ways they can perceive.

**Operable:** Interface components must be operable by all users.

**Understandable:** Information and operation must be understandable.

**Robust:** Content must be robust enough to work with current and future technologies.

### Accessibility Checklist

#### Color and Contrast

```
Minimum Contrast Ratios (WCAG AA):
- Normal text (<18pt): 4.5:1
- Large text (≥18pt or ≥14pt bold): 3:1
- Icons and graphics: 3:1

Tools to Check:
- WebAIM Contrast Checker
- Chrome DevTools (Inspect element)
- Figma plugins (Stark, A11y)

Common Mistakes:
✗ Light gray text on white (#999 on #FFF = 2.8:1 ❌)
✗ Low-contrast buttons
✗ Placeholder text as only label (too light)

Good Practices:
✓ Dark text on light (#333 on #FFF = 12.6:1 ✓)
✓ Test with tools
✓ Don't rely on color alone (add icons, text)

Color-Blind Considerations:
✓ Use patterns in addition to colors
✓ Label colors explicitly
✓ Test with color-blind simulators

Example:
Status indicators:
❌ Red/green only
✓ Red with X icon / Green with ✓ icon
✓ "Error" / "Success" text labels
```

#### Keyboard Navigation

```
Requirements:
✓ All interactive elements focusable
✓ Logical tab order (top to bottom, left to right)
✓ Visible focus indicator
✓ Keyboard shortcuts don't trap users
✓ Skip links for repetitive content

Tab Order:
1. Header (logo, nav, search)
2. Main content (primary actions first)
3. Sidebar (if applicable)
4. Footer

Focus Indicators:
✓ Outline around focused element
✓ High contrast (distinct from background)
✓ Doesn't disappear on custom styles

Keyboard Shortcuts:
- Tab: Next element
- Shift+Tab: Previous element
- Enter/Space: Activate button/link
- ESC: Close modal/dropdown
- Arrow keys: Navigate lists/menus

Testing:
□ Can you navigate entire site with keyboard only?
□ Is focus visible at all times?
□ Can you access all features?
□ Can you escape from modals/dropdowns?
```

#### Screen Reader Support

```
Semantic HTML:
✓ <button> for buttons (not <div onclick>)
✓ <a href> for links
✓ <input> with <label>
✓ <nav>, <main>, <aside>, <footer> landmarks
✓ <h1>-<h6> in hierarchical order

ARIA Labels:
✓ aria-label for icons without text
✓ aria-describedby for additional context
✓ aria-live for dynamic content
✓ alt text for images

Examples:
Icon Button:
<button aria-label="Close">
  <svg>...</svg>
</button>

Form Field:
<label for="email">Email</label>
<input id="email" type="email" aria-describedby="email-help">
<span id="email-help">We'll never share your email</span>

Dynamic Content:
<div aria-live="polite">
  Item added to cart
</div>

Images:
<img src="chart.png" alt="Sales increased 45% in Q4">

Decorative Images:
<img src="divider.png" alt="" role="presentation">
```

#### Forms and Inputs

```
Labels:
✓ Every input has associated label
✓ Label visible (not just placeholder)
✓ Label describes purpose clearly

Required Fields:
✓ Marked with * or "required"
✓ Indicated in label (not just color)
✓ aria-required="true"

Error Messages:
✓ Associated with field (aria-describedby)
✓ Clear, specific, helpful
✓ Announced to screen readers
✓ Visually distinct (not just color)

Example:
<label for="password">
  Password <span aria-label="required">*</span>
</label>
<input
  id="password"
  type="password"
  aria-required="true"
  aria-invalid="true"
  aria-describedby="password-error"
>
<span id="password-error" role="alert">
  Password must be at least 8 characters
</span>
```

#### Content Structure

```
Headings:
✓ One <h1> per page
✓ Hierarchical (don't skip levels)
✓ Describe section content

Example:
<h1>Product Page</h1>
  <h2>Product Details</h2>
    <h3>Specifications</h3>
    <h3>Reviews</h3>
  <h2>Related Products</h2>

Links:
✓ Descriptive text (not "click here")
✓ Distinguishable from regular text
✓ Purpose clear from context

Good: "Read our privacy policy"
Bad: "Click here to read more"

Lists:
✓ Use <ul>, <ol>, <dl> for lists
✓ Screen readers announce list and item count

Tables:
✓ <th> for headers with scope
✓ <caption> for table title
✓ Simple structure (avoid nested tables)
```

---

## 3. Mobile-First Design

### Core Principles

**Mobile-First:** Design for smallest screen first, then enhance for larger screens.

**Why:**
- Forces prioritization (only essential content fits)
- Majority of traffic is mobile
- Easier to scale up than down
- Better performance (load less initially)

### Mobile Design Patterns

#### Touch Targets

```
Minimum Sizes:
- Buttons: 44x44pt (iOS), 48x48dp (Android)
- Any tappable element: 44x44pt minimum
- Spacing between targets: 8pt minimum

Example:
❌ Tiny link (20x20pt) - hard to tap
✓ Button with padding (44x44pt minimum)

Mobile Navigation:
✓ Hamburger menu for many items
✓ Bottom tab bar for primary actions (3-5 items)
✓ Sticky header for key actions
✗ Hover-based menus (no hover on mobile)
```

#### Responsive Layout

```
Breakpoints (Common):
- Mobile: 0-640px
- Tablet: 641-1024px
- Desktop: 1025px+

Mobile Layout:
- Single column
- Stack elements vertically
- Full-width buttons
- Larger text (16px minimum to prevent zoom)

Tablet Layout:
- 2-column grid (in some sections)
- Side-by-side content where appropriate
- Optimize for both portrait and landscape

Desktop Layout:
- Multi-column grid
- Side navigation
- More content visible simultaneously
```

#### Mobile Forms

```
Best Practices:
✓ One column layout
✓ Large input fields (44pt height minimum)
✓ Proper input types (email, tel, number)
✓ Auto-capitalize/auto-correct where appropriate
✓ Minimize typing (use selects, checkboxes)
✓ Show password option
✓ Sticky submit button (always visible)

Input Types (show correct keyboard):
type="email" - Shows @ key
type="tel" - Shows number pad
type="url" - Shows .com key
type="number" - Shows numeric keyboard
type="date" - Shows date picker

Example:
<input type="email" placeholder="you@example.com">
- Mobile shows keyboard with @ easily accessible
```

#### Mobile Navigation

```
Patterns:

1. Hamburger Menu:
   - Three lines icon
   - Opens full-screen or side drawer
   - For 5+ navigation items

2. Bottom Tab Bar:
   - 3-5 primary sections
   - Always visible
   - Icons + labels

3. Top App Bar:
   - Logo, title, search, profile
   - Primary actions on right
   - Back button on left

4. Priority+:
   - Show important items
   - "More" for less important
   - Adapts to screen size

Best Practice:
- Primary actions: Bottom tab bar
- Secondary: Hamburger menu
- Don't hide primary navigation
```

### Performance Optimization

```
Mobile Performance:
✓ Lazy load images
✓ Optimize image sizes (WebP, responsive images)
✓ Minimize JavaScript
✓ Critical CSS inline
✓ Fast server response (<200ms)

Target Metrics:
- First Contentful Paint: <1.8s
- Largest Contentful Paint: <2.5s
- Time to Interactive: <3.9s
- Total page weight: <1MB (ideally <500KB)

Tools:
- Google PageSpeed Insights
- Lighthouse (Chrome DevTools)
- WebPageTest
```

---

## 4. Information Architecture

### Site Structure

#### Card Sorting

**Method to organize content based on user mental models.**

```
Process:
1. Write content topics on cards (physical or digital)
2. Ask users (15-30) to group cards into categories
3. Ask them to name each category
4. Analyze patterns

Types:
- Open card sort: Users create own categories
- Closed card sort: You provide categories
- Hybrid: Mix of both

Tools:
- OptimalSort
- UserZoom
- Simple: Index cards + whiteboard

Result:
- Categories that match user expectations
- Navigation structure
- Content groupings
```

#### Tree Testing

**Validate navigation structure before building.**

```
Process:
1. Create text-only site structure
2. Give users tasks: "Where would you find X?"
3. They navigate text-only tree
4. Measure success, time, directness

Tools:
- Treejack (Optimal Workshop)
- UserZoom

Metrics:
- Success rate (found correct page)
- Directness (correct first click)
- Time taken

Goal: >70% success rate, >60% direct navigation
```

### Navigation Patterns

```
Global Navigation (Top):
- Logo (links home)
- Primary sections (5-7 max)
- Search
- User account/cart

Local Navigation (Sidebar):
- Sub-sections
- Filters
- Related links

Breadcrumbs:
Home > Products > Shoes > Running Shoes
- Shows where you are
- Allows jumping to parent levels
- Especially important for deep sites

Footer:
- Secondary navigation
- Legal links
- Contact info
- Social media
- Sitemap
```

---

## 5. User Journey Mapping

### Creating User Journeys

**Template:**

```
User: [Persona name]
Goal: [What they want to accomplish]
Scenario: [Context/situation]

Journey Stages:
1. Awareness
2. Consideration
3. Purchase/Signup
4. Onboarding
5. Usage
6. Loyalty/Advocacy

For Each Stage:
- Actions: What user does
- Touchpoints: Where they interact
- Thoughts: What they're thinking
- Emotions: How they feel (😊 😐 😞)
- Pain Points: Frustrations
- Opportunities: How to improve
```

**Example: SaaS Product**

```
User: Sarah, Marketing Manager
Goal: Find tool to manage team projects

AWARENESS STAGE:
Action: Searches "project management for marketing teams"
Touchpoint: Google search, blog posts
Thoughts: "I need something simple, not overly technical"
Emotions: Curious 😊
Pain Points: Too many options, unclear differences
Opportunity: Clear comparison content, marketing-specific messaging

CONSIDERATION STAGE:
Action: Visits 3 product websites, reads reviews
Touchpoint: Product page, review sites, comparison pages
Thoughts: "Which one fits our team size and budget?"
Emotions: Confused 😐
Pain Points: Unclear pricing, can't see features without signup
Opportunity: Transparent pricing, interactive demos without signup

SIGNUP STAGE:
Action: Signs up for free trial
Touchpoint: Signup form
Thoughts: "I hope this isn't complicated to set up"
Emotions: Hopeful 😊
Pain Points: Too many form fields, unclear next steps
Opportunity: Minimal signup form, clear expectations

ONBOARDING STAGE:
Action: Creates first project, invites team
Touchpoint: Onboarding flow, email notifications
Thoughts: "Can I get this set up in 10 minutes?"
Emotions: Impatient 😐
Pain Points: Unclear how to invite team, overwhelming features
Opportunity: Guided setup, contextual help, templates

USAGE STAGE:
Action: Daily task management, weekly planning
Touchpoint: Web app, mobile app, email notifications
Thoughts: "This is saving me time"
Emotions: Satisfied 😊
Pain Points: Occasional bug, missing integration
Opportunity: Proactive support, feature requests

RENEWAL STAGE:
Action: Reviews value before renewal
Touchpoint: Usage dashboard, billing page
Thoughts: "Is this worth $99/month?"
Emotions: Evaluating 😐
Pain Points: Not sure about ROI, alternatives cheaper
Opportunity: Show value metrics, testimonials from similar companies
```

---

## Summary: Quick Reference Checklist

### Essential UX Checks

```
Before Launch:
□ All interactive elements keyboard accessible
□ Color contrast meets WCAG AA (4.5:1)
□ All images have alt text
□ Forms have visible labels
□ Error messages are helpful
□ Mobile responsive (test on real devices)
□ Loading states for all actions
□ Confirmation for destructive actions
□ Clear call-to-action on every page
□ Help/support easily accessible

User Testing:
□ 5 users complete key tasks
□ Measure task success rate (target: >80%)
□ Identify confusion points
□ Fix top 3 usability issues
□ Iterate and test again

Analytics Setup:
□ Track key user journeys
□ Monitor error rates
□ Measure time to complete tasks
□ A/B test variations
□ Collect user feedback
```

Good UX is invisible. Users should accomplish goals without thinking about the interface.
