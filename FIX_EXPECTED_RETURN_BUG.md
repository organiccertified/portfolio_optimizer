# Fix: Expected Return Bug - Always Shows Computed Value

## Problem Fixed

The Expected Return card was incorrectly showing the target return (20%) instead of the actual computed expected return from optimized weights.

## Changes Made

### 1. Backend (`backend/production_app.py`)

**Removed the buggy code** that forced `expected_return = target_return`:
- **Lines 460-468 (OLD)**: Code that forced `actual_return = target_return` for target_return strategy
- **NEW**: Always compute expected return from weights: `sum(weights * individual_returns)`

**Added consistency checks**:
- Verify weights sum to 1.0 (within 1e-6 tolerance)
- Normalize weights if needed and recalculate metrics
- Check for negative weights (shorting not allowed)

**Improved tolerance check**:
- Changed from 0.5% (0.005) to 0.25% (0.0025) tolerance
- More accurate `target_achieved` determination

**Added debug logging** for target_return strategy:
- Logs target_return_input, computed_expected_return, difference, tolerance, and target_achieved status

### 2. Frontend (`src/OptimizedApp.js`)

**Updated labels**:
- "Expected Return (Annual)" → "Portfolio Expected Return (Annual)"
- Added subtitle: "Computed from optimized weights"
- "Achieved: ..." → "Achieved (Expected): ..."

**Fixed Target Return card**:
- Shows user input target return (never changes)
- Shows actual computed expected return in "Achieved" line
- Shows ❌ if not achieved (instead of ⚠)
- Shows "Closest feasible solution" message when not achieved

**Fixed Beta display**:
- For target_return strategy: Shows "(informational only)" instead of ✓/⚠
- For other strategies: Shows ✓/⚠ based on tolerance (0.1)

### 3. Message Generation

Updated optimization messages to be more accurate:
- Shows actual expected return (not forced to target)
- Clarifies when target is not achievable
- Uses 2 decimal places for precision

## Formula Verification

### Expected Return Card
```
expected_return = sum_i (w_i * mu_i)
```
Where:
- `w_i` = final optimized weight of stock i
- `mu_i` = expected annual return for stock i (from individual_returns)

### Target Return Card
```
target_return = user_input / 100
```
Always shows the user's input, never changes.

### Achieved Line
```
achieved_return = expected_return (computed from weights)
is_achieved = abs(expected_return - target_return) <= 0.0025
```

## Testing

After this fix, you should see:
- **Expected Return**: ~16.95% (computed from actual weights)
- **Target Return**: 20.0% (user input)
- **Achieved**: ~16.95% (❌) - unless optimizer truly finds weights that reach 20%

## Debug Logging

When using target_return strategy, check server logs for:
```
Target Return Strategy Debug:
  target_return_input: 0.2000 (20.00%)
  computed_expected_return: 0.1695 (16.95%)
  difference: 0.0305 (3.05%)
  tolerance: 0.0025 (0.25%)
  target_achieved: False
```

This helps verify the fix is working correctly.

