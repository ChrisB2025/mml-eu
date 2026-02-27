/**
 * Google Apps Script — MML EU Board Declaration Webhook
 *
 * SETUP INSTRUCTIONS:
 * 1. Go to https://sheets.google.com and create a new spreadsheet
 * 2. Add these column headers in row 1:
 *    Timestamp | Role | Title | Surname | First Name | Nationality | Profession |
 *    Flat | Building | Number | Extension | Street Name | PO Box |
 *    Postal Code | City | Country | Email
 * 3. Go to Extensions > Apps Script
 * 4. Delete any existing code and paste this entire file
 * 5. Click Deploy > New deployment
 * 6. Set type to "Web app"
 * 7. Set "Execute as" to "Me"
 * 8. Set "Who has access" to "Anyone"
 * 9. Click Deploy and copy the web app URL
 * 10. Paste that URL into mml-eu-board-declaration.html
 *     (replace YOUR_GOOGLE_APPS_SCRIPT_URL_HERE)
 */

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = JSON.parse(e.postData.contents);

  sheet.appendRow([
    new Date().toISOString(),
    data.role || '',
    data.title || '',
    data.surname || '',
    data.first_name || '',
    data.nationality || '',
    data.profession || '',
    data.flat || '',
    data.building || '',
    data.number || '',
    data.extension || '',
    data.street_name || '',
    data.po_box || '',
    data.postal_code || '',
    data.city || '',
    data.country || '',
    data.email || ''
  ]);

  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}

// Optional: test function to verify the script works
function doGet() {
  return ContentService
    .createTextOutput('MML EU Board Declaration webhook is active.')
    .setMimeType(ContentService.MimeType.TEXT);
}
