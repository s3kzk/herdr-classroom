// Sunrise and sunset: when the sun's centre is 0.833° below the horizon (the usual
// approximation, as in suncalc). Returns both as ms since the epoch, for the local day.
const RAD = Math.PI / 180, DAY = 86400000, J1970 = 2440588, J2000 = 2451545, J0 = 0.0009;
export function sunTimes(now, lat, lng) {
  const d = Math.round(now / DAY - 0.5 + J1970 - J2000 - J0 + lng / 360);
  const lw = -lng * RAD, phi = lat * RAD;
  const transit = (ht) => J0 + (ht + lw) / (2 * Math.PI) + d;
  const ds = transit(0);
  const M = RAD * (357.5291 + 0.98560028 * ds);
  const L = M + RAD * (1.9148 * Math.sin(M) + 0.02 * Math.sin(2 * M) + 0.0003 * Math.sin(3 * M)) + RAD * 102.9372 + Math.PI;
  const dec = Math.asin(Math.sin(RAD * 23.4397) * Math.sin(L));
  const at = (j) => J2000 + j + 0.0053 * Math.sin(M) - 0.0069 * Math.sin(2 * L);
  const w = Math.acos((Math.sin(-0.833 * RAD) - Math.sin(phi) * Math.sin(dec)) / (Math.cos(phi) * Math.cos(dec)));
  const noon = at(ds), set = at(transit(w));
  const ms = (j) => (j + 0.5 - J1970) * DAY;
  return [ms(noon - (set - noon)), ms(set)];
}
