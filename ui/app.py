import customtkinter as ctk
import threading
from ollamaka.ollamaka import AIClient

def run_app():
    client = AIClient()
    stop_requested = [False] # 使用列表包装，方便在线程间共享状态
    is_running = [False]

    ctk.set_appearance_mode("Dark")
    app = ctk.CTk()
    app.title("AI Desktop Multi-Engine")
    app.geometry("500x850")

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    # --- 顶部状态栏 ---
    top_frame = ctk.CTkFrame(app, fg_color="transparent")
    top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    label = ctk.CTkLabel(top_frame, text=f"模型: {client.config['model']}", font=("Arial", 12))
    label.pack(side="left", padx=5)

    def open_settings():
        settings = ctk.CTkToplevel(app)
        settings.title("API 设置")
        settings.geometry("400x350")
        settings.attributes("-topmost", True)
        settings.grab_set()

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
            label.configure(text=f"模型: {client.config['model']}")
            settings.destroy()

        ctk.CTkButton(settings, text="保存配置", command=save).pack(pady=20)

    setting_btn = ctk.CTkButton(top_frame, text="⚙️ 设置", width=60, command=open_settings)
    setting_btn.pack(side="right", padx=5)

    # --- 对话框 ---
    display_box = ctk.CTkTextbox(app, wrap="word", font=("Microsoft YaHei", 12))
    display_box.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
    display_box.configure(state="disabled")

    def update_display(text):
        display_box.configure(state="normal")
        display_box.insert("end", text)
        display_box.configure(state="disabled")
        display_box.yview("end")

    # --- 底部控制区 ---
    footer_frame = ctk.CTkFrame(app, fg_color="transparent")
    footer_frame.grid(row=2, column=0, padx=15, pady=20, sticky="ew")
    footer_frame.grid_columnconfigure(0, weight=1)

    input_entry = ctk.CTkEntry(footer_frame, placeholder_text="输入指令...", height=45)
    input_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

    # 终止按钮
    stop_btn = ctk.CTkButton(footer_frame, text="🛑 终止", width=80, height=45, fg_color="#A33", hover_color="#C44", state="disabled")
    stop_btn.grid(row=0, column=1)

    def trigger_stop():
        stop_requested[0] = True
        update_display("\n[系统] 正在尝试终止任务...\n")

    stop_btn.configure(command=trigger_stop)

    def handle_send():
        text = input_entry.get()
        if not text or is_running[0]: return
        
        input_entry.delete(0, "end")
        update_display(f"【你】: {text}\n")
        
        # 任务启动状态
        stop_requested[0] = False
        is_running[0] = True
        stop_btn.configure(state="normal")
        
        def run():
            # 核心：将 stop_requested 的状态传递给 chat
            res = client.chat(
                text, 
                status_callback=lambda s: app.after(0, lambda: update_display(f"  > {s}\n")),
                check_stop=lambda: stop_requested[0]
            )
            
            def finalize():
                update_display(f"【AI】: {res}\n\n" + "-"*35 + "\n")
                stop_btn.configure(state="disabled")
                is_running[0] = False
            
            app.after(0, finalize)
        
        threading.Thread(target=run, daemon=True).start()

    input_entry.bind("<Return>", lambda e: handle_send())

    app.mainloop()

if __name__ == "__main__":
    run_app()