import ollama

def main():
    model_name = "hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF" # デフォルトモデル。ユーザーに確認後に変更可能

    while True:
        user_input = input("質問を入力してください ('終了'でプログラムを終了): ")
        if user_input.lower() == '終了':
            break

        # 1. モデルに回答方法を考えさせる
        thinking_prompt = f"質問: {user_input}\n\nこの質問に対する回答を生成するためのステップを考えてください。こおでは回答生成のステップのみを考え、実際に回答する必要はありません。"
        thinking_response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': thinking_prompt}], stream=True)
        print("\n思考プロセス:")
        thinking_result = ""
        for part in thinking_response:
            thinking_result += part['message']['content']
            print(part['message']['content'], end="", flush=True)
        print("\n")

        # 2. 思考結果を用いて回答を生成
        answer_prompt = f"思考プロセス:\n{thinking_result}\n\nユーザーからの質問: {user_input}\n\n上記の思考プロセスに基づいてユーザーに対する質問への回答を生成してください。なお、思考プロセスを再度出力する必要はなく、回答のみを生成してください。"
        answer_response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': answer_prompt}], stream=True)
        print("\n回答:")
        for part in answer_response:
            print(part['message']['content'], end="", flush=True)
        print("\n---")

if __name__ == "__main__":
    main()