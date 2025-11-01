import os
import subprocess
import base64
from io import BytesIO
import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk

def generar_qr():
    mensaje = entry_text.get("1.0", tk.END).strip()
    if not mensaje:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un texto para generar el QR.")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(mensaje)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Guardar QR como"
    )
    if save_path:
        img.save(save_path)
        messagebox.showinfo("Éxito", f"El QR se ha guardado como PNG en:\n{save_path}")
    else:
        messagebox.showwarning("Cancelado", "No se guardó el QR.")

def generar_qr_desde_imagen():
    file_path = filedialog.askopenfilename(
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")],
        title="Seleccionar imagen"
    )

    if not file_path:
        return

    img = Image.open(file_path)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    tamanio_kb = len(buffer.getvalue()) / 1024

    if tamanio_kb > 300:
        if messagebox.askyesno("Imagen grande", f"La imagen pesa {tamanio_kb:.1f} KB.\n¿Reducirla para que funcione?"):
            img.thumbnail((400, 400))
        else:
            messagebox.showwarning("Cancelado", "La imagen es demasiado grande para usar en un QR.")
            return

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode()

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(base64_img)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Guardar QR desde imagen"
    )
    if save_path:
        img_qr.save(save_path)
        messagebox.showinfo("Éxito", f"QR generado desde imagen guardado en:\n{save_path}")

def actualizar_programa():
    try:
        if os.name == 'nt':
            exe_path = os.path.abspath(__file__)
            update_script = os.path.join(os.path.dirname(exe_path), "update.bat")
            subprocess.run([update_script], check=True)
        else:
            result = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
            if "Already up to date." in result.stdout:
                messagebox.showinfo("Actualización", "El programa ya está actualizado.")
            else:
                messagebox.showinfo("Actualización", "Se actualizó correctamente. Reinicia para aplicar cambios.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el programa.\n{e}")

def cambiar_idioma(idioma):
    textos = {
        "es": {
            "title": "Generador de QR",
            "generate": "🖋 Generar QR",
            "imageqr": "🖼 Imagen → QR",
            "update": "🔍 Buscar Actualizaciones",
            "exit": "⛔ Salir",
        },
        "en": {
            "title": "QR Generator",
            "generate": "🖋 Generate QR",
            "imageqr": "🖼 Image → QR",
            "update": "🔍 Check for Updates",
            "exit": "⛔ Exit",
        }
    }

    lang = textos.get(idioma, textos["es"])
    root.title(lang["title"])
    label_title.config(text=lang["title"])
    btn_generate.config(text=lang["generate"])
    btn_image_qr.config(text=lang["imageqr"])
    btn_update.config(text=lang["update"])
    btn_exit.config(text=lang["exit"])

# GUI
root = tk.Tk()
root.title("ShadowCrypt-Security")
root.geometry("800x600")
root.resizable(False, False)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

menu_language = tk.Menu(menu_bar, tearoff=0)
menu_language.add_command(label="Español", command=lambda: cambiar_idioma("es"))
menu_language.add_command(label="English", command=lambda: cambiar_idioma("en"))
menu_bar.add_cascade(label="Idioma", menu=menu_language)

label_title = tk.Label(root, text="Generador de QR", font=("Arial", 35, "bold"), fg="blue")
label_title.pack(pady=10)

frame_text = tk.Frame(root)
frame_text.pack(pady=20)

scrollbar = tk.Scrollbar(frame_text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

entry_text = tk.Text(frame_text, height=15, width=70, wrap=tk.WORD, yscrollcommand=scrollbar.set)
entry_text.pack()

scrollbar.config(command=entry_text.yview)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20)

btn_generate = tk.Button(frame_buttons, text="🖋 Generar QR", font=("Arial", 12), bg="green", fg="white", command=generar_qr)
btn_generate.grid(row=0, column=0, padx=10)

btn_image_qr = tk.Button(frame_buttons, text="🖼 Imagen → QR", font=("Arial", 12), bg="blue", fg="white", command=generar_qr_desde_imagen)
btn_image_qr.grid(row=0, column=1, padx=10)

btn_update = tk.Button(frame_buttons, text="🔍 Buscar Actualizaciones", font=("Arial", 12), bg="orange", fg="white", command=actualizar_programa)
btn_update.grid(row=1, column=0, padx=10, pady=10)

btn_exit = tk.Button(frame_buttons, text="⛔ Salir", font=("Arial", 12), bg="red", fg="white", command=root.quit)
btn_exit.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
