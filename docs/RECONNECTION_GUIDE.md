# Intelligent Reconnection System

## Overview

The transcriber now implements a smart reconnection system that distinguishes between different types of connection failures and applies appropriate backoff strategies.

## Reconnection Types

### 1. Network Issues (General Errors)
- **Initial Delay**: 10 seconds
- **Max Delay**: 5 minutes
- **Multiplier**: 1.5x per failure
- **Examples**: DNS failures, network timeouts, general connection errors

### 2. Feed Outages (HTTP 404/503 Errors)
- **Initial Delay**: 1 minute
- **Max Delay**: 30 minutes  
- **Multiplier**: 1.5x per failure
- **Examples**: Feed offline, "Error connecting to feed" on Broadcastify

## How It Works

### Feed Outage Detection
When the audio processor encounters HTTP 404 (Not Available) errors, it raises a `StreamURLError`. The transcriber catches this specific error and:

1. **First 3 attempts**: Uses shorter delays (1-3 minutes) assuming temporary outage
2. **After 3 attempts**: Switches to extended backoff (up to 30 minutes)
3. **Provides context**: Explains that feeds often go offline overnight or for maintenance

### Success Reset
- Network delays reset to 10 seconds after successful stream extraction
- Feed outage delays reset to 1 minute after successful transcription
- Consecutive error counters reset after any successful operation

## User Experience

### Console Output Examples

**Network Issue:**
```
🔄 Stream disconnected, reconnecting in 10 seconds...
```

**Feed Outage (Early attempts):**
```
❌ Feed outage detected: Invalid stream URL: HTTP 404
🔍 Feed has been unavailable for 2 consecutive attempts
🔄 Feed may be temporarily down, retrying in 90 seconds...
   📊 Attempt #2 - Using feed outage backoff
```

**Feed Outage (Extended):**
```
❌ Feed outage detected: Invalid stream URL: HTTP 404
🔍 Feed has been unavailable for 5 consecutive attempts
📻 Feed appears to be offline, will keep checking every 5m 3s...
🔄 Many radio feeds go offline overnight or during maintenance
   📊 Attempt #5 - Extended backoff active
```

## Benefits

1. **Efficient Resource Usage**: Longer delays for known feed outages prevent excessive server requests
2. **Better User Experience**: Clear messaging about what type of issue is occurring
3. **Persistent Operation**: Will never give up, only stops on Ctrl+C
4. **Context Awareness**: Explains that feed outages are normal for radio systems

## Configuration

Current delays are tuned for typical HAM radio feed patterns:
- Many feeds go offline overnight (10 PM - 6 AM)
- Maintenance windows are common
- Emergency services may have irregular availability

The 30-minute maximum delay balances responsiveness with resource efficiency.
