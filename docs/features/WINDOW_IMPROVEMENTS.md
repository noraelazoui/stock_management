# Window Management Improvements

## Date: October 1, 2025

## Changes Made

### 1. Fixed Taskbar Visibility Issue
**Problem:** The application was hiding the Linux/Windows taskbar by using fullscreen mode without window decorations.

**Solution:** 
- Removed aggressive fullscreen settings that hid the taskbar
- Changed from `resizable(False, False)` to `resizable(True, True)` to allow user flexibility
- Adjusted window geometry to account for taskbar height (50px buffer)
- Used `state('zoomed')` which maximizes the window while keeping system UI visible

### 2. Added Close Button Confirmation
**Problem:** No confirmation when closing the application window.

**Solution:**
- Added `protocol("WM_DELETE_WINDOW", self.on_closing)` to intercept close button clicks
- Created `on_closing()` method that shows a confirmation dialog before closing
- User must confirm with "OK" to close, or "Cancel" to stay in the app

## Technical Details

### File Modified: `/views/main_view.py`

#### Before:
```python
# Set window to fullscreen size
self.geometry(f"{screen_width}x{screen_height}+0+0")

# Prevent window resizing
self.resizable(False, False)

# Try to maximize window (platform specific)
try:
    self.attributes('-zoomed', True)  # For some Linux systems
except:
    try:
        self.state('zoomed')  # For Windows
    except:
        pass
```

#### After:
```python
# Set window to maximized but keep window decorations and taskbar visible
# Leave some space for taskbar (typically 40-50px)
taskbar_height = 50
window_height = screen_height - taskbar_height
self.geometry(f"{screen_width}x{window_height}+0+0")

# Allow window resizing
self.resizable(True, True)

# Try to maximize window (platform specific) - this keeps taskbar visible
try:
    self.state('zoomed')  # For Windows and some Linux systems
except:
    pass  # Use geometry setting above as fallback

# Add close button functionality
self.protocol("WM_DELETE_WINDOW", self.on_closing)
```

#### New Method Added:
```python
def on_closing(self):
    """Handle window close button click"""
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application ?"):
        self.destroy()
```

## User Benefits

1. **Taskbar Always Accessible:** Users can now access their Linux/Windows taskbar while using the app
2. **Window Controls Available:** Standard minimize, maximize, and close buttons are now functional
3. **Resizable Window:** Users can resize the window if needed for their workflow
4. **Confirm Before Exit:** Prevents accidental application closure with a confirmation dialog
5. **Better User Experience:** More intuitive and follows standard desktop application behavior

## Platform Compatibility

✅ **Linux:** Uses `state('zoomed')` for maximization, keeps taskbar visible  
✅ **Windows:** Same behavior, standard maximize button works as expected  
✅ **Cross-platform:** Fallback geometry settings ensure compatibility

## Testing

The application has been tested and confirms:
- Taskbar remains visible on Linux
- Window can be resized and maximized normally
- Close button shows confirmation dialog
- All existing functionality preserved
