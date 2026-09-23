import math
import tkinter as tk


# ---------------------------------------------------------------------------
# Core calculation logic
# ---------------------------------------------------------------------------

def fmt(value):
    """Format a numeric result: show as int when it is a whole number."""
    return str(int(value)) if isinstance(value, float) and value == int(value) else str(value)


def calculate(a, op, b):
    """Perform the arithmetic operation and return the result as a string."""
    if op == "+":
        return fmt(a + b)
    elif op == "-":
        return fmt(a - b)
    elif op == "*":
        return fmt(a * b)
    elif op == "/":
        if b == 0:
            return "Error: Div by zero"
        return fmt(a / b)
    elif op == "**":
        return fmt(math.pow(a, b))
    return "Error: Unknown op"


# ---------------------------------------------------------------------------
# GUI calculator
# ---------------------------------------------------------------------------

def main():
    # --- State variables ---
    # first_number: the operand saved when an operator button is pressed
    # operator:     the operator chosen (+, -, *, /)
    # reset_next:   when True the next digit clears the display first
    first_number = [None]
    operator     = [None]
    reset_next   = [False]

    # --- Window ---
    window = tk.Tk()
    window.resizable(True, True)
    window.minsize(380, 560)
    window.configure(bg="#1e1e2e")

    # Make all 4 columns and every button row stretch with the window
    for col in range(4):
        window.columnconfigure(col, weight=1)
    for row in range(10):         # rows 0-9
        window.rowconfigure(row, weight=1 if row > 0 else 0)

    # --- Display ---
    display_var = tk.StringVar(value="0")
    display = tk.Entry(
        window,
        textvariable=display_var,
        font=("Helvetica", 32, "bold"),
        justify="right",
        state="readonly",
        readonlybackground="#2d2d44",
        fg="#ffffff",
        insertbackground="#ffffff",
        bd=0,
        relief="flat",
    )
    display.grid(row=0, column=0, columnspan=4,
                 padx=12, pady=(14, 6), sticky="nsew", ipady=18)

    # --- Callbacks ---

    def press_digit(digit):
        current = display_var.get()
        if reset_next[0]:
            current = "0"
            reset_next[0] = False
        if current == "0" and digit != ".":
            display_var.set(digit)
        else:
            if digit == "." and "." in current:
                return
            display_var.set(current + digit)

    def press_operator(op):
        first_number[0] = float(display_var.get())
        operator[0]     = op
        reset_next[0]   = True

    def press_equals():
        if first_number[0] is None or operator[0] is None:
            return
        try:
            second = float(display_var.get())
        except ValueError:
            display_var.set("Error")
            return
        display_var.set(calculate(first_number[0], operator[0], second))
        first_number[0] = None
        operator[0]     = None
        reset_next[0]   = True

    def press_sqrt():
        """Calculate the square root of the currently displayed number."""
        try:
            value = float(display_var.get())
        except ValueError:
            display_var.set("Error")
            return
        if value < 0:
            display_var.set("Error: Negative √")
            return
        display_var.set(fmt(math.sqrt(value)))
        reset_next[0] = True  # next digit starts a fresh number

    def press_trig(fn):
        """Apply a trig function (sin/cos/tan) to the displayed value in degrees."""
        try:
            value = float(display_var.get())
        except ValueError:
            display_var.set("Error")
            return
        radians = math.radians(value)   # convert degrees → radians
        display_var.set(fmt(fn(radians)))
        reset_next[0] = True  # next digit starts a fresh number

    def press_square():
        """Square the number currently displayed."""
        try:
            value = float(display_var.get())
        except ValueError:
            display_var.set("Error")
            return
        display_var.set(fmt(value ** 2))
        reset_next[0] = True  # next digit starts a fresh number

    def press_reciprocal():
        """Calculate 1/x for the number currently displayed."""
        try:
            value = float(display_var.get())
        except ValueError:
            display_var.set("Error")
            return
        if value == 0:
            display_var.set("Error: Div by zero")
            return
        display_var.set(fmt(1 / value))
        reset_next[0] = True  # next digit starts a fresh number

    def press_pi():
        """Insert the value of π into the display."""
        display_var.set(fmt(math.pi))
        reset_next[0] = True  # next digit starts a fresh number

    def press_clear():
        display_var.set("0")
        first_number[0] = None
        operator[0]     = None
        reset_next[0]   = False

    # -----------------------------------------------------------------------
    # Colour palette
    # -----------------------------------------------------------------------
    CLR_BG       = "#1e1e2e"   # window background
    CLR_DIGIT    = "#313149"   # digit button face
    CLR_DIGIT_H  = "#44446a"   # digit hover / active
    CLR_OP       = "#f0a500"   # operator button face  (+  -  *  /  =)
    CLR_OP_H     = "#d4941e"   # operator active
    CLR_SCI      = "#2e4a6e"   # scientific button face
    CLR_SCI_H    = "#3d6494"   # scientific active
    CLR_CLEAR    = "#8b1a1a"   # clear button face
    CLR_CLEAR_H  = "#b22222"   # clear active
    FG           = "#ffffff"   # all button text

    OPERATORS = {"+", "-", "*", "/", "="}
    SCI_LABELS = {"√", "x²", "xʸ", "sin", "cos", "tan", "π", "1/x"}

    def make_btn(parent, label, cmd, colspan=1, bg=None, bg_h=None):
        """Create and return a styled Button — does NOT call .grid()."""
        if bg is None:
            if label == "C":
                bg, bg_h = CLR_CLEAR, CLR_CLEAR_H
            elif label in OPERATORS:
                bg, bg_h = CLR_OP, CLR_OP_H
            elif label in SCI_LABELS:
                bg, bg_h = CLR_SCI, CLR_SCI_H
            else:
                bg, bg_h = CLR_DIGIT, CLR_DIGIT_H

        btn = tk.Button(
            parent,
            text=label,
            font=("Helvetica", 16, "bold"),
            fg=FG,
            bg=bg,
            activebackground=bg_h,
            activeforeground=FG,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=cmd,
        )
        return btn

    # -----------------------------------------------------------------------
    # Row 1 – Scientific functions  (4 columns)
    # -----------------------------------------------------------------------
    sci_buttons = [
        ("√",   press_sqrt),
        ("x²",  press_square),
        ("xʸ",  lambda: press_operator("**")),
        ("π",   press_pi),
        ("sin", lambda: press_trig(math.sin)),
        ("cos", lambda: press_trig(math.cos)),
        ("tan", lambda: press_trig(math.tan)),
        ("C",   press_clear),
        ("1/x", press_reciprocal),
    ]

    # Place scientific buttons in rows 1-3 across 4 columns
    # 9 buttons: row1=idx0-3, row2=idx4-7, row3=idx8 (col0 only)
    for idx, (label, cmd) in enumerate(sci_buttons):
        r = 1 + idx // 4
        c = idx % 4
        btn = make_btn(window, label, cmd)
        btn.grid(row=r, column=c, padx=5, pady=4, sticky="nsew", ipady=10)

    # Separator lives at row 4 – safely below all 3 scientific rows
    sep = tk.Label(window, bg="#44445a", text="", height=1)
    sep.grid(row=4, column=0, columnspan=4, sticky="ew", padx=8, pady=4)

    # -----------------------------------------------------------------------
    # Rows 5-8 – Main keypad
    # -----------------------------------------------------------------------
    main_buttons = [
        # row 5
        ("7", lambda: press_digit("7")),
        ("8", lambda: press_digit("8")),
        ("9", lambda: press_digit("9")),
        ("/", lambda: press_operator("/")),
        # row 6
        ("4", lambda: press_digit("4")),
        ("5", lambda: press_digit("5")),
        ("6", lambda: press_digit("6")),
        ("*", lambda: press_operator("*")),
        # row 7
        ("1", lambda: press_digit("1")),
        ("2", lambda: press_digit("2")),
        ("3", lambda: press_digit("3")),
        ("-", lambda: press_operator("-")),
        # row 8
        ("0", lambda: press_digit("0")),
        (".", lambda: press_digit(".")),
        ("=", press_equals),
        ("+", lambda: press_operator("+")),
    ]

    for idx, (label, cmd) in enumerate(main_buttons):
        r = 5 + idx // 4
        c = idx % 4
        btn = make_btn(window, label, cmd)
        btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew", ipady=14)

    window.mainloop()


if __name__ == "__main__":
    main()
