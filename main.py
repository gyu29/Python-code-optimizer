import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import ast
import astor
import subprocess
import sys
import io
import contextlib
from PIL import Image, ImageTk
import customtkinter as ctk

class CodeOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.load_config()
        self.setup_ui()

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "config.json file not found!")
            sys.exit(1)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def setup_ui(self):
        self.root.title("Code Optimizer")
        self.root.geometry(self.config["window_size"])
        try:
            logo_image = Image.open("assets/logo.png")
            logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
            self.logo = ImageTk.PhotoImage(logo_image)
            self.logo_label = ctk.CTkLabel(self.root, image=self.logo, text="")
            self.logo_label.pack(pady=10)
        except FileNotFoundError:
            self.logo_label = ctk.CTkLabel(self.root, text="Code Optimizer", font=("Helvetica", 20))
            self.logo_label.pack(pady=10)
        self.input_label = ctk.CTkLabel(self.root, text="Input Your Code Here:")
        self.input_label.pack(pady=10)
        self.input_code = scrolledtext.ScrolledText(self.root, width=120, height=20, wrap=tk.WORD)
        self.input_code.pack(padx=10, pady=10)
        self.test_case_label = ctk.CTkLabel(self.root, text="Input Test Cases (One per line):")
        self.test_case_label.pack(pady=10)
        self.test_cases = scrolledtext.ScrolledText(self.root, width=120, height=10, wrap=tk.WORD)
        self.test_cases.insert(tk.END, "\n".join(self.config["default_test_cases"]))
        self.test_cases.pack(padx=10, pady=10)
        try:
            optimize_icon = Image.open("assets/optimize_icon.png")
            optimize_icon = optimize_icon.resize((20, 20), Image.ANTIALIAS)
            self.optimize_icon = ImageTk.PhotoImage(optimize_icon)
        except FileNotFoundError:
            self.optimize_icon = None
        self.optimize_button = ctk.CTkButton(
            self.root,
            text="Optimize and Verify Code",
            image=self.optimize_icon,
            compound="left",
            command=self.optimize_and_verify,
        )
        self.optimize_button.pack(pady=10)
        self.output_label = ctk.CTkLabel(self.root, text="Optimized Code:")
        self.output_label.pack(pady=10)
        self.output_code = scrolledtext.ScrolledText(self.root, width=120, height=20, wrap=tk.WORD, state="disabled")
        self.output_code.pack(padx=10, pady=10)
        self.suggestions_label = ctk.CTkLabel(self.root, text="Optimization Suggestions:")
        self.suggestions_label.pack(pady=10)
        self.suggestions = scrolledtext.ScrolledText(self.root, width=120, height=10, wrap=tk.WORD, state="disabled")
        self.suggestions.pack(padx=10, pady=10)
        self.test_results_label = ctk.CTkLabel(self.root, text="Test Case Results:")
        self.test_results_label.pack(pady=10)
        self.test_results = scrolledtext.ScrolledText(self.root, width=120, height=10, wrap=tk.WORD, state="disabled")
        self.test_results.pack(padx=10, pady=10)

    def optimize_and_verify(self):
        code = self.input_code.get("1.0", tk.END)
        test_cases = self.test_cases.get("1.0", tk.END).strip().split("\n")
        try:
            parsed_code = ast.parse(code)
            optimized_code, suggestions = self.analyze_and_optimize(parsed_code)
            self.output_code.config(state="normal")
            self.output_code.delete("1.0", tk.END)
            self.output_code.insert(tk.END, optimized_code)
            self.output_code.config(state="disabled")
            self.suggestions.config(state="normal")
            self.suggestions.delete("1.0", tk.END)
            self.suggestions.insert(tk.END, "\n".join(suggestions))
            self.suggestions.config(state="disabled")
            self.test_results.config(state="normal")
            self.test_results.delete("1.0", tk.END)
            for test_case in test_cases:
                if test_case.strip():
                    original_output = self.run_code(code, test_case)
                    optimized_output = self.run_code(optimized_code, test_case)
                    if original_output == optimized_output:
                        self.test_results.insert(tk.END, f"Test Case '{test_case}': PASSED\n")
                    else:
                        self.test_results.insert(tk.END, f"Test Case '{test_case}': FAILED\n")
            self.test_results.config(state="disabled")
        except SyntaxError as e:
            self.output_code.config(state="normal")
            self.output_code.delete("1.0", tk.END)
            self.output_code.insert(tk.END, f"Syntax Error: {e}")
            self.output_code.config(state="disabled")

    def analyze_and_optimize(self, parsed_code):
        suggestions = []
        optimized_code = astor.to_source(parsed_code)
        pylint_output = self.run_pylint(optimized_code)
        if pylint_output:
            suggestions.append("Pylint Suggestions:\n" + pylint_output)
        flake8_output = self.run_flake8(optimized_code)
        if flake8_output:
            suggestions.append("Flake8 Suggestions:\n" + flake8_output)
        optimized_code = self.run_autopep8(optimized_code)
        return optimized_code, suggestions

    def run_pylint(self, code):
        try:
            result = subprocess.run(
                ["pylint", "--from-parseable", "-"],
                input=code,
                text=True,
                capture_output=True,
            )
            return result.stdout
        except Exception as e:
            return f"Error running pylint: {e}"

    def run_flake8(self, code):
        try:
            result = subprocess.run(
                ["flake8", "-"],
                input=code,
                text=True,
                capture_output=True,
            )
            return result.stdout
        except Exception as e:
            return f"Error running flake8: {e}"

    def run_autopep8(self, code):
        try:
            result = subprocess.run(
                ["autopep8", "-"],
                input=code,
                text=True,
                capture_output=True,
            )
            return result.stdout
        except Exception as e:
            return code

    def run_code(self, code, test_case):
        try:
            output_capture = io.StringIO()
            with contextlib.redirect_stdout(output_capture):
                exec_globals = {}
                exec_locals = {}
                exec(code, exec_globals, exec_locals)
                if "solution" in exec_locals:
                    result = exec_locals["solution"](*eval(test_case))
                    print(result)
                else:
                    print("Error: 'solution' function not found in code.")
            return output_capture.getvalue().strip()
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    root = ctk.CTk()
    app = CodeOptimizerApp(root)
    root.mainloop()
