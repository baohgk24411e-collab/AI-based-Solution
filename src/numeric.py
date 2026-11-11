"""Recalculate only explicitly comparable quantities; no inference of denominators."""
import math

DIMENSIONS = ('company','year','material','geography','boundary','measurement_basis')
UNITS = {'kg':1.0, 't':1000.0, 'tonnes':1000.0, 'metric tons':1000.0}

def check_rate(numerator, denominator, reported_percent, tolerance_pp=0.5):
    for field in DIMENSIONS:
        a, b = numerator.get(field), denominator.get(field)
        if a is None or b is None or str(a).strip() == '' or str(b).strip() == '':
            return dict(status='not_comparable', reason=f'Missing {field}')
        if str(a).strip().casefold() != str(b).strip().casefold():
            return dict(status='not_comparable', reason=f'Different {field}')
    if numerator.get('unit') not in UNITS or denominator.get('unit') not in UNITS:
        return dict(status='not_comparable', reason='Unsupported or missing mass unit')
    try:
        n = float(numerator['value'])*UNITS[numerator['unit']]
        d = float(denominator['value'])*UNITS[denominator['unit']]
        r = float(reported_percent)
        if not all(math.isfinite(x) for x in [n,d,r,tolerance_pp]) or n < 0 or d <= 0 or not 0 <= r <= 100 or tolerance_pp < 0:
            raise ValueError()
    except (ValueError, TypeError, KeyError):
        return dict(status='invalid_input', reason='Require finite nonnegative numerator, positive denominator and percentage 0–100')
    calculated = 100*n/d
    delta = r-calculated
    return dict(status='consistent' if abs(delta) <= tolerance_pp else 'potential_inconsistency',
                calculated_percent=round(calculated,6), reported_percent=r,
                difference_percentage_points=round(delta,6), tolerance_pp=tolerance_pp,
                formula=f'{n:g} kg / {d:g} kg × 100',
                reason='Arithmetic check only; source definitions must be reviewed by a person')
