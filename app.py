from flask import Flask, render_template, request
from markupsafe import Markup  # Corrected import for Markup
from calculator import perform_addition, perform_subtraction, perform_multiplication, perform_division
from io import StringIO
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_super_secret_key_change_me'


@app.route('/', methods=['GET', 'POST'])
def index():
    # Initial values for the template
    result_dms = None
    paperwork = ""

    if request.method == 'POST':
        # --- 1. Get Input Data ---
        calc_type = request.form.get('calc_type')

        # Angle A (always needed)
        try:
            A_d = int(request.form.get('A_d', 0))
            A_m = int(request.form.get('A_m', 0))
            A_s = int(request.form.get('A_s', 0))

            # Angle B (only for ADD/SUB)
            if calc_type in ['ADD', 'SUB']:
                B_d = int(request.form.get('B_d', 0))
                B_m = int(request.form.get('B_m', 0))
                B_s = int(request.form.get('B_s', 0))
            else:
                B_d, B_m, B_s = 0, 0, 0  # Keep defined, but unused

            # Factor (only for MULT/DIV)
            factor = int(request.form.get('factor', 1))

        except ValueError:
            return render_template('index.html', result="Error: Please enter valid integer numbers for all fields.",
                                   paperwork="")

        # --- 2. Perform Calculation and Capture Paperwork ---
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        try:
            R_d, R_m, R_s = 0, 0, 0

            if calc_type == 'ADD':
                R_d, R_m, R_s = perform_addition(A_d, A_m, A_s, B_d, B_m, B_s)
                result_dms = f"Result (ADD): **{R_d:02d}:{R_m:02d}:{R_s:02d}**"

            elif calc_type == 'SUB':
                R_d, R_m, R_s = perform_subtraction(A_d, A_m, A_s, B_d, B_m, B_s)
                # Subtraction returns the sign in R_d, so we handle the format here:
                sign = "-" if R_d < 0 else ""
                result_dms = f"Result (SUB): **{sign}{abs(R_d):02d}:{R_m:02d}:{R_s:02d}**"

            elif calc_type == 'MULT':
                R_d, R_m, R_s = perform_multiplication(A_d, A_m, A_s, factor)
                result_dms = f"Result (MULT): **{R_d}:{R_m:02d}:{R_s:02d}**"

            elif calc_type == 'DIV':
                R_d, R_m, R_s = perform_division(A_d, A_m, A_s, factor)
                result_dms = f"Result (DIV): {R_d}:{R_m}:{R_s}"

        except ZeroDivisionError:
            result_dms = "Error: Cannot divide by zero factor."
        except Exception as e:
            result_dms = f"An unexpected error occurred: {e}"
        finally:
            sys.stdout = old_stdout  # Restore stdout
            # Convert print output to HTML (newlines to <br>)
            paperwork = redirected_output.getvalue().replace('\n', '<br>')

            # Render the template with the calculation results
    return render_template('index.html', result=result_dms, paperwork=Markup(paperwork))


if __name__ == '__main__':
    app.run(debug=True)