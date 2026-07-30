/**
 * 트래비티 문의 메일 알림 + 구글시트 저장 (Apps Script)
 * — 이전 트래비티 랜딩(trevity-landing)과 같은 방식입니다.
 *
 * 설치:
 * 1. 구글시트 새로 만들기 → 확장 프로그램 → Apps Script
 * 2. 이 코드를 붙여넣고 MAIL_TO 를 원하는 수신 메일로 수정
 * 3. 배포 → 새 배포 → 웹 앱 → 액세스 권한 "모든 사용자" → 배포
 * 4. 나온 /exec URL을 SEO 관리(localhost:5723/seo.html) → 문의 메일 알림 → Apps Script 웹앱 URL 에 붙여넣고 저장
 */
var MAIL_TO = 'notice@trevity.com';   // ← 수신 메일

function doPost(e) {
  var p = e.parameter || {};
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['접수시각', '회사', '담당자', '연락처', '이메일', '내용', '유입']);
  }
  sheet.appendRow([
    new Date(), p.company || '', p.name || '', p.phone || '',
    p.email || '', p.message || '', p.page || '',
  ]);
  MailApp.sendEmail({
    to: MAIL_TO,
    subject: '[트래비티] 새 문의 — ' + (p.company || p.name || '무기명'),
    body: '회사: ' + (p.company || '') + '\n'
        + '담당자: ' + (p.name || '') + '\n'
        + '연락처: ' + (p.phone || '') + '\n'
        + '이메일: ' + (p.email || '') + '\n\n'
        + (p.message || '') + '\n\n'
        + '접수: ' + (p.ts || new Date().toISOString()),
  });
  return ContentService.createTextOutput('ok');
}
