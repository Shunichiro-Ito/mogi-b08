import os

# スクリプトの絶対パスを取得
script_path = os.path.abspath(__file__)

# スクリプトがあるディレクトリを取得
script_dir = os.path.dirname(script_path)

print("Script Path:", script_path)
print("Script Directory:", script_dir)