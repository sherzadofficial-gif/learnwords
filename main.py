import json, os, random
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button

# Diňe kompýuterde kiçi ekran; telefonda doly ekran
if platform not in ('android', 'ios'):
    Window.size = (1220, 2592)()

KV = """
#:import dp kivy.metrics.dp

<RBtn>:
    background_normal: ''
    background_down: ''
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    bold: True
    font_size: '18sp'
    canvas.before:
        Color:
            rgba: self.bg
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16)]

<Base>:
    canvas.before:
        Color:
            rgba: 0.87, 0.95, 0.98, 1
        Rectangle:
            pos: self.pos
            size: self.size

<Menu>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(30)
        spacing: dp(16)
        Label:
            text: '[color=2ecc40]Learn[/color]\\n[color=f1c40f]WORDS[/color]'
            markup: True
            font_size: '46sp'
            bold: True
            halign: 'center'
        RBtn:
            text: 'Search'
            bg: 0.2, 0.45, 0.9, 1
            size_hint_y: None
            height: dp(60)
            on_release: app.go('search')
        RBtn:
            text: 'Add word'
            bg: 0.9, 0.25, 0.25, 1
            size_hint_y: None
            height: dp(60)
            on_release: app.go('add')
        RBtn:
            text: 'Play'
            bg: 0.15, 0.7, 0.3, 1
            size_hint_y: None
            height: dp(60)
            on_release: app.go('play')
        Widget:
            size_hint_y: 0.3

<AddScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(12)
        RBtn:
            text: '< Back'
            bg: 0.5, 0.55, 0.6, 1
            size_hint: None, None
            size: dp(90), dp(40)
            on_release: app.go('menu', 'right')
        Label:
            text: 'ADD WORDS'
            color: 0.1, 0.2, 0.3, 1
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(50)
        TextInput:
            id: word
            hint_text: 'Write a word that you want translate'
            multiline: False
            size_hint_y: None
            height: dp(48)
        TextInput:
            id: tr
            hint_text: 'Write translate'
            size_hint_y: None
            height: dp(110)
        RBtn:
            text: 'Add'
            bg: 0.15, 0.7, 0.3, 1
            size_hint_y: None
            height: dp(52)
            on_release: root.add()
        RBtn:
            text: 'Clear'
            bg: 0.9, 0.25, 0.25, 1
            size_hint_y: None
            height: dp(52)
            on_release: root.clear()
        Label:
            id: msg
            text: ''
            color: 0.1, 0.4, 0.1, 1
            bold: True
        Widget:

<SearchScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(12)
        RBtn:
            text: '< Back'
            bg: 0.5, 0.55, 0.6, 1
            size_hint: None, None
            size: dp(90), dp(40)
            on_release: app.go('menu', 'right')
        TextInput:
            id: q
            hint_text: 'Search...'
            multiline: False
            size_hint_y: None
            height: dp(48)
            on_text: root.search(self.text)
        ScrollView:
            GridLayout:
                id: results
                cols: 1
                spacing: dp(8)
                size_hint_y: None
                height: self.minimum_height

<PlayScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(10)
        RBtn:
            text: '< Back'
            bg: 0.5, 0.55, 0.6, 1
            size_hint: None, None
            size: dp(90), dp(40)
            on_release: app.go('menu', 'right')
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(150)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(18)]
            Label:
                id: question
                text: 'Scret answer'
                color: 0, 0, 0, 1
                font_size: '38sp'
                bold: True
            Label:
                id: hidden
                text: 'tt'
                color: 0.4, 0.4, 0.4, 1
                font_size: '14sp'
        RBtn:
            id: o0
            bg: 0.2, 0.45, 0.9, 1
            size_hint_y: None
            height: dp(52)
            on_release: root.answer(self)
        RBtn:
            id: o1
            bg: 0.2, 0.45, 0.9, 1
            size_hint_y: None
            height: dp(52)
            on_release: root.answer(self)
        RBtn:
            id: o2
            bg: 0.2, 0.45, 0.9, 1
            size_hint_y: None
            height: dp(52)
            on_release: root.answer(self)
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(30)
            padding: dp(30), 0
            RBtn:
                id: okb
                text: 'OK 0'
                bg: 0.15, 0.7, 0.3, 1
            RBtn:
                id: badb
                text: 'X 0'
                bg: 0.9, 0.25, 0.25, 1
        ProgressBar:
            id: pb
            max: 10
            value: 0
            size_hint_y: None
            height: dp(14)
"""

DEFAULT_WORDS = [
    {"word": "book", "tr": "kitap", "score": 0},
    {"word": "learn", "tr": "öwrenmek", "score": 0},
    {"word": "notebook", "tr": "depter", "score": 0},
    {"word": "pen", "tr": "ruçka", "score": 0},
]


class RBtn(Button):
    bg = ListProperty([0.2, 0.45, 0.9, 1])


class Base(Screen):
    pass


class Menu(Base):
    pass


class AddScreen(Base):
    def add(self):
        w = self.ids.word.text.strip()
        t = self.ids.tr.text.strip()
        if not w or not t:
            self.ids.msg.color = (0.8, 0.1, 0.1, 1)
            self.ids.msg.text = 'Ikisini hem ýaz!'
            return
        App.get_running_app().add_word(w, t)
        self.ids.msg.color = (0.1, 0.5, 0.1, 1)
        self.ids.msg.text = 'Üstünlikli goşuldy!'
        self.ids.word.text = ''
        self.ids.tr.text = ''

    def clear(self):
        self.ids.word.text = ''
        self.ids.tr.text = ''
        self.ids.msg.text = ''


class SearchScreen(Base):
    def on_pre_enter(self):
        self.ids.q.text = ''
        self.search('')

    def search(self, text):
        text = text.strip().lower()
        box = self.ids.results
        box.clear_widgets()
        for it in App.get_running_app().words:
            if text in it['word'].lower() or text in it['tr'].lower():
                row = BoxLayout(size_hint_y=None, height=dp(48),
                                spacing=dp(8))
                lbl = RBtn(text=f"{it['word'].upper()} - {it['tr'].upper()}",
                           bg=[1, 1, 1, 1], color=(0, 0, 0, 1))
                dele = RBtn(text='X', bg=[0.9, 0.25, 0.25, 1],
                            size_hint_x=None, width=dp(56))
                dele.bind(on_release=lambda b, item=it: self.delete(item))
                row.add_widget(lbl)
                row.add_widget(dele)
                box.add_widget(row)

    def delete(self, item):
        App.get_running_app().delete_word(item)
        self.search(self.ids.q.text)


class PlayScreen(Base):
    current = None
    ok = 0
    bad = 0
    count = 0

    def on_pre_enter(self):
        self.ok = self.bad = self.count = 0
        self.update_stats()
        self.next_q()

    def update_stats(self):
        self.ids.okb.text = f'OK {self.ok}'
        self.ids.badb.text = f'X {self.bad}'
        self.ids.pb.value = self.count % 10

    def next_q(self, *a):
        words = App.get_running_app().words
        if len(words) < 3:
            self.current = None
            self.ids.question.text = 'Azyndan 3 söz ekle!'
            for i in range(3):
                self.ids[f'o{i}'].text = ''
                self.ids[f'o{i}'].disabled = True
            return
        # ýalňyş jogap berlen sözler (pes score) köplenç gelýär
        weights = [max(1, 5 - w['score']) for w in words]
        self.current = random.choices(words, weights)[0]
        others = [w for w in words if w is not self.current]
        opts = random.sample(others, 2) + [self.current]
        random.shuffle(opts)
        self.ids.question.text = self.current['word'].upper()
        self.ids.hidden.text = 'Secret answer'
        for i, o in enumerate(opts):
            b = self.ids[f'o{i}']
            b.text = f"{'abc'[i]}) {o['tr']}"
            b.answer = o['tr']
            b.bg = [0.2, 0.45, 0.9, 1]
            b.disabled = False

    def answer(self, btn):
        if not self.current:
            return
        for i in range(3):
            self.ids[f'o{i}'].disabled = True
        right = btn.answer == self.current['tr']
        self.count += 1
        if right:
            btn.bg = [0.15, 0.7, 0.3, 1]
            self.ok += 1
            self.current['score'] += 1
        else:
            btn.bg = [0.9, 0.25, 0.25, 1]
            self.bad += 1
            self.current['score'] -= 1
            for i in range(3):
                b = self.ids[f'o{i}']
                if b.answer == self.current['tr']:
                    b.bg = [0.15, 0.7, 0.3, 1]
        self.ids.hidden.text = self.current['tr']
        App.get_running_app().save()
        self.update_stats()
        Clock.schedule_once(self.next_q, 1.0)


class SozOwrenApp(App):
    def build(self):
        self.path = os.path.join(self.user_data_dir, 'words.json')
        self.words = self.load()
        Builder.load_string(KV)
        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(Menu(name='menu'))
        self.sm.add_widget(AddScreen(name='add'))
        self.sm.add_widget(SearchScreen(name='search'))
        self.sm.add_widget(PlayScreen(name='play'))
        return self.sm

    def go(self, name, direction='left'):
        self.sm.transition.direction = direction
        self.sm.current = name

    def load(self):
        try:
            with open(self.path, encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return [dict(w) for w in DEFAULT_WORDS]

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.words, f, ensure_ascii=False, indent=2)

    def add_word(self, w, t):
        self.words.append({"word": w, "tr": t, "score": 0})
        self.save()

    def delete_word(self, item):
        if item in self.words:
            self.words.remove(item)
            self.save()


if __name__ == '__main__':
    SozOwrenApp().run()