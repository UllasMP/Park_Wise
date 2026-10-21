"""One shared lock so two gates can never take the same slot.

Entry and payment both change slot usage, so both run inside this lock.
(The database also has unique constraints as a second safety net.)
"""
import threading

parking_lock = threading.RLock()
