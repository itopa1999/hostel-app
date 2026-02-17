# STAFF GUIDE - HotelOS Staff Workflow & Operations

## Table of Contents
1. [Staff Dashboard](#staff-dashboard)
2. [Getting Started as Staff](#getting-started-as-staff)
3. [Your Daily Tasks](#your-daily-tasks)
4. [Sidebar Navigation](#sidebar-navigation)
5. [Managing Check-Ins](#managing-check-ins)
6. [Managing Check-Outs](#managing-check-outs)
7. [Guest Management](#guest-management)
8. [Viewing Bookings](#viewing-bookings)
9. [Important Rules & Checks](#important-rules--checks)
10. [Troubleshooting](#troubleshooting)

---

## Staff Dashboard

When you login as a staff member, you see a simplified dashboard focused on your daily tasks.

### Your Dashboard Shows

```
┌─────────────────────────────────────────────────────┐
│ STAFF DASHBOARD - Today's Overview                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│ TODAY'S SUMMARY                                     │
│ ├─ Check-ins Due Today:       3                     │
│ ├─ Check-outs Due Today:      2                     │
│ ├─ Available Rooms:            15                   │
│ └─ Occupied Rooms:             22                   │
│                                                     │
│ QUICK ALERTS                                        │
│ ├─ 🔴 2 OVERDUE check-outs!                        │
│ ├─ 🟡 Rooms needing cleaning                       │
│ └─ 🟢 1 check-in arriving today                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Key Information at a Glance

| Widget | What It Tells You | Action Needed |
|--------|------------------|--------------|
| **Today's Check-ins** | Guests checking in today | Be ready to process check-ins |
| **Today's Check-outs** | Guests checking out today | Start checkout procedures |
| **Available Rooms** | Clean rooms ready for guests | Can assign new bookings |
| **Occupied Rooms** | Rooms with active guests | Cannot assign these rooms |

---

## Getting Started as Staff

### Your First Day

1. **Receive Welcome Email**
   - Contains your login username
   - Temporary password
   - System URL

2. **First Login**
   - Go to system URL
   - Enter email and password
   - Change password to something only you know
   - ✓ You're in!

3. **What You Can See**
   - Bookings list
   - Guest information
   - Room status
   - Check-in/Check-out functions
   - Invoice information (read-only)

4. **What You Cannot See**
   - Staff management
   - Financial reports
   - System settings
   - Audit logs
   - Payment processing (admin/manager only)

### Your Permissions (What You Can Do)

✓ **CAN DO**:
- View all bookings
- View guest information
- Check-in guests (with verification)
- Check-out guests (with verification)
- View available rooms
- View today's schedule
- Search bookings and guests

✗ **CANNOT DO**:
- Create bookings
- Delete bookings
- Change room prices
- Process payments (not your job)
- Access admin settings
- Modify staff accounts
- View financial reports

---

## Your Daily Tasks

### Morning Routine (Start of Shift)

**When You Start Your Shift**:

1. **Check Your Dashboard**
   - How many check-ins are due today?
   - How many check-outs are due today?
   - Any alerts or warnings?

2. **Prepare for Check-ins**
   ```
   Expected Today:
   - Guest 1: Ahmed Ali (Room 201) - 2:00 PM arrival
   - Guest 2: Sarah Smith (Room 305) - 3:30 PM arrival
   ```
   - Have rooms cleaned and ready
   - Have keys/access cards prepared
   - Prepare welcome materials if available

3. **Prepare for Check-outs**
   ```
   Expected Today:
   - John Doe (Room 102) - Must leave by 11:00 AM
   - Emma Johnson (Room 405) - Must leave by 11:00 AM
   ```
   - Verify guests are aware
   - Prepare checkout procedures
   - Have cleaning team ready

---

### During Your Shift

**As Guests Arrive/Leave**:

1. **When Guest Arrives**: Process check-in immediately
2. **During Stay**: Assist with requests, maintain records
3. **Before Guest Leaves**: Remind about checkout time
4. **When Guest Leaves**: Process check-out immediately

---

### End of Shift

1. **Verify All Tasks Completed**
   - All check-ins processed?
   - All check-outs processed?
   - All rooms assigned?
   - Any issues recorded?

2. **Handover to Next Shift**
   - Note any ongoing issues
   - Alert next staff about pending tasks
   - Leave system in clean state

---

## Sidebar Navigation

### 📊 Dashboard
- **Location**: Top of sidebar
- **What You See**: Your daily summary and today's tasks
- **Actions**: 
  - View today's schedule
  - See alerts and warnings
  - Quick stats
- **Use**: Check this first when you start shift

---

### 🏨 Bookings

**What It Does**: View and manage guest bookings

**What You See**:
```
BOOKINGS LIST
├─ Guest Name
├─ Room Number
├─ Check-in Date/Time
├─ Check-out Date/Time
├─ Status (RESERVED, CHECKED_IN, CHECKED_OUT)
├─ Number of Guests
└─ Payment Status (PENDING, COMPLETED)
```

**Actions Available**:
- 👁️ **View Details** - See full booking info
- ✓ **Check-In** - Process guest arrival
- ✓ **Check-Out** - Process guest departure
- 📞 **Contact Guest** - Call/email guest
- 📋 **View Invoice** - See charges and payment status

**Filters to Help You**:
- By status (Today, Upcoming, Checked-in, etc.)
- By date range
- By room number
- By guest name

**Search**:
- Search by guest name
- Search by room number
- Search by booking ID

---

### 👥 Guests

**What It Does**: View guest information

**What You See**:
- Guest name
- Contact details (phone, email)
- ID/Passport information
- Check-in history
- Current booking (if any)
- Special requests or notes
- Allergies or preferences (if noted)

**Actions Available**:
- 👁️ **View Profile** - See all guest details
- 📞 **Call Guest** - Quick phone access
- 📧 **Email Guest** - Send message
- 📋 **Booking History** - See past stays
- 📝 **Add Note** - Write special requests or issues

**Example Notes You Might Add**:
```
Notes:
- Guest prefers extra pillows
- Guest is wheelchair accessible room preference
- Guest requested late checkout (not guaranteed)
- Guest has pet (if pets allowed)
- Guest prefers room away from elevator
```

---

### 🏥 Rooms

**What It Does**: View and manage room status

**What You See**:
```
ROOMS LIST
├─ Room Number
├─ Floor
├─ Type (Single, Double, Dorm, etc.)
├─ Status (AVAILABLE, OCCUPIED, MAINTENANCE)
├─ Current Guest (if occupied)
└─ Cleanliness Status
```

**Room Status Meanings**:

| Status | Meaning | Can Book It? |
|--------|---------|------------|
| AVAILABLE | Clean, ready for guests | ✓ YES |
| OCCUPIED | Guest currently in room | ✗ NO |
| MAINTENANCE | Being cleaned or repaired | ✗ NO |

**Actions Available**:
- 👁️ **View Room Details** - Full info
- 📋 **Booking History** - Previous guests in this room
- 🧹 **Mark Cleaned** - Set to AVAILABLE after cleaning
- 🔧 **Report Issue** - Notify about problem

---

## Managing Check-Ins

### Understanding Check-In

**What is Check-In?**
The moment when a guest arrives and officially enters the room. You must verify everything is correct.

### The Check-In Process

**STEP-BY-STEP GUIDE**:

```
STEP 1: GUEST ARRIVES
├─ Greet guest warmly
├─ Verify identity
└─ Smile! (First impression matters)

STEP 2: OPEN THE SYSTEM
├─ Go to: Invoices
├─ Search: Guest name or booking ID
└─ Find: The correct booking/invoice

STEP 3: VERIFY EVERYTHING
├─ ✓ Guest name matches
├─ ✓ Room number is correct
├─ ✓ Check-in date is today or earlier
├─ ✓ Payment status shows COMPLETED
├─ ✓ Room status shows AVAILABLE
└─ ✓ Booking status shows RESERVED

STEP 4: PROCESS CHECK-IN
├─ Click: CHECK-IN button
├─ Read: The confirmation modal
├─ Review: Guest and room details
├─ Click: CONFIRM CHECK-IN

STEP 5: SYSTEM UPDATES
├─ Booking status → CHECKED_IN
├─ Room status → OCCUPIED
├─ Records: Exact check-in time
├─ Shows: Success message
└─ Provides: Confirmation details

STEP 6: COMPLETE WITH GUEST
├─ Provide: Room key/access card
├─ Explain: Room features and amenities
├─ Point out: WiFi password, emergency exits
├─ Ask: "Any questions?"
├─ Say: "Welcome! Enjoy your stay!"
└─ Done! ✓
```

---

### When Can You Check-In a Guest?

**All These Must Be TRUE**:

✓ **Payment is COMPLETED**
- Reason: Guest has paid for the room
- Check: Payment status shows "COMPLETED"
- If Not: Ask guest to pay or contact manager

✓ **Check-in Date is Today or Earlier**
- Reason: You cannot check in before the booking date
- Check: Today's date ≥ Check-in date
- If Not: Tell guest "Come back on [date]"

✓ **Room is AVAILABLE**
- Reason: Cannot put guest in occupied or maintenance room
- Check: Room status shows "AVAILABLE"
- If Not: Assign different room or wait

✓ **Booking Status is RESERVED**
- Reason: Guest hasn't checked in yet
- Check: Status shows "RESERVED"
- If Shows "CHECKED_IN": Guest already checked-in somewhere else

✓ **Room is Clean and Ready**
- Reason: Guest pays for clean room
- Check: Visual inspection + system confirmation
- If Not: Schedule cleaning first

---

### What if Check-In Fails?

**If You See an Error Message**:

| Error Message | What It Means | Fix |
|---------------|--------------|-----|
| "Payment not completed" | Guest hasn't paid | Contact manager, get payment first |
| "Check-in date not reached" | Date is in future | Wait until check-in date |
| "Room not available" | Room occupied or maintenance | Pick different room |
| "Already checked-in" | Guest already has active booking | Check if double booking or error |
| "Booking cancelled" | Booking was cancelled | Create new booking if needed |

---

### Check-In Checklist

Before clicking CHECK-IN, verify this checklist:

```
☑️ VERIFICATION CHECKLIST
├─ ☑ Guest name matches ID
├─ ☑ Room number correct
├─ ☑ Payment status COMPLETED
├─ ☑ Room status AVAILABLE
├─ ☑ Room is clean
├─ ☑ Check-in date is today or past
├─ ☑ All luggage/belongings arrived
└─ ☑ Guest ready to proceed
```

Once all checked, click CHECK-IN ✓

---

## Managing Check-Outs

### Understanding Check-Out

**What is Check-Out?**
When a guest leaves and vacates the room. Process confirms departure and prepares room for next guest.

### The Check-Out Process

**STEP-BY-STEP GUIDE**:

```
STEP 1: GUEST NOTIFIES YOU OF DEPARTURE
├─ Guest approaches desk
├─ Guest returns key/access card
└─ Guest ready to settle any final bills

STEP 2: OPEN THE SYSTEM
├─ Go to: Invoices
├─ Search: Guest name or booking ID
└─ Find: The checked-in booking

STEP 3: VERIFY EVERYTHING
├─ ✓ Guest name matches ID
├─ ✓ Room number is correct
├─ ✓ Booking status shows CHECKED_IN
├─ ✓ Check-out date is today or earlier
└─ ✓ Room being vacated

STEP 4: CHECK FOR ADDITIONAL CHARGES
├─ Any room damage? (Report to manager)
├─ Any items used beyond booking? (Add charges if applicable)
├─ Any payment still pending? (Collect payment)
└─ Guest agrees to final amount

STEP 5: PROCESS CHECK-OUT
├─ Click: CHECK-OUT button
├─ Read: The confirmation modal
├─ Review: Guest and room details
├─ Verify: Check-out date and charges
├─ Click: CONFIRM CHECK-OUT

STEP 6: SYSTEM UPDATES
├─ Booking status → CHECKED_OUT
├─ Room status → AVAILABLE
├─ Records: Exact check-out time
├─ Shows: Success message
└─ Booking complete!

STEP 7: COMPLETE WITH GUEST
├─ Say: "Thank you for staying with us"
├─ Provide: Receipt/proof of checkout
├─ Ask: "How was your stay?"
├─ Offer: "Hope to see you again!"
├─ Open: Door for guest
└─ Done! ✓

STEP 8: PREPARE ROOM
├─ Collect: Towels and linens
├─ Check: Room condition
├─ Note: Any damage
├─ Alert: Maintenance if needed
├─ Schedule: Cleaning crew
└─ When clean: Mark room AVAILABLE in system
```

---

### When Can You Check-Out a Guest?

**All These Should Be TRUE**:

✓ **Booking Status is CHECKED_IN**
- Reason: Guest must be checked-in first
- Check: Status shows "CHECKED_IN"
- If Not: This booking wasn't checked-in yet

✓ **Check-Out Date is Today or Earlier**
- Reason: Guest's stay is complete
- Check: Today's date ≥ Check-out date
- Note: You can process early checkouts if guest requests

✓ **Guest is Physically Vacating Room**
- Reason: Prevent checking out while guest still inside
- Check: Guest confirms they're leaving
- If Not: Tell guest "You can checkout on [date]"

---

### What if Check-Out Fails?

**If You See an Error Message**:

| Error Message | What It Means | Fix |
|---------------|--------------|-----|
| "Not checked in" | Booking wasn't checked-in | Check-in guest first |
| "Already checked out" | Guest already checked-out | Booking complete, no action needed |
| "Booking cancelled" | Booking was cancelled | No checkout needed |
| "Date not reached" | Check-out date is future | Wait until checkout date |

---

### Check-Out Checklist

Before clicking CHECK-OUT, verify this checklist:

```
☑️ DEPARTURE CHECKLIST
├─ ☑ Guest physically leaving
├─ ☑ Guest returned room key
├─ ☑ Guest agreed to final charges
├─ ☑ Payment settled (if any additional charges)
├─ ☑ Booking status shows CHECKED_IN
├─ ☑ Check-out date is today or past
├─ ☑ All personal items removed from room
├─ ☑ No outstanding issues
└─ ☑ Guest has receipt/proof
```

Once all checked, click CHECK-OUT ✓

---

## Guest Management

### Viewing Guest Information

**To Find a Guest**:

1. Go to **Guests** menu
2. Use search to find guest:
   - Search by name
   - Search by email
   - Search by phone
3. Click on guest to view profile

**Information You Can See**:
- Full name and contact details
- ID/Passport number
- Address
- Emergency contact
- Booking history (all past stays)
- Current booking (if any)
- Special requests or notes
- Join date (when first registered)

---

### Adding Guest Notes

**Why Add Notes?**
To remember preferences and help provide better service

**Examples of Useful Notes**:
```
Notes Examples:
- "Guest prefers high floor"
- "Guest requested NO morning calls"
- "Guest allergic to peanuts (if serving food)"
- "Guest in wheelchair - accessible room needed"
- "Guest mentioned visiting for business"
- "Guest requested late checkout"
- "Guest complained about noise - give quiet room"
- "Guest very friendly - likes to chat"
```

**How to Add Note**:
1. Go to **Guests**
2. Find and click guest
3. Click **Add Note** or **Edit Profile**
4. Add your note in notes section
5. Click **Save**

**Important**: Keep notes professional and helpful. Other staff will read these.

---

### Creating New Guest

**When to Create New Guest**:
- Guest is arriving for first time
- New person not in system yet
- Walk-in guest booking

**How to Create**:

1. Go to **Guests**
2. Click **Create New** or **+ Add Guest**
3. Enter required information:
   - Full name (required)
   - Email (required)
   - Phone (required)
   - ID/Passport number (required)
   - Address (required)
4. Optional information:
   - Emergency contact name/phone
   - Special requests
   - Notes
5. Click **Save**
6. Guest is now in system ✓

**Note**: Manager or Admin can create bookings for this guest

---

## Viewing Bookings

### Booking List View

**To Find Bookings**:
1. Go to **Bookings** menu
2. You see list of all bookings
3. Use filters to narrow down:
   - By status (Today, Upcoming, etc.)
   - By date range
   - By room number
   - By guest name
4. Use search to find specific booking

**What You See**:
- Guest name
- Room number
- Check-in date
- Check-out date
- Current status (RESERVED, CHECKED_IN, CHECKED_OUT)
- Payment status (PENDING, COMPLETED)
- Number of guests

---

### Booking Detail View

**To See Full Booking Details**:

1. Click on booking in list
2. View details screen shows:
   - Guest information
   - Room details
   - Check-in date and time
   - Check-out date and time
   - Number of guests
   - Special requests
   - Booking status
   - Payment status
   - Invoice amount
   - Check-in/Check-out history

---

### Understanding Booking Statuses

| Status | Meaning | Your Action |
|--------|---------|------------|
| RESERVED | Booking created, not checked-in yet | Check-in guest when arrives |
| CHECKED_IN | Guest in room right now | Check-out guest when leaves |
| CHECKED_OUT | Guest has left | Prepare room for next guest |
| CANCELLED | Booking was cancelled | Do nothing, this booking is over |

---

## Important Rules & Checks

### Critical Verification Before Check-In

**NEVER check-in a guest without verifying ALL of these**:

```
✓✓✓ MANDATORY VERIFICATION ✓✓✓

1. PAYMENT VERIFICATION
   ├─ Go to Invoice
   ├─ Check: Payment Status = COMPLETED
   ├─ If PENDING or PARTIAL: Tell guest "Payment incomplete"
   └─ If other issue: Get manager

2. IDENTITY VERIFICATION
   ├─ Ask: "Can I see your ID?"
   ├─ Check: Name on ID matches booking
   ├─ Check: Photo looks like guest
   └─ If doesn't match: Verify with manager

3. DATE VERIFICATION
   ├─ Check: Today's date ≥ Check-in date
   ├─ Check: Today's date ≤ Check-out date
   └─ If date issue: Verify booking is correct

4. ROOM VERIFICATION
   ├─ Check: Room status = AVAILABLE
   ├─ Check: Room is clean
   ├─ Check: Room number matches booking
   └─ If any issue: Pick different room

5. BOOKING VERIFICATION
   ├─ Check: Status = RESERVED
   ├─ Check: Not already checked-in elsewhere
   └─ If issue: Contact manager
```

**No Exceptions!** Always verify all 5 items before proceeding.

---

### What You CANNOT Do

**Strict Rules** (You Will Get in Trouble):

❌ **Cannot Modify Booking Details**
- Cannot change check-in date
- Cannot change check-out date
- Cannot change room assignment
- Cannot change guest name
- **Reason**: Admin/Manager only, prevents fraud

❌ **Cannot Process Payments**
- Cannot accept cash for room
- Cannot charge card
- Cannot transfer money
- **Reason**: Financial duties reserved for manager
- **What to Do**: Direct guest to manager

❌ **Cannot Delete Records**
- Cannot delete bookings
- Cannot delete guests
- Cannot delete rooms
- **Reason**: Would hide transaction history
- **What to Do**: Contact manager if needed

❌ **Cannot Access System Settings**
- Cannot change tax rate
- Cannot modify room prices
- Cannot add staff members
- Cannot change security settings
- **Reason**: Admin only privileges

---

### Security Rules

**Protect Guest Privacy**:
- ✓ Do NOT share guest phone numbers with other guests
- ✓ Do NOT discuss guest information publicly
- ✓ Do NOT leave guest details on desk
- ✓ Do NOT share passwords
- ✓ Do LOCK your computer when away
- ✓ Do LOGOUT before end of shift

**Protect System Access**:
- ✓ Never share your login password
- ✓ Never leave browser logged in unattended
- ✓ Never use someone else's account
- ✓ Always logout before leaving

---

## Troubleshooting

### Issue: "Cannot Check-In Guest"

**When You See**:
- Button is greyed out
- Error message appears
- System won't process check-in

**Check These**:

1. **Is Payment Completed?**
   - Go to Invoice
   - Look for: Payment status = "COMPLETED"
   - If "PENDING": Tell guest to pay first
   - If "PARTIAL": Contact manager

2. **Is Check-in Date Correct?**
   - Verify today's date ≥ Check-in date
   - If future date: Tell guest "Come back on [date]"
   - If unsure: Check booking details

3. **Is Room Available?**
   - Check room status
   - If "OCCUPIED": Pick different room
   - If "MAINTENANCE": Wait for cleaning or pick different room

4. **Is This the Right Booking?**
   - Verify guest name matches
   - Verify room number correct
   - If wrong booking: Search for correct one

**If Still Doesn't Work**:
- Contact your manager
- Provide: Guest name, booking ID, room number
- Provide: Error message text

---

### Issue: "Cannot Check-Out Guest"

**When You See**:
- Button is greyed out
- Error message appears
- System won't process checkout

**Check These**:

1. **Is Guest Actually Checked-In?**
   - Check booking status
   - If "RESERVED": Guest never checked-in, skip checkout
   - If "CHECKED_OUT": Already checked out, nothing to do
   - If "CHECKED_IN": Proceed

2. **Is Check-Out Date Correct?**
   - Verify today's date ≥ Check-out date
   - If future date: Tell guest "Checkout date is [date]"
   - Can do early checkout with guest permission

3. **Is Guest Actually Leaving?**
   - Verify guest is vacating room
   - Do not check out if guest still inside

**If Still Doesn't Work**:
- Contact your manager
- Provide: Guest name, booking ID, room number
- Provide: Error message text

---

### Issue: "Guest Information Won't Load"

**Cause**: Browser cache or system issue

**Quick Fixes**:
1. Refresh page: Ctrl+F5 (hard refresh)
2. Clear browser cache
3. Close and reopen browser
4. Try different browser
5. Restart computer

**If Persists**:
- Contact manager or IT support
- Provide: Which guest/booking won't load
- Provide: Browser type and version

---

### Issue: "Room Status Shows Wrong"

**Cause**: Cache not updated (updates every 6 hours)

**Quick Fixes**:
1. Refresh page: Ctrl+F5
2. Check-in or check-out a guest (clears cache)
3. Wait up to 6 hours for auto-update
4. Try different browser

**If Persists**:
- Contact manager
- Provide: Room number, current status, expected status

---

### Issue: "Cannot Find Guest in System"

**Possible Reasons**:
1. Guest was never registered
2. Typo in guest name
3. Guest account deactivated
4. Different spelling used

**What to Do**:
1. Search by phone instead of name
2. Search by email address
3. Search by ID/passport number
4. Ask guest their email

**If Still Not Found**:
- Guest needs to be registered
- Ask manager to create guest account
- Provide: Guest full name, phone, email, ID number

---

### Issue: "Receive Error About Cache"

**What It Means**: System data might be stale

**Solutions** (in order):
1. Hard refresh: Ctrl+F5 or Cmd+Shift+R
2. Clear cookies:
   - Chrome: Ctrl+Shift+Delete → Clear cookies for this site
   - Firefox: Ctrl+Shift+Delete → Clear All
3. Check-in or check-out a guest (clears cache)
4. Wait 6 hours for automatic cache refresh
5. Close and reopen browser

---

## Daily Tips for Success

### Morning Checklist
- [ ] Check today's check-ins count
- [ ] Check today's check-outs count
- [ ] Read any notes from previous shift
- [ ] Verify rooms are clean and ready
- [ ] Test that your login works

### During Shift
- [ ] Greet each guest warmly
- [ ] Verify information before check-in/checkout
- [ ] Add helpful notes in system
- [ ] Report any room issues immediately
- [ ] Keep your area organized

### End of Shift
- [ ] Verify all check-ins processed
- [ ] Verify all check-outs processed
- [ ] Note any ongoing issues
- [ ] Logout and close browser
- [ ] Brief next shift on open items

---

## Common Guest Questions (How to Answer)

### "Can I check-in early?"
- "Let me check if the room is available. If it's cleaned and ready, I can check you in! Give me a moment to verify."
- If available: Process early check-in
- If not available: "I can store your luggage and you can come back at [normal check-in time]"

### "Can I check-out late?"
- "Let me check with our manager. Late checkout is sometimes available for an additional fee. One moment please."
- Contact manager for approval
- If approved: Process late checkout at appropriate time

### "Where's my package/delivery?"
- Check with front desk or storage area
- If found: Provide to guest
- If not found: Take note, contact manager

### "How do I connect to WiFi?"
- "The password is [password]. It's also on the welcome card in your room."

### "What time is breakfast?"
- Provide breakfast times
- If guest has questions about food: Direct to manager

### "I have a problem with the room"
- Listen to complaint
- Offer solution if simple (extra pillow, towels, etc.)
- For complex issues: "Let me contact maintenance right away."
- Document in system notes
- Follow up later: "Did we solve that for you?"

---

## Your Responsibilities Summary

### You ARE Responsible For

✓ Greeting guests warmly and professionally
✓ Verifying guest information before check-in
✓ Processing check-ins when eligible
✓ Processing check-outs when eligible
✓ Maintaining guest records and notes
✓ Reporting room issues and problems
✓ Assisting guests with general requests
✓ Keeping the front area organized and clean
✓ Following security protocols
✓ Using the system correctly

### You ARE NOT Responsible For

✗ Processing payments or refunds
✗ Creating or modifying bookings
✗ Adjusting room prices
✗ Managing staff or security settings
✗ Deleting any records
✗ Accessing admin-only reports
✗ Making system-wide changes

---

## Quick Reference

### Check-In: 5 Verifications
1. ✓ Payment COMPLETED
2. ✓ Check-in date is today/past
3. ✓ Room is AVAILABLE
4. ✓ Guest identity verified
5. ✓ Room is clean and ready

### Check-Out: 3 Verifications
1. ✓ Booking is CHECKED_IN
2. ✓ Check-out date is today/past
3. ✓ Guest is leaving

### If Something Goes Wrong
→ Do NOT guess
→ DO contact your manager
→ DO provide: Guest name, room #, booking ID, error message

---

## Support & Help

**For Questions**:
1. Check this guide (use Table of Contents)
2. Ask your manager
3. Ask experienced colleagues
4. Contact IT support if system issue

**When Contacting Support, Provide**:
- Your name and shift time
- Guest name and booking ID (if applicable)
- Room number (if applicable)
- Exact error message
- Steps you took before the error

---

Congratulations! You're now ready to help guests enjoy their stay! 🎉

**Remember**: You're the first impression guests have. Be friendly, be helpful, be professional. You've got this! 💪

