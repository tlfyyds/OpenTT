import customtkinter as ctk
import threading
from ollamaka.ollamaka import AIClient

def run_app():
    client = AIClient()
    ctk.set_appearance_mode("Dark")
    app = ctk.CTk()
    app.title("AI Desktop Multi-Engine")
    app.geometry("500x800")

    # --- UI 布局 ---
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    # 顶部设置栏
    top_frame = ctk.CTkFrame(app, fg_color="transparent")
    top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    label = ctk.CTkLabel(top_frame, text=f"当前模型: {client.config['model']}", font=("Arial", 12))
    label.pack(side="left", padx=5)

    # --- 设置弹窗逻辑 ---
    def open_settings():
        settings = ctk.CTkToplevel(app)
        settings.title("API 设置")
        settings.geometry("400x350")
        settings.attributes("-topmost", True)

        ctk.CTkLabel(settings, text="Base URL:").pack(pady=(10,0))
        url_entry = ctk.CTkEntry(settings, width=300)
        url_entry.insert(0, client.config['base_url'])
        url_entry.pack(pady=5)

        ctk.CTkLabel(settings, text="API Key:").pack(pady=(10,0))
        key_entry = ctk.CTkEntry(settings, width=300, show="*")
        key_entry.insert(0, client.config['api_key'])
        key_entry.pack(pady=5)

        ctk.CTkLabel(settings, text="Model Name:").pack(pady=(10,0))
        mod_entry = ctk.CTkEntry(settings, width=300)
        mod_entry.insert(0, client.config['model'])
        mod_entry.pack(pady=5)

        def save():
            client.save_config(key_entry.get(), url_entry.get(), mod_entry.get())
            label.configure(text=f"当前模型: {client.config['model']}")
            settings.destroy()

        ctk.CTkButton(settings, text="保存配置", command=save).pack(pady=20)

    setting_btn = ctk.CTkButton(top_frame, text="⚙️ 设置", width=60, command=open_settings)
    setting_btn.pack(side="right", padx=5)

    # 对话框
    display_box = ctk.CTkTextbox(app, wrap="word")
    display_box.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
    display_box.configure(state="disabled")

    def update_display(text):
        display_box.configure(state="normal")
        display_box.insert("end", text)
        display_box.configure(state="disabled")
        display_box.yview("end")

    # 输入框
    input_entry = ctk.CTkEntry(app, placeholder_text="输入指令...", height=40)
    input_entry.grid(row=2, column=0, padx=15, pady=20, sticky="ew")

    def handle_send():
        text = input_entry.get()
        if not text: return
        input_entry.delete(0, "end")
        update_display(f"【你】: {text}\n")
        
        def run():
            res = client.chat(text, status_callback=lambda s: app.after(0, lambda: update_display(f"  > {s}\n")))
            app.after(0, lambda: update_display(f"【AI】: {res}\n\n" + "-"*30 + "\n"))
        
        threading.Thread(target=run, daemon=True).start()

    input_entry.bind("<Return>", lambda e: handle_send())

    app.mainloop()

if __name__ == "__main__":
    run_app()