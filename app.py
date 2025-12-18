"""
Графический интерфейс генератора мелодий на Tkinter.
"""

import shutil
import tempfile
from pathlib import Path
from tkinter import (
    DISABLED,
    END,
    HORIZONTAL,
    NORMAL,
    Button,
    Frame,
    IntVar,
    Label,
    OptionMenu,
    Scale,
    StringVar,
    Text,
    Tk,
    filedialog,
)

from PIL import Image, ImageTk

from src.entities.scale import NOTE_TO_MIDI
from src.entities.scale import Scale as MusicScale
from src.entities.scale import ScaleType
from src.entities.settings import GeneratorSettings
from src.services.exporter import export_to_midi
from src.services.generator import MelodyGenerator
from src.services.player import play_midi
from src.services.visualizer import plot_piano_roll, pretty_print_melody


class MelodyGeneratorApp:
    """Главный класс приложения генератора мелодий."""

    def __init__(self):
        """Инициализация приложения."""
        self.root = Tk()
        self.root.title("Генератор мелодий")
        self.root.geometry("950x700")
        self.root.configure(bg="#1a1a2e")

        # Данные
        self.keys = sorted(set(NOTE_TO_MIDI.keys()))
        self.scales = [s.value for s in ScaleType]
        self.current_midi_path = None
        self.photo_image = None

        # Переменные
        self.key_var = StringVar(value="C")
        self.scale_var = StringVar(value="major")
        self.length_var = IntVar(value=8)
        self.tempo_var = IntVar(value=120)
        self.octave_var = IntVar(value=1)

        self._create_ui()

    def _create_ui(self):
        """Создание пользовательского интерфейса."""
        main_frame = Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title = Label(
            main_frame,
            text="Генератор мелодий",
            font=("Helvetica", 28, "bold"),
            fg="#a78bfa",
            bg="#1a1a2e",
        )
        title.pack(pady=(0, 20))

        # Контент
        content = Frame(main_frame, bg="#1a1a2e")
        content.pack(fill="both", expand=True)

        # Боковая панель
        sidebar = Frame(content, bg="#252538", width=280)
        sidebar.pack(side="left", fill="y", padx=(0, 15))
        sidebar.pack_propagate(False)
        self._create_sidebar(sidebar)

        # Основная область
        main_area = Frame(content, bg="#1a1a2e")
        main_area.pack(side="left", fill="both", expand=True)
        self._create_main_area(main_area)

    def _create_sidebar(self, parent):
        """Создание боковой панели настроек."""
        Label(
            parent,
            text="Настройки",
            font=("Helvetica", 16, "bold"),
            fg="#e4e4e7",
            bg="#252538",
        ).pack(pady=(20, 15))

        self._create_dropdown(parent, "Тональность", self.key_var, self.keys)
        self._create_dropdown(parent, "Тип гаммы", self.scale_var, self.scales)
        self._create_slider(parent, "Количество нот", self.length_var, 4, 32)
        self._create_slider(parent, "Темп (BPM)", self.tempo_var, 60, 200)
        self._create_slider(parent, "Диапазон октав", self.octave_var, 0, 2)

        btn_frame = Frame(parent, bg="#252538")
        btn_frame.pack(fill="x", padx=20, pady=(30, 10))

        self.generate_btn = Button(
            btn_frame,
            text="Сгенерировать",
            font=("Helvetica", 14, "bold"),
            bg="#7c3aed",
            fg="#a78bfa",
            activebackground="#6d28d9",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._generate_melody,
        )
        self.generate_btn.pack(fill="x", pady=5, ipady=8)

        self.play_btn = Button(
            btn_frame,
            text="Воспроизвести",
            font=("Helvetica", 12),
            bg="#374151",
            fg="#a78bfa",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            state=DISABLED,
            command=self._play_melody,
        )
        self.play_btn.pack(fill="x", pady=5, ipady=5)

        self.save_btn = Button(
            btn_frame,
            text="Сохранить MIDI",
            font=("Helvetica", 12),
            bg="#374151",
            fg="#a78bfa",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            state=DISABLED,
            command=self._save_midi,
        )
        self.save_btn.pack(fill="x", pady=5, ipady=5)

    def _create_dropdown(self, parent, label_text, variable, options):
        """Создание выпадающего списка с подписью."""
        frame = Frame(parent, bg="#252538")
        frame.pack(fill="x", padx=20, pady=(10, 0))

        Label(
            frame,
            text=label_text,
            font=("Helvetica", 11),
            fg="#a1a1aa",
            bg="#252538",
        ).pack(anchor="w")

        menu = OptionMenu(frame, variable, *options)
        menu.config(
            font=("Helvetica", 11),
            bg="#374151",
            fg="black",
            activebackground="#4b5563",
            activeforeground="white",
            highlightthickness=0,
            relief="flat",
        )
        menu["menu"].config(
            bg="#374151",
            fg="black",
            activebackground="#7c3aed",
            activeforeground="white",
        )
        menu.pack(fill="x", pady=(5, 0))

    def _create_slider(self, parent, label_text, variable, from_, to):
        """Создание слайдера с подписью."""
        frame = Frame(parent, bg="#252538")
        frame.pack(fill="x", padx=20, pady=(15, 0))

        label_frame = Frame(frame, bg="#252538")
        label_frame.pack(fill="x")

        Label(
            label_frame,
            text=label_text,
            font=("Helvetica", 11),
            fg="#a1a1aa",
            bg="#252538",
        ).pack(side="left")

        value_label = Label(
            label_frame,
            text=str(variable.get()),
            font=("Helvetica", 11, "bold"),
            fg="#a78bfa",
            bg="#252538",
        )
        value_label.pack(side="right")

        slider = Scale(
            frame,
            from_=from_,
            to=to,
            orient=HORIZONTAL,
            variable=variable,
            showvalue=False,
            bg="#374151",
            fg="white",
            troughcolor="#1a1a2e",
            activebackground="#7c3aed",
            highlightthickness=0,
            command=lambda v: value_label.config(text=str(int(float(v)))),
        )
        slider.pack(fill="x", pady=(5, 0))

    def _create_main_area(self, parent):
        """Создание основной области контента."""
        self.info_label = Label(
            parent,
            text="Сгенерируйте мелодию для визуализации",
            font=("Helvetica", 12),
            fg="#a1a1aa",
            bg="#252538",
            pady=10,
        )
        self.info_label.pack(fill="x", pady=(0, 10))

        self.image_frame = Frame(parent, bg="#252538", height=350)
        self.image_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.image_frame.pack_propagate(False)

        self.image_label = Label(
            self.image_frame,
            text="Пиано-ролл",
            font=("Helvetica", 14),
            fg="#71717a",
            bg="#252538",
        )
        self.image_label.pack(expand=True)

        text_frame = Frame(parent, bg="#252538")
        text_frame.pack(fill="x")

        self.melody_text = Text(
            text_frame,
            height=8,
            font=("Courier", 11),
            bg="#1e1e2e",
            fg="#e4e4e7",
            insertbackground="white",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.melody_text.pack(fill="x", padx=10, pady=10)
        self.melody_text.insert("1.0", "Ноты появятся здесь после генерации...")
        self.melody_text.config(state=DISABLED)

    def _generate_melody(self):
        """Генерация новой мелодии."""
        key = self.key_var.get()
        scale_type = ScaleType(self.scale_var.get())
        length = self.length_var.get()
        tempo = self.tempo_var.get()
        octave_range = self.octave_var.get()

        scale = MusicScale.from_key(key, scale_type)
        settings = GeneratorSettings(
            length=length,
            allowed_durations=[0.25, 0.5, 1.0],
            octave_range=octave_range,
        )

        generator = MelodyGenerator(scale, settings)
        melody = generator.generate()

        dur = melody.total_duration()
        info_text = f"{key} {self.scale_var.get()} | {tempo}bpm | {dur:.1f} долей"
        self.info_label.config(text=info_text, fg="#e4e4e7")

        text_output = pretty_print_melody(melody, key=key)
        self.melody_text.config(state=NORMAL)
        self.melody_text.delete("1.0", END)
        self.melody_text.insert("1.0", text_output)
        self.melody_text.config(state=DISABLED)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img_path = tmp.name

        plot_piano_roll(
            melody,
            key=key,
            scale_name=self.scale_var.get(),
            output_path=img_path,
            show=False,
        )

        img = Image.open(img_path)
        frame_width = self.image_frame.winfo_width() - 20
        frame_height = self.image_frame.winfo_height() - 20
        if frame_width > 100 and frame_height > 100:
            img.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)

        self.photo_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo_image, text="")

        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp:
            self.current_midi_path = tmp.name

        export_to_midi(melody, self.current_midi_path, tempo=tempo)

        self.play_btn.config(state=NORMAL)
        self.save_btn.config(state=NORMAL)

    def _play_melody(self):
        """Воспроизведение сгенерированной мелодии."""
        if self.current_midi_path:
            self.play_btn.config(text="Играет...")
            self.root.update()
            try:
                play_midi(self.current_midi_path, wait=True)
            finally:
                self.play_btn.config(text="Воспроизвести")

    def _save_midi(self):
        """Сохранение MIDI файла."""
        if self.current_midi_path:
            filename = filedialog.asksaveasfilename(
                defaultextension=".mid",
                filetypes=[("MIDI файлы", "*.mid"), ("Все файлы", "*.*")],
                initialfile=f"мелодия_{self.key_var.get()}_{self.scale_var.get()}.mid",
            )
            if filename:
                shutil.copy(self.current_midi_path, filename)
                self.info_label.config(text=f"Сохранено: {Path(filename).name}")

    def run(self):
        """Запуск приложения."""
        self.root.mainloop()


def main():
    """Точка входа в приложение."""
    app = MelodyGeneratorApp()
    app.run()


if __name__ == "__main__":
    main()
