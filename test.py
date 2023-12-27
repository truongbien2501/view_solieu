from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
import concurrent.futures

KV = '''
<Content>
    orientation: "vertical"
    spacing: -40
    
    MDSpinner:
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': 0.1}
        active: True
    MDLabel:
        text: "Processing..."
        pos_hint: {'center_x': .7}

FloatLayout:

    MDFlatButton:
        text: "ALERT DIALOG"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.start()
'''


class Content(BoxLayout):
    pass

class Example(MDApp):
    dialog = None

    def build(self):
        return Builder.load_string(KV)

    def start(self):
        # this must be done on the main thread
        self.pop_up1()

        executor = concurrent.futures.ThreadPoolExecutor()
        # f1 = executor.submit(self.pop_up1)  # this must be done on the main thread
        f2 = executor.submit(self.test)


    def pop_up1(self):
        '''Displays a pop_up with a spinning wheel'''
        self.dialog = MDDialog(
            size_hint=(.45, None),
            auto_dismiss=True,
            type="custom",
            content_cls=Content(),
        )
        self.dialog.open()

    def test(self):
        '''Counts to 1000000 and then it closes pop_up1 and opens pop_up2'''
        for number in range(100000):
            print(number)
        self.dismiss()
        Clock.schedule_once( self.pop_up2)  # pop_up2() must be done on the main thread

    def pop_up2(self,*args):
        self.dialog = MDDialog(
            title="Done",
            size_hint=(.6, None),
            text="Done",
                )
        self.dialog.open()

    @mainthread
    def dismiss(self, *args):
        self.dialog.dismiss()


Example().run()