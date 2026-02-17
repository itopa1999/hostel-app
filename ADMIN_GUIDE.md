# ADMIN GUIDE - HotelOS Complete Admin Workflow

## Table of Contents
1. [Admin Dashboard](#admin-dashboard)
2. [Sidebar Navigation](#sidebar-navigation)
3. [Hostel Management](#hostel-management)
4. [Administrator Panel](#administrator-panel)
5. [Financial Management](#financial-management)
6. [Reports & Analytics](#reports--analytics)
7. [Settings & Configuration](#settings--configuration)
8. [Common Workflows](#common-workflows)
9. [Security & Audit](#security--audit)

---

## Admin Dashboard

The admin dashboard is your command center. When you login, you see:

### Key Metrics (Top Section)

| Metric | What It Means | Color |
|--------|---------------|-------|
| **Total Revenue** | All money earned from completed bookings this month | Green |
| **Active Bookings** | Guests currently checked-in | Blue |
| **Today's Check-ins** | Guests checking in today | Orange |
| **Today's Check-outs** | Guests checking out today | Red |
| **Available Rooms** | Rooms ready for new guests | Purple |
| **Occupied Rooms** | Rooms currently occupied | Gray |

### Dashboard Widgets

1. **Quick Stats**
   - Total guests this month
   - Total booking value
   - Average occupancy rate
   - Revenue trend

2. **Today's Activity**
   - Check-ins scheduled today
   - Check-outs scheduled today
   - New bookings created today

3. **Recent Activities**
   - Latest bookings
   - Latest check-ins
   - Latest payments
   - Latest staff actions

### Action Buttons

Quick shortcuts to common tasks:
- **Create Booking** - New guest booking
- **Add Guest** - Register new guest
- **Create Invoice** - Manual invoice (rare)
- **View Reports** - Access analytics

---

## Sidebar Navigation

The left sidebar contains all admin features. Here's what each section does:

### 📊 Dashboard
- **Location**: Top of sidebar
- **What You See**: Overview metrics and activities
- **Actions**: View charts, export data
- **Permission**: All admins can access
- **Common Use**: Check daily operations status

### 🏨 HOSTEL MANAGEMENT (Main Section)

#### 1. **Bookings**

**What It Does**: Manage all guest reservations

**Sidebar View**:
```
├── Bookings
│   ├── List View (default)
│   ├── Calendar View (optional)
│   └── Create New
```

**What You See**:
- Guest name
- Room assigned
- Check-in date
- Check-out date
- Number of guests
- Booking status (RESERVED, CHECKED_IN, CHECKED_OUT, CANCELLED)
- Duration
- Total amount

**Actions Available**:
- 👁️ **View Details** - See full booking info
- ✏️ **Edit** - Modify booking (ONLY if payment not completed)
- 🚫 **Cancel** - Cancel booking
- ✓ **Check-In** - Mark guest as checked-in (if eligible)
- ✓ **Check-Out** - Mark guest as checked-out (if eligible)
- 🗑️ **Delete** - Remove booking (admin only, logged)

**Eligibility Checks for Check-In**:
- Payment status must be COMPLETED ✓
- Check-in date must be today or earlier ✓
- Check-in date must not be in future ✓
- Room must be AVAILABLE ✓
- Booking status must be RESERVED ✓

**Eligibility Checks for Check-Out**:
- Booking status must be CHECKED_IN ✓
- Check-out date should be today or earlier ✓
- Cannot check-out if already checked-out ✓

**Filters Available**:
- By status (RESERVED, CHECKED_IN, CHECKED_OUT, CANCELLED)
- By date range
- By guest name
- By room number
- By payment status

**Search Features**:
- Search by guest name
- Search by room number
- Search by booking ID

---

#### 2. **Guests**

**What It Does**: Manage guest information database

**Sidebar View**:
```
├── Guests
│   ├── List View
│   ├── Create New
│   └── Import Guests
```

**What You See**:
- Guest name
- Email
- Phone number
- ID/Passport number
- Address
- Total bookings made
- Last booking date
- Status (Active/Inactive)

**Actions Available**:
- 👁️ **View Profile** - Full guest details
- ✏️ **Edit** - Update guest information
- 📞 **Contact** - Quick contact options
- 📝 **Booking History** - All past bookings
- 🚫 **Deactivate** - Mark guest as inactive
- 🗑️ **Delete** - Remove guest (with confirmation)

**Information Stored**:
- Full name (required)
- Email (required, unique)
- Phone (required)
- ID number and type (Passport, Driver's License, etc.)
- Address (street, city, country, postal code)
- Emergency contact
- Special notes/preferences
- Join date (auto)
- Last booking date (auto)

**Filters Available**:
- By active status
- By country
- By booking count
- By registration date

**Important**: Guests cannot be deleted if they have active bookings. Complete/cancel bookings first.

---

#### 3. **Rooms**

**What It Does**: Manage all physical rooms and their status

**Sidebar View**:
```
├── Rooms
│   ├── List View
│   ├── Grid View (visual)
│   ├── Create New
│   └── Bulk Actions
```

**What You See**:
- Room number
- Floor
- Room type (Single, Double, Dorm, Suite)
- Current status (AVAILABLE, OCCUPIED, MAINTENANCE)
- Price per night
- Current guest (if occupied)
- Last maintenance date
- Cleanliness status

**Actions Available**:
- 👁️ **View Details** - Full room information
- ✏️ **Edit** - Update room settings
- 🔄 **Change Status** - Update room status:
  - AVAILABLE → OCCUPIED (when checked-in)
  - OCCUPIED → AVAILABLE (when checked-out)
  - Any Status → MAINTENANCE
  - MAINTENANCE → AVAILABLE (after cleaning)
- 🧹 **Mark Cleaned** - Set cleanliness status
- 📋 **Booking History** - Previous guests
- 📸 **Upload Photos** - Add room images
- 🗑️ **Delete** - Remove room (admin only)

**Bulk Actions**:
- Change multiple rooms to MAINTENANCE
- Mark multiple rooms as cleaned
- Export room list

**Room Status Management**:

```
┌─────────────────────────────────────────┐
│ AVAILABLE                               │
│ Room is clean and ready for guests      │
└─────────────────────────────────────────┘
           ↓
Guest Checks-in → System auto-updates to OCCUPIED
           ↓
┌─────────────────────────────────────────┐
│ OCCUPIED                                │
│ Guest currently occupying room          │
└─────────────────────────────────────────┘
           ↓
Guest Checks-out → System auto-updates to AVAILABLE
           ↓
Or You Can Manually Set → MAINTENANCE for cleaning
           ↓
┌─────────────────────────────────────────┐
│ MAINTENANCE                             │
│ Room being cleaned or repaired          │
└─────────────────────────────────────────┘
           ↓
After cleaning complete → You change to AVAILABLE
```

**Filters Available**:
- By status (AVAILABLE, OCCUPIED, MAINTENANCE)
- By floor
- By room type
- By price range

---

#### 4. **Room Types**

**What It Does**: Define different room categories and pricing

**Sidebar View**:
```
├── Room Types
│   ├── List View
│   └── Create New
```

**What You See**:
- Room type name (Single, Double, Dorm, Suite, etc.)
- Description
- Max occupancy (number of guests)
- Base price per night
- Amenities list
- Number of rooms of this type
- Active status

**Actions Available**:
- 👁️ **View Details** - Full room type info
- ✏️ **Edit** - Update pricing and details
- 🗑️ **Delete** - Remove room type (if no rooms assigned)

**What You Configure**:
- **Name**: Type name (e.g., "Deluxe Double")
- **Max Occupancy**: How many guests can stay (e.g., 2)
- **Base Price**: Price per night in your currency (e.g., $50)
- **Description**: What makes this room special
- **Amenities**:
  - Free WiFi
  - Air Conditioning
  - TV
  - Mini Bar
  - Private Bathroom
  - Balcony
  - (Custom amenities can be added)

**Important**: Once created, you cannot change max occupancy or base price affects all future bookings.

---

#### 5. **Floors**

**What It Does**: Organize rooms by floor/level

**Sidebar View**:
```
├── Floors
│   ├── List View
│   ├── Create New
│   └── Bulk Actions
```

**What You See**:
- Floor name (Ground, 1st, 2nd, etc.)
- Number of rooms on floor
- Available rooms count
- Occupied rooms count
- Maintenance count
- Rooms currently occupied

**Actions Available**:
- 👁️ **View Details** - Rooms on this floor
- ✏️ **Edit** - Update floor info
- 📋 **View Rooms** - List all rooms on floor
- 🗑️ **Delete** - Remove floor (no rooms should be assigned)

**Information**:
- Floor number/name
- Total rooms capacity
- Facilities on floor (Elevator, WiFi, etc.)
- Emergency exits count
- Safety notes

---

### 👤 ADMINISTRATOR (Management Section)

#### 1. **Staff**

**What It Does**: Manage staff members and their access

**Sidebar View**:
```
├── Staff
│   ├── List View
│   ├── Roles
│   ├── Create New
│   └── Activity Log
```

**What You See**:
- Staff name
- Email
- Phone
- Role (Staff, Manager, Admin)
- Status (Active/Inactive)
- Last login
- Permissions

**Actions Available**:
- 👁️ **View Profile** - Staff details
- ✏️ **Edit** - Update staff info
- 🔑 **Reset Password** - Force password reset
- 📋 **Activity Log** - What staff has done
- 🚫 **Deactivate** - Disable account
- 🗑️ **Delete** - Remove staff (permanent)

**Creating New Staff**:

1. Click **Create New** or **+ Add Staff**
2. Enter:
   - Full name (required)
   - Email (required, unique)
   - Phone (required)
   - Password (must be strong: 8+ chars, mix of uppercase, lowercase, numbers)
   - Role:
     - **Staff**: Can check-in/check-out guests, view bookings, manage guests
     - **Manager**: Can do staff tasks + create bookings, manage payments
     - **Admin**: Full access to all features
3. Click **Save**
4. System sends welcome email to staff member

**Role Permissions**:

| Action | Staff | Manager | Admin |
|--------|-------|---------|-------|
| View Bookings | ✓ | ✓ | ✓ |
| Create Booking | ✗ | ✓ | ✓ |
| Check-in Guest | ✓ | ✓ | ✓ |
| Check-out Guest | ✓ | ✓ | ✓ |
| Cancel Booking | ✗ | ✓ | ✓ |
| View Guests | ✓ | ✓ | ✓ |
| Add Guest | ✗ | ✓ | ✓ |
| Manage Rooms | ✗ | ✗ | ✓ |
| Manage Staff | ✗ | ✗ | ✓ |
| View Reports | ✗ | ✓ | ✓ |
| Manage Settings | ✗ | ✗ | ✓ |
| View Audit Log | ✗ | ✗ | ✓ |

---

#### 2. **Audit Log**

**What It Does**: Complete record of all actions in system

**Sidebar View**:
```
├── Audit Log
│   └── View All Activities
```

**What You See**:
- Who performed action (staff name)
- What action (Create, Update, Delete, Check-in, Check-out)
- When (timestamp with exact time)
- What changed (specific field and old/new values)
- On what (booking ID, guest ID, etc.)
- Status (Success/Failed)

**Example Log Entries**:
```
2026-02-18 10:30:15 | John Admin | Created | Booking #1245 | 
  Guest: Ahmed Ali, Room: 201, Check-in: 2026-02-20

2026-02-18 11:45:00 | Sarah Staff | Checked-in | Booking #1245 | 
  Guest: Ahmed Ali moved to Room 201, Room status: OCCUPIED

2026-02-18 13:20:30 | John Admin | Updated | Guest | 
  Guest: Ahmed Ali, Field: Email, Old: old@email.com, New: new@email.com

2026-02-18 15:00:00 | Sarah Staff | Checked-out | Booking #1245 | 
  Guest: Ahmed Ali checked out, Room: 201 status: AVAILABLE

2026-02-18 16:10:45 | System | System | Generated | Invoice #INV-1245 | 
  Auto-generated invoice for Booking #1245
```

**Filters Available**:
- By staff member
- By action type
- By date range
- By object type (Booking, Guest, Room, etc.)
- By status (Success/Failed)

**Key Checks Available**:
- ✓ Verify who checked-in a guest
- ✓ Confirm when room status changed
- ✓ Track guest information changes
- ✓ See payment processing history
- ✓ Detect suspicious activities

**Can You Change Audit Logs?** NO. Audit logs are permanent and cannot be modified or deleted. This is for security.

---

### 💰 FINANCIAL MANAGEMENT (Money Section)

#### 1. **Invoices**

**What It Does**: Manage all financial transactions

**Sidebar View**:
```
├── Invoices
│   ├── List View
│   ├── Pending Invoices
│   ├── Completed Invoices
│   ├── Create Manual Invoice
│   └── Export/Reports
```

**What You See**:
- Invoice number (auto-generated, e.g., INV-001245)
- Guest name
- Room booked
- Check-in date
- Check-out date
- Number of nights
- Base amount (room price × nights)
- Tax amount
- Discount amount
- Total amount (what guest pays)
- Payment status (PENDING, COMPLETED, PARTIAL)
- Invoice date
- Due date
- Actions (Pay, Email, Print, Edit, Delete)

**Understanding Invoice Calculations**:

```
Invoice Calculation Example:
─────────────────────────────
Room Type:        Double Room
Price/Night:      $50
Number of Nights: 3
─────────────────────────────
Base Amount:      50 × 3 = $150.00
Tax (10%):        150 × 0.10 = $15.00
Discount (0%):    0
─────────────────────────────
TOTAL:            $165.00
─────────────────────────────
```

**Invoice Status Flow**:

```
Invoice Created (PENDING)
    ↓
Payment Received (COMPLETED)
    ↓
Guest Can Check-in
```

**Actions Available**:
- 👁️ **View Full Invoice** - See all details
- 💳 **Mark as Paid** - Manually mark payment received
- 📧 **Send Invoice** - Email to guest
- 🖨️ **Print** - Print for records
- ✏️ **Edit** - Only if PENDING (not yet paid)
- 🗑️ **Delete** - Remove (admin only, logged in audit)
- 📥 **Download PDF** - Save copy

**Payment Status Meanings**:

| Status | Meaning | Guest Can Check-in? |
|--------|---------|-------------------|
| PENDING | Invoice created, no payment yet | ❌ NO |
| PARTIAL | Some payment received | ❌ NO |
| COMPLETED | Full payment received | ✓ YES |

**Filters Available**:
- By payment status (PENDING, COMPLETED, PARTIAL)
- By date range
- By guest name
- By room
- By amount range

**Search**: Search by invoice number, guest name, or booking ID

---

#### 2. **Payments**

**What It Does**: Track and record payment transactions

**Sidebar View**:
```
├── Payments
│   ├── List View
│   ├── Pending Payments
│   ├── Completed Payments
│   ├── Record Payment
│   └── Payment Methods
```

**What You See**:
- Payment ID
- Guest name
- Invoice number
- Amount due
- Amount paid
- Payment method (Cash, Card, Transfer, Cheque, Other)
- Payment date
- Receipt number
- Status
- Reference number

**Recording Payment - Step by Step**:

1. Click **Record Payment**
2. Select or search invoice
3. Verify:
   - Guest name
   - Booking details
   - Amount due
4. Enter:
   - Amount received
   - Payment method:
     - **Cash**: Direct payment in hand
     - **Card**: Credit/debit card (get card last 4 digits)
     - **Transfer**: Bank transfer (get reference number)
     - **Cheque**: Cheque payment (get cheque number)
     - **Other**: Other method (specify)
5. Add notes if any (e.g., "Paid 50% now, rest later")
6. Upload receipt image (optional)
7. Click **Save**
8. System updates invoice status
9. Guest now eligible for check-in (if full payment)

**Payment Verification Checklist**:
- ✓ Correct guest selected
- ✓ Correct amount entered
- ✓ Payment method recorded
- ✓ Receipt or reference number saved
- ✓ Notes added if partial payment

---

### 📊 REPORTS & ANALYTICS

#### 1. **Reports**

**What It Does**: View business performance and metrics

**Sidebar View**:
```
├── Reports
│   ├── Revenue Report
│   ├── Occupancy Report
│   ├── Guest Report
│   ├── Staff Performance
│   └── Export Reports
```

**Available Reports**:

**A. Revenue Report**
- Total revenue by date range
- Revenue by room type
- Revenue by month/quarter/year
- Average revenue per booking
- Cancellation losses
- Charts and graphs

**B. Occupancy Report**
- Occupancy rate (percentage of rooms occupied)
- Occupancy by room type
- Occupancy trends
- Peak and low seasons
- Available vs occupied rooms count

**C. Guest Report**
- Total guests served
- Repeat guest count
- Guest demographics
- Average stay duration
- Guest satisfaction (if available)

**D. Staff Performance Report**
- Check-ins completed by staff
- Check-outs completed by staff
- Bookings created
- Payment processing time
- Activity frequency

**Exporting Reports**:
1. Select report type
2. Choose date range
3. Click **Export**
4. Choose format:
   - PDF (for printing/emails)
   - Excel (for analysis)
   - CSV (for data import)

---

### ⚙️ SETTINGS & CONFIGURATION

#### 1. **System Settings**

**What It Does**: Configure how the system operates

**Sidebar View**:
```
├── Settings
│   ├── General Settings
│   ├── Tax Configuration
│   ├── Discount Settings
│   ├── Payment Methods
│   ├── Backup & Restore
│   └── About
```

**General Settings**:
- Hotel name
- Hotel description
- Contact email
- Contact phone
- Address
- City, Country, Postal Code
- Hotel website
- Logo and images
- Business hours
- Check-in time (default, e.g., 2 PM)
- Check-out time (default, e.g., 11 AM)

**Tax Configuration**:
- Tax percentage (e.g., 10%)
- Tax name (e.g., "VAT", "GST")
- Apply tax to all invoices (yes/no)
- Tax calculation method

**Discount Settings**:
- Default discount percentage
- Allow staff to apply discounts
- Max discount allowed per booking
- Require approval for discounts over X amount

**Payment Methods**:
- Enable/disable payment methods:
  - Cash
  - Card/Credit
  - Bank Transfer
  - Cheque
  - Mobile Money (if applicable)
- Default payment method

**Backup & Restore**:
- Schedule automatic backups
- Manual backup now
- Download backup
- Restore from backup (admin only)

---

## Common Workflows

### Workflow 1: Creating and Completing a Booking

**Full Process** (Start to Finish):

```
STEP 1: CREATE BOOKING
├─ Go to: Bookings → Create New
├─ Select: Guest (or create new guest)
├─ Select: Room
├─ Enter: Check-in date
├─ Enter: Check-out date
├─ Enter: Number of guests
├─ Add: Notes (optional)
└─ Click: SAVE

SYSTEM AUTO-GENERATES INVOICE
├─ Calculates: Room price × nights
├─ Adds: Tax (if configured)
├─ Applies: Discount (if any)
├─ Creates: Invoice with status PENDING
└─ Status: Booking created as RESERVED

STEP 2: RECORD PAYMENT
├─ Go to: Payments → Record Payment
├─ Select: The invoice
├─ Verify: Amount matches
├─ Select: Payment method
├─ Enter: Amount received
├─ Upload: Receipt (optional)
└─ Click: SAVE

SYSTEM UPDATES INVOICE
├─ Status: Changes to COMPLETED
├─ Guest: Now eligible for check-in
└─ Log: Payment recorded in audit log

STEP 3: CHECK-IN GUEST
├─ Go to: Invoices
├─ Find: Guest's invoice
├─ Verify: Payment is COMPLETED ✓
├─ Verify: Check-in date is today or past ✓
├─ Verify: Room is AVAILABLE ✓
├─ Click: CHECK-IN button
├─ Confirm: In modal dialog
└─ Click: CONFIRM CHECK-IN

SYSTEM PROCESSES CHECK-IN
├─ Updates: Booking status → CHECKED_IN
├─ Updates: Room status → OCCUPIED
├─ Records: Check-in timestamp
├─ Clears: Cache (for fresh data)
├─ Shows: Success message
└─ Log: Check-in recorded in audit log

GUEST STAYS IN ROOM (Days pass...)

STEP 4: CHECK-OUT GUEST
├─ Go to: Invoices
├─ Find: Guest's invoice
├─ Verify: Check-out date is today or past ✓
├─ Verify: Booking status is CHECKED_IN ✓
├─ Click: CHECK-OUT button
├─ Confirm: In modal dialog
└─ Click: CONFIRM CHECK-OUT

SYSTEM PROCESSES CHECK-OUT
├─ Updates: Booking status → CHECKED_OUT
├─ Updates: Room status → AVAILABLE
├─ Records: Check-out timestamp
├─ Clears: Cache (for fresh data)
├─ Shows: Success message
└─ Log: Check-out recorded in audit log

BOOKING COMPLETE ✓
├─ Guest has vacated room
├─ Room is ready for next guest
├─ Invoice marked as completed
└─ Revenue recorded in reports
```

---

### Workflow 2: Handling a Cancelled Booking

**If Guest Cancels**:

1. Go to **Bookings**
2. Find booking
3. Click **Cancel Booking**
4. Select reason:
   - Guest requested
   - No-show
   - Payment failed
   - Other (specify)
5. Add notes (optional)
6. Click **Confirm Cancel**
7. System:
   - Sets booking status to CANCELLED
   - Marks invoice as cancelled
   - Frees up room
   - Logs action in audit log
   - May handle refund (if configured)

---

### Workflow 3: Handling Room Maintenance

**When Room Needs Cleaning/Repair**:

1. Go to **Rooms**
2. Find room
3. Click on room
4. Click **Change Status**
5. Select: **MAINTENANCE**
6. Add reason:
   - Cleaning scheduled
   - Repair needed
   - Inspection
   - Deep cleaning
7. Estimated time to complete
8. Click **Save**

**What Happens**:
- ✓ Room disappears from available rooms
- ✓ Cannot book room during maintenance
- ✓ Staff sees it's under maintenance

**When Maintenance Complete**:

1. Go to **Rooms**
2. Find room (filtered by MAINTENANCE status)
3. Click **Mark as Cleaned** or **Change Status**
4. Select: **AVAILABLE**
5. Click **Save**

---

### Workflow 4: Adding New Staff Member

**Process**:

1. Go to **Administrator** → **Staff**
2. Click **Create New** or **+ Add Staff**
3. Enter:
   - Full name: (First and Last name)
   - Email: (Must be unique, e.g., john.doe@hostel.com)
   - Phone: (With country code if international)
   - Password: (Generate strong password)
   - Role: (Choose: Staff, Manager, or Admin)
4. Review permissions for selected role
5. Click **Save**
6. System:
   - Creates staff account
   - Sends welcome email with login info
   - Logs action in audit log
   - Activates account immediately

**Staff Access**:
- Email and temporary password sent to staff
- Staff logs in and changes password
- Access based on assigned role

---

## Security & Audit

### Understanding Permissions

**Admin Capabilities**:
- ✓ Full system access
- ✓ Create, edit, delete any record
- ✓ Manage staff and permissions
- ✓ View audit logs
- ✓ Configure system settings
- ✓ Access sensitive reports
- ✓ Cannot be removed without super-admin

### Fraud Prevention Mechanisms

**Booking Protection**:
Once payment is COMPLETED, these fields CANNOT be modified:
- ❌ Check-in date
- ❌ Check-out date
- ❌ Room assignment
- ❌ Number of guests
- ❌ Guest details

**Why?** Prevents fraud like:
- Changing dates after payment to extend stay
- Switching to cheaper room after payment
- Modification of guest records after transaction

### Audit Trail

**Everything is Logged**:
- ✓ Who did what
- ✓ When they did it
- ✓ What changed
- ✓ Old and new values
- ✓ Success or failure
- ✓ Cannot be modified

**Use Audit Log To**:
- ✓ Track staff activities
- ✓ Verify changes
- ✓ Detect unauthorized access
- ✓ Investigate disputes
- ✓ Compliance records

### Best Practices

1. **Password Management**:
   - Change password regularly (every 90 days)
   - Use strong passwords (8+ chars, mix of types)
   - Never share password with anyone
   - Use unique password for each user

2. **Data Protection**:
   - Don't share guest data unnecessarily
   - Use HTTPS for all connections
   - Enable automatic backups
   - Regularly verify backups

3. **Access Control**:
   - Give staff minimal required permissions
   - Deactivate unused accounts
   - Regularly review staff access
   - Audit log suspicious activities

4. **Backup & Recovery**:
   - Enable automatic daily backups
   - Test restore process monthly
   - Store backups securely
   - Keep backup location private

---

## Troubleshooting Guide for Admins

### Issue: Guest Cannot Check-In

**Checklist**:
- ✓ Payment status is COMPLETED?
  - If No: Process payment first
- ✓ Check-in date is today or earlier?
  - If No: Wait until check-in date arrives
- ✓ Room is AVAILABLE?
  - If No: Assign different room or change room status
- ✓ Booking status is RESERVED?
  - If No: Booking might be already checked-in or cancelled

**Solution**: Address each failed check, then try again.

---

### Issue: Cannot Edit Booking

**Message**: "This booking cannot be modified because payment is completed"

**This is Intentional**: It's a fraud prevention feature.

**Workaround** (if absolutely necessary):
1. Contact Admin Support
2. Provide justification
3. May require admin approval
4. Changes logged in audit trail

---

### Issue: Invoice Shows Old Data

**Cause**: Cache has old data (updated every 6 hours)

**Solutions**:
1. **Quick Fix**: Perform check-in or check-out (clears cache)
2. **Refresh**: Refresh browser (Ctrl+F5)
3. **Wait**: Cache auto-updates every 6 hours
4. **Contact IT**: If issue persists

---

### Issue: Room Status Not Updating

**Possible Causes**:
1. Browser cache (clear cache and refresh)
2. System cache (wait 6 hours or check-in/check-out guest)
3. Permission issue (verify user role)
4. System error (check server logs)

**Solution**:
1. Hard refresh: Ctrl+F5 or Cmd+Shift+R
2. Clear browser cookies for this domain
3. Try again in 5 minutes
4. If persists, contact IT support

---

### Issue: Staff Account Not Receiving Welcome Email

**Possible Causes**:
1. Wrong email entered (typo)
2. Email server not configured
3. Email marked as spam
4. Email server issues

**Solution**:
1. Verify email address is correct
2. Check staff junk/spam folder
3. Ask staff to check spam folder
4. Manually provide temporary login info
5. Contact IT if email system issues

---

### Issue: Cannot Delete Guest

**Reason**: Guest has active bookings

**Solution**:
1. View guest's booking history
2. Complete or cancel all bookings
3. Then try deleting guest again

---

## Tips for Efficient Admin Operations

1. **Daily Check**:
   - Check Today's Check-ins count
   - Check Today's Check-outs count
   - Verify all are processed
   - Check for any issues

2. **Weekly Review**:
   - Review occupancy rates
   - Check revenue trends
   - Verify staff activity (audit log)
   - Review guest feedback (if available)

3. **Monthly Tasks**:
   - Generate revenue report
   - Export occupancy data
   - Review all audit logs
   - Verify payment records
   - Check for discrepancies

4. **Data Backup**:
   - Ensure automatic backups are running
   - Monthly test restore process
   - Keep backup drive in safe place
   - Monitor backup storage space

---

## Support & Escalation

**If You Get Stuck**:
1. Check "Troubleshooting Guide" section above
2. Review relevant workflow section
3. Check system logs (admin only)
4. Contact IT Support with:
   - Exact error message
   - Steps to reproduce
   - Screenshots if applicable
   - Browser and version info

---

Congratulations! You now have complete knowledge of the admin panel. Happy managing! 🎉

