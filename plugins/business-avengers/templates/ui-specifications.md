# UI Specifications: {{PROJECT_NAME}}

**Version:** {{VERSION}}
**Date:** {{DATE}}
**Design Lead:** {{DESIGN_LEAD}}

---

## Component Library

### Buttons

#### Primary Button

**Purpose:** {{BTN_PRIMARY_PURPOSE}}

**Visual Specifications:**
- Height: {{BTN_PRIMARY_HEIGHT}}
- Padding: {{BTN_PRIMARY_PADDING}}
- Border Radius: {{BTN_PRIMARY_RADIUS}}
- Font Size: {{BTN_PRIMARY_FONT_SIZE}}
- Font Weight: {{BTN_PRIMARY_FONT_WEIGHT}}
- Text Transform: {{BTN_PRIMARY_TEXT_TRANSFORM}}

**Color Specifications:**

| State | Background | Text | Border | Shadow |
|-------|------------|------|--------|--------|
| Default | {{BTN_P_BG_DEFAULT}} | {{BTN_P_TEXT_DEFAULT}} | {{BTN_P_BORDER_DEFAULT}} | {{BTN_P_SHADOW_DEFAULT}} |
| Hover | {{BTN_P_BG_HOVER}} | {{BTN_P_TEXT_HOVER}} | {{BTN_P_BORDER_HOVER}} | {{BTN_P_SHADOW_HOVER}} |
| Active | {{BTN_P_BG_ACTIVE}} | {{BTN_P_TEXT_ACTIVE}} | {{BTN_P_BORDER_ACTIVE}} | {{BTN_P_SHADOW_ACTIVE}} |
| Focus | {{BTN_P_BG_FOCUS}} | {{BTN_P_TEXT_FOCUS}} | {{BTN_P_BORDER_FOCUS}} | {{BTN_P_SHADOW_FOCUS}} |
| Disabled | {{BTN_P_BG_DISABLED}} | {{BTN_P_TEXT_DISABLED}} | {{BTN_P_BORDER_DISABLED}} | {{BTN_P_SHADOW_DISABLED}} |
| Loading | {{BTN_P_BG_LOADING}} | {{BTN_P_TEXT_LOADING}} | {{BTN_P_BORDER_LOADING}} | {{BTN_P_SHADOW_LOADING}} |

**Size Variants:**

| Size | Height | Padding | Font Size | Icon Size |
|------|--------|---------|-----------|-----------|
| Small | {{BTN_P_SM_HEIGHT}} | {{BTN_P_SM_PADDING}} | {{BTN_P_SM_FONT}} | {{BTN_P_SM_ICON}} |
| Medium | {{BTN_P_MD_HEIGHT}} | {{BTN_P_MD_PADDING}} | {{BTN_P_MD_FONT}} | {{BTN_P_MD_ICON}} |
| Large | {{BTN_P_LG_HEIGHT}} | {{BTN_P_LG_PADDING}} | {{BTN_P_LG_FONT}} | {{BTN_P_LG_ICON}} |

**Accessibility:**
- Min Touch Target: {{BTN_P_TOUCH_TARGET}}
- Focus Indicator: {{BTN_P_FOCUS_INDICATOR}}
- ARIA Label: {{BTN_P_ARIA}}

---

#### Secondary Button

**Purpose:** {{BTN_SECONDARY_PURPOSE}}

**Visual Specifications:**
- Height: {{BTN_SECONDARY_HEIGHT}}
- Padding: {{BTN_SECONDARY_PADDING}}
- Border Radius: {{BTN_SECONDARY_RADIUS}}
- Border Width: {{BTN_SECONDARY_BORDER_WIDTH}}
- Font Size: {{BTN_SECONDARY_FONT_SIZE}}
- Font Weight: {{BTN_SECONDARY_FONT_WEIGHT}}

**Color Specifications:**

| State | Background | Text | Border | Shadow |
|-------|------------|------|--------|--------|
| Default | {{BTN_S_BG_DEFAULT}} | {{BTN_S_TEXT_DEFAULT}} | {{BTN_S_BORDER_DEFAULT}} | {{BTN_S_SHADOW_DEFAULT}} |
| Hover | {{BTN_S_BG_HOVER}} | {{BTN_S_TEXT_HOVER}} | {{BTN_S_BORDER_HOVER}} | {{BTN_S_SHADOW_HOVER}} |
| Active | {{BTN_S_BG_ACTIVE}} | {{BTN_S_TEXT_ACTIVE}} | {{BTN_S_BORDER_ACTIVE}} | {{BTN_S_SHADOW_ACTIVE}} |
| Focus | {{BTN_S_BG_FOCUS}} | {{BTN_S_TEXT_FOCUS}} | {{BTN_S_BORDER_FOCUS}} | {{BTN_S_SHADOW_FOCUS}} |
| Disabled | {{BTN_S_BG_DISABLED}} | {{BTN_S_TEXT_DISABLED}} | {{BTN_S_BORDER_DISABLED}} | {{BTN_S_SHADOW_DISABLED}} |

---

### Form Components

#### Text Input

**Purpose:** {{INPUT_PURPOSE}}

**Visual Specifications:**
- Height: {{INPUT_HEIGHT}}
- Padding: {{INPUT_PADDING}}
- Border Radius: {{INPUT_RADIUS}}
- Border Width: {{INPUT_BORDER_WIDTH}}
- Font Size: {{INPUT_FONT_SIZE}}
- Font Family: {{INPUT_FONT_FAMILY}}

**States:**

| State | Border Color | Background | Text Color | Label Color | Helper Text |
|-------|--------------|------------|------------|-------------|-------------|
| Default | {{INPUT_BORDER_DEFAULT}} | {{INPUT_BG_DEFAULT}} | {{INPUT_TEXT_DEFAULT}} | {{INPUT_LABEL_DEFAULT}} | {{INPUT_HELPER_DEFAULT}} |
| Focus | {{INPUT_BORDER_FOCUS}} | {{INPUT_BG_FOCUS}} | {{INPUT_TEXT_FOCUS}} | {{INPUT_LABEL_FOCUS}} | {{INPUT_HELPER_FOCUS}} |
| Error | {{INPUT_BORDER_ERROR}} | {{INPUT_BG_ERROR}} | {{INPUT_TEXT_ERROR}} | {{INPUT_LABEL_ERROR}} | {{INPUT_HELPER_ERROR}} |
| Success | {{INPUT_BORDER_SUCCESS}} | {{INPUT_BG_SUCCESS}} | {{INPUT_TEXT_SUCCESS}} | {{INPUT_LABEL_SUCCESS}} | {{INPUT_HELPER_SUCCESS}} |
| Disabled | {{INPUT_BORDER_DISABLED}} | {{INPUT_BG_DISABLED}} | {{INPUT_TEXT_DISABLED}} | {{INPUT_LABEL_DISABLED}} | {{INPUT_HELPER_DISABLED}} |

**Label Specifications:**
- Position: {{INPUT_LABEL_POSITION}}
- Font Size: {{INPUT_LABEL_FONT_SIZE}}
- Font Weight: {{INPUT_LABEL_FONT_WEIGHT}}
- Margin Bottom: {{INPUT_LABEL_MARGIN}}

**Helper Text Specifications:**
- Font Size: {{INPUT_HELPER_FONT_SIZE}}
- Margin Top: {{INPUT_HELPER_MARGIN}}
- Max Width: {{INPUT_HELPER_MAX_WIDTH}}

**Icon Specifications:**
- Size: {{INPUT_ICON_SIZE}}
- Position: {{INPUT_ICON_POSITION}}
- Padding: {{INPUT_ICON_PADDING}}

---

#### Dropdown/Select

**Purpose:** {{SELECT_PURPOSE}}

**Visual Specifications:**
- Height: {{SELECT_HEIGHT}}
- Padding: {{SELECT_PADDING}}
- Border Radius: {{SELECT_RADIUS}}
- Icon: {{SELECT_ICON}}

**Dropdown Menu:**
- Max Height: {{SELECT_MENU_MAX_HEIGHT}}
- Item Height: {{SELECT_ITEM_HEIGHT}}
- Item Padding: {{SELECT_ITEM_PADDING}}
- Shadow: {{SELECT_MENU_SHADOW}}

**States:**

| State | Border | Background | Text | Icon |
|-------|--------|------------|------|------|
| Default | {{SELECT_BORDER_DEFAULT}} | {{SELECT_BG_DEFAULT}} | {{SELECT_TEXT_DEFAULT}} | {{SELECT_ICON_DEFAULT}} |
| Hover | {{SELECT_BORDER_HOVER}} | {{SELECT_BG_HOVER}} | {{SELECT_TEXT_HOVER}} | {{SELECT_ICON_HOVER}} |
| Focus | {{SELECT_BORDER_FOCUS}} | {{SELECT_BG_FOCUS}} | {{SELECT_TEXT_FOCUS}} | {{SELECT_ICON_FOCUS}} |
| Disabled | {{SELECT_BORDER_DISABLED}} | {{SELECT_BG_DISABLED}} | {{SELECT_TEXT_DISABLED}} | {{SELECT_ICON_DISABLED}} |

---

#### Checkbox

**Purpose:** {{CHECKBOX_PURPOSE}}

**Visual Specifications:**
- Size: {{CHECKBOX_SIZE}}
- Border Radius: {{CHECKBOX_RADIUS}}
- Border Width: {{CHECKBOX_BORDER_WIDTH}}
- Checkmark Icon: {{CHECKBOX_ICON}}

**States:**

| State | Border | Background | Checkmark | Label |
|-------|--------|------------|-----------|-------|
| Unchecked Default | {{CB_BORDER_UNCHECKED}} | {{CB_BG_UNCHECKED}} | {{CB_CHECK_UNCHECKED}} | {{CB_LABEL_UNCHECKED}} |
| Unchecked Hover | {{CB_BORDER_UNCHECKED_H}} | {{CB_BG_UNCHECKED_H}} | {{CB_CHECK_UNCHECKED_H}} | {{CB_LABEL_UNCHECKED_H}} |
| Checked Default | {{CB_BORDER_CHECKED}} | {{CB_BG_CHECKED}} | {{CB_CHECK_CHECKED}} | {{CB_LABEL_CHECKED}} |
| Checked Hover | {{CB_BORDER_CHECKED_H}} | {{CB_BG_CHECKED_H}} | {{CB_CHECK_CHECKED_H}} | {{CB_LABEL_CHECKED_H}} |
| Indeterminate | {{CB_BORDER_INDET}} | {{CB_BG_INDET}} | {{CB_CHECK_INDET}} | {{CB_LABEL_INDET}} |
| Disabled Unchecked | {{CB_BORDER_DIS_UN}} | {{CB_BG_DIS_UN}} | {{CB_CHECK_DIS_UN}} | {{CB_LABEL_DIS_UN}} |
| Disabled Checked | {{CB_BORDER_DIS_CH}} | {{CB_BG_DIS_CH}} | {{CB_CHECK_DIS_CH}} | {{CB_LABEL_DIS_CH}} |

---

#### Radio Button

**Purpose:** {{RADIO_PURPOSE}}

**Visual Specifications:**
- Size: {{RADIO_SIZE}}
- Border Width: {{RADIO_BORDER_WIDTH}}
- Dot Size: {{RADIO_DOT_SIZE}}

**States:**

| State | Border | Background | Dot | Label |
|-------|--------|------------|-----|-------|
| Unselected Default | {{RADIO_BORDER_UNSEL}} | {{RADIO_BG_UNSEL}} | {{RADIO_DOT_UNSEL}} | {{RADIO_LABEL_UNSEL}} |
| Unselected Hover | {{RADIO_BORDER_UNSEL_H}} | {{RADIO_BG_UNSEL_H}} | {{RADIO_DOT_UNSEL_H}} | {{RADIO_LABEL_UNSEL_H}} |
| Selected Default | {{RADIO_BORDER_SEL}} | {{RADIO_BG_SEL}} | {{RADIO_DOT_SEL}} | {{RADIO_LABEL_SEL}} |
| Selected Hover | {{RADIO_BORDER_SEL_H}} | {{RADIO_BG_SEL_H}} | {{RADIO_DOT_SEL_H}} | {{RADIO_LABEL_SEL_H}} |
| Disabled Unselected | {{RADIO_BORDER_DIS_UN}} | {{RADIO_BG_DIS_UN}} | {{RADIO_DOT_DIS_UN}} | {{RADIO_LABEL_DIS_UN}} |
| Disabled Selected | {{RADIO_BORDER_DIS_SEL}} | {{RADIO_BG_DIS_SEL}} | {{RADIO_DOT_DIS_SEL}} | {{RADIO_LABEL_DIS_SEL}} |

---

#### Toggle/Switch

**Purpose:** {{TOGGLE_PURPOSE}}

**Visual Specifications:**
- Width: {{TOGGLE_WIDTH}}
- Height: {{TOGGLE_HEIGHT}}
- Track Border Radius: {{TOGGLE_TRACK_RADIUS}}
- Thumb Size: {{TOGGLE_THUMB_SIZE}}
- Thumb Offset: {{TOGGLE_THUMB_OFFSET}}

**States:**

| State | Track Color | Thumb Color | Thumb Position |
|-------|-------------|-------------|----------------|
| Off Default | {{TOGGLE_TRACK_OFF}} | {{TOGGLE_THUMB_OFF}} | {{TOGGLE_POS_OFF}} |
| Off Hover | {{TOGGLE_TRACK_OFF_H}} | {{TOGGLE_THUMB_OFF_H}} | {{TOGGLE_POS_OFF_H}} |
| On Default | {{TOGGLE_TRACK_ON}} | {{TOGGLE_THUMB_ON}} | {{TOGGLE_POS_ON}} |
| On Hover | {{TOGGLE_TRACK_ON_H}} | {{TOGGLE_THUMB_ON_H}} | {{TOGGLE_POS_ON_H}} |
| Disabled Off | {{TOGGLE_TRACK_DIS_OFF}} | {{TOGGLE_THUMB_DIS_OFF}} | {{TOGGLE_POS_DIS_OFF}} |
| Disabled On | {{TOGGLE_TRACK_DIS_ON}} | {{TOGGLE_THUMB_DIS_ON}} | {{TOGGLE_POS_DIS_ON}} |

---

### Navigation Components

#### Top Navigation Bar

**Purpose:** {{NAV_PURPOSE}}

**Visual Specifications:**
- Height: {{NAV_HEIGHT}}
- Padding: {{NAV_PADDING}}
- Background: {{NAV_BACKGROUND}}
- Border Bottom: {{NAV_BORDER}}
- Shadow: {{NAV_SHADOW}}
- Z-Index: {{NAV_Z_INDEX}}

**Logo:**
- Max Height: {{NAV_LOGO_HEIGHT}}
- Max Width: {{NAV_LOGO_WIDTH}}

**Navigation Items:**
- Font Size: {{NAV_ITEM_FONT_SIZE}}
- Font Weight: {{NAV_ITEM_FONT_WEIGHT}}
- Padding: {{NAV_ITEM_PADDING}}
- Gap: {{NAV_ITEM_GAP}}

**States:**

| State | Text Color | Background | Border Bottom |
|-------|------------|------------|---------------|
| Default | {{NAV_ITEM_TEXT_DEFAULT}} | {{NAV_ITEM_BG_DEFAULT}} | {{NAV_ITEM_BORDER_DEFAULT}} |
| Hover | {{NAV_ITEM_TEXT_HOVER}} | {{NAV_ITEM_BG_HOVER}} | {{NAV_ITEM_BORDER_HOVER}} |
| Active | {{NAV_ITEM_TEXT_ACTIVE}} | {{NAV_ITEM_BG_ACTIVE}} | {{NAV_ITEM_BORDER_ACTIVE}} |

---

#### Sidebar Navigation

**Purpose:** {{SIDEBAR_PURPOSE}}

**Visual Specifications:**
- Width: {{SIDEBAR_WIDTH}}
- Collapsed Width: {{SIDEBAR_COLLAPSED_WIDTH}}
- Background: {{SIDEBAR_BACKGROUND}}
- Border: {{SIDEBAR_BORDER}}
- Padding: {{SIDEBAR_PADDING}}

**Navigation Items:**
- Height: {{SIDEBAR_ITEM_HEIGHT}}
- Padding: {{SIDEBAR_ITEM_PADDING}}
- Border Radius: {{SIDEBAR_ITEM_RADIUS}}
- Icon Size: {{SIDEBAR_ICON_SIZE}}
- Gap: {{SIDEBAR_ITEM_GAP}}

**States:**

| State | Background | Text | Icon | Border |
|-------|------------|------|------|--------|
| Default | {{SIDE_ITEM_BG_DEFAULT}} | {{SIDE_ITEM_TEXT_DEFAULT}} | {{SIDE_ITEM_ICON_DEFAULT}} | {{SIDE_ITEM_BORDER_DEFAULT}} |
| Hover | {{SIDE_ITEM_BG_HOVER}} | {{SIDE_ITEM_TEXT_HOVER}} | {{SIDE_ITEM_ICON_HOVER}} | {{SIDE_ITEM_BORDER_HOVER}} |
| Active | {{SIDE_ITEM_BG_ACTIVE}} | {{SIDE_ITEM_TEXT_ACTIVE}} | {{SIDE_ITEM_ICON_ACTIVE}} | {{SIDE_ITEM_BORDER_ACTIVE}} |

---

### Cards

#### Standard Card

**Purpose:** {{CARD_PURPOSE}}

**Visual Specifications:**
- Border Radius: {{CARD_RADIUS}}
- Padding: {{CARD_PADDING}}
- Background: {{CARD_BACKGROUND}}
- Border: {{CARD_BORDER}}
- Shadow: {{CARD_SHADOW}}

**Header:**
- Padding: {{CARD_HEADER_PADDING}}
- Border Bottom: {{CARD_HEADER_BORDER}}
- Font Size: {{CARD_HEADER_FONT_SIZE}}
- Font Weight: {{CARD_HEADER_FONT_WEIGHT}}

**Body:**
- Padding: {{CARD_BODY_PADDING}}
- Font Size: {{CARD_BODY_FONT_SIZE}}
- Line Height: {{CARD_BODY_LINE_HEIGHT}}

**Footer:**
- Padding: {{CARD_FOOTER_PADDING}}
- Border Top: {{CARD_FOOTER_BORDER}}
- Alignment: {{CARD_FOOTER_ALIGN}}

**States:**

| State | Background | Border | Shadow |
|-------|------------|--------|--------|
| Default | {{CARD_BG_DEFAULT}} | {{CARD_BORDER_DEFAULT}} | {{CARD_SHADOW_DEFAULT}} |
| Hover | {{CARD_BG_HOVER}} | {{CARD_BORDER_HOVER}} | {{CARD_SHADOW_HOVER}} |
| Active/Selected | {{CARD_BG_ACTIVE}} | {{CARD_BORDER_ACTIVE}} | {{CARD_SHADOW_ACTIVE}} |

---

### Modals

#### Modal Dialog

**Purpose:** {{MODAL_PURPOSE}}

**Visual Specifications:**
- Max Width: {{MODAL_MAX_WIDTH}}
- Border Radius: {{MODAL_RADIUS}}
- Background: {{MODAL_BACKGROUND}}
- Shadow: {{MODAL_SHADOW}}
- Padding: {{MODAL_PADDING}}

**Backdrop:**
- Background: {{MODAL_BACKDROP_BG}}
- Opacity: {{MODAL_BACKDROP_OPACITY}}
- Blur: {{MODAL_BACKDROP_BLUR}}

**Header:**
- Padding: {{MODAL_HEADER_PADDING}}
- Border Bottom: {{MODAL_HEADER_BORDER}}
- Font Size: {{MODAL_HEADER_FONT_SIZE}}
- Font Weight: {{MODAL_HEADER_FONT_WEIGHT}}

**Body:**
- Padding: {{MODAL_BODY_PADDING}}
- Max Height: {{MODAL_BODY_MAX_HEIGHT}}
- Overflow: {{MODAL_BODY_OVERFLOW}}

**Footer:**
- Padding: {{MODAL_FOOTER_PADDING}}
- Border Top: {{MODAL_FOOTER_BORDER}}
- Alignment: {{MODAL_FOOTER_ALIGN}}
- Gap: {{MODAL_FOOTER_GAP}}

**Close Button:**
- Size: {{MODAL_CLOSE_SIZE}}
- Position: {{MODAL_CLOSE_POSITION}}
- Color: {{MODAL_CLOSE_COLOR}}
- Hover Color: {{MODAL_CLOSE_HOVER}}

**Size Variants:**

| Size | Max Width | Min Height |
|------|-----------|------------|
| Small | {{MODAL_SM_WIDTH}} | {{MODAL_SM_HEIGHT}} |
| Medium | {{MODAL_MD_WIDTH}} | {{MODAL_MD_HEIGHT}} |
| Large | {{MODAL_LG_WIDTH}} | {{MODAL_LG_HEIGHT}} |

---

### Alerts & Notifications

#### Alert Banner

**Purpose:** {{ALERT_PURPOSE}}

**Visual Specifications:**
- Padding: {{ALERT_PADDING}}
- Border Radius: {{ALERT_RADIUS}}
- Border Width: {{ALERT_BORDER_WIDTH}}
- Font Size: {{ALERT_FONT_SIZE}}
- Icon Size: {{ALERT_ICON_SIZE}}

**Variants:**

| Type | Background | Border | Text | Icon |
|------|------------|--------|------|------|
| Success | {{ALERT_SUCCESS_BG}} | {{ALERT_SUCCESS_BORDER}} | {{ALERT_SUCCESS_TEXT}} | {{ALERT_SUCCESS_ICON}} |
| Warning | {{ALERT_WARNING_BG}} | {{ALERT_WARNING_BORDER}} | {{ALERT_WARNING_TEXT}} | {{ALERT_WARNING_ICON}} |
| Error | {{ALERT_ERROR_BG}} | {{ALERT_ERROR_BORDER}} | {{ALERT_ERROR_TEXT}} | {{ALERT_ERROR_ICON}} |
| Info | {{ALERT_INFO_BG}} | {{ALERT_INFO_BORDER}} | {{ALERT_INFO_TEXT}} | {{ALERT_INFO_ICON}} |

---

#### Toast/Snackbar

**Purpose:** {{TOAST_PURPOSE}}

**Visual Specifications:**
- Max Width: {{TOAST_MAX_WIDTH}}
- Min Width: {{TOAST_MIN_WIDTH}}
- Padding: {{TOAST_PADDING}}
- Border Radius: {{TOAST_RADIUS}}
- Shadow: {{TOAST_SHADOW}}
- Position: {{TOAST_POSITION}}
- Z-Index: {{TOAST_Z_INDEX}}

**Animation:**
- Entry: {{TOAST_ENTRY_ANIMATION}}
- Exit: {{TOAST_EXIT_ANIMATION}}
- Duration: {{TOAST_DURATION}}

---

## Animations

### Transition Timings

| Type | Duration | Easing | Usage |
|------|----------|--------|-------|
| Instant | {{ANIM_INSTANT}} | {{ANIM_INSTANT_EASE}} | {{ANIM_INSTANT_USAGE}} |
| Fast | {{ANIM_FAST}} | {{ANIM_FAST_EASE}} | {{ANIM_FAST_USAGE}} |
| Normal | {{ANIM_NORMAL}} | {{ANIM_NORMAL_EASE}} | {{ANIM_NORMAL_USAGE}} |
| Slow | {{ANIM_SLOW}} | {{ANIM_SLOW_EASE}} | {{ANIM_SLOW_USAGE}} |

### Hover Effects

| Component | Property | Value | Duration |
|-----------|----------|-------|----------|
| {{HOVER_COMP_1}} | {{HOVER_PROP_1}} | {{HOVER_VAL_1}} | {{HOVER_DUR_1}} |
| {{HOVER_COMP_2}} | {{HOVER_PROP_2}} | {{HOVER_VAL_2}} | {{HOVER_DUR_2}} |
| {{HOVER_COMP_3}} | {{HOVER_PROP_3}} | {{HOVER_VAL_3}} | {{HOVER_DUR_3}} |

---

## Responsive Breakpoints

| Breakpoint | Min Width | Max Width | Typical Changes |
|------------|-----------|-----------|-----------------|
| Mobile S | {{BP_XS_MIN}} | {{BP_XS_MAX}} | {{BP_XS_CHANGES}} |
| Mobile M | {{BP_SM_MIN}} | {{BP_SM_MAX}} | {{BP_SM_CHANGES}} |
| Mobile L | {{BP_MD_MIN}} | {{BP_MD_MAX}} | {{BP_MD_CHANGES}} |
| Tablet | {{BP_LG_MIN}} | {{BP_LG_MAX}} | {{BP_LG_CHANGES}} |
| Desktop | {{BP_XL_MIN}} | {{BP_XL_MAX}} | {{BP_XL_CHANGES}} |
| Desktop XL | {{BP_XXL_MIN}} | - | {{BP_XXL_CHANGES}} |

---

## Dark Mode

### Color Overrides

| Component | Light Mode | Dark Mode |
|-----------|------------|-----------|
| Background | {{LM_BG}} | {{DM_BG}} |
| Surface | {{LM_SURFACE}} | {{DM_SURFACE}} |
| Primary Text | {{LM_TEXT_PRIMARY}} | {{DM_TEXT_PRIMARY}} |
| Secondary Text | {{LM_TEXT_SECONDARY}} | {{DM_TEXT_SECONDARY}} |
| Border | {{LM_BORDER}} | {{DM_BORDER}} |
| Card Background | {{LM_CARD_BG}} | {{DM_CARD_BG}} |
| Input Background | {{LM_INPUT_BG}} | {{DM_INPUT_BG}} |

---

## Accessibility Requirements

**WCAG Level:** {{WCAG_LEVEL}}

**Focus Indicators:**
- Outline Color: {{FOCUS_OUTLINE_COLOR}}
- Outline Width: {{FOCUS_OUTLINE_WIDTH}}
- Outline Offset: {{FOCUS_OUTLINE_OFFSET}}

**Minimum Touch Targets:** {{MIN_TOUCH_TARGET}}

**Color Contrast Ratios:**
- Normal Text: {{CONTRAST_NORMAL}}
- Large Text: {{CONTRAST_LARGE}}
- UI Components: {{CONTRAST_UI}}

---

## Implementation Notes

**CSS Framework:** {{CSS_FRAMEWORK}}
**Component Library:** {{COMPONENT_LIBRARY}}
**Design Tokens:** {{DESIGN_TOKENS_FILE}}

**Developer Handoff:**
{{DEVELOPER_HANDOFF_NOTES}}
