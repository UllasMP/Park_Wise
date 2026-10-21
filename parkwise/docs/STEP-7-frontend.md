# Step 7 - React frontend (`frontend/src`)

```
api/client.js              every fetch() call in one place; throws {code, message}
context/ParkingContext.jsx shared state with useContext (operator, slots, dashboard)
components/                OperatorPicker, SlotMap, DevClock
pages/                     EntryPage, ExitPage, DashboardPage  (the 3 screens)
App.jsx                    header + tabs (a simple useState, no router)
```

**State management:** `ParkingProvider` holds data several screens need.
Components read it with the `useParking()` hook. Page-only data (form text, ticket result)
stays in local `useState`.

**After every entry/exit** we call `refreshAll()`, which re-fetches the slot map and dashboard
from the server. The frontend never computes fees or slots.

**Errors:** the server's `message` is shown directly under the form.
