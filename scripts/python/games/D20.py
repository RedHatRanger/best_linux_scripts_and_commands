import random, time, os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# A **sequential set** of frames rolling straight forward (away from player)
ROLL_SEQUENCE = [
"""
        /\\
       /{0:2}\\
      /____\\
      \\    /
       \\  /
        \\/
""",
"""
       .----.
      / {0:2}  \\
     /______\\
     \\      /
      \\ {0:2}  /
       `----`
""",
"""
      _______
     /   {0:2} /\\
    /______/  \\
    \\   {0:2} \\  /
     \\______/ 
""",
"""
       _____
      / {0:2} /\\
     /____/  \\
     \\    \\  /
      \\ {0:2} \\/
       \\_____/
""",
"""
       ____ 
      / {0:2}\\
     /_____\\
     \\     /
      \\{0:2}/
       `-´
""",
"""
       /\\
      /{0:2}\\
      \\__/
"""
]

def animate_d20_roll():
    clear()
    print("🎲 Rolling the D20 away... 🎲\n")

    # Slow down realistically: small -> large delay
    delays = [0.05, 0.07, 0.09, 0.12, 0.16, 0.22, 0.3, 0.4]

    for i, delay in enumerate(delays):
        frame = ROLL_SEQUENCE[i % len(ROLL_SEQUENCE)]
        number = random.randint(1, 20)  # changing visible face
        clear()
        print("🎲 Rolling the D20 away... 🎲\n")
        print(frame.format(number))
        time.sleep(delay)

    # Final result is shown in last (smallest/distant) frame
    result = random.randint(1, 20)
    clear()
    print("🎲 FINAL RESULT 🎲\n")
    print(ROLL_SEQUENCE[-1].format(result))
    print(f"==> {result} <==\n")

    if result == 20:
        print("🎉 CRITICAL HIT! Natural 20! 🎉")
    elif result == 1:
        print("💀 CRITICAL FAIL! Natural 1 💀")
    return result

def main():
    print("ASCII d20: Sequential Straight‑Back Tumbling 🎲\n")
    try:
        while True:
            input("Press Enter to roll...")
            animate_d20_roll()
    except KeyboardInterrupt:
        print("\nThanks for rolling! 🎲")

if __name__ == "__main__":
    main()
