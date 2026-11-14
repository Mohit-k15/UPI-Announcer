# UPI Announcer — Android starter project

This is a **starter prototype**, not a live payment-verification system.

## Included in this first build
- Kivy Android app interface
- Hindi / English voice-test button using Android TextToSpeech
- Local SQLite payment-history database
- Clearly marked demo-payment button
- GitHub Actions workflow to build a debug APK in the cloud

## Important safety limitation
The demo button creates a fake ₹100 record. It does not receive or verify money.
This starter does **not** yet read Google Pay, PhonePe, Paytm, BHIM, or other UPI notifications.
Do not hand over goods based on a notification or an announcement. For real shop use,
payment must be verified through the bank/acquirer or an authenticated payment-provider
integration. Notification text can be delayed, altered, incomplete, or spoofed.

## Build from an Android phone
1. Create a GitHub account and a new repository named `UPI-Announcer`.
2. Upload all files and folders from this ZIP, preserving the `.github/workflows/build.yml` path.
3. Open the repository's **Actions** tab.
4. Select **Build UPI Announcer APK** and press **Run workflow**.
5. When it finishes successfully, open the run and download the artifact
   `UPI-Announcer-debug-APK`.
6. Extract the ZIP and install the APK on your Android phone.

The first cloud build can take several minutes. The APK is a debug build for testing.

## Files
- `main.py` — Python/Kivy app
- `buildozer.spec` — Android build configuration
- `.github/workflows/build.yml` — cloud APK build workflow

## Next development stage
Add an Android notification-listener service with a properly merged Android manifest,
then test notification formats for each payment app. For production, replace notification
parsing with verified payment confirmation from an acquiring bank/payment provider.
