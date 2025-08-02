# File: main.py

import os
from workflows.full_build import run_full_pipeline

def save_outputs(output_dict: dict, directory="build"):
    """
    Save each output from the agent pipeline into a .txt file inside the specified directory.
    """
    os.makedirs(directory, exist_ok=True)
    for name, content in output_dict.items():
        file_path = os.path.join(directory, f"{name}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip() if isinstance(content, str) else str(content))

if __name__ == "__main__":
    try:
        requirement = input("\n📌 Enter product requirements: ")
        output = run_full_pipeline(requirement)

        if isinstance(output, dict):
            print("\n🎉 All outputs generated and approved successfully!")
            save_outputs(output)
            print("🗂️ Outputs saved to ./build/ directory.")
            for k, v in output.items():
                print(f"\n=== {k.upper()} ===\n{v}")
        else:
            print(f"\n❌ Process halted: {output}")

    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user.")
    except Exception as e:
        print(f"\n🔥 Unexpected error: {str(e)}")
