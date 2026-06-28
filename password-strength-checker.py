#!/usr/bin/env python3

import string
import random
import math
from datetime import datetime
from getpass import getpass

# Common weak passwords
COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty",
    "abc123", "admin", "welcome", "password123",
    "letmein", "football"
}

# -------------------------
# Password Checks
# -------------------------

def has_upper(password):
    return any(c.isupper() for c in password)


def has_lower(password):
    return any(c.islower() for c in password)


def has_digit(password):
    return any(c.isdigit() for c in password)


def has_symbol(password):
    return any(c in string.punctuation for c in password)


def repeated(password):
    return len(set(password)) <= 2

# -------------------------
# Entropy Calculation
# -------------------------

def calculate_entropy(password):

    charset = 0

    if has_lower(password):
        charset += 26
    if has_upper(password):
        charset += 26
    if has_digit(password):
        charset += 10
    if has_symbol(password):
        charset += len(string.punctuation)

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

# -------------------------
# Password Generator
# -------------------------

def generate_password(length=14):

    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))

        if (
            has_upper(password)
            and has_lower(password)
            and has_digit(password)
            and has_symbol(password)
        ):
            return password

# -------------------------
# Logger
# -------------------------

def log_result(strength, score):

    with open("password_log.txt", "a") as file:
        file.write(
            f"{datetime.now()} | Strength: {strength} | Score: {score}/100\n"
        )

# -------------------------
# Evaluation
# -------------------------

def evaluate(password):

    score = 0
    feedback = []

    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    else:
        feedback.append("Use at least 8 characters.")

    if has_upper(password):
        score += 15
    else:
        feedback.append("Add uppercase letters.")

    if has_lower(password):
        score += 15
    else:
        feedback.append("Add lowercase letters.")

    if has_digit(password):
        score += 15
    else:
        feedback.append("Add numbers.")

    if has_symbol(password):
        score += 20
    else:
        feedback.append("Add special characters.")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        feedback.append("This is a commonly used password.")

    if repeated(password):
        score -= 15
        feedback.append("Avoid repeated characters.")

    if " " in password:
        score -= 10
        feedback.append("Avoid spaces.")

    score = max(0, min(score, 100))

    if score < 40:
        strength = "Weak"
    elif score < 70:
        strength = "Medium"
    elif score < 90:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return score, strength, feedback

# -------------------------
# Main Program
# -------------------------

print("=" * 60)
print("         PASSWORD STRENGTH CHECKER")
print("=" * 60)

password = getpass("Enter your password: ")

score, strength, feedback = evaluate(password)
entropy = calculate_entropy(password)

log_result(strength, score)

print("\nPassword Strength :", strength)
print("Password Score    :", score, "/100")
print("Entropy           :", entropy, "bits")

if feedback:
    print("\nSuggestions:")
    for item in feedback:
        print("-", item)
else:
    print("\nExcellent password!")

if strength == "Weak":
    print("\nSuggested Strong Password:")
    print(generate_password())

print("\nResults saved in password_log.txt")
