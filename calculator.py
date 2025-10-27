import sys


# --- Helper Functions ---

def format_dms(d, m, s, separator=':'):
    """Formats the output string."""
    # Ensure components are non-negative for display, degrees carries the sign if any.
    return f"{d:02}{separator}{m:02}{separator}{s:02}"


def get_angle_input(prompt):
    """Gets D:M:S input from the user."""
    print(prompt)
    try:
        # Use an internal list for easy checking and unpacking
        d = int(input("  Degrees (D): "))
        m = int(input("  Minutes (M): "))
        s = int(input("  Seconds (S): "))
        return d, m, s
    except ValueError:
        print("\nError: Please enter only integer values.")
        # Re-raise or exit is usually better in production, but we'll return to the main loop here
        # For simplicity in a single-file script, exiting is fine if input is critical.
        sys.exit()


# --- Core Calculation Functions with Paperwork Display ---

def perform_addition(A_d, A_m, A_s, B_d, B_m, B_s):
    print("\n--- ADDITION: Paper-and-Pen Steps ---")

    # 1. Component Addition
    R_s = A_s + B_s
    R_m = A_m + B_m
    R_d = A_d + B_d

    print("      D     M     S")
    print(f"    {A_d:02} : {A_m:02} : {A_s:02}")
    print(f"  + {B_d:02} : {B_m:02} : {B_s:02}")
    print("  -------------------")
    print(f"  = {R_d:02} : {R_m:02} : {R_s:02} (Initial Sum)")

    # 2. Normalize Seconds (Carry to Minutes)
    s_carry = R_s // 60
    R_s_norm = R_s % 60
    R_m_temp = R_m + s_carry

    if s_carry > 0:
        print("\n--- Carry Seconds (S -> M) ---")
        print(f"  * {R_s}'' is {s_carry}' and {R_s_norm}''")
        print(f"  * Carry {s_carry} to Minutes (New M: {R_m_temp})")
        R_m = R_m_temp

    # 3. Normalize Minutes (Carry to Degrees)
    m_carry = R_m // 60
    R_m_norm = R_m % 60
    R_d_final = R_d + m_carry

    if m_carry > 0:
        print("\n--- Carry Minutes (M -> D) ---")
        print(f"  * {R_m}' is {m_carry}° and {R_m_norm}'")
        print(f"  * Carry {m_carry} to Degrees (Final D: {R_d_final})")

    print("\n-----------------------------")
    print(f"  Final Normalized Result:")
    print(f"  = {R_d_final:02} : {R_m_norm:02} : {R_s_norm:02}")

    return R_d_final, R_m_norm, R_s_norm


def perform_subtraction(A_d, A_m, A_s, B_d, B_m, B_s):
    print("\n--- SUBTRACTION: Paper-and-Pen Steps (Borrowing) ---")

    A_sec = (A_d * 3600) + (A_m * 60) + A_s
    B_sec = (B_d * 3600) + (B_m * 60) + B_s
    final_sign = 1

    # If B is larger, swap for positive borrowing/display, and apply sign later
    if A_sec < B_sec:
        # Swap the angle components for internal calculation
        A_d, B_d = B_d, A_d
        A_m, B_m = B_m, A_m
        A_s, B_s = B_s, A_s
        final_sign = -1
        print("Note: Angles swapped to perform (Larger - Smaller). Final result will be negative.")

    # Start D:M:S Subtraction (Borrowing)
    A_m_borrow = A_m
    A_d_borrow = A_d

    print("      D     M     S")
    print(f"    {A_d:02} : {A_m:02} : {A_s:02}")
    print(f"  - {B_d:02} : {B_m:02} : {B_s:02}")
    print("  -------------------")

    # 1. Seconds Subtraction (Borrow from Minutes if needed)
    R_s = A_s - B_s
    if R_s < 0:
        A_m_borrow -= 1
        R_s += 60
        print(f"  * Borrow 1' from Minutes: {A_m}' -> {A_m_borrow}' and add 60'' to Seconds.")

    # 2. Minutes Subtraction (Borrow from Degrees if needed)
    R_m = A_m_borrow - B_m
    if R_m < 0:
        A_d_borrow -= 1
        R_m += 60
        print(f"  * Borrow 1° from Degrees: {A_d_borrow + 1}° -> {A_d_borrow}° and add 60' to Minutes.")

    # 3. Degrees Subtraction
    R_d = A_d_borrow - B_d

    print("\n  Final Subtraction of components:")
    print(f"  = {R_d:02} : {R_m:02} : {R_s:02}")

    R_d_final = R_d * final_sign

    return R_d_final, R_m, R_s


def perform_multiplication(A_d, A_m, A_s, factor):
    print("\n--- MULTIPLICATION: Paper-and-Pen Steps (Component Multiplication & Carry) ---")

    # 1. Simple Component Multiplication
    mult_s = A_s * factor
    mult_m = A_m * factor
    mult_d = A_d * factor

    print(f"  {A_d:02} : {A_m:02} : {A_s:02}")
    print(f"  x {factor}")
    print("  -------------------")
    print(f"  {mult_d:04} : {mult_m:04} : {mult_s:04} (Initial Product)")  # Use mult_d for initial display

    # 2. Normalize Seconds (Carry to Minutes)
    s_carry = mult_s // 60
    R_s_norm = mult_s % 60
    R_m_temp = mult_m + s_carry

    if s_carry > 0:
        print("\n--- Carry Seconds (S -> M) ---")
        print(f"  * {mult_s}'' is {s_carry}' and {R_s_norm}''")
        print(f"  * Carry {s_carry} to Minutes.")
        R_m = R_m_temp
    else:
        R_m = mult_m

    # 3. Normalize Minutes (Carry to Degrees)
    m_carry = R_m // 60
    R_m_norm = R_m % 60
    R_d_final = mult_d + m_carry

    if m_carry > 0:
        print("\n--- Carry Minutes (M -> D) ---")
        print(f"  * {R_m}' is {m_carry}° and {R_m_norm}'")
        print(f"  * Carry {m_carry} to Degrees.")

    # 4. Final output style to match the paper
    print("\n")
    print(f"= {R_d_final} : {R_m_norm:02} : {R_s_norm:02} = Answer")

    return R_d_final, R_m_norm, R_s_norm


def perform_division(A_d, A_m, A_s, factor):
    """
    Performs D:M:S long division, replicating the multi-step, manual
    paperwork style shown in the provided image using dynamic quotient components.
    """

    # --- Pre-Calculation (Ensuring correct final result) ---
    sign = 1
    if A_d < 0:
        sign = -1
        A_d = abs(A_d)
        print(f"Note: Input degree was negative. Result will be negative.")

    # 1. Degrees Division
    Q_d = A_d // factor
    R_d = A_d % factor
    R_d_to_m = R_d * 60
    D_d_sub = Q_d * factor

    # 2. Minutes Division
    D_m = R_d_to_m + A_m
    Q_m = D_m // factor
    R_m = D_m % factor
    R_m_to_s = R_m * 60

    # 3. Seconds Division
    D_s = R_m_to_s + A_s
    Q_s = D_s // factor
    R_s = D_s % factor

    # --- Dynamic Calculation for Minutes Subtraction Printout ---

    # Q_m = 49. We need to break this into Q_m_p1 = 40 and Q_m_p2 = 9.
    Q_m_p1_digit = Q_m // 10  # The '4' in 49
    Q_m_p2_digit = Q_m % 10  # The '9' in 49

    # FIX: The first subtraction is Q_m_p1_digit * factor (4 * 25 = 100)
    # The alignment in the image handles the magnitude implicitly.
    D_m_sub_p1_print = Q_m_p1_digit * factor  # 4 * 25 = 100
    D_m_sub_p1_value = D_m_sub_p1_print * 10  # 100 * 10 = 1000 (The actual value being subtracted)

    D_m_sub_p2 = Q_m_p2_digit * factor  # 9 * 25 = 225

    # --- Dynamic Calculation for Seconds Subtraction Printout ---
    Q_s_p1_digit = Q_s // 10  # 3
    Q_s_p2_digit = Q_s % 10  # 6

    D_s_sub_p1_print = Q_s_p1_digit * factor  # 3 * 25 = 75
    D_s_sub_p1_value = D_s_sub_p1_print * 10  # 750 (The actual value being subtracted)

    D_s_sub_p2_print = Q_s_p2_digit * factor  # 6 * 25 = 150

    R_s_p1_print = D_s - D_s_sub_p1_value  # 912 - 750 = 162

    # --- Paperwork Display (Matching Image Alignment and Steps) ---
    print("\n--- DIVISION: Long Division Paperwork ---")

    # Output: 25) 120 : 40 : 12 [4-49-36
    print(f" {factor}) {A_d} : {A_m} : {A_s} [{Q_d}-{Q_m}-{Q_s}")

    # --- Degrees Division ---
    # Output: -100
    print(f"   - {D_d_sub} ")
    print("  ----------------- ")

    # Output: 20x60 -> convert to minute
    print(f"      {R_d} x 60")

    # --- Minutes Division Setup ---
    # Output: 1200+40 -> Add Minutes [In Dividend]
    print(f"      {R_d_to_m} + {A_m}")

    # Output: 1240
    print("    -----------------")
    print(f"      {D_m}")

    # --- Minutes Division (Two-Step Subtraction) ---

    # Step 1: Subtract the first large part (100 in the printout)
    # This comes from the '4' of the 49 quotient: 4 * 25 = 100.
    print(f"    - {D_m_sub_p1_print}")  # DYNAMIC: 4 * 25 = 100
    print("    -----------------------")

    # Output: 240 (Intermediate Remainder)
    R_m_temp_print = D_m - D_m_sub_p1_value  # 1240 - 1000 = 240
    print(f"     {R_m_temp_print}")

    # Step 2: Subtract the remainder part (225)
    print(f"   - {D_m_sub_p2}")  # DYNAMIC: 9 * 25 = 225
    print("    -----------------")

    # Output: 15 (Final Minute Remainder)
    print(f"      {R_m}")
    print(f"      {R_m} x 60")

    # --- Seconds Division Setup ---
    # Output: 900+12 = 912
    print("    --------------------")
    print(f"      {R_m_to_s} + {A_s} = {D_s}")

    # Line 1: D_s (912)
    print(f"      {D_s}")

    # Line 2: -75 (3 * 25)
    print(f"    - {D_s_sub_p1_print}")
    print("   --------------------")

    # Line 3: 162 (R_s_p1_print)
    print(f"      {R_s_p1_print}")

    # Line 4: -150 (6 * 25)
    print(f"    - {D_s_sub_p2_print}")
    print("  -----------------")

    # Line 5: 12 (final remainder)
    print(f"      {R_s}")
    print("   **********************************************************")

    # Final Result is returned
    return Q_d * sign, Q_m, Q_s

# --- Main Logic Loop ---

def main():
    while True:
        print("\n" + "=" * 60)
        print("D:M:S Angle Calculator (Degrees:Minutes:Seconds)")
        print("=" * 60)

        # Get calculation choice
        calc_type = ""
        while calc_type not in ['ADD', 'SUB', 'MULT', 'DIV', 'EXIT']:
            calc_type = input("Enter calculation type (ADD, SUB, MULT, DIV) or EXIT: ").upper()
            if calc_type == 'EXIT':
                print("Exiting calculator. Goodbye! 👋")
                sys.exit()
            if calc_type not in ['ADD', 'SUB', 'MULT', 'DIV']:
                print("Invalid choice. Please enter ADD, SUB, MULT, DIV, or EXIT.")

        # Get Angle A
        A_d, A_m, A_s = get_angle_input("\n--- Input Angle A (First Angle) ---")

        # Perform Calculation
        R_d, R_m, R_s = 0, 0, 0

        if calc_type in ['ADD', 'SUB']:
            B_d, B_m, B_s = get_angle_input("\n--- Input Angle B (Second Angle) ---")
            if calc_type == 'ADD':
                R_d, R_m, R_s = perform_addition(A_d, A_m, A_s, B_d, B_m, B_s)
            elif calc_type == 'SUB':
                R_d, R_m, R_s = perform_subtraction(A_d, A_m, A_s, B_d, B_m, B_s)

        elif calc_type in ['MULT', 'DIV']:
            try:
                factor = int(input("\n--- Input Factor (Multiplier/Divisor) ---\nEnter a simple integer factor: "))
            except ValueError:
                print("\nError: Please enter only an integer for the factor.")
                continue

            if calc_type == 'MULT':
                R_d, R_m, R_s = perform_multiplication(A_d, A_m, A_s, factor)
            elif calc_type == 'DIV':
                R_d, R_m, R_s = perform_division(A_d, A_m, A_s, factor)

        # Print Final Result
        print("\n" + "=" * 60)

        # Match the "ans -- D : M : S" style for Division
        if calc_type == 'DIV':
            print(f"ans -- {R_d} : {R_m} : {R_s}")
        # Match the "Result (TYPE): **D:M:S**" for other operations
        else:
            print("FINAL ANSWER")
            print(f"Result ({calc_type}): {format_dms(R_d, R_m, R_s)}")

        print("=" * 60)


if __name__ == "__main__":
    main()