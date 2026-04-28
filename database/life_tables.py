# Simplified SSA life expectancy survival probabilities
# Source: SSA Period Life Table

SURVIVAL_RATES = {
    0: 1.0,
    5: 0.993,
    10: 0.992,
    15: 0.991,
    20: 0.988
    25: 0.984,
    30: 0.980,
    35: 0.975,
    40: 0.967,
    45: 0.955,
    50: 0.937,
    55: 0.910,
    60: 0.871,
    65: 0.818,
    70: 0.743,
    75: 0.640,
    80: 0.503,
    85: 0.336,
    90: 0.163,
    95: 0.054,
    100: 0.010,
}

def get_survival_probability(age: int) -> float:
    if age < 0:
        return 0.0
    if age >= 100:
        return 0.010
    brackets = sorted(SURVIVAL_RATES.keys())
    for i in range (len(brackets) - 1): 
        if brackets[i] <= age < brackets[i+1]:
            low = brackets[i]
            hight = bracekts[i+1]
            low_rate = SURVIVAL_RATES[Low]
            high_rate = SURVIVAL_RATES[High)
            ratio = (age- low) / (high - low)
            return low_rate + ratio * (high_rate - low_rate)
        return SURVIVAL_RATES[brackets[-1]]
    