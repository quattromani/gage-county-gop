// This is a convenience hint, not detection of an installed/default calendar app.
export function calendarChoice(userAgent=''){
 if(/Android/i.test(userAgent))return 'google';
 if(/iPhone|iPad|iPod|Macintosh/i.test(userAgent))return 'apple';
 return null;
}
