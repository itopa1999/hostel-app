# Getting Started with HotelOS - Hostel Management System

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation & Setup](#installation--setup)
3. [Initial Configuration](#initial-configuration)
4. [First Login](#first-login)
5. [Basic Concepts](#basic-concepts)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Hardware Requirements
- **Server**: Minimum 2GB RAM, 10GB storage space
- **Internet**: Stable connection (for cloud deployment)
- **Browser Compatibility**: 
  - Chrome (recommended, latest version)
  - Firefox (latest version)
  - Safari (latest version)
  - Edge (latest version)

### Software Requirements
- Python 3.8 or higher
- PostgreSQL 12+ (or MySQL 5.7+)
- Redis (for caching)
- Modern web browser

---

## Installation & Setup

### Step 1: Download and Install the Application

```bash
# Download the application files
# Extract to your desired location
cd /path/to/hostel-app

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
# Copy .env.example to .env
cp .env.example .env

# Edit .env file with your settings:
# - Database credentials
# - Secret key
# - Debug mode (False for production)
# - Allowed hosts
```

### Step 2: Database Setup

```bash
# Create database
# For PostgreSQL:
createdb hostel_management

# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to set:
# - Username (e.g., admin)
# - Email (e.g., admin@hostel.com)
# - Password (strong password recommended)
```

### Step 3: Start the Server

```bash
# Development server
python manage.py runserver

# Production server
# Use gunicorn or your preferred production server
# For example: gunicorn backend.wsgi:application
```

### Step 4: Access the Application

Open your browser and navigate to:
- **Local**: `http://localhost:8000`
- **Remote**: `https://your-domain.com`

---

## Initial Configuration

### Step 1: Run the Setup Wizard

After database migration, run the interactive setup wizard:

```bash
python manage.py create_hotel
```

This wizard will guide you through:
- **Creating the Hotel Instance** - Hotel name, address, contact info, check-in/check-out times
- **Setting Up Admin Account** - Create your admin user and password
- **Configuring System Settings** - Tax percentage, discount settings

**Example Output**:
```
Hotel Setup Wizard
==================================================
(Press Enter to skip optional fields)

STEP 1: Setting up Admin Group
==================================================
✓ Admin group created
✓ Staff group created

STEP 2: Hotel Information
==================================================
Hotel name: My Awesome Hostel
Address: 123 Main Street
City: New York
...
Check-in time (HH:MM) [default: 14:00]: 14:00
Check-out time (HH:MM) [default: 12:00]: 11:00

STEP 3: Create Admin Account
==================================================
Admin username: admin
Admin password: ••••••••
Confirm password: ••••••••
✓ Admin account created successfully!

STEP 4: Configure Settings
==================================================
Tax percentage [default: 0]: 10
Default discount percentage [default: 0]: 5
✓ Settings created successfully!

✓ HOTEL SETUP COMPLETED SUCCESSFULLY!
```

After completing this wizard, your system is ready to use!

---

## First Login

### Admin First Login
1. Navigate to login page
2. Enter superuser email/username
3. Enter password
4. You'll see the **Admin Dashboard** with:
   - Key metrics (Total Revenue, Active Bookings, etc.)
   - Quick actions
   - Recent activities

### Staff First Login
1. Navigate to login page
2. Enter staff credentials (provided by admin)
3. You'll see the **Staff Dashboard** with:
   - Today's check-ins/check-outs
   - Available rooms
   - Guest information
   - Limited management options

---

## Basic Concepts

### Understanding the Booking Flow

```
Guest Booking Created
    ↓
Invoice Generated (Automatic)
    ↓
Payment Pending
    ↓
Payment Completed
    ↓
Guest Can Check-In (from check-in date)
    ↓
Guest Checked-In (Room status: OCCUPIED)
    ↓
Guest Checks Out (on check-out date)
    ↓
Room Back to AVAILABLE
    ↓
Booking Completed
```

### Room Status Meanings

- **Available**: Room is clean and ready for guests
- **Occupied**: Room currently has an active guest
- **Maintenance**: Room is being cleaned or repaired
- **Unavailable**: Room is blocked/reserved

### Booking Status Meanings

- **RESERVED**: Booking created
- **CHECKED_IN**: Guest has checked in, currently occupying room
- **CHECKED_OUT**: Guest has left
- **CANCELLED**: Booking was cancelled
- **NO_SHOW**: Guest didn't arrive for booking

### Payment Status Meanings

- **PENDING**: Invoice created, waiting for payment
- **COMPLETED**: Full payment received

### Checkout Status Meanings

- **ON_TIME**: Check-out date is in future
- **TODAY**: Check-out date is today
- **OVERDUE**: Check-out date has passed
- **CHECKED_OUT**: Guest has already checked out

---

## Important Features Explained

### Automatic Invoice Generation
When you create a booking, the system automatically:
1. Calculates total cost (room price × nights)
2. Applies tax and discount
3. Creates invoice
4. Generates payment record
5. All calculated instantly

### Cache System (6-Hour Refresh)
The system caches invoice and payment data for 6 hours for performance. This means:
- Data updates every 6 hours automatically
- Manual refresh clears cache immediately
- Check-in/Check-out always clears cache for fresh data

### Audit Logging
Every action (create, update, delete, check-in, check-out) is automatically logged:
- Who performed the action
- When it was performed
- What was changed
- Records cannot be altered

### Protected Bookings
Once payment is completed, you cannot modify:
- Check-in date
- Check-out date
- Room assignment
- Number of guests
- Guest details

**Reason**: Prevents fraud and maintains data integrity

---

## Common Tasks

### Creating a Booking

1. Go to **Hostel Management** → **Bookings**
2. Click **Create Booking**
3. Select guest
4. Select room
5. Enter check-in date
6. Enter check-out date
7. Enter number of guests
8. Add notes (optional)
9. Click **Save**
10. System auto-generates invoice

### Checking Guest In

1. Go to **Invoices**
2. Find the guest's invoice
3. Verify:
   - Payment status is COMPLETED
   - Check-in date is today or in past
   - Room is AVAILABLE
4. Click **Check-In** button
5. Confirm in modal dialog
6. System updates room to OCCUPIED

### Checking Guest Out

1. Go to **Invoices**
2. Find the guest's invoice
3. Verify check-out date
4. Click **Check-Out** button
5. Confirm in modal dialog
6. System returns room to AVAILABLE

### Processing Payment

1. Go to **Payments**
2. Find the pending payment
3. Verify payment details
4. Click **Mark as Completed**
5. Invoice status changes to COMPLETED

---

## Troubleshooting

### Issue: "Cannot login"
**Solution**: 
- Verify username/email is correct
- Check caps lock
- Reset password if forgotten
- Contact admin

### Issue: "Room is not available"
**Solution**: 
- Room status might be OCCUPIED or MAINTENANCE
- Select a different room
- Contact admin to change room status

### Issue: "Cannot check-in guest"
**Solutions**:
- Payment not completed: Complete payment first
- Check-in date not reached yet: Wait until check-in date
- Room not available: Select different room

### Issue: "Data not updating"
**Solution**: 
- Refresh browser (Ctrl+F5 or Cmd+Shift+R)
- Clear browser cache
- Cache updates every 6 hours automatically
- Check-in/Check-out actions clear cache immediately

### Issue: "Cannot modify booking"
**Solution**: 
- Payment already completed: Cannot modify certain fields
- Contact admin if changes are critical
- System prevents modification to maintain data integrity

### Issue: "Invoice shows old data"
**Solution**: 
- Perform a check-in or check-out to clear cache
- Wait up to 6 hours for automatic cache refresh
- Refresh browser cache manually

---

## Support & Help

For issues not covered here:
1. Check the specific guide (Admin Guide or Staff Guide)
2. Contact your system administrator
3. Check audit logs for what happened (Admin only)
4. Provide error message and steps to reproduce

---

## Next Steps

After setup, refer to:
- **ADMIN_GUIDE.md** - For complete admin functionality
- **STAFF_GUIDE.md** - For staff operations

Enjoy using HotelOS! 🏨
