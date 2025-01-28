# Code Optimizer

**Code Optimizer** is a Python-based desktop application designed to help programmers optimize their code for efficiency and readability. It integrates tools like `pylint`, `flake8`, and `autopep8` to analyze and improve code quality. Additionally, it allows users to verify the functionality of their code by running it against custom test cases, ensuring that optimizations do not alter the intended behavior. This tool is particularly useful for algorithmic programming, such as solving problems on platforms like LeetCode or Baekjoon.

---

## Features

- **Code Optimization**:
  - Automatically formats code using `autopep8`.
  - Provides static code analysis using `pylint` and `flake8`.
  - Suggests improvements for unused variables, inefficient loops, and more.

- **Test Case Verification**:
  - Allows users to input custom test cases.
  - Compares the output of the original and optimized code to ensure functionality remains unchanged.

- **Modern User Interface**:
  - Built with `customtkinter` for a sleek, modern look.
  - Includes a logo, icons, and customizable themes.

- **Configuration File**:
  - Uses a `config.json` file to store UI themes, fonts, and default test cases.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gyu29/python-code-optimizer
   cd python-code-optimizer
   ```

2. Install dependencies:
   ```bash
   pip install customtkinter pillow
   ```

3. Run the application:
   ```bash
   python main.py
   ```

---

## Usage

1. **Input Your Code**:
   - Paste your Python code into the "Input Your Code Here" section.

2. **Add Test Cases**:
   - Enter test cases (one per line) in the "Input Test Cases" section. For example:
     ```
     1, 2
     3, 4
     5, 6
     ```

3. **Optimize and Verify**:
   - Click the "Optimize and Verify Code" button to analyze and optimize your code.
   - View the optimized code, suggestions, and test case results in their respective sections.

---

## Tools Used

- **Python**: Core programming language.
- **Tkinter/CustomTkinter**: For building the user interface.
- **Pylint**: Static code analysis.
- **Flake8**: Linting tool for style and syntax checks.
- **Autopep8**: Automatic code formatting.
- **Pillow**: For handling images in the UI.

---

## Contributing

Contributions are welcome! If you'd like to improve this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Screenshots

![Screenshot 1](assets/screenshot1.png)  
*Input code and test cases.*

![Screenshot 2](assets/screenshot2.png)  
*Optimized code and suggestions.*

---
