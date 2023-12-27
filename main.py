from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.toast import toast
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior, CircularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.behaviors import ButtonBehavior
import numpy as np
from kivymd.uix.button import MDIconButton
import requests
from datetime import datetime,timedelta
from ftplib import FTP
from kivymd.uix.list import OneLineListItem,OneLineIconListItem,IconLeftWidget,OneLineRightIconListItem
from kivy.metrics import dp
from kivy_garden.graph import Graph,BarPlot,LinePlot
from kivymd.uix.datatables import MDDataTable
# from kivymd.uix.spinner import MDSpinner
from kivy.properties import NumericProperty
from kivymd.uix.spinner import MDSpinner
from kivy.clock import Clock


# from functools import partial
# Window.size = (450, 600)

class LoadingWidget(Screen):
    pass

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class Homescreen(ScreenManager):
    def login(self,username, password):
        # print('da click')
        # Thực hiện xác thực đăng nhập ở đây (ví dụ: kiểm tra tên đăng nhập và mật khẩu)
        if username == 'admin' and password == 'ttb':
            app = MDApp.get_running_app()
            app.root.current = 'trangchu'  # Chuyển đến màn hình chính
        else:
            # self.show_error_dialog()
            self.thongbao()

class RectangularRippleButton(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    pass


class RectangularRippleImage(CircularRippleBehavior, ButtonBehavior, Image):
    pass

class SOLIEU_KTTV(MDApp):
    zoom = NumericProperty(1)
    
    def build(self):
        # self.spinner = None
        self.title = "KTTV TTB"
        self.theme_cls.primary_palette = "LightBlue"
        Builder.load_file('main.kv')
        # Builder.load_file('vidu.kv')
        self.scr = Homescreen()
        # self.scr1 = LoadingWidget()
        # sm =ScreenManager()
        # sm.add_widget(self.scr)
        # sm.add_widget(self.scr1)
        self.scr.current = 'trangchu'
        # self.scr.current = 'tram'
        return self.scr

    def on_start(self):
        tinh = ['Quang Ngai','Quang Nam','Da Nang', 'Thua Thien Hue','Quang Tri','Quang Binh']
        # tạo các icon
        for tram in tinh:
            icon_item = OneLineIconListItem(
                IconLeftWidget(icon="city"),
                text=tram,
                on_press=self.click_vao_tinh
            )
            self.root.ids.provin.add_widget(icon_item)
        

    def ten_tinh_txt(self,tentinh):
        if tentinh=='Quang Ngai':
            tentinh = 'QNGA.txt'
        elif tentinh=='Quang Nam':
            tentinh = 'QNAM.txt'
        elif tentinh=='Da Nang':
            tentinh = 'DNAN.txt'
        elif tentinh=='Thua Thien Hue':
            tentinh = 'HUE.txt'
        elif tentinh=='Quang Tri':
            tentinh = 'QTRI.txt'
        elif tentinh=='Quang Binh':
            tentinh = 'QBIN.txt'
        return tentinh

    def click_vao_tinh(self,instance):# su kien click vao ten tinh
        self.root.ids.tramkttv_mua_tinh.clear_widgets()
        self.root.ids.tramkttv_gio_tinh.clear_widgets()
        self.root.ids.tramkttv_mucnuoc_tinh.clear_widgets()
        self.root.ids.tramkttv_nhiet_tinh.clear_widgets()
        self.root.ids.tramkttv_ap_tinh.clear_widgets()
        app = MDApp.get_running_app()
        app.root.current = 'solieu'
        spner = MDSpinner(
                        size_hint=(None, None),
                        size=(dp(46), dp(46)),
                        pos_hint={'center_x': .5, 'center_y': .5},
                        active=True,
                        palette=[
                            [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
                            [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
                            [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
                            [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
                        ]
                    )
         # them cho load vao man hinh hien tai
        self.root.ids.solieumua.add_widget(spner)
        # load sau 2s
        Clock.schedule_once(lambda dt: self.creat_point_provin(instance.text,spner), 2) 
    
    def creat_point_provin(self,tinh_click,spner): 
        self.root.ids.tramkttv_mua_tinh.add_widget(OneLineListItem(text='Trạm',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_mua_tinh.add_widget(OneLineListItem(text='Xu thế',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_mua_tinh.add_widget(OneLineListItem(text='Giờ',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_mua_tinh.add_widget(OneLineListItem(text='1h(mm)',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_mucnuoc_tinh.add_widget(OneLineListItem(text='Trạm',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_mucnuoc_tinh.add_widget(OneLineListItem(text='Xu thế',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_mucnuoc_tinh.add_widget(OneLineListItem(text='Giờ',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_mucnuoc_tinh.add_widget(OneLineListItem(text='H(m)',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text='Trạm',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text='Xu thế',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text='Giờ',font_style='Body1',bg_color='#00bfff'))
        self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text='Độ C',font_style='Body1',bg_color='#00bfff'))    
        

        self.root.ids.provin.title = tinh_click
        self.root.ids.hintexx.hint_text = "Tìm kiếm:" + tinh_click
        tentinh = self.ten_tinh_txt(tinh_click)
        ds_tram = np.genfromtxt('tinh/' + tentinh, delimiter=',', dtype=None, names=True, encoding=None)
        for tram in ds_tram:
            if str(tram[4]) == str(tinh_click):
                if 'mua' in str(tram[2]):
                    muatong = self.TTB_API_muatong(tram[0],tram[2])
                    # ten tram
                    self.root.ids.tramkttv_mua_tinh.add_widget(OneLineListItem(text=tram[1] + '-'  + tram[3],font_style='Caption',on_release=self.click_ten_tram))
                    # xu the
                    maune_value = ''
                    if muatong[0] !='-':
                        if float(muatong[0]) == 0:
                            maune_value = '#32cd32'
                            self.root.ids.tramkttv_mua_tinh.add_widget(MDIconButton(icon="circle",theme_icon_color="Custom",icon_color= maune_value))
                        elif float(muatong[0]) > 0 and float(muatong[0]) <10:
                            maune_value = '#32cd32'
                            self.root.ids.tramkttv_mua_tinh.add_widget(MDIconButton(icon="circle",theme_icon_color="Custom",icon_color= maune_value))
                        elif float(muatong[0]) >= 10 and float(muatong[0]) <30:
                            maune_value = '#ffff00' 
                            self.root.ids.tramkttv_mua_tinh.add_widget(MDIconButton(icon="circle",theme_icon_color="Custom",icon_color= maune_value))
                        elif float(muatong[0]) >= 30:
                            maune_value = '#ff0000' 
                            self.root.ids.tramkttv_mua_tinh.add_widget(MDIconButton(icon="circle",theme_icon_color="Custom",icon_color= maune_value))
                    else:
                        self.root.ids.tramkttv_mua_tinh.add_widget(OneLineRightIconListItem(text='-'))
                    # gio
                    if muatong[-1] != '-':
                        self.root.ids.tramkttv_mua_tinh.add_widget(OneLineListItem(text=muatong[-1].strftime('%H:%M'),font_style='Body2'))
                    else:
                        self.root.ids.tramkttv_mua_tinh.add_widget(OneLineListItem(text='-',font_style='Body2'))
                    # gia tri
                    if maune_value =='#ff0000' :
                        self.root.ids.tramkttv_mua_tinh.add_widget(OneLineListItem(text=muatong[0],bg_color=maune_value,font_style='Body2'))
                    else:
                        self.root.ids.tramkttv_mua_tinh.add_widget(OneLineListItem(text=muatong[0],font_style='Body2'))
                    
                elif 'mucnuoc' in str(tram[2]):
                    muatong = self.TTB_API_kiemtraxuthe(tram[0],tram[2])
                    self.root.ids.tramkttv_mucnuoc_tinh.add_widget(OneLineListItem(text=tram[1] + '-'  + tram[3],font_style='Caption',on_release=self.click_ten_tram))
                    if muatong[0] !='-':
                        if float(muatong[0]) == float(muatong[1]):
                            trend = ("arrow-down-bold",[39 / 256, 174 / 256, 96 / 256, 1],'Xuống')
                            self.root.ids.tramkttv_mucnuoc_tinh.add_widget(MDIconButton(icon="swap-horizontal-bold",theme_icon_color="Custom",icon_color= '#32cd32'))
                        elif float(muatong[0]) >  float(muatong[1]):
                            self.root.ids.tramkttv_mucnuoc_tinh.add_widget(MDIconButton(icon="arrow-up-bold",theme_icon_color="Custom",icon_color= '#32cd32'))
                        elif float(muatong[0]) < float(muatong[1]) :
                            self.root.ids.tramkttv_mucnuoc_tinh.add_widget(MDIconButton(icon="arrow-down-bold",theme_icon_color="Custom",icon_color= '#32cd32'))
                    else:
                        self.root.ids.tramkttv_mucnuoc_tinh.add_widget(OneLineListItem(text='-',font_style='Body2'))
                    # gio
                    if muatong[-1] != '-':
                        self.root.ids.tramkttv_mucnuoc_tinh.add_widget(OneLineListItem(text=muatong[-1].strftime('%H:%M'),font_style='Body2'))
                    else:
                        self.root.ids.tramkttv_mucnuoc_tinh.add_widget(OneLineListItem(text='-',font_style='Body2'))
                    # gia tri
                    self.root.ids.tramkttv_mucnuoc_tinh.add_widget(OneLineListItem(text=muatong[0],font_style='Body2'))
                elif ('Gio' in str(tram[2])) or ('gio' in str(tram[2]) or ('Gio' in str(tram[3]))):
                    self.root.ids.tramkttv_gio_tinh.add_widget(OneLineListItem(text=tram[1] + '-' + tram[3],font_style='Caption',on_release=self.click_ten_tram))
                elif 'nhietdo' in str(tram[2]):
                    muatong = self.TTB_API_kiemtraxuthe(tram[0],tram[2])
                    self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text=tram[1] + '-'  + tram[3] ,font_style='Caption',on_release=self.click_ten_tram))
                    if muatong[0] !='-':
                        if float(muatong[0]) == float(muatong[1]):
                            trend = ("arrow-down-bold",[39 / 256, 174 / 256, 96 / 256, 1],'Xuống')
                            self.root.ids.tramkttv_nhiet_tinh.add_widget(MDIconButton(icon="swap-horizontal-bold",theme_icon_color="Custom",icon_color= '#32cd32'))
                        elif float(muatong[0]) >  float(muatong[1]):
                            self.root.ids.tramkttv_nhiet_tinh.add_widget(MDIconButton(icon="arrow-up-bold",theme_icon_color="Custom",icon_color= '#32cd32'))
                        elif float(muatong[0]) < float(muatong[1]) :
                            self.root.ids.tramkttv_nhiet_tinh.add_widget(MDIconButton(icon="arrow-down-bold",theme_icon_color="Custom",icon_color= '#32cd32'))
                    else:
                        self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text='-',font_style='Body2'))
                    # gio
                    if muatong[-1] != '-':
                        self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text=muatong[-1].strftime('%H:%M'),font_style='Body2'))
                    else:
                        self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text='-',font_style='Body2'))
                    # gia tri
                    self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text=muatong[0],font_style='Body2'))
                    # self.root.ids.tramkttv_nhiet_tinh.add_widget(OneLineListItem(text=tram[1],font_style='Caption',on_release=self.click_ten_tram))
                else:
                    self.root.ids.tramkttv_ap_tinh.add_widget(OneLineListItem(text=tram[1] + '-' + tram[3],font_style='Caption',on_release=self.click_ten_tram))

        self.root.ids.solieumua.remove_widget(spner)
    def search_tram(self, search_text):# su kien tìm kiếm
        
        self.root.ids.tramkttv_mua_tinh.clear_widgets()
        self.root.ids.tramkttv_gio_tinh.clear_widgets()
        self.root.ids.tramkttv_mucnuoc_tinh.clear_widgets()
        self.root.ids.tramkttv_nhiet_tinh.clear_widgets()
        self.root.ids.tramkttv_ap_tinh.clear_widgets()

        # self.root.ids.hintexx.helper_text = self.root.ids.tieude_solieu.title
        tentinh = self.ten_tinh_txt(self.root.ids.provin.title)
        ds_tram = np.genfromtxt('tinh/' + tentinh, delimiter=',', dtype=None, names=True, encoding=None)
        for tram in ds_tram:
            if str(tram[1]) == str(search_text):
                if 'mua' in str(tram[2]):
                    bieutuong = "weather-partly-rainy"                    
                elif 'mucnuoc' in str(tram[2]):
                    bieutuong = 'waves-arrow-up'
                elif ('Gio' in str(tram[2])) or ('gio' in str(tram[2]) or ('Gio' in str(tram[3]))):
                    bieutuong = 'wind-power'
                elif 'nhietdo' in str(tram[2]):
                    bieutuong = 'temperature-celsius'
                elif 'khiap' in str(tram[2]):
                    bieutuong = 'car-brake-low-pressure'
                elif 'doam' in str(tram[2]):
                    bieutuong = 'cloud-percent' 
                elif 'nguon' in str(tram[2]):
                    bieutuong = 'car-battery' 
                elif ('luuluong' in str(tram[2])) or ('Luu Luong' in str(tram[3])):
                    bieutuong = 'waves-arrow-right '     
                else:
                    bieutuong = ''
                icon_item = OneLineIconListItem(
                    IconLeftWidget(icon=bieutuong),
                    text=tram[1] + ' - ' + tram[3],
                    on_release=self.click_ten_tram
                )
                # gán su kien cho icon
                if  bieutuong == "weather-partly-rainy":
                    self.root.ids.tramkttv_mua_tinh.add_widget(icon_item)
                elif bieutuong == "waves-arrow-up":
                    self.root.ids.tramkttv_mucnuoc_tinh.add_widget(icon_item)
                elif bieutuong == "wind-power":
                    self.root.ids.tramkttv_gio_tinh.add_widget(icon_item)
                elif bieutuong == "temperature-celsius":
                    self.root.ids.tramkttv_nhiet_tinh.add_widget(icon_item)
                else:
                    self.root.ids.tramkttv_ap_tinh.add_widget(icon_item)
    
    def click_ten_tram(self,instance): # su kien click vao ten tram
        app = MDApp.get_running_app()
        app.root.current = 'tram'
        self.root.ids.tieude_tram_click.text = instance.text
        self.root.ids.solieutram.clear_widgets()
        spner = MDSpinner(
                        size_hint=(None, None),
                        size=(dp(46), dp(46)),
                        pos_hint={'center_x': .5, 'center_y': .5},
                        active=True,
                        palette=[
                            [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
                            [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
                            [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
                            [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
                        ]
                    )
         # them cho load vao man hinh hien tai
        self.root.ids.scr_solieutramchitiet.add_widget(spner)
        
        # load sau 2s
        Clock.schedule_once(lambda dt: self.solieu_chitiet(instance.text,spner), 2) 
    
    
    def solieu_chitiet(self,clicked_text,spner):
        tt_tram = clicked_text.split('-')
        tentram = str(tt_tram[0]).strip()
        yeuto = str(tt_tram[1]).strip()
        
        tentinh = self.ten_tinh_txt(self.root.ids.provin.title)
        # print(tentinh)
        # print(yeuto)
        ds_tram = np.genfromtxt('tinh/' + tentinh, delimiter=',', dtype=None, names=True, encoding=None)
        for tram in ds_tram:
    
            if str(tram[1]) == str(tentram) and str(tram[3]) == str(yeuto):
                solieu = self.TTB_API(tram[0],tram[2])
                for tencot in solieu:
                    if 'SoLieu'in tencot:
                        tencot_sl = 'SoLieu'
                        break
                    else:
                        tencot_sl = 'Solieu'
                        break
                for value in range(len(solieu) - 1, -1, -1):
                    icon_item = OneLineIconListItem(
                        text=solieu[value]['Thoigian_SL'] + ' : ' + solieu[value][tencot_sl]
                    )
                    # gán su kien cho icon
                    self.root.ids.solieutram.add_widget(icon_item)
                break
        self.root.ids.scr_solieutramchitiet.remove_widget(spner)
        # self.root.ids.scr_solieutramchitiet.opacity = 0

    def callback_trangchu(self):
        app = MDApp.get_running_app()
        app.root.current = 'trangchu'
    def callback_manhinhcho(self):
        app = MDApp.get_running_app()
        app.root.current = 'manhinhcho'
    def callback_dienmua(self,**kwargs):
        # self.root.ids.Spinner.activate = True
        self.root.ids.dienmua_layout.clear_widgets()
        app = MDApp.get_running_app()
        app.root.current = 'dienmua'
        
        spner = MDSpinner(
                size_hint=(None, None),
                size=(dp(46), dp(46)),
                pos_hint={'center_x': .5, 'center_y': .5},
                active=True,
                palette=[
                    [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
                    [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
                    [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
                    [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
                ]
            )
         # them cho load vao man hinh hien tai
        self.root.ids.dienmua.add_widget(spner)
        self.root.ids.dienmua_layout.add_widget(OneLineListItem(text='Trạm-Giờ',bg_color='#20b2aa',font_style='Body2'))
        self.root.ids.dienmua_layout.add_widget(OneLineListItem(text='1h',bg_color='#20b2aa',font_style='H6'))
        self.root.ids.dienmua_layout.add_widget(OneLineListItem(text='3h',bg_color='#20b2aa',font_style='H6'))
        self.root.ids.dienmua_layout.add_widget(OneLineListItem(text='6h',bg_color='#20b2aa',font_style='H6'))
        self.root.ids.dienmua_layout.add_widget(OneLineListItem(text='12h',bg_color='#20b2aa',font_style='H6'))
        self.root.ids.dienmua_layout.add_widget(OneLineListItem(text='24h',bg_color='#20b2aa',font_style='H6'))
        self.root.ids.dienmua_layout.add_widget(OneLineListItem(text='48h',bg_color='#20b2aa',font_style='H6'))
        self.root.ids.dienmua_layout.add_widget(OneLineListItem(text='72h',bg_color='#20b2aa',font_style='H6'))
        
        # tinh_click = self.root.ids.provin.title
        # load sau 2s
        Clock.schedule_once(lambda dt: self.tinh_mua_tong_ket(spner), 2) 
        
        
        
        # print(tinh_click)
    def tinh_mua_tong_ket(self,spner):
        tentinh = self.ten_tinh_txt(self.root.ids.provin.title)
        ds_tram = np.genfromtxt('tinh/' + tentinh, delimiter=',', dtype=None, names=True, encoding=None)
        for tram in ds_tram:
            if 'Mua' in tram[3]:
                muatong = self.TTB_API_muatong(tram[0],tram[2])
                self.root.ids.dienmua_layout.add_widget(OneLineListItem(text=tram[1],bg_color='#87cefa',font_style='Body2'))
                for p in range(7):
                    self.root.ids.dienmua_layout.add_widget(OneLineListItem(text=str(muatong[p]),font_style='Body2'))
        self.root.ids.dienmua.remove_widget(spner)

    def callback_dienmua1(self,**kwargs):
        self.root.ids.dienmua_layout.clear_widgets()
        
        app = MDApp.get_running_app()
        app.root.current = 'dienmua'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        data_tables = MDDataTable(
            size_hint=(1, 0.99),
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Trạm-Giờ", dp(20)),
                ("1h", dp(20)),
                ("3h", dp(20)),
                ("6h", dp(20)),
                ("12h", dp(20)),
                ("24h", dp(20)),
                ("48h", dp(20)),
                ("72h", dp(20)),
            ],
        )
        # ac_lout = layout.add_widget(data_tables)
        tinh_click = self.root.ids.provin.title
        # print(tinh_click)
        tentinh = self.ten_tinh_txt(tinh_click)
        ds_tram = np.genfromtxt('tinh/' + tentinh, delimiter=',', dtype=None, names=True, encoding=None)
        for tram in ds_tram:
            if 'mua' in tram[2]:
                muatong = self.TTB_API_muatong(tram[0],tram[2])
                data_tables.add_row((tram[1], muatong[0], muatong[1],muatong[2], muatong[3], muatong[4],muatong[5],muatong[6]))
        data_tables.bind(on_row_press=self.on_row_press)
        self.root.ids.dienmua_layout.add_widget(data_tables)

    def on_row_press(self, instance_table, instance_row):
        """
        Callback khi có một hàng được nhấp.
        """
        print(instance_table, instance_row)
        
    def callback_solieu(self):
        app = MDApp.get_running_app()
        app.root.current = 'solieu'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        
    def callback_solieu_chitiet(self):
        app = MDApp.get_running_app()
        app.root.current = 'tram'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"

    def callback_for_menu_items(self, *args):
        toast(args[0])

    def vebieudo(self,**kwargs):
        now = datetime.now()
        now = datetime(now.year,now.month,now.day)
        gt = []
        tg = []
        for child in self.root.ids.solieutram.children:
            # print(child.text)
            dl = str(child.text).split(':')
            gt.append(float(dl[3].strip()))
            tg.append(datetime.strptime(dl[0].strip() + ':' + dl[1].strip(),"%Y-%m-%d %H:%M"))
        tentram = self.root.ids.tieude_tram_click.text   # lay ten yeo to ve
        self.root.ids.tieude_tram_bieudo.text = tentram
        # index_date = tg.index(now)
        # data_ve = gt[index_date:]
        
        # print(data_ve)
        # print(gt)
        if 'Mua' in tentram:
            result_list = []
            cumulative_sum = 0
            for num in gt:
                cumulative_sum += num
                result_list.append(cumulative_sum)
            gt  = result_list
        data_ve = gt
        # # print(gt)
        # # print(tg)
        app = MDApp.get_running_app()
        app.root.current = 'bieudo'
        # 
        self.root.ids.modulation.clear_widgets()
        if len(data_ve) >3:
            data_ve =np.array(data_ve)
            if 'Mua' in tentram:
                val_y_tick = (round(int(max(data_ve)),-1) + 10) - (round(int(min(data_ve)),-1)-10)
                val_y_tick = val_y_tick/10
                ymax = round(int(max(data_ve)),-1)+10
                ymin = 0
            else:
                if 'Muc Nuoc' in tentram:
                    data_ve = [x * 100 for x in data_ve]
                # print(gt)
                # print(max(gt))
                # print(round(int(max(gt)),-1))
                val_y_tick = (round(int(max(data_ve)),-1) + 10) - (round(int(min(data_ve)),-1)-10)
                val_y_tick = val_y_tick/10
                ymax = round(int(max(data_ve)),-1)+10
                ymin = round(int(min(data_ve)),-1)-10    
                
            self.samples = len(data_ve)
            self.graph = Graph(y_ticks_major=val_y_tick,
                    x_ticks_major=6,
                    border_color=[0, 0, 1, 1],
                    tick_color=[0, 1, 1, 0.7],
                    x_grid=True, y_grid=True,
                    xmin=-0, xmax=self.samples,
                    ymin=ymin, ymax=ymax,
                    draw_border=True,
                    x_grid_label=True, y_grid_label=True,
                    xlabel='Giờ',ylabel=str(tentram))

            self.root.ids.modulation.add_widget(self.graph)
            self.plot = LinePlot(color=[1, 0, 0, 1],line_width=1.5)
            self.graph.add_plot(self.plot)
            self.plot.points = [(t, g) for t, g in enumerate(data_ve)]

    def vebieudo_bar(self,**kwargs):
        now = datetime.now()
        now = datetime(now.year,now.month,now.day)
        tentram = self.root.ids.tieude_tram_bieudo.text   # lay ten yeo to ve
        if 'Mua' in tentram:
            gt = []
            tg = []
            for child in self.root.ids.solieutram.children:
                # print(child.text)
                dl = str(child.text).split(':')
                gt.append(float(dl[3].strip()))
                tg.append(datetime.strptime(dl[0].strip() + ':' + dl[1].strip(),"%Y-%m-%d %H:%M"))
            # print(tentram)
            # print(gt)
            # # print(gt)
            # # print(tg)
            # index_date = tg.index(now)
            # datave = gt[index_date:]
            datave =gt
            app = MDApp.get_running_app()
            app.root.current = 'bieudo'
            # 
            self.root.ids.modulation.clear_widgets()

            if len(datave) >3:
                datave =np.array(datave)              
                if 'Mua' in tentram:
                    val_y_tick = (round(int(max(gt)),-1) + 10) - (round(int(min(gt)),-1)-10)
                    val_y_tick = val_y_tick/5
                    ymax = round(int(max(gt)),-1)+10
                    ymin = 0
                    
                self.samples = len(datave)
                self.graph = Graph(y_ticks_major=val_y_tick,
                        x_ticks_major=6,
                        border_color=[0, 0, 1, 1],
                        tick_color=[0, 1, 1, 0.7],
                        x_grid=True, y_grid=True,
                        xmin=-0, xmax=self.samples,
                        ymin=ymin, ymax=ymax,
                        draw_border=True,
                        x_grid_label=True, y_grid_label=True,
                        xlabel='Giờ',ylabel=str(tentram))

                self.root.ids.modulation.add_widget(self.graph)
                self.plot = BarPlot(color=[1, 0, 0, 1],bar_width=1.5)
                self.graph.add_plot(self.plot)
                self.plot.points = [(t, g) for t, g in enumerate(datave)]



    # def update_zoom(self, value):
    #     if value == '+' and self.zoom < 8:
    #         self.zoom *= 2
    #         self.graph.x_ticks_major /= 2
    #     elif value == '-' and self.zoom > 1:
    #         self.zoom /= 2
    #         self.graph.x_ticks_major *= 2
    #     self.update_plot(1)
    # def update_plot(self, freq):
    #     self.plot_y = np.sin(2*np.pi*freq*self.plot_x)
    #     self.plot.points = [(x, self.plot_y[x]) for x in range(self.samples)]
 
    # def show_example_grid_bottom_sheet(self):
    #     # pass
    #     bottom_sheet_menu = MDGridBottomSheet()
    #     data = {
    #         "Mực nước": "waves-arrow-up",
    #         "Q đến": "alpha-q-circle",
    #         "Q xả": "alpha-d-circle-outline",
    #         "Mưa": "weather-pouring",
    #         "Mưa tại đập": "alpha-c-circle-outline",
    #     }
    #     for item in data.items():
    #         bottom_sheet_menu.add_item(
    #             item[0],
    #             lambda x, y=item[0]: self.callback_for_menu_items(y),
    #             icon_src=item[1],
    #         )
    #     bottom_sheet_menu.open()
    
    # def callback_for_menu_items(self, selected_item):
    #     # Thực hiện cập nhật hình ảnh dựa trên mục được chọn
    #     if selected_item == "Mực nước":
    #         self.read_ftp_sever_image('chart_H.png')
    #         self.root.ids.image_chart_td.source = 'cache/chart_H.png'
    #     elif selected_item == "Q đến":
    #         self.read_ftp_sever_image('chart_Q.png')
    #         self.root.ids.image_chart_td.source = 'cache/chart_Q.png'
    #     elif selected_item == "Q xả":
    #         self.read_ftp_sever_image('chart_Q_xa.png')
    #         self.root.ids.image_chart_td.source = 'cache/chart_Q_xa.png'
    #     elif selected_item == "Mưa":
    #         self.read_ftp_sever_image('chart_mua_tranam2.png')
    #         self.root.ids.image_chart_td.source = 'cache/chart_mua_tranam2.png'
    #     elif selected_item == "Mưa tại đập":
    #         self.read_ftp_sever_image('chart_mua_tramdapst2.png')
    #         self.root.ids.image_chart_td.source = 'cache/chart_mua_tramdapst2.png'
    
    # def show_marker_info(self,tram,thongtin):
    #     toast(tram + ':' + thongtin)

        
    def tinhmua(self,data,bd,kt):
        tonngmua = 0
        for a in range(data.shape[0]-1,1,-1):
            date_object = datetime.strptime(data[a]['Thoigian_SL'], "%Y-%m-%d %H:%M:%S")
            if date_object > bd and date_object <=kt:
                tonngmua+= float(data[a]['SoLieu'])
        return tonngmua
    
    
    def TTB_API(self,matram,ten_bang):
        if 'mua' in ten_bang:
            tinhtong = 1
        else:
            tinhtong = 0
        now = datetime.now()
        kt = datetime(now.year,now.month,now.day,now.hour)
        bd = kt - timedelta(days=3)
        # mua
        pth = 'http://113.160.225.84:2018/API_TTB/JSON/solieu.php?matram={}&ten_table={}&sophut=60&tinhtong={}&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(matram,ten_bang,tinhtong,bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        # print(pth)
        response = requests.get(pth)
        mua = np.array(response.json())
        # print(mua)
        # if len(mua) < 5:
        #     return '-','-'
        return mua
    
    def TTB_API_muatong(self,matram,tenbang):
        now = datetime.now()
        kt = datetime(now.year,now.month,now.day,now.hour)
        bd = kt - timedelta(days=3)
        # mua
        pth = 'http://113.160.225.84:2018/API_TTB/JSON/solieu.php?matram={}&ten_table={}&sophut=60&tinhtong=1&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(matram,tenbang,bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        response = requests.get(pth)
        mua = np.array(response.json())
        if len(mua) < 5:
            return '-','-','-','-','-','-','-','-'
        else:
            giohientai = datetime.strptime(mua[-1]['Thoigian_SL'], '%Y-%m-%d %H:%M:%S')
            mua1 = self.tinhmua(mua,giohientai-timedelta(hours=1),giohientai)
            mua1 = '{:.2f}'.format(mua1)
            mua3 = self.tinhmua(mua,giohientai-timedelta(hours=3),giohientai)
            mua3 = '{:.2f}'.format(mua3)
            mua6 = self.tinhmua(mua,giohientai-timedelta(hours=6),giohientai)
            mua6 = '{:.2f}'.format(mua6)
            mua12 = self.tinhmua(mua,giohientai-timedelta(hours=12),giohientai)
            mua12 = '{:.2f}'.format(mua12)
            mua24 = self.tinhmua(mua,giohientai-timedelta(hours=24),giohientai)
            mua24 = '{:.2f}'.format(mua24)
            mua48 = self.tinhmua(mua,giohientai-timedelta(hours=48),giohientai)
            mua48 = '{:.2f}'.format(mua48)
            mua72 = self.tinhmua(mua,giohientai-timedelta(hours=72),giohientai)
            mua72 = '{:.2f}'.format(mua72)
        return mua1,mua3,mua6,mua12,mua24,mua48,mua72,giohientai
    
    def TTB_API_yeutokhac(self,matram,tenbang):
        now = datetime.now()
        kt = datetime(now.year,now.month,now.day,now.hour)
        bd = kt - timedelta(days=3)
        # mua
        pth = 'http://113.160.225.84:2018/API_TTB/JSON/solieu.php?matram={}&ten_table={}&sophut=60&tinhtong=0&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(matram,tenbang,bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        # print(pth)
        response = requests.get(pth)
        mua = np.array(response.json())
        if len(mua) > 5:
            for tencot in mua:
                if 'SoLieu'in tencot:
                    tencot_sl = 'SoLieu'
                    break
                else:
                    tencot_sl = 'Solieu'
                    break
        if len(mua) < 5:
            return '-','-','-','-','-','-','-','-'
        else:
            giohientai = datetime.strptime(mua[-1]['Thoigian_SL'], '%Y-%m-%d %H:%M:%S')
            h1 = mua[-1][tencot_sl]
            h3 = mua[-3][tencot_sl]
            h6 = mua[-6][tencot_sl]
            h12 = mua[-12][tencot_sl]
            h24 = mua[-24][tencot_sl]
            h48 = mua[-48][tencot_sl]
            try:
                h72 = mua[-72][tencot_sl]
            except:
                h72 ='-'
        return h1,h3,h6,h12,h24,h48,h72,giohientai
    
    def TTB_API_kiemtraxuthe(self,matram,tenbang):
        now = datetime.now()
        kt = datetime(now.year,now.month,now.day,now.hour)
        bd = kt - timedelta(days=1)
        # mua
        pth = 'http://113.160.225.84:2018/API_TTB/JSON/solieu.php?matram={}&ten_table={}&sophut=60&tinhtong=0&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(matram,tenbang,bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        # print(pth)
        response = requests.get(pth)
        mua = np.array(response.json())
        if len(mua) > 5:
            for tencot in mua:
                if 'SoLieu'in tencot:
                    tencot_sl = 'SoLieu'
                    break
                else:
                    tencot_sl = 'Solieu'
                    break
        if len(mua) < 5:
            return '-','-','-'
        else:
            giohientai = datetime.strptime(mua[-1]['Thoigian_SL'], '%Y-%m-%d %H:%M:%S')
            h1 = mua[-1][tencot_sl]
            h2 = mua[-2][tencot_sl]

        return h1,h2,giohientai
    
    def read_ftp_sever_image(self,tenanh):
        # Thông tin máy chủ FTP và đường dẫn đến file ftp://203.209.181.174/DAKDRINH/Image
        ftp_host = '203.209.181.174'
        ftp_user = 'admin'
        ftp_password = 'Supportdng'
        file_path = 'SONGTRANH/Image' + '/' + tenanh
        # Kết nối đến máy chủ FTP
        ftp = FTP(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_password)
        with open('cache/'+ tenanh, 'wb') as local_file:
            ftp.retrbinary('RETR ' + file_path, local_file.write)
        ftp.quit()
        
    
    def get_ftp_image(self,tram):
        self.read_ftp_sever_image(tram)
        self.root.ids.image_chart_tvhn.source = "cache/" + tram


    def get_custom_value(self):
        mucnuoc,qve = self.TTB_API_HC()
        # Trả về giá trị bạn muốn
        return mucnuoc[-1]['Solieu'],qve[-1]['Solieu']


if __name__ == '__main__':
    SOLIEU_KTTV().run()
