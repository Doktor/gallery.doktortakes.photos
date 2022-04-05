export function twoDigitPad(n) {
  return n <= 9 ? "0" + n : n;
}

export function formatDate(str) {
  if (str === null) {
    return "N/A";
  }

  let date = new Date(Date.parse(str));
  return "{0}-{1}-{2}".format(
    date.getFullYear(),
    twoDigitPad(date.getMonth() + 1),
    twoDigitPad(date.getDate())
  );
}

export function formatDateTime(str) {
  if (str === null) {
    return "N/A";
  }

  let date = new Date(Date.parse(str));
  return "{0} {1}:{2}:{3}".format(
    formatDate(date),

    twoDigitPad(date.getHours()),
    twoDigitPad(date.getMinutes()),
    twoDigitPad(date.getSeconds())
  );
}
